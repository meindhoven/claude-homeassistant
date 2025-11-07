---
description: Create a new Home Assistant automation with guided workflow
---

You are running the **Create Automation** workflow using the Home Assistant Agent System.

Your task is to help the user create a complete, tested, and documented automation.

## Workflow Steps

Execute the complete automation creation workflow by:

1. **Understanding the Intent**: Ask the user to describe what they want the automation to do
2. **Entity Discovery**: Help find the relevant entities needed
3. **Design Automation**: Create the YAML configuration
4. **Best Practices Review**: Check for security and performance issues
5. **Validation**: Run all validation checks
6. **Testing**: Simulate scenarios
7. **Documentation**: Generate documentation
8. **Save**: Write the automation to config/automations.yaml

## Implementation

Use the Orchestrator Agent with the CREATE_AUTOMATION workflow:

```python
from agents.orchestrator import OrchestratorAgent
from agents.shared_context import SharedContext

# Initialize
context = SharedContext()
orchestrator = OrchestratorAgent(context)

# Get user description
description = "<user's automation description>"

# Run workflow
result = orchestrator.run(
    workflow='create_automation',
    description=description
)

# Present results
print(result.message)
print("\nAutomation created:")
print(yaml.dump(result.data['automation']))

if result.recommendations:
    print("\n💡 Recommendations:")
    for rec in result.recommendations:
        print(f"  [{rec['priority']}] {rec['description']}")
```

## Key Points

- Use the orchestrator to coordinate all agents
- Present recommendations to the user
- Ask for confirmation before writing to automations.yaml
- Run validation hooks after writing

## User Interaction

Be interactive! Ask clarifying questions:
- Which specific entities should be used?
- What conditions should limit when it runs?
- Should there be a timeout or auto-off?
- What name/alias should it have?
