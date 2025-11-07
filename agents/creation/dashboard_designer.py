"""
Dashboard Designer Agent

Helps design Home Assistant dashboards with best practices for:
- Card selection based on entity types
- Layout organization and responsive design
- User experience and accessibility
- Visual hierarchy and information architecture
- Dashboard structure (views, sections, cards)
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import yaml
from ..base_agent import BaseAgent, AgentResult, AgentStatus, AgentPriority


class DashboardDesignerAgent(BaseAgent):
    """Agent for designing Home Assistant dashboards with UX best practices"""

    def __init__(self, context=None):
        super().__init__(context)
        self._capabilities = [
            "card_selection",
            "layout_design",
            "view_organization",
            "responsive_design",
            "entity_grouping",
            "theme_suggestions"
        ]

        # Card type recommendations based on entity domain and device class
        self.card_recommendations = {
            'light': {
                'single': 'light',
                'group': 'entities',
                'grid': 'grid',
                'recommended': 'Use light card for quick toggles, entities card for detailed controls'
            },
            'climate': {
                'single': 'thermostat',
                'group': 'entities',
                'recommended': 'Thermostat card provides best UX for temperature control'
            },
            'media_player': {
                'single': 'media-control',
                'group': 'entities',
                'recommended': 'Media control card with album art and playback controls'
            },
            'camera': {
                'single': 'picture-entity',
                'group': 'grid',
                'recommended': 'Picture entity or picture glance for live feed'
            },
            'sensor': {
                'temperature': 'sensor',
                'humidity': 'sensor',
                'battery': 'entities',
                'default': 'entity',
                'recommended': 'Gauge or sensor card for numeric values, entity for simple display'
            },
            'binary_sensor': {
                'motion': 'entity',
                'door': 'entity',
                'window': 'entity',
                'default': 'entity',
                'recommended': 'Entity card with custom icons for status visualization'
            },
            'switch': {
                'single': 'button',
                'group': 'entities',
                'recommended': 'Button card for actions, entities for grouped switches'
            },
            'cover': {
                'single': 'cover',
                'group': 'entities',
                'recommended': 'Cover card with position slider for blinds/shades'
            },
            'lock': {
                'single': 'lock',
                'group': 'entities',
                'recommended': 'Lock card with secure controls'
            },
            'vacuum': {
                'single': 'vacuum',
                'recommended': 'Vacuum card with map and controls'
            },
            'weather': {
                'single': 'weather-forecast',
                'recommended': 'Weather forecast card with hourly/daily view'
            },
            'alarm_control_panel': {
                'single': 'alarm-panel',
                'recommended': 'Alarm panel card for security system control'
            }
        }

        # Layout best practices
        self.layout_patterns = {
            'overview': {
                'description': 'Main dashboard view with key information',
                'sections': ['Quick Actions', 'Status Summary', 'Climate', 'Security', 'Energy'],
                'card_limit': 12,
                'columns': 'auto'
            },
            'room': {
                'description': 'Single room control view',
                'sections': ['Lighting', 'Climate', 'Media', 'Sensors'],
                'card_limit': 8,
                'columns': 2
            },
            'security': {
                'description': 'Security and monitoring view',
                'sections': ['Alarm', 'Cameras', 'Sensors', 'Locks'],
                'card_limit': 10,
                'columns': 'auto'
            },
            'climate': {
                'description': 'Climate and energy management',
                'sections': ['Thermostats', 'Temperature Sensors', 'Energy Usage'],
                'card_limit': 8,
                'columns': 2
            },
            'media': {
                'description': 'Media and entertainment control',
                'sections': ['Now Playing', 'Devices', 'Favorites'],
                'card_limit': 6,
                'columns': 1
            }
        }

    @property
    def name(self) -> str:
        return "Dashboard Designer"

    @property
    def description(self) -> str:
        return "Designs user-friendly Home Assistant dashboards with best practices"

    @property
    def capabilities(self) -> List[str]:
        return self._capabilities

    def execute(self, **kwargs) -> AgentResult:
        """
        Execute dashboard design task

        Args:
            design_type: Type of design task (full_dashboard, view, card, optimize)
            description: Natural language description of desired dashboard
            entities: List of entity IDs to include
            layout_type: Layout pattern (overview, room, security, climate, media)
            existing_dashboard: Existing dashboard config to optimize

        Returns:
            AgentResult with dashboard configuration
        """
        design_type = kwargs.get('design_type', 'full_dashboard')

        try:
            if design_type == 'full_dashboard':
                return self._design_full_dashboard(**kwargs)
            elif design_type == 'view':
                return self._design_view(**kwargs)
            elif design_type == 'card':
                return self._design_card(**kwargs)
            elif design_type == 'optimize':
                return self._optimize_dashboard(**kwargs)
            elif design_type == 'suggest_cards':
                return self._suggest_cards_for_entities(**kwargs)
            else:
                return AgentResult(
                    success=False,
                    message=f"Unknown design type: {design_type}",
                    agent_name=self.name
                )

        except Exception as e:
            return AgentResult(
                success=False,
                message=f"Dashboard design failed: {str(e)}",
                agent_name=self.name,
                errors=[str(e)]
            )

    def _design_full_dashboard(self, **kwargs) -> AgentResult:
        """Design complete dashboard with multiple views"""
        description = kwargs.get('description', '')
        entities = kwargs.get('entities', [])

        # If no entities provided, get from context
        if not entities and self.context:
            all_entities = self.context.get_entities()
            entities = [e['entity_id'] for e in all_entities if not e.get('disabled', False)]

        # Group entities by area and domain
        grouped_entities = self._group_entities(entities)

        # Create views based on areas and common patterns
        views = []

        # Overview view (always include)
        overview_view = self._create_overview_view(grouped_entities)
        views.append(overview_view)

        # Room views for each area
        for area, area_entities in grouped_entities.get('by_area', {}).items():
            if area and area != 'none' and len(area_entities) >= 3:
                room_view = self._create_room_view(area, area_entities)
                views.append(room_view)

        # Specialized views
        if grouped_entities.get('by_domain', {}).get('camera', []):
            security_view = self._create_security_view(grouped_entities)
            views.append(security_view)

        if grouped_entities.get('by_domain', {}).get('climate', []):
            climate_view = self._create_climate_view(grouped_entities)
            views.append(climate_view)

        if grouped_entities.get('by_domain', {}).get('media_player', []):
            media_view = self._create_media_view(grouped_entities)
            views.append(media_view)

        dashboard_config = {
            'title': 'Home Dashboard',
            'views': views
        }

        recommendations = [
            {
                'priority': 'high',
                'description': 'Test dashboard on mobile devices for responsive design',
                'category': 'ux'
            },
            {
                'priority': 'medium',
                'description': 'Consider adding custom themes for better visual consistency',
                'category': 'design'
            },
            {
                'priority': 'medium',
                'description': 'Use badges for quick status overview at top of dashboard',
                'category': 'layout'
            }
        ]

        return AgentResult(
            success=True,
            message=f"Created dashboard with {len(views)} views",
            agent_name=self.name,
            data={
                'dashboard': dashboard_config,
                'view_count': len(views),
                'entity_count': len(entities)
            },
            recommendations=recommendations
        )

    def _design_view(self, **kwargs) -> AgentResult:
        """Design a single dashboard view"""
        view_name = kwargs.get('view_name', 'New View')
        entities = kwargs.get('entities', [])
        layout_type = kwargs.get('layout_type', 'overview')

        # Get layout pattern
        pattern = self.layout_patterns.get(layout_type, self.layout_patterns['overview'])

        # Group entities
        grouped = self._group_entities(entities)

        # Create cards organized by sections
        cards = []

        # Add cards based on entity types
        for domain, domain_entities in grouped.get('by_domain', {}).items():
            section_cards = self._create_cards_for_domain(domain, domain_entities)
            cards.extend(section_cards)

        view_config = {
            'title': view_name,
            'path': view_name.lower().replace(' ', '_'),
            'cards': cards
        }

        # Add layout configuration
        if pattern['columns'] != 'auto':
            view_config['column'] = pattern['columns']

        recommendations = []

        # Check card count
        if len(cards) > pattern['card_limit']:
            recommendations.append({
                'priority': 'medium',
                'description': f"View has {len(cards)} cards, recommended max is {pattern['card_limit']}. Consider splitting into multiple views.",
                'category': 'layout'
            })

        return AgentResult(
            success=True,
            message=f"Created view '{view_name}' with {len(cards)} cards",
            agent_name=self.name,
            data={
                'view': view_config,
                'card_count': len(cards),
                'pattern_used': layout_type
            },
            recommendations=recommendations
        )

    def _design_card(self, **kwargs) -> AgentResult:
        """Design a single card for specific entities"""
        entities = kwargs.get('entities', [])
        card_type = kwargs.get('card_type', 'auto')

        if not entities:
            return AgentResult(
                success=False,
                message="No entities provided for card design",
                agent_name=self.name
            )

        # Auto-detect card type if needed
        if card_type == 'auto':
            card_type = self._recommend_card_type(entities)

        # Create card configuration
        card_config = self._create_card_config(card_type, entities)

        return AgentResult(
            success=True,
            message=f"Created {card_type} card with {len(entities)} entities",
            agent_name=self.name,
            data={
                'card': card_config,
                'card_type': card_type,
                'entity_count': len(entities)
            }
        )

    def _optimize_dashboard(self, **kwargs) -> AgentResult:
        """Optimize existing dashboard for better UX"""
        dashboard = kwargs.get('existing_dashboard')

        if not dashboard:
            return AgentResult(
                success=False,
                message="No dashboard provided for optimization",
                agent_name=self.name
            )

        issues = []
        optimizations = []

        # Check views
        views = dashboard.get('views', [])

        for idx, view in enumerate(views):
            view_name = view.get('title', f'View {idx + 1}')
            cards = view.get('cards', [])

            # Check card count
            if len(cards) > 15:
                issues.append({
                    'view': view_name,
                    'issue': 'Too many cards',
                    'count': len(cards),
                    'recommendation': 'Split into multiple views or use grid cards for grouping'
                })

            # Check for inefficient card types
            for card in cards:
                card_type = card.get('type')
                entities = card.get('entities', [])

                if card_type == 'entities' and len(entities) == 1:
                    optimizations.append({
                        'view': view_name,
                        'optimization': f"Single entity in entities card - use entity card instead",
                        'entity': entities[0] if entities else 'unknown'
                    })

                # Check for missing titles
                if not card.get('title') and card_type not in ['picture', 'weather-forecast']:
                    optimizations.append({
                        'view': view_name,
                        'optimization': f"Add title to {card_type} card for better clarity"
                    })

        recommendations = []

        if issues:
            for issue in issues:
                recommendations.append({
                    'priority': 'high',
                    'description': f"{issue['view']}: {issue['issue']} ({issue['count']} cards) - {issue['recommendation']}",
                    'category': 'layout'
                })

        if optimizations:
            for opt in optimizations[:5]:  # Top 5 optimizations
                recommendations.append({
                    'priority': 'medium',
                    'description': f"{opt['view']}: {opt['optimization']}",
                    'category': 'ux'
                })

        return AgentResult(
            success=True,
            message=f"Analyzed dashboard: found {len(issues)} issues and {len(optimizations)} optimization opportunities",
            agent_name=self.name,
            data={
                'issues': issues,
                'optimizations': optimizations,
                'view_count': len(views)
            },
            recommendations=recommendations
        )

    def _suggest_cards_for_entities(self, **kwargs) -> AgentResult:
        """Suggest appropriate card types for given entities"""
        entities = kwargs.get('entities', [])

        if not entities:
            return AgentResult(
                success=False,
                message="No entities provided",
                agent_name=self.name
            )

        suggestions = []

        # Group by domain
        grouped = self._group_entities(entities)

        for domain, domain_entities in grouped.get('by_domain', {}).items():
            recommendation = self.card_recommendations.get(domain, {})

            if len(domain_entities) == 1:
                card_type = recommendation.get('single', 'entity')
            else:
                card_type = recommendation.get('group', 'entities')

            suggestions.append({
                'domain': domain,
                'entity_count': len(domain_entities),
                'entities': domain_entities,
                'recommended_card': card_type,
                'reason': recommendation.get('recommended', 'Standard display')
            })

        return AgentResult(
            success=True,
            message=f"Generated card suggestions for {len(entities)} entities",
            agent_name=self.name,
            data={
                'suggestions': suggestions,
                'entity_count': len(entities)
            }
        )

    def _group_entities(self, entity_ids: List[str]) -> Dict:
        """Group entities by area and domain"""
        by_area = {}
        by_domain = {}

        if not self.context:
            # Fallback: group by domain from entity_id
            for entity_id in entity_ids:
                domain = entity_id.split('.')[0]
                if domain not in by_domain:
                    by_domain[domain] = []
                by_domain[domain].append(entity_id)

            return {'by_area': {}, 'by_domain': by_domain}

        # Get entity details from context
        for entity_id in entity_ids:
            if self.context.entity_exists(entity_id):
                entity = self.context.get_entity(entity_id)

                # Group by area
                area = entity.get('area_id', 'none')
                if area not in by_area:
                    by_area[area] = []
                by_area[area].append(entity_id)

                # Group by domain
                domain = entity_id.split('.')[0]
                if domain not in by_domain:
                    by_domain[domain] = []
                by_domain[domain].append(entity_id)
            else:
                # Entity not in registry, group by domain only
                domain = entity_id.split('.')[0]
                if domain not in by_domain:
                    by_domain[domain] = []
                by_domain[domain].append(entity_id)

        return {'by_area': by_area, 'by_domain': by_domain}

    def _create_overview_view(self, grouped_entities: Dict) -> Dict:
        """Create overview dashboard view"""
        cards = []

        # Welcome/Status card (markdown)
        cards.append({
            'type': 'markdown',
            'content': '# 🏠 Home Overview\nWelcome home!'
        })

        # Quick actions (lights, climate)
        by_domain = grouped_entities.get('by_domain', {})

        if by_domain.get('light'):
            lights = by_domain['light'][:6]  # Top 6 lights
            cards.append({
                'type': 'entities',
                'title': 'Lights',
                'entities': lights
            })

        if by_domain.get('climate'):
            cards.append({
                'type': 'thermostat',
                'entity': by_domain['climate'][0]
            })

        # Security status
        if by_domain.get('alarm_control_panel'):
            cards.append({
                'type': 'alarm-panel',
                'entity': by_domain['alarm_control_panel'][0]
            })

        # Weather
        if by_domain.get('weather'):
            cards.append({
                'type': 'weather-forecast',
                'entity': by_domain['weather'][0]
            })

        return {
            'title': 'Overview',
            'path': 'overview',
            'icon': 'mdi:home',
            'cards': cards
        }

    def _create_room_view(self, area: str, entities: List[str]) -> Dict:
        """Create view for a specific room/area"""
        cards = []

        # Group entities by domain
        grouped = self._group_entities(entities)
        by_domain = grouped.get('by_domain', {})

        # Lights
        if by_domain.get('light'):
            cards.append({
                'type': 'entities',
                'title': 'Lights',
                'entities': by_domain['light']
            })

        # Climate
        if by_domain.get('climate'):
            cards.append({
                'type': 'thermostat',
                'entity': by_domain['climate'][0]
            })

        # Media players
        if by_domain.get('media_player'):
            for player in by_domain['media_player']:
                cards.append({
                    'type': 'media-control',
                    'entity': player
                })

        # Sensors (temperature, humidity)
        sensors = []
        for entity_id in by_domain.get('sensor', []):
            if any(x in entity_id for x in ['temperature', 'humidity', 'battery']):
                sensors.append(entity_id)

        if sensors:
            cards.append({
                'type': 'entities',
                'title': 'Sensors',
                'entities': sensors
            })

        return {
            'title': area.replace('_', ' ').title(),
            'path': area,
            'icon': 'mdi:floor-plan',
            'cards': cards
        }

    def _create_security_view(self, grouped_entities: Dict) -> Dict:
        """Create security monitoring view"""
        cards = []
        by_domain = grouped_entities.get('by_domain', {})

        # Alarm panel
        if by_domain.get('alarm_control_panel'):
            cards.append({
                'type': 'alarm-panel',
                'entity': by_domain['alarm_control_panel'][0]
            })

        # Cameras
        if by_domain.get('camera'):
            for camera in by_domain['camera'][:4]:  # Max 4 cameras
                cards.append({
                    'type': 'picture-entity',
                    'entity': camera,
                    'camera_view': 'live'
                })

        # Door/window sensors
        sensors = []
        for entity_id in by_domain.get('binary_sensor', []):
            if any(x in entity_id for x in ['door', 'window', 'motion']):
                sensors.append(entity_id)

        if sensors:
            cards.append({
                'type': 'entities',
                'title': 'Sensors',
                'entities': sensors
            })

        # Locks
        if by_domain.get('lock'):
            cards.append({
                'type': 'entities',
                'title': 'Locks',
                'entities': by_domain['lock']
            })

        return {
            'title': 'Security',
            'path': 'security',
            'icon': 'mdi:shield-home',
            'cards': cards
        }

    def _create_climate_view(self, grouped_entities: Dict) -> Dict:
        """Create climate control view"""
        cards = []
        by_domain = grouped_entities.get('by_domain', {})

        # Thermostats
        if by_domain.get('climate'):
            for thermostat in by_domain['climate']:
                cards.append({
                    'type': 'thermostat',
                    'entity': thermostat
                })

        # Temperature sensors
        temp_sensors = []
        for entity_id in by_domain.get('sensor', []):
            if 'temperature' in entity_id:
                temp_sensors.append(entity_id)

        if temp_sensors:
            cards.append({
                'type': 'entities',
                'title': 'Temperature Sensors',
                'entities': temp_sensors
            })

        return {
            'title': 'Climate',
            'path': 'climate',
            'icon': 'mdi:thermostat',
            'cards': cards
        }

    def _create_media_view(self, grouped_entities: Dict) -> Dict:
        """Create media control view"""
        cards = []
        by_domain = grouped_entities.get('by_domain', {})

        if by_domain.get('media_player'):
            for player in by_domain['media_player']:
                cards.append({
                    'type': 'media-control',
                    'entity': player
                })

        return {
            'title': 'Media',
            'path': 'media',
            'icon': 'mdi:music',
            'cards': cards
        }

    def _create_cards_for_domain(self, domain: str, entities: List[str]) -> List[Dict]:
        """Create appropriate cards for entities in a domain"""
        cards = []
        recommendation = self.card_recommendations.get(domain, {})

        if len(entities) == 1:
            card_type = recommendation.get('single', 'entity')
            cards.append(self._create_card_config(card_type, entities))
        else:
            # Group multiple entities
            card_type = recommendation.get('group', 'entities')
            cards.append(self._create_card_config(card_type, entities))

        return cards

    def _recommend_card_type(self, entities: List[str]) -> str:
        """Recommend card type based on entities"""
        if not entities:
            return 'entity'

        # Get domain from first entity
        domain = entities[0].split('.')[0]
        recommendation = self.card_recommendations.get(domain, {})

        if len(entities) == 1:
            return recommendation.get('single', 'entity')
        else:
            return recommendation.get('group', 'entities')

    def _create_card_config(self, card_type: str, entities: List[str]) -> Dict:
        """Create card configuration"""
        config = {
            'type': card_type
        }

        if card_type in ['entity', 'light', 'thermostat', 'media-control', 'picture-entity', 'lock', 'alarm-panel', 'weather-forecast']:
            # Single entity cards
            config['entity'] = entities[0]
        else:
            # Multi-entity cards
            config['entities'] = entities

        return config
