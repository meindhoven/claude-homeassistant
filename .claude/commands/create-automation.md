---
description: Create a new Home Assistant automation with guided workflow
---

You are running the **Create Automation** workflow using the Home Assistant Agent System.

Your task is to help the user create a complete, tested, and documented automation.

## Workflow Steps

Execute the complete automation creation workflow by:

1. **Understanding the Intent**: Ask the user to describe what they want the automation to do
2. **Entity Discovery**: Help find the relevant entities needed (use `/find-entities`)
3. **Live State Verification** (🔴 **USE MCP**): Verify entities are online and responding
   - Check if entities are currently available (not 'unavailable')
   - Verify battery levels for battery-powered sensors
   - Confirm entities can be controlled (for action targets)
4. **Design Automation**: Create the YAML configuration
5. **Best Practices Review**: Check for security and performance issues
6. **Validation**: Run all validation checks
7. **Testing**: Simulate scenarios AND test with MCP if possible
8. **Documentation**: Generate documentation
9. **Save**: Write the automation to config/automations.yaml

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
- **USE MCP to verify entities before finalizing automation**
- Present recommendations to the user
- Ask for confirmation before writing to automations.yaml
- Run validation hooks after writing

## Live State Verification with MCP

Before finalizing the automation, **always verify entities with MCP**:

```python
# After entity discovery, verify they're actually available
entities_to_check = ['binary_sensor.home_kitchen_motion', 'light.home_kitchen_ceiling']

print("\n🔍 Verifying entities are online...\n")

for entity_id in entities_to_check:
    state = homeassistant_get_states(entity_id=entity_id)

    if state['state'] == 'unavailable':
        print(f"⚠️  WARNING: {entity_id} is OFFLINE")
        print(f"   This automation may not work until the device is back online")

        # Check battery if available
        if 'battery_level' in state.get('attributes', {}):
            battery = state['attributes']['battery_level']
            print(f"   Battery level: {battery}%")
            if battery < 20:
                print(f"   ⚠️  Low battery - replace soon!")
    else:
        print(f"✅ {entity_id} is online (state: {state['state']})")

        # Show helpful info
        if 'battery_level' in state.get('attributes', {}):
            battery = state['attributes']['battery_level']
            print(f"   Battery: {battery}%")

        if 'last_updated' in state:
            print(f"   Last updated: {state['last_updated']}")
```

## Testing Actions with MCP

Before deploying, you can test if actions will work:

```python
# Test if we can actually control the light
test_entity = 'light.home_kitchen_ceiling'

print(f"\n🧪 Testing if {test_entity} can be controlled...\n")

# Get available services
services = homeassistant_get_services()
light_services = services.get('light', {})

if 'turn_on' in light_services:
    print(f"✅ Service 'light.turn_on' is available")

    # Optionally, test calling it (ASK USER FIRST!)
    user_consent = input("Test turn on the light now? (y/n): ")
    if user_consent.lower() == 'y':
        result = homeassistant_call_service(
            domain='light',
            service='turn_on',
            target={'entity_id': test_entity},
            service_data={'brightness_pct': 50}
        )
        print(f"✅ Successfully turned on {test_entity} to 50%")
        print(f"   You can verify it's working, then turn it off manually")
else:
    print(f"❌ Service 'light.turn_on' is NOT available")
```

## User Interaction

Be interactive! Ask clarifying questions:
- Which specific entities should be used?
- What conditions should limit when it runs?
- Should there be a timeout or auto-off?
- What name/alias should it have?
- **Would you like me to verify entities are online before creating?** (use MCP)
