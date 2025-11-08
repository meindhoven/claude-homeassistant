"""
Dashboard Best Practices Agent

Reviews dashboards for:
- User experience (UX) best practices
- Accessibility standards
- Visual design principles
- Information architecture
- Responsive design
- Performance optimization
"""

from typing import Dict, List, Optional, Any
from ..base_agent import BaseAgent, AgentResult, AgentStatus, AgentPriority


class DashboardBestPracticesAgent(BaseAgent):
    """Agent for reviewing dashboard design quality and UX"""

    def __init__(self, context=None):
        super().__init__(context)
        self._capabilities = [
            "ux_review",
            "accessibility_audit",
            "design_review",
            "performance_analysis",
            "mobile_optimization",
            "information_architecture"
        ]

        # UX best practices patterns
        self.ux_patterns = {
            'progressive_disclosure': {
                'name': 'Progressive Disclosure',
                'description': 'Show most important info first, details on demand',
                'importance': 'high'
            },
            'visual_hierarchy': {
                'name': 'Visual Hierarchy',
                'description': 'Clear distinction between primary and secondary content',
                'importance': 'high'
            },
            'consistency': {
                'name': 'Consistency',
                'description': 'Similar items should look and behave similarly',
                'importance': 'high'
            },
            'feedback': {
                'name': 'Immediate Feedback',
                'description': 'User actions should have immediate visual feedback',
                'importance': 'medium'
            },
            'error_prevention': {
                'name': 'Error Prevention',
                'description': 'Design to prevent errors before they occur',
                'importance': 'high'
            },
            'recognition_vs_recall': {
                'name': 'Recognition over Recall',
                'description': 'Show options rather than requiring memorization',
                'importance': 'medium'
            },
            'flexibility': {
                'name': 'Flexibility and Efficiency',
                'description': 'Support both novice and expert users',
                'importance': 'low'
            }
        }

        # Accessibility guidelines (WCAG-inspired for HA dashboards)
        self.accessibility_checks = {
            'color_contrast': {
                'description': 'Ensure sufficient color contrast for readability',
                'wcag_level': 'AA'
            },
            'text_size': {
                'description': 'Text should be readable without zooming',
                'wcag_level': 'AA'
            },
            'touch_targets': {
                'description': 'Interactive elements should be large enough for touch (44x44px minimum)',
                'wcag_level': 'AAA'
            },
            'meaningful_labels': {
                'description': 'All controls should have meaningful labels',
                'wcag_level': 'A'
            },
            'keyboard_navigation': {
                'description': 'All functionality should be keyboard accessible',
                'wcag_level': 'A'
            },
            'status_indicators': {
                'description': 'Use icons with text, not color alone, for status',
                'wcag_level': 'A'
            }
        }

        # Dashboard anti-patterns
        self.anti_patterns = {
            'information_overload': {
                'description': 'Too many cards/entities on single view',
                'impact': 'high',
                'threshold': 15
            },
            'inconsistent_cards': {
                'description': 'Mixing card types unnecessarily',
                'impact': 'medium'
            },
            'poor_grouping': {
                'description': 'Related items not grouped together',
                'impact': 'medium'
            },
            'missing_context': {
                'description': 'Cards without titles or context',
                'impact': 'medium'
            },
            'cluttered_layout': {
                'description': 'No visual breathing room',
                'impact': 'medium'
            },
            'hidden_functionality': {
                'description': 'Important controls buried in submenus',
                'impact': 'high'
            },
            'non_responsive': {
                'description': 'Layout breaks on mobile devices',
                'impact': 'high'
            }
        }

    @property
    def name(self) -> str:
        return "Dashboard Best Practices"

    @property
    def description(self) -> str:
        return "Reviews dashboards for UX, accessibility, and design best practices"

    @property
    def capabilities(self) -> List[str]:
        return self._capabilities

    def execute(self, **kwargs) -> AgentResult:
        """
        Execute dashboard best practices review

        Args:
            review_type: Type of review (full, ux, accessibility, design, performance)
            dashboard: Dashboard configuration to review
            dashboard_path: Path to dashboard YAML file

        Returns:
            AgentResult with review findings and recommendations
        """
        review_type = kwargs.get('review_type', 'full')
        dashboard = kwargs.get('dashboard')

        if not dashboard:
            return AgentResult(
                success=False,
                message="No dashboard provided for review",
                agent_name=self.name
            )

        try:
            if review_type == 'full':
                return self._full_review(dashboard)
            elif review_type == 'ux':
                return self._ux_review(dashboard)
            elif review_type == 'accessibility':
                return self._accessibility_review(dashboard)
            elif review_type == 'design':
                return self._design_review(dashboard)
            elif review_type == 'performance':
                return self._performance_review(dashboard)
            else:
                return AgentResult(
                    success=False,
                    message=f"Unknown review type: {review_type}",
                    agent_name=self.name
                )

        except Exception as e:
            return AgentResult(
                success=False,
                message=f"Review failed: {str(e)}",
                agent_name=self.name,
                errors=[str(e)]
            )

    def _full_review(self, dashboard: Dict) -> AgentResult:
        """Comprehensive dashboard review"""
        issues = []
        warnings = []
        recommendations = []

        # Run all review types
        ux_result = self._ux_review(dashboard)
        accessibility_result = self._accessibility_review(dashboard)
        design_result = self._design_review(dashboard)
        performance_result = self._performance_review(dashboard)

        # Consolidate results
        all_results = [ux_result, accessibility_result, design_result, performance_result]

        for result in all_results:
            issues.extend(result.errors)
            warnings.extend(result.warnings)
            recommendations.extend(result.recommendations)

        # Calculate quality score
        score = self._calculate_quality_score(dashboard, issues, warnings)

        # Prioritize recommendations
        recommendations = self._prioritize_recommendations(recommendations)

        return AgentResult(
            success=True,
            message=f"Dashboard review complete: Quality score {score}/100",
            agent_name=self.name,
            data={
                'quality_score': score,
                'issues': issues,
                'warnings': warnings,
                'view_count': len(dashboard.get('views', [])),
                'total_cards': self._count_total_cards(dashboard)
            },
            errors=issues,
            warnings=warnings,
            recommendations=recommendations[:10]  # Top 10 recommendations
        )

    def _ux_review(self, dashboard: Dict) -> AgentResult:
        """Review UX best practices"""
        issues = []
        warnings = []
        recommendations = []

        views = dashboard.get('views', [])

        for idx, view in enumerate(views):
            view_name = view.get('title', f'View {idx + 1}')
            cards = view.get('cards', [])

            # Check information overload
            if len(cards) > self.anti_patterns['information_overload']['threshold']:
                issues.append(f"{view_name}: Too many cards ({len(cards)})")
                recommendations.append({
                    'priority': 'high',
                    'description': f"Split '{view_name}' into multiple views - currently has {len(cards)} cards",
                    'category': 'ux',
                    'action': 'Consider grouping related cards into separate views'
                })

            # Check for missing titles
            untitled_cards = 0
            for card in cards:
                card_type = card.get('type', 'unknown')
                if not card.get('title') and card_type not in ['picture', 'weather-forecast', 'media-control']:
                    untitled_cards += 1

            if untitled_cards > 0:
                warnings.append(f"{view_name}: {untitled_cards} cards without titles")
                recommendations.append({
                    'priority': 'medium',
                    'description': f"Add titles to {untitled_cards} cards in '{view_name}' for better context",
                    'category': 'ux'
                })

            # Check for visual hierarchy
            has_header = any(card.get('type') == 'markdown' for card in cards)
            if not has_header and idx == 0:  # Overview view
                recommendations.append({
                    'priority': 'low',
                    'description': f"Add header/welcome card to '{view_name}' for better visual hierarchy",
                    'category': 'ux'
                })

        # Check view organization
        if len(views) == 1 and self._count_total_cards(dashboard) > 10:
            recommendations.append({
                'priority': 'high',
                'description': "Consider organizing into multiple views (e.g., Overview, Rooms, Security)",
                'category': 'ux',
                'action': 'Create specialized views for different functional areas'
            })

        return AgentResult(
            success=True,
            message=f"UX review complete: {len(issues)} issues, {len(warnings)} warnings",
            agent_name=self.name,
            data={
                'issues_count': len(issues),
                'warnings_count': len(warnings)
            },
            errors=issues,
            warnings=warnings,
            recommendations=recommendations
        )

    def _accessibility_review(self, dashboard: Dict) -> AgentResult:
        """Review accessibility standards"""
        issues = []
        warnings = []
        recommendations = []

        views = dashboard.get('views', [])

        for idx, view in enumerate(views):
            view_name = view.get('title', f'View {idx + 1}')
            cards = view.get('cards', [])

            # Check for meaningful labels
            for card in cards:
                entities = card.get('entities', [])

                if isinstance(entities, list):
                    for entity in entities:
                        if isinstance(entity, str):
                            # Entity without custom name
                            warnings.append(f"{view_name}: Entity '{entity}' may need custom name for clarity")

            # Check icon usage
            if not view.get('icon'):
                recommendations.append({
                    'priority': 'low',
                    'description': f"Add icon to '{view_name}' for better visual recognition",
                    'category': 'accessibility'
                })

        # General accessibility recommendations
        recommendations.append({
            'priority': 'medium',
            'description': "Ensure custom themes maintain sufficient color contrast (4.5:1 for text)",
            'category': 'accessibility',
            'action': 'Test with WCAG contrast checker'
        })

        recommendations.append({
            'priority': 'medium',
            'description': "Use icons with text labels, not color alone, for status indication",
            'category': 'accessibility'
        })

        return AgentResult(
            success=True,
            message=f"Accessibility review complete: {len(warnings)} potential issues",
            agent_name=self.name,
            data={
                'warnings_count': len(warnings)
            },
            warnings=warnings,
            recommendations=recommendations
        )

    def _design_review(self, dashboard: Dict) -> AgentResult:
        """Review visual design and consistency"""
        issues = []
        warnings = []
        recommendations = []

        views = dashboard.get('views', [])

        # Track card types used
        card_types_by_view = {}

        for idx, view in enumerate(views):
            view_name = view.get('title', f'View {idx + 1}')
            cards = view.get('cards', [])

            card_types = {}
            for card in cards:
                card_type = card.get('type', 'unknown')
                card_types[card_type] = card_types.get(card_type, 0) + 1

            card_types_by_view[view_name] = card_types

            # Check for inconsistent card usage
            if len(card_types) > 5:
                warnings.append(f"{view_name}: Uses {len(card_types)} different card types (may feel inconsistent)")
                recommendations.append({
                    'priority': 'low',
                    'description': f"Consider standardizing card types in '{view_name}'",
                    'category': 'design'
                })

        # Check for consistent view structure
        if len(views) > 2:
            # Check if all views have icons
            views_without_icons = [v.get('title', 'Untitled') for v in views if not v.get('icon')]
            if views_without_icons:
                recommendations.append({
                    'priority': 'medium',
                    'description': f"Add icons to views: {', '.join(views_without_icons)}",
                    'category': 'design',
                    'action': 'Icons improve navigation and visual consistency'
                })

        # General design recommendations
        recommendations.append({
            'priority': 'low',
            'description': "Consider using a custom theme for visual consistency across all cards",
            'category': 'design'
        })

        recommendations.append({
            'priority': 'medium',
            'description': "Use consistent spacing and padding between cards",
            'category': 'design'
        })

        return AgentResult(
            success=True,
            message=f"Design review complete: {len(warnings)} consistency issues",
            agent_name=self.name,
            data={
                'card_types_by_view': card_types_by_view
            },
            warnings=warnings,
            recommendations=recommendations
        )

    def _performance_review(self, dashboard: Dict) -> AgentResult:
        """Review performance and optimization"""
        issues = []
        warnings = []
        recommendations = []

        views = dashboard.get('views', [])
        total_cards = self._count_total_cards(dashboard)

        # Check total dashboard complexity
        if total_cards > 50:
            warnings.append(f"Dashboard has {total_cards} cards total - may impact performance")
            recommendations.append({
                'priority': 'high',
                'description': f"Large dashboard ({total_cards} cards) - consider splitting or lazy loading",
                'category': 'performance'
            })

        # Check for resource-intensive cards
        for idx, view in enumerate(views):
            view_name = view.get('title', f'View {idx + 1}')
            cards = view.get('cards', [])

            camera_cards = 0
            media_cards = 0

            for card in cards:
                card_type = card.get('type', 'unknown')

                if 'camera' in card_type or 'picture' in card_type:
                    camera_cards += 1
                elif 'media' in card_type:
                    media_cards += 1

            if camera_cards > 4:
                warnings.append(f"{view_name}: {camera_cards} camera cards may impact performance")
                recommendations.append({
                    'priority': 'medium',
                    'description': f"Limit camera cards in '{view_name}' to 4 or less",
                    'category': 'performance',
                    'action': 'Consider separate camera view or use conditional cards'
                })

        # General performance recommendations
        if total_cards > 30:
            recommendations.append({
                'priority': 'medium',
                'description': "Consider using conditional cards to show/hide based on state",
                'category': 'performance',
                'action': 'Reduces initial render load'
            })

        return AgentResult(
            success=True,
            message=f"Performance review complete: {len(warnings)} potential issues",
            agent_name=self.name,
            data={
                'total_cards': total_cards,
                'view_count': len(views)
            },
            warnings=warnings,
            recommendations=recommendations
        )

    def _calculate_quality_score(self, dashboard: Dict, issues: List, warnings: List) -> float:
        """Calculate dashboard quality score (0-100)"""
        score = 100.0

        # Deduct for issues
        score -= len(issues) * 10
        score -= len(warnings) * 5

        # Bonus for good practices
        views = dashboard.get('views', [])

        # Bonus for multiple organized views
        if 2 <= len(views) <= 6:
            score += 5

        # Bonus for views with icons
        views_with_icons = sum(1 for v in views if v.get('icon'))
        score += (views_with_icons / len(views) * 5) if views else 0

        # Bonus for reasonable card count per view
        reasonable_views = 0
        for view in views:
            cards = view.get('cards', [])
            if 3 <= len(cards) <= 12:
                reasonable_views += 1

        if views:
            score += (reasonable_views / len(views) * 10)

        # Ensure score is between 0 and 100
        return max(0.0, min(100.0, score))

    def _prioritize_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """Sort recommendations by priority"""
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

        return sorted(
            recommendations,
            key=lambda r: priority_order.get(r.get('priority', 'low'), 3)
        )

    def _count_total_cards(self, dashboard: Dict) -> int:
        """Count total cards across all views"""
        total = 0
        for view in dashboard.get('views', []):
            total += len(view.get('cards', []))
        return total
