"""
Validation Agent

Comprehensive validation with intelligent error resolution and fix suggestions.
Wraps existing validation tools and adds intelligence layer.
"""

import subprocess
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))

from agents.base_agent import BaseAgent, AgentResult, AgentPriority
from agents.shared_context import SharedContext


class ValidationAgent(BaseAgent):
    """
    Agent for validating Home Assistant configurations.

    Capabilities:
    - Multi-layer validation (YAML, references, official HA)
    - Intelligent error parsing and explanation
    - Specific fix suggestions
    - Conflict detection
    - Entity capability validation
    """

    def __init__(self, context: Optional[SharedContext] = None):
        """Initialize the Validation Agent"""
        super().__init__(context)

        self.tools_dir = Path(__file__).parent.parent.parent / "tools"
        self.config_dir = Path(__file__).parent.parent.parent / "config"

        # Error pattern matchers with fix suggestions
        self.error_patterns = {
            'entity_not_found': {
                'pattern': r"Entity '([^']+)' not found",
                'severity': 'error',
                'fix_suggestion': 'Check entity registry or update entity_id'
            },
            'invalid_yaml': {
                'pattern': r'YAML.*error',
                'severity': 'error',
                'fix_suggestion': 'Check YAML syntax - indentation, colons, quotes'
            },
            'invalid_service': {
                'pattern': r"Service '([^']+)' not found",
                'severity': 'error',
                'fix_suggestion': 'Verify service exists in domain.service format'
            },
            'invalid_platform': {
                'pattern': r"Platform '([^']+)' not found",
                'severity': 'error',
                'fix_suggestion': 'Check platform name spelling'
            },
            'missing_required': {
                'pattern': r"required key not provided.*\[([^\]]+)\]",
                'severity': 'error',
                'fix_suggestion': 'Add required configuration key'
            },
            'disabled_entity': {
                'pattern': r"Entity '([^']+)' is disabled",
                'severity': 'warning',
                'fix_suggestion': 'Enable entity in Home Assistant entity registry'
            }
        }

    @property
    def name(self) -> str:
        return "Validation Agent"

    @property
    def description(self) -> str:
        return "Validates Home Assistant configurations with intelligent error resolution"

    @property
    def capabilities(self) -> List[str]:
        return [
            "validate_yaml",
            "validate_references",
            "validate_official",
            "parse_errors",
            "suggest_fixes",
            "detect_conflicts"
        ]

    def execute(self, **kwargs) -> AgentResult:
        """
        Execute validation based on provided parameters.

        Supported kwargs:
            file_path (str): Specific file to validate
            validation_type (str): 'yaml', 'references', 'official', or 'full'
            automation (dict): Automation config to validate
            fix_errors (bool): Attempt to auto-fix common errors
        """
        file_path = kwargs.get('file_path')
        validation_type = kwargs.get('validation_type', 'full')
        automation = kwargs.get('automation')
        fix_errors = kwargs.get('fix_errors', False)

        if automation:
            return self._validate_automation(automation)

        if validation_type == 'full':
            return self._run_full_validation(file_path, fix_errors)
        elif validation_type == 'yaml':
            return self._run_yaml_validation(file_path)
        elif validation_type == 'references':
            return self._run_reference_validation(file_path)
        elif validation_type == 'official':
            return self._run_official_validation()
        else:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Unknown validation type: {validation_type}",
                errors=[f"Validation type must be one of: full, yaml, references, official"]
            )

    def _run_full_validation(self, file_path: Optional[str], fix_errors: bool) -> AgentResult:
        """Run all validation layers"""
        results = {
            'yaml': None,
            'references': None,
            'official': None
        }

        all_errors = []
        all_warnings = []
        all_suggestions = []

        # Layer 1: YAML Validation
        self.logger.info("Running YAML validation...")
        yaml_result = self._run_yaml_validation(file_path)
        results['yaml'] = yaml_result.to_dict()

        if not yaml_result.success:
            all_errors.extend(yaml_result.errors)
            parsed_errors = self._parse_errors(yaml_result.errors)
            all_suggestions.extend(parsed_errors['suggestions'])
        else:
            all_warnings.extend(yaml_result.warnings)

        # Layer 2: Reference Validation
        self.logger.info("Running reference validation...")
        ref_result = self._run_reference_validation(file_path)
        results['references'] = ref_result.to_dict()

        if not ref_result.success:
            all_errors.extend(ref_result.errors)
            parsed_errors = self._parse_errors(ref_result.errors)
            all_suggestions.extend(parsed_errors['suggestions'])
        else:
            all_warnings.extend(ref_result.warnings)

        # Layer 3: Official HA Validation (only if previous layers pass)
        if yaml_result.success and ref_result.success:
            self.logger.info("Running official HA validation...")
            official_result = self._run_official_validation()
            results['official'] = official_result.to_dict()

            if not official_result.success:
                all_errors.extend(official_result.errors)
                parsed_errors = self._parse_errors(official_result.errors)
                all_suggestions.extend(parsed_errors['suggestions'])
            else:
                all_warnings.extend(official_result.warnings)
        else:
            results['official'] = "Skipped due to earlier failures"

        # Determine overall success
        overall_success = yaml_result.success and ref_result.success

        if results['official'] not in ["Skipped due to earlier failures", None]:
            overall_success = overall_success and results['official']['success']

        # Build result
        message = "All validations passed" if overall_success else "Validation failed"

        result = AgentResult(
            success=overall_success,
            agent_name=self.name,
            message=message,
            data={
                'validation_results': results,
                'summary': {
                    'total_errors': len(all_errors),
                    'total_warnings': len(all_warnings),
                    'layers_passed': sum([
                        1 if results['yaml']['success'] else 0,
                        1 if results['references']['success'] else 0,
                        1 if isinstance(results['official'], dict) and results['official'].get('success') else 0
                    ])
                }
            },
            errors=list(set(all_errors)),  # Deduplicate
            warnings=list(set(all_warnings))
        )

        # Add unique suggestions
        seen_suggestions = set()
        for suggestion in all_suggestions:
            suggestion_key = suggestion['description']
            if suggestion_key not in seen_suggestions:
                seen_suggestions.add(suggestion_key)
                result.add_recommendation(
                    suggestion['description'],
                    suggestion.get('priority', AgentPriority.MEDIUM),
                    suggestion.get('action')
                )

        return result

    def _run_yaml_validation(self, file_path: Optional[str]) -> AgentResult:
        """Run YAML syntax validation"""
        try:
            cmd = ['python', str(self.tools_dir / 'yaml_validator.py')]
            if file_path:
                cmd.append(file_path)

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.config_dir.parent,
                timeout=30
            )

            success = proc.returncode == 0
            output = proc.stdout + proc.stderr

            errors = []
            warnings = []

            # Parse output for errors and warnings
            for line in output.split('\n'):
                if 'error' in line.lower() or 'failed' in line.lower():
                    if line.strip():
                        errors.append(line.strip())
                elif 'warning' in line.lower():
                    if line.strip():
                        warnings.append(line.strip())

            return AgentResult(
                success=success,
                agent_name=self.name,
                message="YAML validation passed" if success else "YAML validation failed",
                data={'output': output},
                errors=errors,
                warnings=warnings
            )

        except subprocess.TimeoutExpired:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="YAML validation timed out",
                errors=["Validation took too long to complete"]
            )
        except Exception as e:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"YAML validation error: {str(e)}",
                errors=[str(e)]
            )

    def _run_reference_validation(self, file_path: Optional[str]) -> AgentResult:
        """Run entity/device reference validation"""
        try:
            cmd = ['python', str(self.tools_dir / 'reference_validator.py')]
            if file_path:
                cmd.append(file_path)

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.config_dir.parent,
                timeout=30
            )

            success = proc.returncode == 0
            output = proc.stdout + proc.stderr

            errors = []
            warnings = []

            for line in output.split('\n'):
                if 'error' in line.lower() or 'not found' in line.lower():
                    if line.strip():
                        errors.append(line.strip())
                elif 'warning' in line.lower() or 'disabled' in line.lower():
                    if line.strip():
                        warnings.append(line.strip())

            return AgentResult(
                success=success,
                agent_name=self.name,
                message="Reference validation passed" if success else "Reference validation failed",
                data={'output': output},
                errors=errors,
                warnings=warnings
            )

        except subprocess.TimeoutExpired:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="Reference validation timed out",
                errors=["Validation took too long to complete"]
            )
        except Exception as e:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Reference validation error: {str(e)}",
                errors=[str(e)]
            )

    def _run_official_validation(self) -> AgentResult:
        """Run official Home Assistant validation"""
        try:
            cmd = ['python', str(self.tools_dir / 'ha_official_validator.py')]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.config_dir.parent,
                timeout=60  # Official validation can take longer
            )

            success = proc.returncode == 0
            output = proc.stdout + proc.stderr

            errors = []
            warnings = []

            for line in output.split('\n'):
                if 'error' in line.lower() or 'failed' in line.lower():
                    if line.strip():
                        errors.append(line.strip())
                elif 'warning' in line.lower():
                    if line.strip():
                        warnings.append(line.strip())

            return AgentResult(
                success=success,
                agent_name=self.name,
                message="Official HA validation passed" if success else "Official HA validation failed",
                data={'output': output},
                errors=errors,
                warnings=warnings
            )

        except subprocess.TimeoutExpired:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="Official validation timed out",
                errors=["Validation took too long to complete"]
            )
        except Exception as e:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Official validation error: {str(e)}",
                errors=[str(e)]
            )

    def _validate_automation(self, automation: Dict) -> AgentResult:
        """Validate a single automation configuration"""
        errors = []
        warnings = []
        suggestions = []

        # Check required fields
        required_fields = ['trigger', 'action']
        for field in required_fields:
            if field not in automation:
                errors.append(f"Missing required field: {field}")

        # Check for ID (recommended)
        if 'id' not in automation:
            warnings.append("Automation missing 'id' field (recommended for UI editing)")
            suggestions.append({
                'description': "Add unique 'id' field to automation",
                'priority': AgentPriority.MEDIUM,
                'action': "Add 'id' field with unique value"
            })

        # Check for alias (recommended)
        if 'alias' not in automation:
            warnings.append("Automation missing 'alias' field (recommended for readability)")
            suggestions.append({
                'description': "Add descriptive 'alias' field to automation",
                'priority': AgentPriority.LOW,
                'action': "Add 'alias' field with descriptive name"
            })

        # Validate trigger
        if 'trigger' in automation:
            trigger_validation = self._validate_trigger(automation['trigger'])
            errors.extend(trigger_validation['errors'])
            warnings.extend(trigger_validation['warnings'])
            suggestions.extend(trigger_validation['suggestions'])

        # Validate condition
        if 'condition' in automation:
            condition_validation = self._validate_condition(automation['condition'])
            errors.extend(condition_validation['errors'])
            warnings.extend(condition_validation['warnings'])
            suggestions.extend(condition_validation['suggestions'])

        # Validate action
        if 'action' in automation:
            action_validation = self._validate_action(automation['action'])
            errors.extend(action_validation['errors'])
            warnings.extend(action_validation['warnings'])
            suggestions.extend(action_validation['suggestions'])

        success = len(errors) == 0

        result = AgentResult(
            success=success,
            agent_name=self.name,
            message="Automation validation passed" if success else "Automation validation failed",
            data={'automation': automation},
            errors=errors,
            warnings=warnings
        )

        for suggestion in suggestions:
            result.add_recommendation(
                suggestion['description'],
                suggestion.get('priority', AgentPriority.MEDIUM),
                suggestion.get('action')
            )

        return result

    def _validate_trigger(self, trigger: Any) -> Dict[str, List]:
        """Validate trigger configuration"""
        errors = []
        warnings = []
        suggestions = []

        triggers = [trigger] if isinstance(trigger, dict) else trigger

        for t in triggers:
            if not isinstance(t, dict):
                errors.append(f"Invalid trigger format: {t}")
                continue

            # Check for platform
            if 'platform' not in t:
                errors.append("Trigger missing 'platform' field")
                continue

            platform = t['platform']

            # Platform-specific validation
            if platform == 'state':
                if 'entity_id' not in t:
                    errors.append("State trigger missing 'entity_id'")
                else:
                    # Verify entity exists
                    entity_ids = [t['entity_id']] if isinstance(t['entity_id'], str) else t['entity_id']
                    for entity_id in entity_ids:
                        if self.context and not self.context.entity_exists(entity_id):
                            errors.append(f"Entity not found: {entity_id}")
                            # Find similar
                            similar = self._find_similar_entity(entity_id)
                            if similar:
                                suggestions.append({
                                    'description': f"Did you mean '{similar}'?",
                                    'priority': AgentPriority.HIGH,
                                    'action': f"Replace '{entity_id}' with '{similar}'"
                                })

            elif platform == 'time':
                if 'at' not in t:
                    errors.append("Time trigger missing 'at' field")

            elif platform == 'sun':
                if 'event' not in t:
                    errors.append("Sun trigger missing 'event' field")

        return {'errors': errors, 'warnings': warnings, 'suggestions': suggestions}

    def _validate_condition(self, condition: Any) -> Dict[str, List]:
        """Validate condition configuration"""
        errors = []
        warnings = []
        suggestions = []

        conditions = [condition] if isinstance(condition, dict) else condition

        for c in conditions:
            if not isinstance(c, dict):
                errors.append(f"Invalid condition format: {c}")
                continue

            # Check for condition type
            if 'condition' not in c:
                errors.append("Condition missing 'condition' field")

        return {'errors': errors, 'warnings': warnings, 'suggestions': suggestions}

    def _validate_action(self, action: Any) -> Dict[str, List]:
        """Validate action configuration"""
        errors = []
        warnings = []
        suggestions = []

        actions = [action] if isinstance(action, dict) else action

        for a in actions:
            if not isinstance(a, dict):
                errors.append(f"Invalid action format: {a}")
                continue

            # Check for service
            if 'service' not in a:
                errors.append("Action missing 'service' field")
                continue

            # Validate service format
            service = a['service']
            if '.' not in service:
                errors.append(f"Invalid service format (should be domain.service): {service}")

            # Check for target or entity_id
            if 'target' not in a and 'entity_id' not in a and 'data' not in a:
                warnings.append(f"Service '{service}' has no target entities")

        return {'errors': errors, 'warnings': warnings, 'suggestions': suggestions}

    def _parse_errors(self, errors: List[str]) -> Dict[str, Any]:
        """Parse error messages and generate fix suggestions"""
        parsed = {
            'categorized_errors': [],
            'suggestions': []
        }

        for error in errors:
            matched = False

            for error_type, config in self.error_patterns.items():
                pattern = config['pattern']
                match = re.search(pattern, error, re.IGNORECASE)

                if match:
                    matched = True
                    parsed['categorized_errors'].append({
                        'type': error_type,
                        'message': error,
                        'severity': config['severity'],
                        'matched_value': match.group(1) if match.groups() else None
                    })

                    # Generate suggestion
                    suggestion = {
                        'description': config['fix_suggestion'],
                        'priority': AgentPriority.HIGH if config['severity'] == 'error' else AgentPriority.MEDIUM,
                        'action': f"Fix: {error}"
                    }

                    # Add specific suggestions for entity not found
                    if error_type == 'entity_not_found' and match.groups():
                        entity_id = match.group(1)
                        similar = self._find_similar_entity(entity_id)
                        if similar:
                            suggestion['description'] = f"Entity '{entity_id}' not found. Did you mean '{similar}'?"
                            suggestion['action'] = f"Replace '{entity_id}' with '{similar}'"

                    parsed['suggestions'].append(suggestion)
                    break

            if not matched:
                # Uncategorized error
                parsed['categorized_errors'].append({
                    'type': 'unknown',
                    'message': error,
                    'severity': 'error'
                })

        return parsed

    def _find_similar_entity(self, entity_id: str) -> Optional[str]:
        """Find similar entity ID for suggestions"""
        if not self.context:
            return None

        # Use entity discovery agent's similarity logic
        entities = self.context.search_entities(entity_id.split('.')[-1])

        if entities:
            return entities[0].get('entity_id')

        return None
