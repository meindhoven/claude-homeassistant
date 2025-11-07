"""
Automation Designer Agent

Converts natural language descriptions into Home Assistant automation YAML.
Provides interactive guidance through trigger/condition/action creation.
"""

import re
import uuid
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from agents.base_agent import BaseAgent, AgentResult, AgentPriority
from agents.shared_context import SharedContext


class AutomationDesignerAgent(BaseAgent):
    """
    Agent for designing Home Assistant automations from natural language.

    Capabilities:
    - Parse natural language automation descriptions
    - Build trigger configurations
    - Build condition configurations
    - Build action sequences
    - Generate complete automation YAML
    - Suggest improvements and optimizations
    """

    def __init__(self, context: Optional[SharedContext] = None):
        """Initialize the Automation Designer Agent"""
        super().__init__(context)

        # Pattern library for common automation types
        self.patterns = {
            'motion_light': {
                'triggers': ['motion'],
                'conditions': ['time', 'sun_position'],
                'actions': ['light_on', 'delay', 'light_off']
            },
            'temperature_control': {
                'triggers': ['temperature_threshold'],
                'conditions': ['time_range'],
                'actions': ['climate_set']
            },
            'presence_based': {
                'triggers': ['person_home', 'person_away'],
                'conditions': ['zone'],
                'actions': ['scene', 'notify']
            }
        }

        # Keyword mappings for natural language parsing
        self.trigger_keywords = {
            'when': ['motion', 'door', 'window', 'temperature', 'time', 'sunrise', 'sunset'],
            'on_state': ['on', 'off', 'open', 'closed', 'active', 'inactive'],
            'on_time': ['at', 'after', 'before', 'sunrise', 'sunset']
        }

        self.condition_keywords = {
            'if': ['above', 'below', 'between', 'equals'],
            'when': ['after', 'before', 'during'],
            'state': ['on', 'off', 'home', 'away']
        }

        self.action_keywords = {
            'turn': ['on', 'off', 'toggle'],
            'set': ['temperature', 'brightness', 'color'],
            'send': ['notification', 'message'],
            'wait': ['for', 'until']
        }

    @property
    def name(self) -> str:
        return "Automation Designer Agent"

    @property
    def description(self) -> str:
        return "Designs Home Assistant automations from natural language descriptions"

    @property
    def capabilities(self) -> List[str]:
        return [
            "parse_natural_language",
            "build_trigger",
            "build_condition",
            "build_action",
            "generate_automation",
            "suggest_improvements"
        ]

    def execute(self, **kwargs) -> AgentResult:
        """
        Execute automation design based on provided parameters.

        Supported kwargs:
            description (str): Natural language automation description
            trigger (dict): Explicit trigger configuration
            condition (dict): Explicit condition configuration
            action (dict): Explicit action configuration
            mode (str): 'full' for complete automation, 'trigger', 'condition', or 'action' for specific part
        """
        description = kwargs.get('description')
        trigger = kwargs.get('trigger')
        condition = kwargs.get('condition')
        action = kwargs.get('action')
        mode = kwargs.get('mode', 'full')

        if description:
            return self._design_from_description(description)
        elif trigger or condition or action:
            return self._build_from_components(trigger, condition, action)
        else:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No automation description or components provided",
                errors=["Provide either 'description' for natural language design or explicit components"]
            )

    def _design_from_description(self, description: str) -> AgentResult:
        """Design complete automation from natural language description"""
        self.logger.info(f"Designing automation from: {description}")

        # Parse the description
        parsed = self._parse_description(description)

        if not parsed.get('valid'):
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="Could not understand automation description",
                errors=[parsed.get('error', 'Unknown parsing error')],
                data={'description': description}
            )

        # Build automation components
        automation = {
            'id': str(uuid.uuid4())[:8],
            'alias': self._generate_alias(description),
            'description': description,
        }

        # Build trigger
        trigger_result = self._build_trigger_from_parsed(parsed)
        if not trigger_result['valid']:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="Could not build trigger",
                errors=[trigger_result.get('error', 'Unknown trigger error')]
            )
        automation['trigger'] = trigger_result['config']

        # Build condition (optional)
        condition_result = self._build_condition_from_parsed(parsed)
        if condition_result['valid'] and condition_result.get('config'):
            automation['condition'] = condition_result['config']

        # Build action
        action_result = self._build_action_from_parsed(parsed)
        if not action_result['valid']:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="Could not build action",
                errors=[action_result.get('error', 'Unknown action error')]
            )
        automation['action'] = action_result['config']

        # Add mode (default to single to prevent overlapping runs)
        automation['mode'] = 'single'

        # Generate suggestions
        suggestions = self._generate_suggestions(automation, parsed)

        result = AgentResult(
            success=True,
            agent_name=self.name,
            message=f"Created automation: {automation['alias']}",
            data={
                'automation': automation,
                'parsed_components': {
                    'trigger': parsed.get('trigger_entities', []),
                    'condition': parsed.get('condition_entities', []),
                    'action': parsed.get('action_entities', [])
                }
            }
        )

        # Add suggestions as recommendations
        for suggestion in suggestions:
            result.add_recommendation(
                suggestion['description'],
                AgentPriority[suggestion['priority'].upper()],
                suggestion.get('action')
            )

        return result

    def _parse_description(self, description: str) -> Dict[str, Any]:
        """Parse natural language description into automation components"""
        desc_lower = description.lower()

        parsed = {
            'valid': False,
            'description': description,
            'trigger_type': None,
            'trigger_entities': [],
            'condition_type': None,
            'condition_entities': [],
            'action_type': None,
            'action_entities': [],
            'modifiers': []
        }

        # Detect trigger type and entities
        trigger_info = self._extract_trigger_info(desc_lower)
        if trigger_info:
            parsed['trigger_type'] = trigger_info['type']
            parsed['trigger_entities'] = trigger_info['entities']

        # Detect conditions
        condition_info = self._extract_condition_info(desc_lower)
        if condition_info:
            parsed['condition_type'] = condition_info['type']
            parsed['condition_entities'] = condition_info['entities']
            parsed['modifiers'].extend(condition_info.get('modifiers', []))

        # Detect actions
        action_info = self._extract_action_info(desc_lower)
        if action_info:
            parsed['action_type'] = action_info['type']
            parsed['action_entities'] = action_info['entities']

        # Validation
        if parsed['trigger_type'] and parsed['action_type']:
            parsed['valid'] = True
        else:
            error_parts = []
            if not parsed['trigger_type']:
                error_parts.append("trigger")
            if not parsed['action_type']:
                error_parts.append("action")
            parsed['error'] = f"Could not identify: {', '.join(error_parts)}"

        return parsed

    def _extract_trigger_info(self, description: str) -> Optional[Dict[str, Any]]:
        """Extract trigger information from description"""
        # Motion detection
        if 'motion' in description:
            entities = self._find_entities_in_text(description, 'binary_sensor', 'motion')
            return {
                'type': 'state',
                'subtype': 'motion',
                'entities': entities,
                'to_state': 'on'
            }

        # Door/window
        if 'door' in description or 'window' in description:
            sensor_type = 'door' if 'door' in description else 'window'
            entities = self._find_entities_in_text(description, 'binary_sensor', sensor_type)
            # Detect if it's opening or closing
            to_state = 'on' if 'open' in description else 'off' if 'close' in description else 'on'
            return {
                'type': 'state',
                'subtype': sensor_type,
                'entities': entities,
                'to_state': to_state
            }

        # Time-based
        time_match = re.search(r'at (\d{1,2}):(\d{2})', description)
        if time_match:
            return {
                'type': 'time',
                'time': f"{time_match.group(1)}:{time_match.group(2)}:00"
            }

        # Sun-based
        if 'sunset' in description:
            return {'type': 'sun', 'event': 'sunset'}
        if 'sunrise' in description:
            return {'type': 'sun', 'event': 'sunrise'}

        # Temperature threshold
        temp_match = re.search(r'(above|below|over|under) (\d+)', description)
        if temp_match and 'temperature' in description:
            entities = self._find_entities_in_text(description, 'sensor', 'temperature')
            return {
                'type': 'numeric_state',
                'subtype': 'temperature',
                'entities': entities,
                'threshold': int(temp_match.group(2)),
                'direction': temp_match.group(1)
            }

        return None

    def _extract_condition_info(self, description: str) -> Optional[Dict[str, Any]]:
        """Extract condition information from description"""
        conditions = []

        # Time conditions
        if 'after sunset' in description or 'after dark' in description:
            conditions.append({
                'type': 'sun',
                'condition': 'after_sunset'
            })
        elif 'before sunrise' in description:
            conditions.append({
                'type': 'sun',
                'condition': 'before_sunrise'
            })
        elif 'during day' in description or 'during daytime' in description:
            conditions.append({
                'type': 'sun',
                'condition': 'during_day'
            })

        # Time range
        time_range = re.search(r'between (\d{1,2}):(\d{2}) and (\d{1,2}):(\d{2})', description)
        if time_range:
            conditions.append({
                'type': 'time',
                'after': f"{time_range.group(1)}:{time_range.group(2)}:00",
                'before': f"{time_range.group(3)}:{time_range.group(4)}:00"
            })

        # State conditions
        if 'when home' in description or 'if home' in description:
            conditions.append({
                'type': 'state',
                'entity_type': 'person',
                'state': 'home'
            })

        if not conditions:
            return None

        return {
            'type': 'and' if len(conditions) > 1 else conditions[0]['type'],
            'entities': [],
            'modifiers': conditions
        }

    def _extract_action_info(self, description: str) -> Optional[Dict[str, Any]]:
        """Extract action information from description"""
        # Turn on/off
        if 'turn on' in description:
            # Find lights, switches
            entities = (
                self._find_entities_in_text(description, 'light') +
                self._find_entities_in_text(description, 'switch')
            )
            return {
                'type': 'service',
                'service': 'turn_on',
                'entities': entities
            }
        elif 'turn off' in description:
            entities = (
                self._find_entities_in_text(description, 'light') +
                self._find_entities_in_text(description, 'switch')
            )
            return {
                'type': 'service',
                'service': 'turn_off',
                'entities': entities
            }

        # Set temperature
        temp_match = re.search(r'set.*temperature.*to (\d+)', description)
        if temp_match:
            entities = self._find_entities_in_text(description, 'climate')
            return {
                'type': 'service',
                'service': 'set_temperature',
                'entities': entities,
                'data': {'temperature': int(temp_match.group(1))}
            }

        # Send notification
        if 'notify' in description or 'notification' in description or 'send message' in description:
            return {
                'type': 'service',
                'service': 'notify',
                'entities': []
            }

        return None

    def _find_entities_in_text(
        self,
        text: str,
        domain: Optional[str] = None,
        device_class: Optional[str] = None
    ) -> List[str]:
        """Find entity IDs mentioned in text by matching room names, device names"""
        if not self.context:
            return []

        entities = self.context.get_entities()
        found = []

        # Filter by domain
        if domain:
            entities = [e for e in entities if e.get('entity_id', '').startswith(f"{domain}.")]

        # Filter by device class
        if device_class:
            entities = [e for e in entities if e.get('device_class') == device_class]

        # Extract location words from text
        words = re.findall(r'\b\w+\b', text.lower())

        for entity in entities:
            entity_id = entity.get('entity_id', '').lower()
            # Check if any word from text appears in entity_id
            for word in words:
                if len(word) > 3 and word in entity_id:  # Skip short words
                    found.append(entity.get('entity_id'))
                    break

        return found[:5]  # Limit to 5 entities

    def _build_trigger_from_parsed(self, parsed: Dict) -> Dict[str, Any]:
        """Build trigger configuration from parsed data"""
        trigger_type = parsed.get('trigger_type')

        if trigger_type == 'state':
            entities = parsed.get('trigger_entities', [])
            if not entities:
                return {'valid': False, 'error': 'No trigger entities found'}

            return {
                'valid': True,
                'config': {
                    'platform': 'state',
                    'entity_id': entities[0] if len(entities) == 1 else entities,
                    'to': parsed.get('to_state', 'on')
                }
            }

        elif trigger_type == 'time':
            return {
                'valid': True,
                'config': {
                    'platform': 'time',
                    'at': parsed.get('time')
                }
            }

        elif trigger_type == 'sun':
            return {
                'valid': True,
                'config': {
                    'platform': 'sun',
                    'event': parsed.get('event')
                }
            }

        elif trigger_type == 'numeric_state':
            entities = parsed.get('trigger_entities', [])
            if not entities:
                return {'valid': False, 'error': 'No sensor entities found for numeric trigger'}

            direction = parsed.get('direction')
            threshold = parsed.get('threshold')

            config = {
                'platform': 'numeric_state',
                'entity_id': entities[0] if len(entities) == 1 else entities,
            }

            if direction in ['above', 'over']:
                config['above'] = threshold
            elif direction in ['below', 'under']:
                config['below'] = threshold

            return {'valid': True, 'config': config}

        return {'valid': False, 'error': f'Unknown trigger type: {trigger_type}'}

    def _build_condition_from_parsed(self, parsed: Dict) -> Dict[str, Any]:
        """Build condition configuration from parsed data"""
        modifiers = parsed.get('modifiers', [])

        if not modifiers:
            return {'valid': True, 'config': None}

        conditions = []

        for modifier in modifiers:
            if modifier['type'] == 'sun':
                if modifier['condition'] == 'after_sunset':
                    conditions.append({
                        'condition': 'sun',
                        'after': 'sunset'
                    })
                elif modifier['condition'] == 'before_sunrise':
                    conditions.append({
                        'condition': 'sun',
                        'before': 'sunrise'
                    })
                elif modifier['condition'] == 'during_day':
                    conditions.append({
                        'condition': 'sun',
                        'after': 'sunrise',
                        'before': 'sunset'
                    })

            elif modifier['type'] == 'time':
                conditions.append({
                    'condition': 'time',
                    'after': modifier.get('after'),
                    'before': modifier.get('before')
                })

            elif modifier['type'] == 'state':
                # Find entities of this type
                if modifier.get('entity_type') == 'person':
                    person_entities = self.context.get_entities_by_domain('person')
                    if person_entities:
                        conditions.append({
                            'condition': 'state',
                            'entity_id': person_entities[0].get('entity_id'),
                            'state': modifier.get('state')
                        })

        if not conditions:
            return {'valid': True, 'config': None}
        elif len(conditions) == 1:
            return {'valid': True, 'config': conditions[0]}
        else:
            return {'valid': True, 'config': conditions}

    def _build_action_from_parsed(self, parsed: Dict) -> Dict[str, Any]:
        """Build action configuration from parsed data"""
        action_type = parsed.get('action_type')
        entities = parsed.get('action_entities', [])

        if action_type == 'service':
            service = parsed.get('service')

            if service in ['turn_on', 'turn_off']:
                if not entities:
                    return {'valid': False, 'error': 'No target entities found for action'}

                # Determine domain from entities
                domain = entities[0].split('.')[0] if entities else 'homeassistant'

                config = {
                    'service': f'{domain}.{service}',
                    'target': {
                        'entity_id': entities[0] if len(entities) == 1 else entities
                    }
                }

                return {'valid': True, 'config': config}

            elif service == 'set_temperature':
                if not entities:
                    return {'valid': False, 'error': 'No climate entities found'}

                return {
                    'valid': True,
                    'config': {
                        'service': 'climate.set_temperature',
                        'target': {
                            'entity_id': entities[0]
                        },
                        'data': parsed.get('data', {})
                    }
                }

            elif service == 'notify':
                return {
                    'valid': True,
                    'config': {
                        'service': 'notify.notify',
                        'data': {
                            'message': parsed.get('description', 'Automation triggered')
                        }
                    }
                }

        return {'valid': False, 'error': f'Unknown action type: {action_type}'}

    def _build_from_components(
        self,
        trigger: Optional[Dict],
        condition: Optional[Dict],
        action: Optional[Dict]
    ) -> AgentResult:
        """Build automation from explicit component configurations"""
        automation = {
            'id': str(uuid.uuid4())[:8],
            'alias': 'Custom Automation',
            'mode': 'single'
        }

        if trigger:
            automation['trigger'] = trigger
        if condition:
            automation['condition'] = condition
        if action:
            automation['action'] = action

        return AgentResult(
            success=True,
            agent_name=self.name,
            message="Built automation from components",
            data={'automation': automation}
        )

    def _generate_alias(self, description: str) -> str:
        """Generate a friendly alias from description"""
        # Capitalize first letter, limit length
        alias = description[:75].strip()
        if len(description) > 75:
            alias += '...'
        return alias[0].upper() + alias[1:]

    def _generate_suggestions(self, automation: Dict, parsed: Dict) -> List[Dict[str, str]]:
        """Generate improvement suggestions for automation"""
        suggestions = []

        # Check for timeout on motion-based automations
        if parsed.get('trigger_type') == 'state' and parsed.get('subtype') == 'motion':
            if 'condition' not in automation:
                suggestions.append({
                    'description': 'Consider adding time or sun condition to limit when this runs',
                    'priority': 'medium',
                    'action': 'Add condition to limit activation times'
                })

            # Check if there's a turn_off action
            action_config = automation.get('action', {})
            if isinstance(action_config, dict) and 'turn_off' not in str(action_config):
                suggestions.append({
                    'description': 'Add timeout action to automatically turn off lights after motion stops',
                    'priority': 'high',
                    'action': 'Add wait_for_trigger and turn_off action'
                })

        # Check for mode optimization
        if automation.get('mode') == 'single':
            suggestions.append({
                'description': 'Mode set to "single" - automation will skip if already running. Consider "restart" or "queued" for different behavior.',
                'priority': 'low',
                'action': 'Review automation mode setting'
            })

        return suggestions
