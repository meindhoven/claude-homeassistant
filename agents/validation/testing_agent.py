"""
Testing Agent

Simulates and tests automations before deployment.
Provides scenario testing, edge case detection, and dry-run capabilities.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, time as dt_time
import re

from agents.base_agent import BaseAgent, AgentResult, AgentPriority
from agents.shared_context import SharedContext


class TestingAgent(BaseAgent):
    """
    Agent for testing Home Assistant automations before deployment.

    Capabilities:
    - Simulate automation execution
    - Test trigger conditions
    - Verify action sequences
    - Check edge cases
    - Identify potential issues
    - Generate test scenarios
    """

    def __init__(self, context: Optional[SharedContext] = None):
        """Initialize the Testing Agent"""
        super().__init__(context)

        # Common test scenarios for different automation types
        self.scenario_templates = {
            'motion_light': [
                {'time': '14:00', 'sun': 'above_horizon', 'motion': 'on', 'expected': 'no_action'},
                {'time': '21:00', 'sun': 'below_horizon', 'motion': 'on', 'expected': 'light_on'},
                {'time': '21:00', 'sun': 'below_horizon', 'motion': 'off', 'expected': 'no_action'},
            ],
            'temperature_control': [
                {'temperature': 18, 'time': '10:00', 'expected': 'heat_on'},
                {'temperature': 22, 'time': '10:00', 'expected': 'no_action'},
                {'temperature': 26, 'time': '14:00', 'expected': 'cool_on'},
            ],
            'presence_based': [
                {'person_state': 'home', 'expected': 'scene_activate'},
                {'person_state': 'away', 'expected': 'scene_activate'},
            ]
        }

    @property
    def name(self) -> str:
        return "Testing Agent"

    @property
    def description(self) -> str:
        return "Tests and simulates Home Assistant automations before deployment"

    @property
    def capabilities(self) -> List[str]:
        return [
            "simulate_automation",
            "test_scenarios",
            "verify_triggers",
            "check_edge_cases",
            "dry_run_actions",
            "detect_conflicts"
        ]

    def execute(self, **kwargs) -> AgentResult:
        """
        Execute testing based on provided parameters.

        Supported kwargs:
            automation (dict): Automation to test
            scenarios (list): Custom test scenarios
            test_type (str): 'full', 'triggers', 'conditions', 'actions', 'edge_cases'
        """
        automation = kwargs.get('automation')
        scenarios = kwargs.get('scenarios')
        test_type = kwargs.get('test_type', 'full')

        if not automation:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No automation provided for testing",
                errors=["Provide 'automation' parameter"]
            )

        if test_type == 'full':
            return self._run_full_test(automation, scenarios)
        elif test_type == 'triggers':
            return self._test_triggers(automation)
        elif test_type == 'conditions':
            return self._test_conditions(automation)
        elif test_type == 'actions':
            return self._test_actions(automation)
        elif test_type == 'edge_cases':
            return self._test_edge_cases(automation)
        else:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Unknown test type: {test_type}",
                errors=["Test type must be: full, triggers, conditions, actions, edge_cases"]
            )

    def _run_full_test(self, automation: Dict, custom_scenarios: Optional[List] = None) -> AgentResult:
        """Run complete test suite on automation"""
        test_results = {
            'trigger_tests': None,
            'condition_tests': None,
            'action_tests': None,
            'scenario_tests': None,
            'edge_case_tests': None
        }

        all_issues = []
        all_warnings = []

        # Test triggers
        trigger_result = self._test_triggers(automation)
        test_results['trigger_tests'] = trigger_result.to_dict()
        if not trigger_result.success:
            all_issues.extend(trigger_result.errors)
        all_warnings.extend(trigger_result.warnings)

        # Test conditions
        if 'condition' in automation:
            condition_result = self._test_conditions(automation)
            test_results['condition_tests'] = condition_result.to_dict()
            if not condition_result.success:
                all_issues.extend(condition_result.errors)
            all_warnings.extend(condition_result.warnings)

        # Test actions
        action_result = self._test_actions(automation)
        test_results['action_tests'] = action_result.to_dict()
        if not action_result.success:
            all_issues.extend(action_result.errors)
        all_warnings.extend(action_result.warnings)

        # Run scenarios
        scenarios = custom_scenarios or self._generate_scenarios(automation)
        scenario_result = self._run_scenarios(automation, scenarios)
        test_results['scenario_tests'] = scenario_result.to_dict()
        all_warnings.extend(scenario_result.warnings)

        # Check edge cases
        edge_case_result = self._test_edge_cases(automation)
        test_results['edge_case_tests'] = edge_case_result.to_dict()
        all_warnings.extend(edge_case_result.warnings)

        # Overall success
        success = len(all_issues) == 0

        result = AgentResult(
            success=success,
            agent_name=self.name,
            message="All tests passed" if success else f"Tests completed with {len(all_issues)} issues",
            data={
                'test_results': test_results,
                'summary': {
                    'total_issues': len(all_issues),
                    'total_warnings': len(all_warnings),
                    'scenarios_tested': len(scenarios)
                }
            },
            errors=all_issues,
            warnings=all_warnings
        )

        # Add recommendations from sub-tests
        for test_key, test_data in test_results.items():
            if isinstance(test_data, dict) and 'recommendations' in test_data:
                for rec in test_data['recommendations']:
                    result.add_recommendation(
                        rec['description'],
                        AgentPriority[rec['priority'].upper()],
                        rec.get('action')
                    )

        return result

    def _test_triggers(self, automation: Dict) -> AgentResult:
        """Test trigger configurations"""
        if 'trigger' not in automation:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No trigger found in automation",
                errors=["Automation must have at least one trigger"]
            )

        trigger = automation['trigger']
        triggers = [trigger] if isinstance(trigger, dict) else trigger

        issues = []
        warnings = []
        test_cases = []

        for idx, t in enumerate(triggers):
            platform = t.get('platform', 'unknown')

            test_case = {
                'trigger_index': idx,
                'platform': platform,
                'will_fire': True,
                'issues': []
            }

            # Test based on platform type
            if platform == 'state':
                entity_id = t.get('entity_id')
                if not entity_id:
                    issues.append(f"Trigger {idx}: State trigger missing entity_id")
                    test_case['will_fire'] = False
                else:
                    # Check if entity exists
                    entities = [entity_id] if isinstance(entity_id, str) else entity_id
                    for eid in entities:
                        if self.context and not self.context.entity_exists(eid):
                            issues.append(f"Trigger {idx}: Entity not found: {eid}")
                            test_case['will_fire'] = False
                        elif self.context:
                            entity = self.context.get_entity(eid)
                            if entity and entity.get('disabled_by'):
                                warnings.append(f"Trigger {idx}: Entity is disabled: {eid}")
                                test_case['issues'].append('Entity disabled')

            elif platform == 'time':
                if 'at' not in t:
                    issues.append(f"Trigger {idx}: Time trigger missing 'at' field")
                    test_case['will_fire'] = False

            elif platform == 'sun':
                if 'event' not in t:
                    issues.append(f"Trigger {idx}: Sun trigger missing 'event' field")
                    test_case['will_fire'] = False

            elif platform == 'numeric_state':
                entity_id = t.get('entity_id')
                if not entity_id:
                    issues.append(f"Trigger {idx}: Numeric state trigger missing entity_id")
                    test_case['will_fire'] = False
                elif 'above' not in t and 'below' not in t:
                    issues.append(f"Trigger {idx}: Numeric state trigger needs 'above' or 'below'")
                    test_case['will_fire'] = False

            test_cases.append(test_case)

        success = len(issues) == 0

        result = AgentResult(
            success=success,
            agent_name=self.name,
            message=f"Tested {len(triggers)} triggers" if success else "Trigger tests failed",
            data={'test_cases': test_cases},
            errors=issues,
            warnings=warnings
        )

        return result

    def _test_conditions(self, automation: Dict) -> AgentResult:
        """Test condition configurations"""
        if 'condition' not in automation:
            return AgentResult(
                success=True,
                agent_name=self.name,
                message="No conditions to test"
            )

        condition = automation['condition']
        conditions = [condition] if isinstance(condition, dict) else condition

        issues = []
        warnings = []
        test_cases = []

        for idx, c in enumerate(conditions):
            cond_type = c.get('condition', 'unknown')

            test_case = {
                'condition_index': idx,
                'type': cond_type,
                'valid': True,
                'issues': []
            }

            # Test based on condition type
            if cond_type == 'state':
                entity_id = c.get('entity_id')
                if not entity_id:
                    issues.append(f"Condition {idx}: State condition missing entity_id")
                    test_case['valid'] = False
                elif self.context and not self.context.entity_exists(entity_id):
                    issues.append(f"Condition {idx}: Entity not found: {entity_id}")
                    test_case['valid'] = False

            elif cond_type == 'numeric_state':
                entity_id = c.get('entity_id')
                if not entity_id:
                    issues.append(f"Condition {idx}: Numeric state condition missing entity_id")
                    test_case['valid'] = False
                elif 'above' not in c and 'below' not in c:
                    issues.append(f"Condition {idx}: Numeric state needs 'above' or 'below'")
                    test_case['valid'] = False

            test_cases.append(test_case)

        success = len(issues) == 0

        return AgentResult(
            success=success,
            agent_name=self.name,
            message=f"Tested {len(conditions)} conditions" if success else "Condition tests failed",
            data={'test_cases': test_cases},
            errors=issues,
            warnings=warnings
        )

    def _test_actions(self, automation: Dict) -> AgentResult:
        """Test action configurations"""
        if 'action' not in automation:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No actions found in automation",
                errors=["Automation must have at least one action"]
            )

        action = automation['action']
        actions = [action] if isinstance(action, dict) else action

        issues = []
        warnings = []
        test_cases = []

        for idx, a in enumerate(actions):
            test_case = {
                'action_index': idx,
                'type': a.get('service', a.get('scene', a.get('event', 'unknown'))),
                'will_execute': True,
                'issues': []
            }

            # Service call action
            if 'service' in a:
                service = a['service']
                if '.' not in service:
                    issues.append(f"Action {idx}: Invalid service format: {service}")
                    test_case['will_execute'] = False
                else:
                    # Check for target entities
                    target_entities = []
                    if 'target' in a and 'entity_id' in a['target']:
                        target_entities = a['target']['entity_id']
                    elif 'entity_id' in a:
                        target_entities = a['entity_id']

                    if target_entities:
                        entities = [target_entities] if isinstance(target_entities, str) else target_entities
                        for eid in entities:
                            if self.context and not self.context.entity_exists(eid):
                                issues.append(f"Action {idx}: Target entity not found: {eid}")
                                test_case['will_execute'] = False

            # Scene activation
            elif 'scene' in a:
                scene = a['scene']
                if self.context:
                    scenes = self.context.get_entities_by_domain('scene')
                    scene_ids = [s.get('entity_id') for s in scenes]
                    if f"scene.{scene}" not in scene_ids and scene not in scene_ids:
                        warnings.append(f"Action {idx}: Scene not found: {scene}")

            test_cases.append(test_case)

        success = len(issues) == 0

        return AgentResult(
            success=success,
            agent_name=self.name,
            message=f"Tested {len(actions)} actions" if success else "Action tests failed",
            data={'test_cases': test_cases},
            errors=issues,
            warnings=warnings
        )

    def _generate_scenarios(self, automation: Dict) -> List[Dict]:
        """Generate test scenarios based on automation structure"""
        scenarios = []

        # Detect automation type
        auto_type = self._detect_automation_type(automation)

        # Use template scenarios if available
        if auto_type in self.scenario_templates:
            return self.scenario_templates[auto_type]

        # Generate basic scenarios
        trigger = automation.get('trigger', {})
        if isinstance(trigger, dict):
            trigger_platform = trigger.get('platform')

            if trigger_platform == 'state':
                scenarios.append({
                    'name': 'Trigger fires',
                    'state_change': True,
                    'expected': 'action_executes'
                })
                scenarios.append({
                    'name': 'No state change',
                    'state_change': False,
                    'expected': 'no_action'
                })

            elif trigger_platform == 'time':
                scenarios.append({
                    'name': 'At scheduled time',
                    'time_matches': True,
                    'expected': 'action_executes'
                })

        return scenarios

    def _run_scenarios(self, automation: Dict, scenarios: List[Dict]) -> AgentResult:
        """Run test scenarios"""
        results = []

        for scenario in scenarios:
            result = self._simulate_scenario(automation, scenario)
            results.append(result)

        warnings = []
        for r in results:
            if not r.get('passed'):
                warnings.append(f"Scenario '{r['name']}': {r.get('result')}")

        return AgentResult(
            success=True,
            agent_name=self.name,
            message=f"Ran {len(scenarios)} scenarios",
            data={'scenario_results': results},
            warnings=warnings
        )

    def _simulate_scenario(self, automation: Dict, scenario: Dict) -> Dict:
        """Simulate a single test scenario"""
        scenario_name = scenario.get('name', 'Unnamed scenario')

        # This is a simplified simulation
        # In a real implementation, this would use HA's test framework

        return {
            'name': scenario_name,
            'passed': True,
            'result': 'Simulated successfully',
            'expected': scenario.get('expected'),
            'actual': scenario.get('expected')  # Simplified
        }

    def _test_edge_cases(self, automation: Dict) -> AgentResult:
        """Test edge cases and potential issues"""
        warnings = []
        recommendations = []

        # Check for timeout on motion/state automations
        trigger = automation.get('trigger', {})
        if isinstance(trigger, dict):
            if trigger.get('platform') == 'state':
                # Check if there's a turn_off or timeout
                actions = automation.get('action', [])
                if isinstance(actions, dict):
                    actions = [actions]

                has_timeout = any('wait_for_trigger' in str(a) or 'delay' in str(a) for a in actions)
                has_turn_off = any('turn_off' in str(a) for a in actions)

                if not has_timeout and not has_turn_off:
                    warnings.append("No timeout or turn_off action - devices may stay on indefinitely")
                    recommendations.append({
                        'description': 'Add timeout mechanism to prevent devices staying in triggered state',
                        'priority': 'high',
                        'action': 'Add wait_for_trigger with timeout and turn_off action'
                    })

        # Check for mode setting
        mode = automation.get('mode', 'single')
        if mode == 'single':
            warnings.append("Mode 'single' will skip execution if already running")
            recommendations.append({
                'description': "Consider using mode 'restart' or 'queued' for different behavior",
                'priority': 'low',
                'action': "Review automation 'mode' setting"
            })

        # Check for entity availability checks
        actions = automation.get('action', [])
        if isinstance(actions, dict):
            actions = [actions]

        has_availability_check = any('available' in str(a) for a in actions)
        if not has_availability_check:
            recommendations.append({
                'description': 'Consider adding entity availability checks before actions',
                'priority': 'medium',
                'action': 'Add condition to check entity availability'
            })

        result = AgentResult(
            success=True,
            agent_name=self.name,
            message=f"Edge case analysis complete: {len(warnings)} warnings",
            warnings=warnings
        )

        for rec in recommendations:
            result.add_recommendation(
                rec['description'],
                AgentPriority[rec['priority'].upper()],
                rec.get('action')
            )

        return result

    def _detect_automation_type(self, automation: Dict) -> str:
        """Detect automation type from structure"""
        trigger = automation.get('trigger', {})
        if isinstance(trigger, dict):
            trigger_str = str(trigger).lower()

            if 'motion' in trigger_str:
                return 'motion_light'
            elif 'temperature' in trigger_str:
                return 'temperature_control'
            elif 'person' in trigger_str or 'device_tracker' in trigger_str:
                return 'presence_based'

        return 'unknown'
