"""
Orchestrator Agent

Master agent that coordinates all specialized sub-agents.
Manages workflows, routes requests, and consolidates results.
"""

from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

from agents.base_agent import BaseAgent, AgentResult, AgentStatus, AgentPriority
from agents.shared_context import SharedContext

# Import specialized agents
from agents.creation.entity_discovery import EntityDiscoveryAgent
from agents.creation.automation_designer import AutomationDesignerAgent
from agents.validation.validation_agent import ValidationAgent
from agents.validation.testing_agent import TestingAgent
from agents.documentation.documentation_agent import DocumentationAgent
from agents.analysis.best_practices import BestPracticesAgent
from agents.analysis.refactoring import RefactoringAgent


class WorkflowType(Enum):
    """Types of workflows the orchestrator can execute"""
    CREATE_AUTOMATION = "create_automation"
    REVIEW_AUTOMATIONS = "review_automations"
    DEBUG_AUTOMATION = "debug_automation"
    REFACTOR_AUTOMATIONS = "refactor_automations"
    DOCUMENT_AUTOMATIONS = "document_automations"
    FIND_ENTITIES = "find_entities"
    VALIDATE_CONFIG = "validate_config"


class OrchestratorAgent(BaseAgent):
    """
    Master orchestrator that coordinates all specialized agents.

    Capabilities:
    - Route user requests to appropriate agents
    - Manage multi-agent workflows
    - Consolidate results from multiple agents
    - Handle error recovery
    - Track workflow state
    """

    def __init__(self, context: Optional[SharedContext] = None):
        """Initialize the Orchestrator Agent"""
        if context is None:
            context = SharedContext()

        super().__init__(context)

        # Initialize all specialized agents
        self.entity_discovery = EntityDiscoveryAgent(context)
        self.automation_designer = AutomationDesignerAgent(context)
        self.validation = ValidationAgent(context)
        self.testing = TestingAgent(context)
        self.documentation = DocumentationAgent(context)
        self.best_practices = BestPracticesAgent(context)
        self.refactoring = RefactoringAgent(context)

        # Agent registry
        self.agents = {
            'entity_discovery': self.entity_discovery,
            'automation_designer': self.automation_designer,
            'validation': self.validation,
            'testing': self.testing,
            'documentation': self.documentation,
            'best_practices': self.best_practices,
            'refactoring': self.refactoring
        }

        # Workflow definitions
        self.workflows = {
            WorkflowType.CREATE_AUTOMATION: self._workflow_create_automation,
            WorkflowType.REVIEW_AUTOMATIONS: self._workflow_review_automations,
            WorkflowType.DEBUG_AUTOMATION: self._workflow_debug_automation,
            WorkflowType.REFACTOR_AUTOMATIONS: self._workflow_refactor_automations,
            WorkflowType.DOCUMENT_AUTOMATIONS: self._workflow_document_automations,
            WorkflowType.FIND_ENTITIES: self._workflow_find_entities,
            WorkflowType.VALIDATE_CONFIG: self._workflow_validate_config
        }

    @property
    def name(self) -> str:
        return "Orchestrator Agent"

    @property
    def description(self) -> str:
        return "Master agent coordinating all Home Assistant development workflows"

    @property
    def capabilities(self) -> List[str]:
        return [
            "create_automation",
            "review_automations",
            "debug_automation",
            "refactor_automations",
            "document_automations",
            "find_entities",
            "validate_config"
        ]

    def execute(self, **kwargs) -> AgentResult:
        """
        Execute workflow based on provided parameters.

        Supported kwargs:
            workflow (WorkflowType or str): Workflow to execute
            description (str): Natural language description for automation creation
            automation (dict): Automation to review/debug/test
            query (str): Entity search query
            validation_type (str): Type of validation to run
            ...additional workflow-specific parameters
        """
        workflow = kwargs.get('workflow')

        if isinstance(workflow, str):
            try:
                workflow = WorkflowType(workflow)
            except ValueError:
                return AgentResult(
                    success=False,
                    agent_name=self.name,
                    message=f"Unknown workflow: {workflow}",
                    errors=[f"Valid workflows: {[w.value for w in WorkflowType]}"]
                )

        if workflow not in self.workflows:
            return self._route_to_agent(kwargs)

        # Execute workflow
        workflow_func = self.workflows[workflow]
        return workflow_func(**kwargs)

    def _route_to_agent(self, kwargs: Dict) -> AgentResult:
        """Route simple requests to appropriate single agent"""
        # Determine which agent to use
        if 'query' in kwargs or 'entity_id' in kwargs:
            return self.entity_discovery.run(**kwargs)
        elif 'description' in kwargs and 'automation' not in kwargs:
            return self.automation_designer.run(**kwargs)
        elif 'automation' in kwargs and 'validation_type' in kwargs:
            return self.validation.run(**kwargs)
        else:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="Could not determine appropriate workflow or agent",
                errors=["Provide 'workflow' parameter or specific agent parameters"]
            )

    # ========== WORKFLOW IMPLEMENTATIONS ==========

    def _workflow_create_automation(self, **kwargs) -> AgentResult:
        """
        Complete workflow for creating a new automation.

        Steps:
        1. Entity Discovery (find relevant entities)
        2. Automation Design (create YAML)
        3. Best Practices Review
        4. Validation (all layers)
        5. Testing (scenarios)
        6. Documentation (generate docs)
        """
        description = kwargs.get('description')

        if not description:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No automation description provided",
                errors=["Provide 'description' parameter with automation intent"]
            )

        workflow_results = {
            'entity_discovery': None,
            'automation_design': None,
            'best_practices': None,
            'validation': None,
            'testing': None,
            'documentation': None
        }

        all_recommendations = []

        # Step 1: Entity Discovery (optional, designer will do its own if needed)
        self.logger.info("Step 1: Entity Discovery")
        # Skip explicit entity discovery, let designer handle it

        # Step 2: Automation Design
        self.logger.info("Step 2: Automation Design")
        design_result = self.automation_designer.run(description=description)
        workflow_results['automation_design'] = design_result.to_dict()

        if not design_result.success:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="Automation design failed",
                data={'workflow_results': workflow_results},
                errors=design_result.errors
            )

        automation = design_result.data.get('automation')
        all_recommendations.extend(design_result.recommendations)

        # Step 3: Best Practices Review
        self.logger.info("Step 3: Best Practices Review")
        practices_result = self.best_practices.run(automation=automation, review_type='full')
        workflow_results['best_practices'] = practices_result.to_dict()
        all_recommendations.extend(practices_result.recommendations)

        # Step 4: Validation
        self.logger.info("Step 4: Validation")
        validation_result = self.validation.run(automation=automation)
        workflow_results['validation'] = validation_result.to_dict()

        if not validation_result.success:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="Automation validation failed",
                data={'workflow_results': workflow_results, 'automation': automation},
                errors=validation_result.errors
            )

        # Step 5: Testing
        self.logger.info("Step 5: Testing")
        testing_result = self.testing.run(automation=automation, test_type='full')
        workflow_results['testing'] = testing_result.to_dict()
        all_recommendations.extend(testing_result.recommendations)

        # Step 6: Documentation
        self.logger.info("Step 6: Documentation")
        doc_result = self.documentation.run(automation=automation, doc_type='automation')
        workflow_results['documentation'] = doc_result.to_dict()

        # Consolidate results
        result = AgentResult(
            success=True,
            agent_name=self.name,
            message=f"✅ Automation created successfully: {automation.get('alias', 'New Automation')}",
            data={
                'workflow': 'create_automation',
                'automation': automation,
                'workflow_results': workflow_results,
                'summary': {
                    'design_success': design_result.success,
                    'validation_success': validation_result.success,
                    'best_practices_score': practices_result.data.get('score', 0),
                    'tests_passed': testing_result.success,
                    'documented': doc_result.success
                }
            }
        )

        # Add consolidated recommendations (prioritized)
        high_priority = [r for r in all_recommendations if r.get('priority') == 'high']
        medium_priority = [r for r in all_recommendations if r.get('priority') == 'medium']
        low_priority = [r for r in all_recommendations if r.get('priority') == 'low']

        for rec in high_priority[:5] + medium_priority[:5] + low_priority[:3]:
            result.add_recommendation(
                rec['description'],
                AgentPriority[rec['priority'].upper()] if isinstance(rec['priority'], str) else rec['priority'],
                rec.get('action')
            )

        return result

    def _workflow_review_automations(self, **kwargs) -> AgentResult:
        """
        Review all existing automations for issues and improvements.

        Steps:
        1. Load all automations
        2. Best Practices Review (all automations)
        3. Refactoring Analysis
        4. Validation Check
        5. Generate Report
        """
        self.logger.info("Starting automation review workflow")

        automations = self.context.get_automations()

        if not automations:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No automations found to review",
                errors=["Load automations into context first"]
            )

        workflow_results = {}

        # Step 1: Best Practices Review
        self.logger.info("Step 1: Best Practices Review")
        all_practices_issues = []
        practices_scores = []

        for auto in automations[:20]:  # Limit to avoid timeout
            result = self.best_practices.run(automation=auto, review_type='full')
            score = result.data.get('score', 0)
            practices_scores.append({
                'automation': auto.get('alias', auto.get('id')),
                'score': score
            })
            if score < 70:
                all_practices_issues.extend(result.recommendations)

        workflow_results['best_practices'] = {
            'scores': practices_scores,
            'average_score': sum(s['score'] for s in practices_scores) / len(practices_scores) if practices_scores else 0
        }

        # Step 2: Refactoring Analysis
        self.logger.info("Step 2: Refactoring Analysis")
        refactor_result = self.refactoring.run(automations=automations, refactor_type='all')
        workflow_results['refactoring'] = refactor_result.to_dict()

        # Step 3: Validation
        self.logger.info("Step 3: Validation Check")
        validation_result = self.validation.run(validation_type='full')
        workflow_results['validation'] = validation_result.to_dict()

        # Consolidate recommendations
        all_recommendations = []
        all_recommendations.extend(all_practices_issues[:10])
        all_recommendations.extend(refactor_result.recommendations[:10])
        all_recommendations.extend(validation_result.recommendations[:5])

        result = AgentResult(
            success=True,
            agent_name=self.name,
            message=f"📊 Review complete: {len(automations)} automations analyzed",
            data={
                'workflow': 'review_automations',
                'automations_reviewed': len(automations),
                'workflow_results': workflow_results,
                'summary': {
                    'average_quality_score': workflow_results['best_practices']['average_score'],
                    'validation_passed': validation_result.success,
                    'refactoring_opportunities': len(refactor_result.data.get('summary', {}).get('optimizations', 0))
                }
            }
        )

        for rec in all_recommendations[:15]:
            result.add_recommendation(
                rec['description'],
                rec.get('priority', AgentPriority.MEDIUM),
                rec.get('action')
            )

        return result

    def _workflow_debug_automation(self, **kwargs) -> AgentResult:
        """
        Debug a failing automation.

        Steps:
        1. Validate configuration
        2. Check entity availability
        3. Test trigger conditions
        4. Simulate execution
        5. Provide diagnosis
        """
        automation = kwargs.get('automation')

        if not automation:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message="No automation provided for debugging",
                errors=["Provide 'automation' parameter"]
            )

        workflow_results = {}

        # Step 1: Validation
        self.logger.info("Step 1: Configuration Validation")
        validation_result = self.validation.run(automation=automation)
        workflow_results['validation'] = validation_result.to_dict()

        # Step 2: Entity Check
        self.logger.info("Step 2: Entity Availability Check")
        entities = self._extract_entities(automation)
        entity_status = {}

        for entity_id in entities:
            entity_result = self.entity_discovery.run(entity_id=entity_id)
            entity_status[entity_id] = {
                'exists': entity_result.success,
                'details': entity_result.data if entity_result.success else None,
                'error': entity_result.errors[0] if entity_result.errors else None
            }

        workflow_results['entity_status'] = entity_status

        # Step 3: Trigger Testing
        self.logger.info("Step 3: Trigger Testing")
        testing_result = self.testing.run(automation=automation, test_type='triggers')
        workflow_results['trigger_test'] = testing_result.to_dict()

        # Step 4: Full Testing
        self.logger.info("Step 4: Scenario Testing")
        full_test_result = self.testing.run(automation=automation, test_type='full')
        workflow_results['full_test'] = full_test_result.to_dict()

        # Generate diagnosis
        issues_found = []
        issues_found.extend(validation_result.errors)
        issues_found.extend([f"Entity issue: {k} - {v['error']}" for k, v in entity_status.items() if not v['exists']])
        issues_found.extend(testing_result.errors)

        success = len(issues_found) == 0

        diagnosis = "✅ No issues found" if success else f"❌ {len(issues_found)} issues identified"

        result = AgentResult(
            success=success,
            agent_name=self.name,
            message=f"🔍 Debugging complete: {diagnosis}",
            data={
                'workflow': 'debug_automation',
                'automation': automation.get('alias', 'Unknown'),
                'workflow_results': workflow_results,
                'diagnosis': {
                    'configuration_valid': validation_result.success,
                    'entities_available': all(v['exists'] for v in entity_status.values()),
                    'triggers_valid': testing_result.success,
                    'issues_found': issues_found
                }
            },
            errors=issues_found
        )

        # Add recommendations from all steps
        for rec in validation_result.recommendations + testing_result.recommendations + full_test_result.recommendations:
            result.add_recommendation(
                rec['description'],
                rec.get('priority', AgentPriority.MEDIUM),
                rec.get('action')
            )

        return result

    def _workflow_refactor_automations(self, **kwargs) -> AgentResult:
        """Execute refactoring workflow"""
        automations = kwargs.get('automations') or self.context.get_automations()

        self.logger.info("Starting refactoring workflow")
        refactor_result = self.refactoring.run(automations=automations, refactor_type='all')

        return refactor_result

    def _workflow_document_automations(self, **kwargs) -> AgentResult:
        """Execute documentation generation workflow"""
        self.logger.info("Starting documentation workflow")

        doc_result = self.documentation.run(doc_type='all')

        return doc_result

    def _workflow_find_entities(self, **kwargs) -> AgentResult:
        """Execute entity discovery workflow"""
        query = kwargs.get('query')
        domain = kwargs.get('domain')
        area = kwargs.get('area')
        context = kwargs.get('context')

        self.logger.info(f"Finding entities: query={query}, domain={domain}, area={area}")

        return self.entity_discovery.run(
            query=query,
            domain=domain,
            area=area,
            context=context
        )

    def _workflow_validate_config(self, **kwargs) -> AgentResult:
        """Execute configuration validation workflow"""
        validation_type = kwargs.get('validation_type', 'full')
        file_path = kwargs.get('file_path')

        self.logger.info(f"Validating configuration: type={validation_type}")

        return self.validation.run(
            validation_type=validation_type,
            file_path=file_path
        )

    # ========== UTILITY METHODS ==========

    def _extract_entities(self, automation: Dict) -> List[str]:
        """Extract all entity IDs from automation"""
        entities = []

        def extract_from_value(value):
            if isinstance(value, str) and '.' in value and value.count('.') == 1:
                # Looks like entity ID
                parts = value.split('.')
                if parts[0] and parts[1]:
                    entities.append(value)
            elif isinstance(value, dict):
                for v in value.values():
                    extract_from_value(v)
            elif isinstance(value, list):
                for item in value:
                    extract_from_value(item)

        extract_from_value(automation)
        return list(set(entities))

    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Get specific agent by name"""
        return self.agents.get(agent_name)

    def list_agents(self) -> List[Dict[str, str]]:
        """List all available agents"""
        return [
            {
                'name': agent.name,
                'description': agent.description,
                'capabilities': agent.capabilities
            }
            for agent in self.agents.values()
        ]

    def get_workflow_types(self) -> List[str]:
        """Get list of available workflows"""
        return [w.value for w in WorkflowType]
