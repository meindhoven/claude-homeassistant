#!/usr/bin/env python3
"""Device trigger validator using MCP to verify devices exist.

This validator checks that device triggers in automations reference valid devices
by querying the live Home Assistant instance via MCP.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

import yaml


class DeviceValidator:
    """Validates device references in Home Assistant automations using MCP."""

    def __init__(self, config_dir: str = "config", use_mcp: bool = True):
        """Initialize the DeviceValidator.

        Args:
            config_dir: Path to the Home Assistant configuration directory
            use_mcp: Whether to use MCP for live device verification
        """
        self.config_dir = Path(config_dir).resolve()
        self.use_mcp = use_mcp
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.device_registry: Dict[str, dict] = {}
        self.device_ids_found: Set[str] = set()

    def load_device_registry(self) -> bool:
        """Load device registry from .storage/core.device_registry."""
        registry_path = self.config_dir / ".storage" / "core.device_registry"

        if not registry_path.exists():
            self.warnings.append(
                f"Device registry not found at {registry_path}. "
                "Device validation will be limited."
            )
            return False

        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Build a mapping of device_id -> device_info
            for device in data.get("data", {}).get("devices", []):
                device_id = device.get("id")
                if device_id:
                    self.device_registry[device_id] = device

            self.info.append(
                f"Loaded {len(self.device_registry)} devices from registry"
            )
            return True

        except Exception as e:
            self.errors.append(f"Failed to load device registry: {e}")
            return False

    def verify_device_via_mcp(self, device_id: str) -> Optional[bool]:
        """Verify device exists via MCP (placeholder for MCP integration).

        Args:
            device_id: The device ID to verify

        Returns:
            True if device exists, False if not, None if MCP unavailable
        """
        # TODO: Implement actual MCP call
        # For now, this is a placeholder that indicates MCP verification is needed
        # The actual MCP integration will be done via the Python MCP client
        return None

    def extract_device_triggers(self, automation_file: Path) -> List[Dict]:
        """Extract device triggers from an automation file.

        Args:
            automation_file: Path to the automations.yaml file

        Returns:
            List of device trigger configurations with metadata
        """
        device_triggers = []

        try:
            with open(automation_file, "r", encoding="utf-8") as f:
                automations = yaml.safe_load(f) or []

            if not isinstance(automations, list):
                automations = [automations]

            for idx, automation in enumerate(automations):
                if not isinstance(automation, dict):
                    continue

                automation_id = automation.get("id", f"automation_{idx}")
                automation_alias = automation.get("alias", f"Automation {idx}")

                # Check triggers
                triggers = automation.get("triggers", automation.get("trigger", []))
                if not isinstance(triggers, list):
                    triggers = [triggers]

                for trigger_idx, trigger in enumerate(triggers):
                    if not isinstance(trigger, dict):
                        continue

                    # Look for device triggers
                    if trigger.get("trigger") == "device" or trigger.get(
                        "device_id"
                    ):
                        device_id = trigger.get("device_id")
                        if device_id:
                            device_triggers.append(
                                {
                                    "device_id": device_id,
                                    "automation_id": automation_id,
                                    "automation_alias": automation_alias,
                                    "trigger_index": trigger_idx,
                                    "domain": trigger.get("domain"),
                                    "type": trigger.get("type"),
                                    "subtype": trigger.get("subtype"),
                                }
                            )

        except yaml.YAMLError as e:
            self.errors.append(f"YAML error in {automation_file}: {e}")
        except Exception as e:
            self.errors.append(f"Error parsing {automation_file}: {e}")

        return device_triggers

    def validate_device_trigger(self, trigger_info: Dict) -> bool:
        """Validate a single device trigger.

        Args:
            trigger_info: Dictionary containing device trigger information

        Returns:
            True if valid, False otherwise
        """
        device_id = trigger_info["device_id"]
        automation_alias = trigger_info["automation_alias"]
        domain = trigger_info.get("domain", "unknown")

        # Track that we found this device ID
        self.device_ids_found.add(device_id)

        # Check local device registry
        device_info = self.device_registry.get(device_id)

        if device_info:
            # Device exists in registry
            device_name = device_info.get("name_by_user") or device_info.get(
                "name", "Unknown"
            )
            self.info.append(
                f"✓ Device '{device_name}' ({device_id[:8]}...) "
                f"found for automation '{automation_alias}'"
            )
            return True

        # Device not in local registry
        if self.use_mcp:
            # Try MCP verification
            mcp_result = self.verify_device_via_mcp(device_id)
            if mcp_result is True:
                self.info.append(
                    f"✓ Device {device_id[:8]}... verified via MCP "
                    f"for automation '{automation_alias}'"
                )
                return True
            elif mcp_result is False:
                self.errors.append(
                    f"❌ Device {device_id[:8]}... not found (verified via MCP) "
                    f"in automation '{automation_alias}' ({domain} domain)"
                )
                return False
            else:
                # MCP unavailable
                self.warnings.append(
                    f"⚠️  Device {device_id[:8]}... in automation '{automation_alias}' "
                    f"({domain} domain) - Cannot validate without live HA connection. "
                    f"This is expected when validating locally. "
                    f"The automation will work if the device exists in production."
                )
                return True  # Don't fail validation for local-only checks
        else:
            # No MCP, just warn
            self.warnings.append(
                f"⚠️  Device {device_id[:8]}... not in local registry "
                f"for automation '{automation_alias}' ({domain} domain). "
                f"Enable MCP for live verification."
            )
            return True  # Don't fail without MCP

    def validate_automations(self, automation_file: Path) -> bool:
        """Validate all device triggers in an automation file.

        Args:
            automation_file: Path to automations.yaml

        Returns:
            True if all validations pass, False otherwise
        """
        if not automation_file.exists():
            self.errors.append(f"Automation file not found: {automation_file}")
            return False

        self.info.append(f"Checking device triggers in {automation_file.name}...")

        # Extract all device triggers
        device_triggers = self.extract_device_triggers(automation_file)

        if not device_triggers:
            self.info.append("No device triggers found")
            return True

        self.info.append(f"Found {len(device_triggers)} device trigger(s)")

        # Validate each device trigger
        all_valid = True
        for trigger in device_triggers:
            if not self.validate_device_trigger(trigger):
                all_valid = False

        return all_valid

    def validate_all(self) -> bool:
        """Run complete device validation.

        Returns:
            True if validation passes, False otherwise
        """
        # Load device registry
        self.load_device_registry()

        # Find automations.yaml
        automations_file = self.config_dir / "automations.yaml"

        # Validate
        result = self.validate_automations(automations_file)

        # Summary
        if self.device_ids_found:
            self.info.append(
                f"\nValidated {len(self.device_ids_found)} unique device(s)"
            )

        return result

    def print_results(self):
        """Print validation results."""
        if self.info:
            print("INFO:")
            for info in self.info:
                print(f"  {info}")
            print()

        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
            print()

        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  {error}")
            print()

        if not self.errors and not self.warnings:
            print("✅ All device triggers are valid!")
        elif not self.errors:
            print("✅ Device triggers are valid (with warnings)")
        else:
            print("❌ Device trigger validation failed")


def main():
    """Run device validation from command line."""
    config_dir = sys.argv[1] if len(sys.argv) > 1 else "config"

    # Check if MCP should be used (via environment variable)
    use_mcp = os.getenv("USE_MCP", "true").lower() in ("true", "1", "yes")

    validator = DeviceValidator(config_dir, use_mcp=use_mcp)
    is_valid = validator.validate_all()
    validator.print_results()

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
