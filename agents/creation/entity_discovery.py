"""
Entity Discovery Agent

Provides context-aware entity search and suggestions for automation creation.
Wraps and enhances the existing entity_explorer.py tool.
"""

import re
from typing import Dict, List, Optional, Any
from pathlib import Path
import sys

# Add tools directory to path for importing entity_explorer
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))

try:
    from entity_explorer import EntityExplorer
except ImportError:
    EntityExplorer = None

from agents.base_agent import BaseAgent, AgentResult, AgentPriority, AgentCapability
from agents.shared_context import SharedContext


class EntityDiscoveryAgent(BaseAgent):
    """
    Agent for discovering and suggesting entities for automations.

    Capabilities:
    - Search entities by natural language description
    - Filter by domain, area, device class
    - Suggest relevant entities based on context
    - Validate entity availability
    - Explain entity capabilities
    """

    def __init__(self, context: Optional[SharedContext] = None):
        """Initialize the Entity Discovery Agent"""
        super().__init__(context)

        # Domain categories for context-aware suggestions
        self.automation_relevant_domains = {
            'trigger': [
                'binary_sensor', 'sensor', 'device_tracker', 'person',
                'sun', 'zone', 'input_boolean', 'input_number',
                'input_select', 'input_datetime'
            ],
            'condition': [
                'sensor', 'binary_sensor', 'sun', 'zone', 'person',
                'device_tracker', 'input_boolean', 'climate', 'weather'
            ],
            'action': [
                'light', 'switch', 'climate', 'cover', 'lock', 'scene',
                'script', 'media_player', 'notify', 'input_boolean',
                'input_number', 'input_select', 'vacuum', 'fan'
            ]
        }

        # Device class meanings for better suggestions
        self.device_class_descriptions = {
            'motion': 'Detects movement/presence',
            'door': 'Detects door open/closed state',
            'window': 'Detects window open/closed state',
            'temperature': 'Measures temperature',
            'humidity': 'Measures humidity',
            'battery': 'Battery level indicator',
            'occupancy': 'Room occupancy detection',
            'light': 'Light level sensor',
            'power': 'Power consumption measurement',
            'energy': 'Energy usage measurement',
        }

    @property
    def name(self) -> str:
        return "Entity Discovery Agent"

    @property
    def description(self) -> str:
        return "Discovers and suggests Home Assistant entities for automation creation"

    @property
    def capabilities(self) -> List[str]:
        return [
            "search_entities",
            "filter_by_domain",
            "filter_by_area",
            "suggest_for_automation",
            "explain_entity",
            "validate_entity"
        ]

    def execute(self, **kwargs) -> AgentResult:
        """
        Execute entity discovery based on provided parameters.

        Supported kwargs:
            query (str): Search query
            domain (str): Filter by domain
            area (str): Filter by area
            context (str): Automation context ('trigger', 'condition', 'action')
            entity_id (str): Get details for specific entity
        """
        query = kwargs.get('query')
        domain = kwargs.get('domain')
        area = kwargs.get('area')
        automation_context = kwargs.get('context')
        entity_id = kwargs.get('entity_id')

        # Specific entity lookup
        if entity_id:
            return self._get_entity_details(entity_id)

        # Context-aware suggestions
        if automation_context:
            return self._suggest_for_context(automation_context, query)

        # General search
        if query or domain or area:
            return self._search_entities(query, domain, area)

        # Default: return summary
        return self._get_summary()

    @AgentCapability("search_entities")
    def _search_entities(
        self,
        query: Optional[str] = None,
        domain: Optional[str] = None,
        area: Optional[str] = None
    ) -> AgentResult:
        """Search entities with filters"""
        if not self.context:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No context available",
                errors=["SharedContext not initialized"]
            )

        entities = self.context.get_entities()
        results = entities

        # Apply filters
        if domain:
            results = [e for e in results if e.get('entity_id', '').startswith(f"{domain}.")]

        if area:
            # Try to match area by name or ID
            area_lower = area.lower()
            area_id = None
            for a in self.context.get_areas():
                if a.get('name', '').lower() == area_lower or a.get('id') == area:
                    area_id = a.get('id')
                    break

            if area_id:
                results = [e for e in results if e.get('area_id') == area_id]

        if query:
            query_lower = query.lower()
            results = [
                e for e in results
                if query_lower in e.get('entity_id', '').lower()
                or query_lower in e.get('name', '').lower()
                or query_lower in e.get('original_name', '').lower()
            ]

        # Format results
        formatted_results = []
        for entity in results[:50]:  # Limit to 50 results
            entity_info = self._format_entity(entity)
            formatted_results.append(entity_info)

        message = f"Found {len(results)} entities"
        if query:
            message += f" matching '{query}'"
        if domain:
            message += f" in domain '{domain}'"
        if area:
            message += f" in area '{area}'"

        result = AgentResult(
            success=True,
            agent_name=self.name,
            message=message,
            data={
                "entities": formatted_results,
                "count": len(results),
                "filters": {
                    "query": query,
                    "domain": domain,
                    "area": area
                }
            }
        )

        # Add recommendations if results seem too broad
        if len(results) > 20:
            result.add_recommendation(
                "Many results found. Consider refining search with domain or area filters.",
                AgentPriority.LOW
            )

        return result

    @AgentCapability("suggest_for_automation")
    def _suggest_for_context(
        self,
        context: str,
        query: Optional[str] = None
    ) -> AgentResult:
        """Suggest entities appropriate for automation context"""
        if context not in self.automation_relevant_domains:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Invalid context: {context}",
                errors=[f"Context must be one of: {list(self.automation_relevant_domains.keys())}"]
            )

        relevant_domains = self.automation_relevant_domains[context]
        entities = self.context.get_entities()

        # Filter by relevant domains
        results = [
            e for e in entities
            if any(e.get('entity_id', '').startswith(f"{d}.") for d in relevant_domains)
        ]

        # Apply query filter if provided
        if query:
            query_lower = query.lower()
            results = [
                e for e in results
                if query_lower in e.get('entity_id', '').lower()
                or query_lower in e.get('name', '').lower()
                or query_lower in e.get('original_name', '').lower()
            ]

        # Format and sort results
        formatted_results = []
        for entity in results[:30]:  # Limit to 30
            entity_info = self._format_entity(entity)
            entity_info['relevance_reason'] = self._explain_relevance(entity, context)
            formatted_results.append(entity_info)

        message = f"Found {len(results)} entities suitable for {context}"
        if query:
            message += f" matching '{query}'"

        return AgentResult(
            success=True,
            agent_name=self.name,
            message=message,
            data={
                "entities": formatted_results,
                "count": len(results),
                "context": context,
                "query": query
            }
        )

    @AgentCapability("validate_entity")
    def _get_entity_details(self, entity_id: str) -> AgentResult:
        """Get detailed information about a specific entity"""
        if not self.context:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No context available",
                errors=["SharedContext not initialized"]
            )

        entity = self.context.get_entity(entity_id)

        if not entity:
            # Try to find similar entities
            similar = self._find_similar_entities(entity_id)

            error_msg = f"Entity '{entity_id}' not found"
            result = AgentResult(
                success=False,
                agent_name=self.name,
                message=error_msg,
                errors=[error_msg]
            )

            if similar:
                result.data['similar_entities'] = [
                    self._format_entity(e) for e in similar[:5]
                ]
                result.add_recommendation(
                    f"Did you mean one of these? {', '.join(e.get('entity_id') for e in similar[:3])}",
                    AgentPriority.HIGH
                )

            return result

        # Entity found - provide detailed info
        entity_info = self._format_entity(entity, detailed=True)

        # Get automation usage
        automations_using = self._find_automations_using_entity(entity_id)

        return AgentResult(
            success=True,
            agent_name=self.name,
            message=f"Entity details for {entity_id}",
            data={
                "entity": entity_info,
                "used_in_automations": automations_using,
                "capabilities": self._get_entity_capabilities(entity)
            }
        )

    def _get_summary(self) -> AgentResult:
        """Get summary of available entities"""
        if not self.context:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No context available",
                errors=["SharedContext not initialized"]
            )

        entities = self.context.get_entities()

        # Count by domain
        domain_counts = {}
        for entity in entities:
            entity_id = entity.get('entity_id', '')
            domain = entity_id.split('.')[0] if '.' in entity_id else 'unknown'
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        # Get areas
        areas = self.context.get_areas()
        area_names = [a.get('name') for a in areas]

        return AgentResult(
            success=True,
            agent_name=self.name,
            message=f"Entity registry contains {len(entities)} entities",
            data={
                "total_entities": len(entities),
                "domains": domain_counts,
                "areas": area_names,
                "top_domains": sorted(
                    domain_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
            }
        )

    def _format_entity(self, entity: Dict, detailed: bool = False) -> Dict[str, Any]:
        """Format entity information for display"""
        entity_id = entity.get('entity_id', 'unknown')
        name = entity.get('name') or entity.get('original_name', entity_id)

        basic_info = {
            'entity_id': entity_id,
            'name': name,
            'domain': entity_id.split('.')[0] if '.' in entity_id else 'unknown',
            'disabled': entity.get('disabled_by') is not None,
        }

        if entity.get('area_id'):
            area_name = self.context.get_area_name(entity.get('area_id'))
            basic_info['area'] = area_name

        if entity.get('device_class'):
            basic_info['device_class'] = entity.get('device_class')

        if not detailed:
            return basic_info

        # Add detailed information
        basic_info.update({
            'platform': entity.get('platform'),
            'unique_id': entity.get('unique_id'),
            'config_entry_id': entity.get('config_entry_id'),
            'device_id': entity.get('device_id'),
            'hidden': entity.get('hidden_by') is not None,
            'icon': entity.get('icon'),
            'unit_of_measurement': entity.get('unit_of_measurement'),
        })

        return basic_info

    def _explain_relevance(self, entity: Dict, context: str) -> str:
        """Explain why an entity is relevant for the automation context"""
        entity_id = entity.get('entity_id', '')
        domain = entity_id.split('.')[0] if '.' in entity_id else ''
        device_class = entity.get('device_class')

        explanations = {
            'trigger': {
                'binary_sensor': 'Can trigger on state change (on/off)',
                'sensor': 'Can trigger on value change or threshold',
                'device_tracker': 'Can trigger on location change',
                'person': 'Can trigger when person arrives/leaves',
            },
            'condition': {
                'binary_sensor': 'Can check if active/inactive',
                'sensor': 'Can compare value against threshold',
                'sun': 'Can check if above/below horizon',
                'climate': 'Can check temperature or mode',
            },
            'action': {
                'light': 'Can turn on/off, adjust brightness/color',
                'switch': 'Can turn on/off',
                'climate': 'Can set temperature, change mode',
                'lock': 'Can lock/unlock',
                'scene': 'Can activate scene',
            }
        }

        reason = explanations.get(context, {}).get(domain, f'Suitable for {context}')

        if device_class and device_class in self.device_class_descriptions:
            reason += f" ({self.device_class_descriptions[device_class]})"

        return reason

    def _find_similar_entities(self, entity_id: str) -> List[Dict]:
        """Find entities with similar IDs"""
        if not self.context:
            return []

        # Extract domain and search term
        parts = entity_id.split('.')
        domain = parts[0] if len(parts) > 1 else ''
        search_term = parts[1] if len(parts) > 1 else entity_id

        entities = self.context.get_entities()
        similar = []

        for entity in entities:
            eid = entity.get('entity_id', '')
            # Same domain
            if domain and eid.startswith(f"{domain}."):
                # Similar name (fuzzy match)
                entity_name = eid.split('.')[1] if '.' in eid else eid
                if self._similarity_score(search_term, entity_name) > 0.6:
                    similar.append(entity)

        return sorted(similar, key=lambda e: self._similarity_score(
            search_term, e.get('entity_id', '').split('.')[1]
        ), reverse=True)

    def _similarity_score(self, s1: str, s2: str) -> float:
        """Calculate simple similarity score between two strings"""
        s1, s2 = s1.lower(), s2.lower()

        # Exact match
        if s1 == s2:
            return 1.0

        # Contains
        if s1 in s2 or s2 in s1:
            return 0.8

        # Common words
        words1 = set(s1.split('_'))
        words2 = set(s2.split('_'))
        common = words1.intersection(words2)

        if not words1 or not words2:
            return 0.0

        return len(common) / max(len(words1), len(words2))

    def _find_automations_using_entity(self, entity_id: str) -> List[str]:
        """Find automations that reference this entity"""
        automations = self.context.get_automations()
        using = []

        for automation in automations:
            # Convert to string and search for entity_id
            auto_str = str(automation)
            if entity_id in auto_str:
                alias = automation.get('alias', automation.get('id', 'unknown'))
                using.append(alias)

        return using

    def _get_entity_capabilities(self, entity: Dict) -> Dict[str, Any]:
        """Determine what the entity can do"""
        entity_id = entity.get('entity_id', '')
        domain = entity_id.split('.')[0] if '.' in entity_id else ''

        capabilities = {
            'can_trigger': domain in self.automation_relevant_domains['trigger'],
            'can_condition': domain in self.automation_relevant_domains['condition'],
            'can_action': domain in self.automation_relevant_domains['action'],
        }

        # Domain-specific capabilities
        if domain == 'light':
            capabilities['actions'] = ['turn_on', 'turn_off', 'toggle', 'brightness', 'color']
        elif domain == 'switch':
            capabilities['actions'] = ['turn_on', 'turn_off', 'toggle']
        elif domain == 'climate':
            capabilities['actions'] = ['set_temperature', 'set_hvac_mode', 'set_preset_mode']
        elif domain == 'lock':
            capabilities['actions'] = ['lock', 'unlock']
        elif domain == 'cover':
            capabilities['actions'] = ['open_cover', 'close_cover', 'stop_cover']

        return capabilities
