"""
Basic smoke tests for the Agent System

Tests that agents can be imported and instantiated successfully.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all agent modules can be imported"""
    print("Testing agent imports...")

    try:
        from agents import (
            BaseAgent,
            AgentResult,
            AgentStatus,
            AgentPriority,
            SharedContext
        )
        print("✓ Core agent classes imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import core classes: {e}")
        return False

    try:
        from agents.creation.entity_discovery import EntityDiscoveryAgent
        print("✓ Entity Discovery Agent imported")
    except ImportError as e:
        print(f"✗ Failed to import Entity Discovery Agent: {e}")
        return False

    try:
        from agents.creation.automation_designer import AutomationDesignerAgent
        print("✓ Automation Designer Agent imported")
    except ImportError as e:
        print(f"✗ Failed to import Automation Designer Agent: {e}")
        return False

    try:
        from agents.validation.validation_agent import ValidationAgent
        print("✓ Validation Agent imported")
    except ImportError as e:
        print(f"✗ Failed to import Validation Agent: {e}")
        return False

    try:
        from agents.validation.testing_agent import TestingAgent
        print("✓ Testing Agent imported")
    except ImportError as e:
        print(f"✗ Failed to import Testing Agent: {e}")
        return False

    try:
        from agents.documentation.documentation_agent import DocumentationAgent
        print("✓ Documentation Agent imported")
    except ImportError as e:
        print(f"✗ Failed to import Documentation Agent: {e}")
        return False

    try:
        from agents.analysis.best_practices import BestPracticesAgent
        print("✓ Best Practices Agent imported")
    except ImportError as e:
        print(f"✗ Failed to import Best Practices Agent: {e}")
        return False

    try:
        from agents.analysis.refactoring import RefactoringAgent
        print("✓ Refactoring Agent imported")
    except ImportError as e:
        print(f"✗ Failed to import Refactoring Agent: {e}")
        return False

    try:
        from agents.orchestrator import OrchestratorAgent
        print("✓ Orchestrator Agent imported")
    except ImportError as e:
        print(f"✗ Failed to import Orchestrator Agent: {e}")
        return False

    try:
        from agents.creation.dashboard_designer import DashboardDesignerAgent
        print("✓ Dashboard Designer Agent imported")
    except ImportError as e:
        print(f"✗ Failed to import Dashboard Designer Agent: {e}")
        return False

    try:
        from agents.analysis.dashboard_best_practices import DashboardBestPracticesAgent
        print("✓ Dashboard Best Practices Agent imported")
    except ImportError as e:
        print(f"✗ Failed to import Dashboard Best Practices Agent: {e}")
        return False

    return True


def test_instantiation():
    """Test that agents can be instantiated"""
    print("\nTesting agent instantiation...")

    try:
        from agents.shared_context import SharedContext
        from agents.orchestrator import OrchestratorAgent

        # Create context
        context = SharedContext()
        print(f"✓ SharedContext created: {context}")

        # Create orchestrator
        orchestrator = OrchestratorAgent(context)
        print(f"✓ Orchestrator created: {orchestrator.name}")

        # List agents
        agents = orchestrator.list_agents()
        print(f"✓ Found {len(agents)} agents:")
        for agent_info in agents:
            print(f"  - {agent_info['name']}")

        # Get workflows
        workflows = orchestrator.get_workflow_types()
        print(f"✓ Available workflows: {', '.join(workflows)}")

        return True

    except Exception as e:
        print(f"✗ Instantiation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_properties():
    """Test agent properties and methods"""
    print("\nTesting agent properties...")

    try:
        from agents.shared_context import SharedContext
        from agents.creation.entity_discovery import EntityDiscoveryAgent

        context = SharedContext()
        agent = EntityDiscoveryAgent(context)

        print(f"✓ Agent name: {agent.name}")
        print(f"✓ Agent description: {agent.description}")
        print(f"✓ Agent capabilities: {', '.join(agent.capabilities)}")
        print(f"✓ Agent status: {agent.get_status()}")

        return True

    except Exception as e:
        print(f"✗ Property test failed: {e}")
        return False


def test_dashboard_agents():
    """Test dashboard agent functionality"""
    print("\nTesting dashboard agents...")

    try:
        from agents.shared_context import SharedContext
        from agents.creation.dashboard_designer import DashboardDesignerAgent
        from agents.analysis.dashboard_best_practices import DashboardBestPracticesAgent

        context = SharedContext()

        # Test Dashboard Designer
        designer = DashboardDesignerAgent(context)
        print(f"✓ Dashboard Designer: {designer.name}")
        print(f"  Capabilities: {', '.join(designer.capabilities)}")

        # Test Dashboard Best Practices
        reviewer = DashboardBestPracticesAgent(context)
        print(f"✓ Dashboard Best Practices: {reviewer.name}")
        print(f"  Capabilities: {', '.join(reviewer.capabilities)}")

        # Test basic dashboard design
        print("\n  Testing basic dashboard design...")
        result = designer.run(
            design_type='suggest_cards',
            entities=['light.test_light', 'sensor.test_temperature']
        )
        if result.success:
            print(f"  ✓ Card suggestions generated for {result.data.get('entity_count', 0)} entities")
        else:
            print(f"  ✗ Card suggestion failed: {result.message}")
            return False

        return True

    except Exception as e:
        print(f"✗ Dashboard agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all smoke tests"""
    print("=" * 60)
    print("Home Assistant Agent System - Smoke Tests")
    print("=" * 60)
    print()

    results = []

    # Test imports
    results.append(("Imports", test_imports()))

    # Test instantiation
    results.append(("Instantiation", test_instantiation()))

    # Test properties
    results.append(("Properties", test_agent_properties()))

    # Test dashboard agents
    results.append(("Dashboard Agents", test_dashboard_agents()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("🎉 All smoke tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
