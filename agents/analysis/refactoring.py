"""
Refactoring Agent

Improves and optimizes existing Home Assistant automations.
Detects duplication, suggests script extraction, and optimizes performance.
"""

from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
import re

from agents.base_agent import BaseAgent, AgentResult, AgentPriority
from agents.shared_context import SharedContext


class RefactoringAgent(BaseAgent):
    """
    Agent for refactoring Home Assistant automations.

    Capabilities:
    - Detect duplicate logic
    - Suggest script extraction
    - Optimize performance
    - Improve readability
    - Batch entity renaming
    - Consolidate similar automations
    """

    def __init__(self, context: Optional[SharedContext] = None):
        """Initialize the Refactoring Agent"""
        super().__init__(context)

        # Pattern signatures for detecting similar automations
        self.pattern_signatures = {}

    @property
    def name(self) -> str:
        return "Refactoring Agent"

    @property
    def description(self) -> str:
        return "Refactors and optimizes Home Assistant automations"

    @property
    def capabilities(self) -> List[str]:
        return [
            "detect_duplicates",
            "suggest_scripts",
            "optimize_performance",
            "improve_readability",
            "rename_entities",
            "consolidate_automations"
        ]

    def execute(self, **kwargs) -> AgentResult:
        """
        Execute refactoring analysis.

        Supported kwargs:
            automation (dict): Single automation to refactor
            automations (list): Multiple automations to analyze
            refactor_type (str): 'duplicates', 'scripts', 'optimize', 'consolidate', 'all'
        """
        automation = kwargs.get('automation')
        automations = kwargs.get('automations')
        refactor_type = kwargs.get('refactor_type', 'all')

        # Get all automations if not provided
        if not automations and self.context:
            automations = self.context.get_automations()

        if not automations and not automation:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No automations provided for refactoring",
                errors=["Provide 'automation' or 'automations' parameter"]
            )

        if automation and not automations:
            automations = [automation]

        if refactor_type == 'all':
            return self._full_refactoring_analysis(automations)
        elif refactor_type == 'duplicates':
            return self._detect_duplicates(automations)
        elif refactor_type == 'scripts':
            return self._suggest_script_extraction(automations)
        elif refactor_type == 'optimize':
            return self._optimize_automations(automations)
        elif refactor_type == 'consolidate':
            return self._consolidate_automations(automations)
        else:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Unknown refactor type: {refactor_type}",
                errors=["Type must be: duplicates, scripts, optimize, consolidate, all"]
            )

    def _full_refactoring_analysis(self, automations: List[Dict]) -> AgentResult:
        """Run complete refactoring analysis"""
        results = {
            'duplicates': None,
            'script_opportunities': None,
            'optimizations': None,
            'consolidations': None
        }

        all_recommendations = []

        # Detect duplicates
        dup_result = self._detect_duplicates(automations)
        results['duplicates'] = dup_result.data
        all_recommendations.extend(dup_result.recommendations)

        # Suggest script extraction
        script_result = self._suggest_script_extraction(automations)
        results['script_opportunities'] = script_result.data
        all_recommendations.extend(script_result.recommendations)

        # Optimization opportunities
        opt_result = self._optimize_automations(automations)
        results['optimizations'] = opt_result.data
        all_recommendations.extend(opt_result.recommendations)

        # Consolidation opportunities
        cons_result = self._consolidate_automations(automations)
        results['consolidations'] = cons_result.data
        all_recommendations.extend(cons_result.recommendations)

        # Summary
        total_opportunities = (
            len(results['duplicates'].get('duplicate_groups', [])) +
            len(results['script_opportunities'].get('extraction_opportunities', [])) +
            len(results['optimizations'].get('optimization_opportunities', [])) +
            len(results['consolidations'].get('consolidation_groups', []))
        )

        result = AgentResult(
            success=True,
            agent_name=self.name,
            message=f"Refactoring analysis complete: {total_opportunities} opportunities found",
            data={
                'summary': {
                    'automations_analyzed': len(automations),
                    'duplicate_patterns': len(results['duplicates'].get('duplicate_groups', [])),
                    'script_opportunities': len(results['script_opportunities'].get('extraction_opportunities', [])),
                    'optimizations': len(results['optimizations'].get('optimization_opportunities', [])),
                    'consolidations': len(results['consolidations'].get('consolidation_groups', []))
                },
                'detailed_results': results
            }
        )

        # Add all recommendations
        for rec in all_recommendations:
            result.add_recommendation(
                rec['description'],
                rec.get('priority', AgentPriority.MEDIUM),
                rec.get('action')
            )

        return result

    def _detect_duplicates(self, automations: List[Dict]) -> AgentResult:
        """Detect duplicate or similar automation patterns"""
        # Group automations by similarity
        duplicate_groups = []

        # Create signatures for each automation
        signatures = {}
        for auto in automations:
            sig = self._create_signature(auto)
            auto_id = auto.get('alias', auto.get('id', 'unknown'))
            signatures[auto_id] = sig

        # Find similar signatures
        checked = set()
        for auto1_id, sig1 in signatures.items():
            if auto1_id in checked:
                continue

            similar_group = [auto1_id]

            for auto2_id, sig2 in signatures.items():
                if auto2_id == auto1_id or auto2_id in checked:
                    continue

                similarity = self._calculate_similarity(sig1, sig2)
                if similarity > 0.7:  # 70% similar
                    similar_group.append(auto2_id)
                    checked.add(auto2_id)

            if len(similar_group) > 1:
                duplicate_groups.append({
                    'automations': similar_group,
                    'count': len(similar_group),
                    'pattern': sig1['pattern_type']
                })
                checked.add(auto1_id)

        # Create recommendations
        recommendations = []
        for group in duplicate_groups:
            recommendations.append({
                'description': f"Found {group['count']} similar {group['pattern']} automations: {', '.join(group['automations'][:3])}",
                'priority': AgentPriority.HIGH,
                'action': "Consider extracting common logic to script or using templates"
            })

        result = AgentResult(
            success=True,
            agent_name=self.name,
            message=f"Found {len(duplicate_groups)} groups of similar automations",
            data={
                'duplicate_groups': duplicate_groups,
                'total_automations': len(automations)
            }
        )

        for rec in recommendations:
            result.add_recommendation(rec['description'], rec['priority'], rec.get('action'))

        return result

    def _suggest_script_extraction(self, automations: List[Dict]) -> AgentResult:
        """Suggest opportunities to extract common logic to scripts"""
        # Find repeated action sequences
        action_patterns = defaultdict(list)

        for auto in automations:
            actions = auto.get('action', [])
            if isinstance(actions, dict):
                actions = [actions]

            # Create pattern for action sequence
            for i in range(len(actions)):
                if i + 2 <= len(actions):  # Look at sequences of 2+ actions
                    pattern = self._create_action_pattern(actions[i:i+2])
                    auto_id = auto.get('alias', auto.get('id', 'unknown'))
                    action_patterns[pattern].append(auto_id)

        # Find patterns used in multiple automations
        extraction_opportunities = []

        for pattern, auto_list in action_patterns.items():
            if len(auto_list) >= 2:  # Used in 2+ automations
                extraction_opportunities.append({
                    'pattern': pattern,
                    'used_in': auto_list,
                    'count': len(auto_list),
                    'recommended_script_name': self._suggest_script_name(pattern)
                })

        # Create recommendations
        recommendations = []
        for opp in extraction_opportunities[:5]:  # Top 5 opportunities
            recommendations.append({
                'description': f"Extract '{opp['recommended_script_name']}' pattern used in {opp['count']} automations",
                'priority': AgentPriority.MEDIUM,
                'action': f"Create script for pattern used by: {', '.join(opp['used_in'][:3])}"
            })

        result = AgentResult(
            success=True,
            agent_name=self.name,
            message=f"Found {len(extraction_opportunities)} script extraction opportunities",
            data={'extraction_opportunities': extraction_opportunities}
        )

        for rec in recommendations:
            result.add_recommendation(rec['description'], rec['priority'], rec.get('action'))

        return result

    def _optimize_automations(self, automations: List[Dict]) -> AgentResult:
        """Find optimization opportunities"""
        optimizations = []

        for auto in automations:
            auto_id = auto.get('alias', auto.get('id', 'unknown'))
            auto_opts = []

            # Check trigger optimization
            trigger = auto.get('trigger', {})
            triggers = [trigger] if isinstance(trigger, dict) else trigger

            for t in triggers:
                # State trigger without 'to' - can be optimized
                if t.get('platform') == 'state' and 'to' not in t:
                    auto_opts.append({
                        'type': 'trigger_optimization',
                        'description': 'Add specific target state to reduce unnecessary triggers',
                        'location': 'trigger'
                    })

                # Numeric state trigger - could use template
                if t.get('platform') == 'numeric_state':
                    auto_opts.append({
                        'type': 'trigger_optimization',
                        'description': 'Consider using template trigger for complex numeric logic',
                        'location': 'trigger'
                    })

            # Check condition optimization
            conditions = auto.get('condition', [])
            if isinstance(conditions, dict):
                conditions = [conditions]

            if len(conditions) > 5:
                auto_opts.append({
                    'type': 'condition_optimization',
                    'description': 'Many conditions - consider using choose action instead',
                    'location': 'condition'
                })

            # Check action optimization
            actions = auto.get('action', [])
            if isinstance(actions, dict):
                actions = [actions]

            # Check for sequential service calls that could be batched
            service_calls = [a for a in actions if 'service' in a]
            if len(service_calls) > 3:
                # Check if same service called multiple times
                services = [a['service'] for a in service_calls]
                from collections import Counter
                service_counts = Counter(services)
                for service, count in service_counts.items():
                    if count > 2:
                        auto_opts.append({
                            'type': 'action_optimization',
                            'description': f"Service '{service}' called {count} times - consider batching targets",
                            'location': 'action'
                        })

            if auto_opts:
                optimizations.append({
                    'automation': auto_id,
                    'opportunities': auto_opts
                })

        # Create recommendations
        recommendations = []
        for opt in optimizations[:10]:  # Top 10
            for opp in opt['opportunities']:
                recommendations.append({
                    'description': f"{opt['automation']}: {opp['description']}",
                    'priority': AgentPriority.LOW,
                    'action': f"Optimize {opp['location']} in {opt['automation']}"
                })

        result = AgentResult(
            success=True,
            agent_name=self.name,
            message=f"Found optimization opportunities in {len(optimizations)} automations",
            data={'optimization_opportunities': optimizations}
        )

        for rec in recommendations[:10]:  # Limit recommendations
            result.add_recommendation(rec['description'], rec['priority'], rec.get('action'))

        return result

    def _consolidate_automations(self, automations: List[Dict]) -> AgentResult:
        """Find automations that could be consolidated"""
        consolidation_groups = []

        # Group by trigger type and target entities
        trigger_groups = defaultdict(list)

        for auto in automations:
            trigger = auto.get('trigger', {})
            if isinstance(trigger, dict):
                trigger_type = trigger.get('platform', 'unknown')
                entity = trigger.get('entity_id', '')

                key = f"{trigger_type}:{entity}"
                auto_id = auto.get('alias', auto.get('id', 'unknown'))
                trigger_groups[key].append(auto_id)

        # Find groups with multiple automations
        for key, auto_list in trigger_groups.items():
            if len(auto_list) >= 2:
                trigger_type = key.split(':')[0]
                consolidation_groups.append({
                    'trigger_type': trigger_type,
                    'automations': auto_list,
                    'count': len(auto_list),
                    'suggestion': f"Consolidate into single automation with choose action"
                })

        # Create recommendations
        recommendations = []
        for group in consolidation_groups[:5]:  # Top 5
            recommendations.append({
                'description': f"Consolidate {group['count']} {group['trigger_type']} automations: {', '.join(group['automations'][:3])}",
                'priority': AgentPriority.MEDIUM,
                'action': group['suggestion']
            })

        result = AgentResult(
            success=True,
            agent_name=self.name,
            message=f"Found {len(consolidation_groups)} consolidation opportunities",
            data={'consolidation_groups': consolidation_groups}
        )

        for rec in recommendations:
            result.add_recommendation(rec['description'], rec['priority'], rec.get('action'))

        return result

    def _create_signature(self, automation: Dict) -> Dict[str, Any]:
        """Create a signature for automation pattern matching"""
        trigger = automation.get('trigger', {})
        if isinstance(trigger, dict):
            trigger_platform = trigger.get('platform', 'unknown')
        else:
            trigger_platform = 'multiple'

        actions = automation.get('action', [])
        if isinstance(actions, dict):
            actions = [actions]

        action_types = []
        for action in actions:
            if 'service' in action:
                action_types.append('service')
            elif 'scene' in action:
                action_types.append('scene')
            elif 'delay' in action:
                action_types.append('delay')
            else:
                action_types.append('other')

        return {
            'trigger_platform': trigger_platform,
            'has_condition': 'condition' in automation,
            'action_sequence': ','.join(action_types),
            'action_count': len(actions),
            'pattern_type': f"{trigger_platform}_automation"
        }

    def _calculate_similarity(self, sig1: Dict, sig2: Dict) -> float:
        """Calculate similarity between two automation signatures"""
        score = 0.0

        # Trigger platform match
        if sig1['trigger_platform'] == sig2['trigger_platform']:
            score += 0.3

        # Condition presence match
        if sig1['has_condition'] == sig2['has_condition']:
            score += 0.2

        # Action sequence similarity
        if sig1['action_sequence'] == sig2['action_sequence']:
            score += 0.4
        elif len(set(sig1['action_sequence'].split(',')) & set(sig2['action_sequence'].split(','))) > 0:
            score += 0.2

        # Action count similarity
        count_diff = abs(sig1['action_count'] - sig2['action_count'])
        if count_diff == 0:
            score += 0.1
        elif count_diff <= 2:
            score += 0.05

        return score

    def _create_action_pattern(self, actions: List[Dict]) -> str:
        """Create a pattern string from action sequence"""
        pattern_parts = []

        for action in actions:
            if 'service' in action:
                service = action['service'].split('.')[1] if '.' in action['service'] else action['service']
                pattern_parts.append(f"service:{service}")
            elif 'scene' in action:
                pattern_parts.append("scene")
            elif 'delay' in action:
                pattern_parts.append("delay")
            elif 'wait_for_trigger' in action:
                pattern_parts.append("wait")
            else:
                pattern_parts.append("other")

        return "->".join(pattern_parts)

    def _suggest_script_name(self, pattern: str) -> str:
        """Suggest a script name based on action pattern"""
        # Extract key actions from pattern
        parts = pattern.split('->')

        if 'turn_on' in pattern and 'delay' in pattern and 'turn_off' in pattern:
            return 'timed_device_control'
        elif 'scene' in pattern:
            return 'scene_activation_sequence'
        elif 'notify' in pattern:
            return 'notification_sequence'
        else:
            return f"action_sequence_{'_'.join(parts[:2])}"
