"""
Best Practices Agent

Enforces Home Assistant best practices, security checks, and optimization recommendations.
"""

import re
from typing import Dict, List, Optional, Any, Tuple

from agents.base_agent import BaseAgent, AgentResult, AgentPriority
from agents.shared_context import SharedContext


class BestPracticesAgent(BaseAgent):
    """
    Agent for reviewing automations against best practices.

    Capabilities:
    - Security review
    - Performance analysis
    - Naming convention enforcement
    - Pattern recognition
    - Anti-pattern detection
    - Optimization suggestions
    """

    def __init__(self, context: Optional[SharedContext] = None):
        """Initialize the Best Practices Agent"""
        super().__init__(context)

        # Security patterns to check
        self.security_patterns = {
            'exposed_token': r'["\']([a-zA-Z0-9_-]{32,})["\']',
            'exposed_password': r'password["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            'exposed_api_key': r'api[_-]?key["\']?\s*[:=]\s*["\']([^"\']+)["\']',
        }

        # Performance anti-patterns
        self.anti_patterns = {
            'polling_sensor': {
                'pattern': r'platform:\s*template.*scan_interval',
                'message': 'Template sensor with scan_interval may cause performance issues',
                'suggestion': 'Use trigger-based template sensors instead'
            },
            'frequent_state_trigger': {
                'pattern': r'platform:\s*state.*for:\s*["\']?00:00:0[0-5]',
                'message': 'Very short state trigger duration can cause excessive triggers',
                'suggestion': 'Consider longer duration or different trigger type'
            }
        }

        # Naming convention pattern
        self.naming_pattern = r'^[a-z]+_[a-z_]+_[a-z_]+(?:_[a-z_]+)?$'

    @property
    def name(self) -> str:
        return "Best Practices Agent"

    @property
    def description(self) -> str:
        return "Reviews automations for best practices, security, and optimization"

    @property
    def capabilities(self) -> List[str]:
        return [
            "security_review",
            "performance_analysis",
            "naming_validation",
            "pattern_recognition",
            "anti_pattern_detection",
            "optimization_suggestions"
        ]

    def execute(self, **kwargs) -> AgentResult:
        """
        Execute best practices review.

        Supported kwargs:
            automation (dict): Automation to review
            review_type (str): 'full', 'security', 'performance', 'naming'
        """
        automation = kwargs.get('automation')
        review_type = kwargs.get('review_type', 'full')

        if not automation:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No automation provided for review",
                errors=["Provide 'automation' parameter"]
            )

        if review_type == 'full':
            return self._full_review(automation)
        elif review_type == 'security':
            return self._security_review(automation)
        elif review_type == 'performance':
            return self._performance_review(automation)
        elif review_type == 'naming':
            return self._naming_review(automation)
        else:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Unknown review type: {review_type}",
                errors=["Review type must be: full, security, performance, naming"]
            )

    def _full_review(self, automation: Dict) -> AgentResult:
        """Run complete best practices review"""
        issues = {
            'security': [],
            'performance': [],
            'naming': [],
            'maintainability': [],
            'reliability': []
        }

        # Security review
        security_result = self._security_review(automation)
        issues['security'] = security_result.errors + security_result.warnings

        # Performance review
        perf_result = self._performance_review(automation)
        issues['performance'] = perf_result.errors + perf_result.warnings

        # Naming review
        naming_result = self._naming_review(automation)
        issues['naming'] = naming_result.errors + naming_result.warnings

        # Maintainability review
        maint_issues = self._check_maintainability(automation)
        issues['maintainability'] = maint_issues

        # Reliability review
        rel_issues = self._check_reliability(automation)
        issues['reliability'] = rel_issues

        # Count critical issues
        critical_issues = issues['security'] + [i for i in issues['performance'] if 'critical' in i.lower()]

        # Generate recommendations
        recommendations = []

        # Security recommendations
        for issue in issues['security']:
            recommendations.append({
                'description': issue,
                'priority': AgentPriority.CRITICAL,
                'category': 'security'
            })

        # Performance recommendations
        for issue in issues['performance']:
            priority = AgentPriority.HIGH if 'performance' in issue.lower() else AgentPriority.MEDIUM
            recommendations.append({
                'description': issue,
                'priority': priority,
                'category': 'performance'
            })

        # Other recommendations
        for category, category_issues in issues.items():
            if category not in ['security', 'performance']:
                for issue in category_issues:
                    recommendations.append({
                        'description': issue,
                        'priority': AgentPriority.MEDIUM if category == 'reliability' else AgentPriority.LOW,
                        'category': category
                    })

        # Determine success (no critical issues)
        success = len(critical_issues) == 0

        result = AgentResult(
            success=success,
            agent_name=self.name,
            message=f"Review complete: {len(critical_issues)} critical issues found",
            data={
                'issues_by_category': {k: len(v) for k, v in issues.items()},
                'detailed_issues': issues,
                'score': self._calculate_score(issues)
            }
        )

        # Add recommendations
        for rec in recommendations:
            result.add_recommendation(
                rec['description'],
                rec['priority'],
                f"Fix {rec['category']} issue"
            )

        return result

    def _security_review(self, automation: Dict) -> AgentResult:
        """Review automation for security issues"""
        issues = []
        warnings = []

        automation_str = str(automation)

        # Check for exposed secrets
        for pattern_name, pattern in self.security_patterns.items():
            matches = re.findall(pattern, automation_str, re.IGNORECASE)
            if matches:
                issues.append(f"Potential {pattern_name.replace('_', ' ')}: {matches[0][:10]}...")

        # Check for unsafe templates
        if '{{' in automation_str:
            if 'exec' in automation_str or 'eval' in automation_str:
                issues.append("Potentially unsafe template code detected")

        # Check for hardcoded credentials
        if 'password' in automation_str.lower() or 'token' in automation_str.lower():
            warnings.append("Hardcoded credentials detected - use secrets.yaml instead")

        # Check for overly permissive triggers
        trigger = automation.get('trigger', {})
        if isinstance(trigger, dict):
            if trigger.get('platform') == 'state' and not trigger.get('from'):
                if not automation.get('condition'):
                    warnings.append("State trigger without 'from' and no conditions - may trigger too frequently")

        success = len(issues) == 0

        result = AgentResult(
            success=success,
            agent_name=self.name,
            message=f"Security review: {len(issues)} issues, {len(warnings)} warnings",
            data={'issues': issues, 'warnings': warnings},
            errors=issues,
            warnings=warnings
        )

        return result

    def _performance_review(self, automation: Dict) -> AgentResult:
        """Review automation for performance issues"""
        issues = []
        warnings = []

        automation_str = str(automation)

        # Check for anti-patterns
        for pattern_name, pattern_config in self.anti_patterns.items():
            if re.search(pattern_config['pattern'], automation_str, re.IGNORECASE):
                warnings.append(f"{pattern_config['message']}: {pattern_config['suggestion']}")

        # Check for efficient trigger patterns
        trigger = automation.get('trigger', {})
        triggers = [trigger] if isinstance(trigger, dict) else trigger

        for t in triggers:
            platform = t.get('platform')

            # State trigger without 'to' can be inefficient
            if platform == 'state' and 'to' not in t and 'above' not in t and 'below' not in t:
                warnings.append("State trigger without target state - will trigger on any state change")

            # Time pattern triggers can be resource-intensive
            if platform == 'time_pattern':
                warnings.append("Time pattern trigger - consider using specific time or time-based alternative")

        # Check for complex templates in triggers
        if '{{' in str(trigger):
            template_complexity = automation_str.count('{{')
            if template_complexity > 5:
                warnings.append("Complex templates in trigger may impact performance")

        # Check action efficiency
        actions = automation.get('action', [])
        if isinstance(actions, dict):
            actions = [actions]

        for action in actions:
            # Check for delays in action sequences
            if 'delay' in action:
                delay_str = str(action['delay'])
                if 'hours' in delay_str:
                    warnings.append("Long delay in action sequence - consider splitting into separate automations")

        # Check mode setting for parallel scenarios
        mode = automation.get('mode', 'single')
        if mode == 'parallel':
            warnings.append("Mode 'parallel' can consume resources - ensure it's necessary")

        success = len(issues) == 0

        result = AgentResult(
            success=success,
            agent_name=self.name,
            message=f"Performance review: {len(issues)} issues, {len(warnings)} warnings",
            data={'issues': issues, 'warnings': warnings},
            errors=issues,
            warnings=warnings
        )

        return result

    def _naming_review(self, automation: Dict) -> AgentResult:
        """Review entity naming conventions"""
        issues = []
        warnings = []

        # Check automation ID and alias
        auto_id = automation.get('id', '')
        alias = automation.get('alias', '')

        if not auto_id:
            warnings.append("Automation missing ID - recommended for UI editing")

        if not alias:
            warnings.append("Automation missing alias - recommended for readability")

        # Check entity naming in automation
        entities = self._extract_all_entities(automation)

        naming_convention = self.context.get_preference('naming_convention') if self.context else 'location_room_device_sensor'

        for entity in entities:
            # Check if follows naming convention
            if '.' in entity:
                entity_name = entity.split('.')[1]

                # Check for location_room_device pattern
                if naming_convention == 'location_room_device_sensor':
                    if not re.match(self.naming_pattern, entity_name):
                        warnings.append(f"Entity '{entity}' doesn't follow naming convention: {naming_convention}")

        success = len(issues) == 0

        result = AgentResult(
            success=success,
            agent_name=self.name,
            message=f"Naming review: {len(issues)} issues, {len(warnings)} warnings",
            data={'issues': issues, 'warnings': warnings, 'entities_checked': len(entities)},
            errors=issues,
            warnings=warnings
        )

        return result

    def _check_maintainability(self, automation: Dict) -> List[str]:
        """Check automation maintainability"""
        issues = []

        # Check for description
        if not automation.get('description'):
            issues.append("Missing description field - add context for future maintenance")

        # Check for meaningful alias
        alias = automation.get('alias', '')
        if len(alias) < 10:
            issues.append("Alias is very short - use descriptive name")

        # Check for complex logic that should be extracted
        actions = automation.get('action', [])
        if isinstance(actions, list) and len(actions) > 10:
            issues.append("Consider extracting complex action sequence to reusable script")

        # Check for inline templates vs input helpers
        automation_str = str(automation)
        template_count = automation_str.count('{{')
        if template_count > 10:
            issues.append("Many inline templates - consider using input helpers for reusability")

        return issues

    def _check_reliability(self, automation: Dict) -> List[str]:
        """Check automation reliability"""
        issues = []

        # Check for entity availability checks
        actions = automation.get('action', [])
        if isinstance(actions, dict):
            actions = [actions]

        has_availability_check = any('available' in str(a) for a in actions)
        if not has_availability_check and actions:
            issues.append("No entity availability check - automation may fail if entities offline")

        # Check for fallback logic
        has_choose = any('choose' in str(a) for a in actions)
        has_default = any('default' in str(a) for a in actions)

        if has_choose and not has_default:
            issues.append("Choose action without default - add fallback behavior")

        # Check for timeout mechanisms on state-based triggers
        trigger = automation.get('trigger', {})
        if isinstance(trigger, dict) and trigger.get('platform') == 'state':
            has_timeout = any('wait_for_trigger' in str(a) or 'delay' in str(a) for a in actions)
            if not has_timeout:
                issues.append("State-based trigger without timeout - consider adding auto-off mechanism")

        # Check mode setting
        if 'mode' not in automation:
            issues.append("Mode not explicitly set - default is 'single' which skips overlapping runs")

        return issues

    def _extract_all_entities(self, automation: Dict) -> List[str]:
        """Extract all entity IDs from automation"""
        entities = []

        def extract_from_value(value):
            if isinstance(value, str) and '.' in value and value.count('.') == 1:
                # Looks like an entity ID
                entities.append(value)
            elif isinstance(value, dict):
                for k, v in value.items():
                    if k == 'entity_id':
                        if isinstance(v, str):
                            entities.append(v)
                        elif isinstance(v, list):
                            entities.extend(v)
                    else:
                        extract_from_value(v)
            elif isinstance(value, list):
                for item in value:
                    extract_from_value(item)

        extract_from_value(automation)
        return list(set(entities))

    def _calculate_score(self, issues: Dict[str, List]) -> float:
        """Calculate automation quality score (0-100)"""
        total_points = 100

        # Deduct points for issues
        deductions = {
            'security': 30,  # -30 per security issue
            'performance': 15,  # -15 per performance issue
            'reliability': 10,  # -10 per reliability issue
            'naming': 5,  # -5 per naming issue
            'maintainability': 5  # -5 per maintainability issue
        }

        for category, category_issues in issues.items():
            deduction = deductions.get(category, 5) * len(category_issues)
            total_points -= deduction

        return max(0, min(100, total_points))
