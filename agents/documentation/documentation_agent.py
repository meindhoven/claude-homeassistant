"""
Documentation Agent

Automatically generates and maintains documentation for Home Assistant automations.
Creates markdown files, entity relationship maps, and changelogs.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import re

from agents.base_agent import BaseAgent, AgentResult, AgentPriority
from agents.shared_context import SharedContext


class DocumentationAgent(BaseAgent):
    """
    Agent for generating automation documentation.

    Capabilities:
    - Generate markdown documentation for automations
    - Create entity relationship maps
    - Maintain changelogs
    - Document best practices
    - Generate searchable indexes
    - Track automation changes over time
    """

    def __init__(self, context: Optional[SharedContext] = None):
        """Initialize the Documentation Agent"""
        super().__init__(context)

        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.automations_docs_dir = self.docs_dir / "automations"
        self.entities_docs_dir = self.docs_dir / "entities"
        self.changelog_path = self.docs_dir / "changelog.md"

        # Category mapping for automation organization
        self.category_keywords = {
            'lighting': ['light', 'lamp', 'brightness', 'motion'],
            'climate': ['temperature', 'heat', 'cool', 'climate', 'thermostat'],
            'security': ['alarm', 'lock', 'door', 'window', 'camera', 'security'],
            'media': ['media_player', 'sonos', 'tv', 'speaker'],
            'presence': ['person', 'device_tracker', 'home', 'away'],
            'energy': ['power', 'energy', 'consumption'],
            'notification': ['notify', 'message', 'alert'],
        }

    @property
    def name(self) -> str:
        return "Documentation Agent"

    @property
    def description(self) -> str:
        return "Generates and maintains documentation for Home Assistant automations"

    @property
    def capabilities(self) -> List[str]:
        return [
            "generate_automation_docs",
            "create_entity_map",
            "update_changelog",
            "generate_index",
            "document_best_practices",
            "track_changes"
        ]

    def execute(self, **kwargs) -> AgentResult:
        """
        Execute documentation generation.

        Supported kwargs:
            automation (dict): Automation to document
            doc_type (str): 'automation', 'entity_map', 'changelog', 'index', 'all'
            update_existing (bool): Update existing documentation
        """
        automation = kwargs.get('automation')
        doc_type = kwargs.get('doc_type', 'automation')
        update_existing = kwargs.get('update_existing', True)

        if doc_type == 'all':
            return self._generate_all_documentation()
        elif doc_type == 'automation' and automation:
            return self._document_automation(automation, update_existing)
        elif doc_type == 'entity_map':
            return self._generate_entity_map()
        elif doc_type == 'changelog':
            return self._update_changelog(automation)
        elif doc_type == 'index':
            return self._generate_index()
        else:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="Invalid documentation type or missing automation",
                errors=["Provide valid 'doc_type' and required parameters"]
            )

    def _document_automation(self, automation: Dict, update_existing: bool) -> AgentResult:
        """Generate markdown documentation for an automation"""
        # Extract automation details
        auto_id = automation.get('id', 'unknown')
        alias = automation.get('alias', auto_id)
        description = automation.get('description', '')

        # Determine category
        category = self._categorize_automation(automation)

        # Create category directory if needed
        category_dir = self.automations_docs_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename from alias
        filename = self._generate_filename(alias) + ".md"
        doc_path = category_dir / filename

        # Check if exists and update_existing is False
        if doc_path.exists() and not update_existing:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Documentation already exists: {doc_path}",
                errors=["Use update_existing=True to overwrite"]
            )

        # Generate documentation content
        doc_content = self._generate_automation_doc_content(automation, category)

        # Write documentation
        try:
            with open(doc_path, 'w') as f:
                f.write(doc_content)

            # Update changelog
            self._add_changelog_entry(automation, 'created' if not doc_path.exists() else 'updated')

            return AgentResult(
                success=True,
                agent_name=self.name,
                message=f"Documentation {'updated' if update_existing else 'created'}: {doc_path}",
                data={
                    'path': str(doc_path),
                    'category': category,
                    'automation_id': auto_id,
                    'alias': alias
                }
            )

        except Exception as e:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Failed to write documentation: {str(e)}",
                errors=[str(e)]
            )

    def _generate_automation_doc_content(self, automation: Dict, category: str) -> str:
        """Generate markdown content for automation documentation"""
        auto_id = automation.get('id', 'unknown')
        alias = automation.get('alias', auto_id)
        description = automation.get('description', 'No description provided')
        mode = automation.get('mode', 'single')

        # Extract entities
        trigger_entities = self._extract_entities_from_config(automation.get('trigger', {}))
        condition_entities = self._extract_entities_from_config(automation.get('condition', {}))
        action_entities = self._extract_entities_from_config(automation.get('action', {}))

        # Get related automations
        related = self._find_related_automations(automation)

        # Format triggers
        trigger_desc = self._describe_triggers(automation.get('trigger', {}))
        condition_desc = self._describe_conditions(automation.get('condition', {}))
        action_desc = self._describe_actions(automation.get('action', {}))

        # Build documentation
        doc = f"""# {alias}

**ID**: `{auto_id}`
**Category**: {category}
**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Last Modified**: {datetime.now().strftime('%Y-%m-%d')}
**Status**: Active
**Mode**: {mode}

## Purpose

{description}

## Behavior

{trigger_desc}

{condition_desc}

{action_desc}

## Entities

### Triggers
"""

        if trigger_entities:
            for entity in trigger_entities:
                entity_info = self._get_entity_info(entity)
                doc += f"- `{entity}` - {entity_info}\n"
        else:
            doc += "- No specific entities\n"

        doc += "\n### Conditions\n"
        if condition_entities:
            for entity in condition_entities:
                entity_info = self._get_entity_info(entity)
                doc += f"- `{entity}` - {entity_info}\n"
        else:
            doc += "- No entity conditions\n"

        doc += "\n### Actions\n"
        if action_entities:
            for entity in action_entities:
                entity_info = self._get_entity_info(entity)
                doc += f"- `{entity}` - {entity_info}\n"
        else:
            doc += "- Service calls without specific entities\n"

        doc += "\n## Edge Cases\n\n"
        edge_cases = self._identify_edge_cases(automation)
        if edge_cases:
            for case in edge_cases:
                doc += f"- {case}\n"
        else:
            doc += "- No known edge cases\n"

        doc += "\n## Potential Improvements\n\n"
        improvements = self._suggest_improvements(automation)
        if improvements:
            for improvement in improvements:
                doc += f"- {improvement}\n"
        else:
            doc += "- None identified\n"

        if related:
            doc += "\n## Related Automations\n\n"
            for r in related:
                doc += f"- `{r}`\n"

        doc += f"\n## Configuration\n\n```yaml\n{yaml.dump(automation, default_flow_style=False, sort_keys=False)}```\n"

        doc += f"\n---\n*Generated by Documentation Agent on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

        return doc

    def _categorize_automation(self, automation: Dict) -> str:
        """Determine category for automation"""
        auto_str = str(automation).lower()

        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in auto_str:
                    return category

        return 'general'

    def _generate_filename(self, alias: str) -> str:
        """Generate filesystem-safe filename from alias"""
        # Remove special characters, replace spaces with underscores
        filename = re.sub(r'[^\w\s-]', '', alias.lower())
        filename = re.sub(r'[-\s]+', '_', filename)
        return filename[:50]  # Limit length

    def _extract_entities_from_config(self, config: Any) -> List[str]:
        """Extract entity IDs from configuration"""
        entities = []

        if isinstance(config, dict):
            for key, value in config.items():
                if key == 'entity_id':
                    if isinstance(value, str):
                        entities.append(value)
                    elif isinstance(value, list):
                        entities.extend(value)
                elif isinstance(value, (dict, list)):
                    entities.extend(self._extract_entities_from_config(value))

        elif isinstance(config, list):
            for item in config:
                entities.extend(self._extract_entities_from_config(item))

        return list(set(entities))  # Deduplicate

    def _describe_triggers(self, trigger: Any) -> str:
        """Generate human-readable description of triggers"""
        if not trigger:
            return "**Trigger**: None"

        triggers = [trigger] if isinstance(trigger, dict) else trigger

        desc = "**Triggers**:\n"
        for t in triggers:
            platform = t.get('platform', 'unknown')

            if platform == 'state':
                entity = t.get('entity_id', 'unknown')
                to_state = t.get('to', 'any state')
                desc += f"- When `{entity}` changes to `{to_state}`\n"

            elif platform == 'time':
                time_at = t.get('at', 'unknown time')
                desc += f"- At time: `{time_at}`\n"

            elif platform == 'sun':
                event = t.get('event', 'unknown')
                desc += f"- At {event}\n"

            elif platform == 'numeric_state':
                entity = t.get('entity_id', 'unknown')
                above = t.get('above')
                below = t.get('below')
                if above:
                    desc += f"- When `{entity}` goes above `{above}`\n"
                if below:
                    desc += f"- When `{entity}` goes below `{below}`\n"

            else:
                desc += f"- Platform: `{platform}`\n"

        return desc

    def _describe_conditions(self, condition: Any) -> str:
        """Generate human-readable description of conditions"""
        if not condition:
            return ""

        conditions = [condition] if isinstance(condition, dict) else condition

        desc = "**Conditions**:\n"
        for c in conditions:
            cond_type = c.get('condition', 'unknown')

            if cond_type == 'state':
                entity = c.get('entity_id', 'unknown')
                state = c.get('state', 'unknown')
                desc += f"- `{entity}` must be `{state}`\n"

            elif cond_type == 'sun':
                after = c.get('after')
                before = c.get('before')
                if after:
                    desc += f"- Sun must be after `{after}`\n"
                if before:
                    desc += f"- Sun must be before `{before}`\n"

            elif cond_type == 'time':
                after = c.get('after', '')
                before = c.get('before', '')
                desc += f"- Time must be between `{after}` and `{before}`\n"

            else:
                desc += f"- Condition type: `{cond_type}`\n"

        return desc

    def _describe_actions(self, action: Any) -> str:
        """Generate human-readable description of actions"""
        if not action:
            return "**Actions**: None"

        actions = [action] if isinstance(action, dict) else action

        desc = "**Actions**:\n"
        for idx, a in enumerate(actions, 1):
            if 'service' in a:
                service = a['service']
                target = a.get('target', {}).get('entity_id', a.get('entity_id', 'no target'))
                desc += f"{idx}. Call service `{service}` on `{target}`\n"

            elif 'scene' in a:
                scene = a['scene']
                desc += f"{idx}. Activate scene `{scene}`\n"

            elif 'delay' in a:
                delay = a['delay']
                desc += f"{idx}. Wait for `{delay}`\n"

            elif 'wait_for_trigger' in a:
                desc += f"{idx}. Wait for trigger condition\n"

            else:
                desc += f"{idx}. Action: {list(a.keys())[0] if a else 'unknown'}\n"

        return desc

    def _get_entity_info(self, entity_id: str) -> str:
        """Get friendly description of entity"""
        if not self.context:
            return "Unknown entity"

        entity = self.context.get_entity(entity_id)
        if not entity:
            return "Entity not found"

        name = entity.get('name') or entity.get('original_name', entity_id)
        area_id = entity.get('area_id')
        area_name = self.context.get_area_name(area_id) if area_id else None

        info = f"{name}"
        if area_name:
            info += f" ({area_name})"

        return info

    def _identify_edge_cases(self, automation: Dict) -> List[str]:
        """Identify potential edge cases"""
        edge_cases = []

        # Check for timeout issues
        actions = automation.get('action', [])
        if isinstance(actions, dict):
            actions = [actions]

        has_state_trigger = any(
            t.get('platform') == 'state'
            for t in ([automation.get('trigger', {})] if isinstance(automation.get('trigger', {}), dict) else automation.get('trigger', []))
        )

        has_timeout = any('wait_for_trigger' in str(a) or 'delay' in str(a) for a in actions)

        if has_state_trigger and not has_timeout:
            edge_cases.append("⚠️ No timeout mechanism - state may persist indefinitely")

        # Check for entity availability
        has_availability_check = any('available' in str(a) for a in actions)
        if not has_availability_check:
            edge_cases.append("⚠️ No entity availability check - may fail if entities offline")

        # Check mode
        mode = automation.get('mode', 'single')
        if mode == 'single':
            edge_cases.append("ℹ️ Mode 'single' - will skip if already running")

        return edge_cases

    def _suggest_improvements(self, automation: Dict) -> List[str]:
        """Suggest potential improvements"""
        improvements = []

        # Check for description
        if not automation.get('description'):
            improvements.append("Add description field for better documentation")

        # Check for mode setting
        if 'mode' not in automation:
            improvements.append("Explicitly set 'mode' (single/restart/queued/parallel)")

        # Check for conditions on time-based automations
        trigger = automation.get('trigger', {})
        if isinstance(trigger, dict) and trigger.get('platform') == 'time':
            if 'condition' not in automation:
                improvements.append("Consider adding conditions to limit when time-based automation runs")

        return improvements

    def _find_related_automations(self, automation: Dict) -> List[str]:
        """Find related automations based on shared entities"""
        if not self.context:
            return []

        # Extract entities from current automation
        current_entities = set(self._extract_entities_from_config(automation))

        related = []
        automations = self.context.get_automations()

        for auto in automations:
            if auto.get('id') == automation.get('id'):
                continue  # Skip self

            auto_entities = set(self._extract_entities_from_config(auto))

            # Check for overlap
            if current_entities.intersection(auto_entities):
                alias = auto.get('alias', auto.get('id', 'unknown'))
                related.append(alias)

        return related[:5]  # Limit to 5

    def _generate_entity_map(self) -> AgentResult:
        """Generate entity relationship map"""
        if not self.context:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No context available",
                errors=["SharedContext not initialized"]
            )

        # Build entity usage map
        entity_usage = {}
        automations = self.context.get_automations()

        for auto in automations:
            auto_id = auto.get('alias', auto.get('id', 'unknown'))
            entities = self._extract_entities_from_config(auto)

            for entity in entities:
                if entity not in entity_usage:
                    entity_usage[entity] = []
                entity_usage[entity].append(auto_id)

        # Generate markdown
        doc_path = self.entities_docs_dir / "entity_map.md"
        doc_path.parent.mkdir(parents=True, exist_ok=True)

        content = f"""# Entity Usage Map

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This document shows which automations use which entities.

## Entities by Automation Count

"""

        # Sort by usage count
        sorted_entities = sorted(entity_usage.items(), key=lambda x: len(x[1]), reverse=True)

        for entity, auto_list in sorted_entities:
            entity_info = self._get_entity_info(entity)
            content += f"\n### `{entity}`\n"
            content += f"**Description**: {entity_info}  \n"
            content += f"**Used in {len(auto_list)} automation(s)**:\n\n"
            for auto_name in auto_list:
                content += f"- {auto_name}\n"

        try:
            with open(doc_path, 'w') as f:
                f.write(content)

            return AgentResult(
                success=True,
                agent_name=self.name,
                message=f"Entity map generated: {doc_path}",
                data={'path': str(doc_path), 'entities_mapped': len(entity_usage)}
            )

        except Exception as e:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Failed to generate entity map: {str(e)}",
                errors=[str(e)]
            )

    def _update_changelog(self, automation: Optional[Dict]) -> AgentResult:
        """Update changelog with automation changes"""
        self.changelog_path.parent.mkdir(parents=True, exist_ok=True)

        if automation:
            self._add_changelog_entry(automation, 'modified')

        return AgentResult(
            success=True,
            agent_name=self.name,
            message=f"Changelog updated: {self.changelog_path}"
        )

    def _add_changelog_entry(self, automation: Dict, action: str):
        """Add entry to changelog"""
        alias = automation.get('alias', automation.get('id', 'unknown'))
        date = datetime.now().strftime('%Y-%m-%d')

        entry = f"- **{date}**: {action.capitalize()} automation `{alias}`\n"

        # Read existing changelog
        if self.changelog_path.exists():
            with open(self.changelog_path, 'r') as f:
                content = f.read()
        else:
            content = "# Automation Changelog\n\n"

        # Add new entry at top (after header)
        lines = content.split('\n')
        header_end = 2  # After title and empty line
        lines.insert(header_end, entry)

        # Write back
        with open(self.changelog_path, 'w') as f:
            f.write('\n'.join(lines))

    def _generate_index(self) -> AgentResult:
        """Generate searchable index of all automations"""
        index_path = self.automations_docs_dir / "INDEX.md"

        content = f"""# Automation Index

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## By Category

"""

        # Scan documentation directories
        categories = {}
        for category_dir in self.automations_docs_dir.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                categories[category] = []

                for doc_file in category_dir.glob("*.md"):
                    if doc_file.name != "INDEX.md":
                        categories[category].append(doc_file.stem)

        for category, docs in sorted(categories.items()):
            content += f"\n### {category.capitalize()}\n\n"
            for doc in sorted(docs):
                content += f"- [{doc.replace('_', ' ').title()}]({category}/{doc}.md)\n"

        try:
            with open(index_path, 'w') as f:
                f.write(content)

            return AgentResult(
                success=True,
                agent_name=self.name,
                message=f"Index generated: {index_path}",
                data={'categories': len(categories)}
            )

        except Exception as e:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Failed to generate index: {str(e)}",
                errors=[str(e)]
            )

    def _generate_all_documentation(self) -> AgentResult:
        """Generate all documentation types"""
        results = []

        # Generate docs for all automations
        automations = self.context.get_automations() if self.context else []

        for auto in automations:
            result = self._document_automation(auto, update_existing=True)
            results.append(result.success)

        # Generate entity map
        entity_map_result = self._generate_entity_map()
        results.append(entity_map_result.success)

        # Generate index
        index_result = self._generate_index()
        results.append(index_result.success)

        success = all(results)

        return AgentResult(
            success=success,
            agent_name=self.name,
            message=f"Generated documentation for {len(automations)} automations",
            data={
                'automations_documented': len(automations),
                'entity_map_generated': entity_map_result.success,
                'index_generated': index_result.success
            }
        )
