"""
Shared Context Management for Home Assistant Agent System

This module provides a centralized context that agents can use to share
state, cache data, and communicate with each other.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging


class SharedContext:
    """
    Centralized context for sharing data between agents.

    This class provides:
    - Entity registry access
    - Device registry access
    - Area registry access
    - Automation cache
    - Configuration paths
    - User preferences
    - Inter-agent communication
    """

    def __init__(self, config_dir: str = "/home/user/claude-homeassistant/config"):
        """
        Initialize shared context.

        Args:
            config_dir: Path to Home Assistant config directory
        """
        self.config_dir = Path(config_dir)
        self.storage_dir = self.config_dir / ".storage"
        self.logger = logging.getLogger(__name__)

        # Cached data
        self._entity_registry: Optional[Dict] = None
        self._device_registry: Optional[Dict] = None
        self._area_registry: Optional[Dict] = None
        self._automations: Optional[List] = None
        self._scripts: Optional[Dict] = None

        # Agent communication
        self._agent_messages: Dict[str, List[Dict]] = {}
        self._shared_data: Dict[str, Any] = {}

        # User preferences
        self.preferences = {
            "location": "home",  # default location for entities
            "auto_document": True,
            "auto_validate": True,
            "verbose_output": False,
            "naming_convention": "location_room_device_sensor"
        }

        self._load_registries()

    def _load_registries(self):
        """Load entity, device, and area registries"""
        try:
            # Load entity registry
            entity_reg_path = self.storage_dir / "core.entity_registry"
            if entity_reg_path.exists():
                with open(entity_reg_path, 'r') as f:
                    self._entity_registry = json.load(f)
                self.logger.info(
                    f"Loaded {len(self._entity_registry.get('data', {}).get('entities', []))} entities"
                )

            # Load device registry
            device_reg_path = self.storage_dir / "core.device_registry"
            if device_reg_path.exists():
                with open(device_reg_path, 'r') as f:
                    self._device_registry = json.load(f)
                self.logger.info(
                    f"Loaded {len(self._device_registry.get('data', {}).get('devices', []))} devices"
                )

            # Load area registry
            area_reg_path = self.storage_dir / "core.area_registry"
            if area_reg_path.exists():
                with open(area_reg_path, 'r') as f:
                    self._area_registry = json.load(f)
                self.logger.info(
                    f"Loaded {len(self._area_registry.get('data', {}).get('areas', []))} areas"
                )

        except Exception as e:
            self.logger.error(f"Error loading registries: {e}")

    def reload_registries(self):
        """Reload all registries from disk"""
        self._entity_registry = None
        self._device_registry = None
        self._area_registry = None
        self._load_registries()

    def get_entities(self) -> List[Dict]:
        """Get all entities from registry"""
        if self._entity_registry is None:
            return []
        return self._entity_registry.get('data', {}).get('entities', [])

    def get_entity(self, entity_id: str) -> Optional[Dict]:
        """
        Get specific entity by ID.

        Args:
            entity_id: Entity ID to look up

        Returns:
            Entity dict or None if not found
        """
        entities = self.get_entities()
        for entity in entities:
            if entity.get('entity_id') == entity_id:
                return entity
        return None

    def entity_exists(self, entity_id: str) -> bool:
        """Check if entity exists in registry"""
        return self.get_entity(entity_id) is not None

    def get_entities_by_domain(self, domain: str) -> List[Dict]:
        """Get all entities for a specific domain (e.g., 'light', 'sensor')"""
        entities = self.get_entities()
        return [e for e in entities if e.get('entity_id', '').startswith(f"{domain}.")]

    def get_entities_by_area(self, area_id: str) -> List[Dict]:
        """Get all entities in a specific area"""
        entities = self.get_entities()
        return [e for e in entities if e.get('area_id') == area_id]

    def search_entities(self, query: str) -> List[Dict]:
        """
        Search entities by name or entity_id.

        Args:
            query: Search query (case-insensitive)

        Returns:
            List of matching entities
        """
        query = query.lower()
        entities = self.get_entities()
        results = []

        for entity in entities:
            entity_id = entity.get('entity_id', '').lower()
            name = entity.get('name', '').lower() or entity.get('original_name', '').lower()

            if query in entity_id or query in name:
                results.append(entity)

        return results

    def get_devices(self) -> List[Dict]:
        """Get all devices from registry"""
        if self._device_registry is None:
            return []
        return self._device_registry.get('data', {}).get('devices', [])

    def get_areas(self) -> List[Dict]:
        """Get all areas from registry"""
        if self._area_registry is None:
            return []
        return self._area_registry.get('data', {}).get('areas', [])

    def get_area_name(self, area_id: str) -> Optional[str]:
        """Get area name by ID"""
        areas = self.get_areas()
        for area in areas:
            if area.get('id') == area_id:
                return area.get('name')
        return None

    def load_automations(self) -> List[Dict]:
        """Load automations from automations.yaml"""
        import yaml

        automations_path = self.config_dir / "automations.yaml"
        if not automations_path.exists():
            return []

        try:
            with open(automations_path, 'r') as f:
                self._automations = yaml.safe_load(f) or []
            return self._automations
        except Exception as e:
            self.logger.error(f"Error loading automations: {e}")
            return []

    def get_automations(self) -> List[Dict]:
        """Get cached automations (loads if not cached)"""
        if self._automations is None:
            return self.load_automations()
        return self._automations

    def get_automation(self, automation_id: str) -> Optional[Dict]:
        """Get specific automation by ID"""
        automations = self.get_automations()
        for auto in automations:
            if auto.get('id') == automation_id:
                return auto
        return None

    def load_scripts(self) -> Dict:
        """Load scripts from scripts.yaml"""
        import yaml

        scripts_path = self.config_dir / "scripts.yaml"
        if not scripts_path.exists():
            return {}

        try:
            with open(scripts_path, 'r') as f:
                self._scripts = yaml.safe_load(f) or {}
            return self._scripts
        except Exception as e:
            self.logger.error(f"Error loading scripts: {e}")
            return {}

    def get_scripts(self) -> Dict:
        """Get cached scripts (loads if not cached)"""
        if self._scripts is None:
            return self.load_scripts()
        return self._scripts

    # Inter-agent communication
    def send_message(self, from_agent: str, to_agent: str, message: Dict[str, Any]):
        """Send a message from one agent to another"""
        if to_agent not in self._agent_messages:
            self._agent_messages[to_agent] = []

        self._agent_messages[to_agent].append({
            "from": from_agent,
            "timestamp": datetime.now().isoformat(),
            "message": message
        })

    def get_messages(self, agent_name: str) -> List[Dict]:
        """Get all messages for an agent"""
        return self._agent_messages.get(agent_name, [])

    def clear_messages(self, agent_name: str):
        """Clear messages for an agent"""
        if agent_name in self._agent_messages:
            self._agent_messages[agent_name] = []

    # Shared data storage
    def set_data(self, key: str, value: Any):
        """Store data in shared context"""
        self._shared_data[key] = value

    def get_data(self, key: str, default: Any = None) -> Any:
        """Retrieve data from shared context"""
        return self._shared_data.get(key, default)

    def has_data(self, key: str) -> bool:
        """Check if key exists in shared data"""
        return key in self._shared_data

    def clear_data(self, key: Optional[str] = None):
        """Clear shared data (specific key or all)"""
        if key is None:
            self._shared_data = {}
        elif key in self._shared_data:
            del self._shared_data[key]

    # Configuration paths
    def get_config_path(self, filename: str) -> Path:
        """Get full path to a config file"""
        return self.config_dir / filename

    def get_automations_path(self) -> Path:
        """Get path to automations.yaml"""
        return self.config_dir / "automations.yaml"

    def get_scripts_path(self) -> Path:
        """Get path to scripts.yaml"""
        return self.config_dir / "scripts.yaml"

    def get_entity_registry_path(self) -> Path:
        """Get path to entity registry"""
        return self.storage_dir / "core.entity_registry"

    # User preferences
    def set_preference(self, key: str, value: Any):
        """Set a user preference"""
        self.preferences[key] = value

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference"""
        return self.preferences.get(key, default)

    # Statistics and summary
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of context state"""
        return {
            "entities": len(self.get_entities()),
            "devices": len(self.get_devices()),
            "areas": len(self.get_areas()),
            "automations": len(self.get_automations()),
            "scripts": len(self.get_scripts()),
            "shared_data_keys": list(self._shared_data.keys()),
            "preferences": self.preferences
        }

    def __repr__(self) -> str:
        summary = self.get_summary()
        return (
            f"SharedContext("
            f"entities={summary['entities']}, "
            f"devices={summary['devices']}, "
            f"areas={summary['areas']}, "
            f"automations={summary['automations']}, "
            f"scripts={summary['scripts']})"
        )
