---
description: Debug a failing or misbehaving automation
---

You are running the **Debug Automation** workflow using the Home Assistant Agent System.

Your task is to diagnose why an automation isn't working and provide specific solutions.

## Usage

The user reports an automation that's not working. Your job is to systematically diagnose the problem.

## Implementation

```python
from agents.orchestrator import OrchestratorAgent
from agents.shared_context import SharedContext
import yaml

# Initialize
context = SharedContext()
orchestrator = OrchestratorAgent(context)

# Get the problematic automation
# Either by name/alias or from automations.yaml
automation_name = "<user's automation name>"
automations = context.get_automations()
automation = next((a for a in automations if a.get('alias') == automation_name), None)

if not automation:
    print(f"❌ Automation '{automation_name}' not found")
    # List available automations
    print("\nAvailable automations:")
    for auto in automations:
        print(f"  - {auto.get('alias', auto.get('id'))}")
else:
    # Run debug workflow
    result = orchestrator.run(
        workflow='debug_automation',
        automation=automation
    )

    # Present diagnosis
    print(f"🔍 Debug Results for: {automation.get('alias')}\n")

    diagnosis = result.data['diagnosis']

    print("Configuration:")
    status = "✅" if diagnosis['configuration_valid'] else "❌"
    print(f"  {status} YAML syntax and structure")

    print("\nEntities:")
    status = "✅" if diagnosis['entities_available'] else "❌"
    print(f"  {status} All entities exist and available")

    print("\nTriggers:")
    status = "✅" if diagnosis['triggers_valid'] else "❌"
    print(f"  {status} Trigger configuration valid")

    if diagnosis['issues_found']:
        print(f"\n🚨 Issues Found ({len(diagnosis['issues_found'])}):\n")
        for idx, issue in enumerate(diagnosis['issues_found'], 1):
            print(f"  {idx}. {issue}")

    if result.recommendations:
        print(f"\n💡 Recommendations:\n")
        for idx, rec in enumerate(result.recommendations, 1):
            priority = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(rec['priority'], '⚪')
            print(f"  {idx}. {priority} {rec['description']}")
            if rec.get('action'):
                print(f"      Action: {rec['action']}")
```

## Diagnostic Steps

The workflow performs these checks:

1. **Configuration Validation**
   - YAML syntax correct?
   - Required fields present?
   - Service names valid?

2. **Entity Availability**
   - Do all referenced entities exist?
   - Are any entities disabled?
   - What's the battery status?
   - When did entity last update?

3. **Trigger Testing**
   - Will triggers actually fire?
   - Are trigger entities responsive?
   - Is trigger logic sound?

4. **Condition Testing**
   - Are conditions reachable?
   - Do condition entities exist?

5. **Action Testing**
   - Are target entities controllable?
   - Are services available?

## Common Issues & Solutions

Present common issues found:

### Entity Not Found
```
Problem: Entity 'light.kitchen' not found
Solution: Entity registry shows:
  - light.home_kitchen_ceiling
  - light.home_kitchen_under_cabinet
Did you mean 'light.home_kitchen_ceiling'?
```

### Entity Disabled
```
Problem: binary_sensor.home_kitchen_motion is disabled
Solution:
  1. Check battery level (currently 5% - critically low)
  2. Replace battery
  3. Re-enable entity in Home Assistant
  4. Test automation again
```

### Trigger Never Fires
```
Problem: State trigger without target state
Solution: Add specific 'to' state:
  from: 'off'
  to: 'on'
Instead of triggering on any state change
```

### Service Not Available
```
Problem: Service 'light.toggle' not found
Solution: Use 'light.turn_on' or 'light.turn_off' instead
```

## Interactive Debugging

After presenting diagnosis, offer to:

1. **Fix Issues**: "Would you like me to fix these issues?"
2. **Test Changes**: "Should I test the automation with simulated scenarios?"
3. **Improve Logic**: "I can suggest improvements to make it more reliable"
4. **Monitor**: "I can help you monitor when it actually runs"

## Entity Details

When entity issues are found, provide detailed information:

```python
entity_info = orchestrator.run(workflow='find_entities', entity_id=problem_entity)

print(f"\n📋 Entity Details: {problem_entity}")
entity = entity_info.data['entity']
print(f"  Name: {entity['name']}")
print(f"  Area: {entity.get('area', 'None')}")
print(f"  Platform: {entity.get('platform', 'Unknown')}")
print(f"  Status: {'Disabled' if entity['disabled'] else 'Enabled'}")
print(f"  Device class: {entity.get('device_class', 'None')}")

# Show alternative entities
if entity['disabled']:
    print(f"\n  Alternative entities in same area:")
    similar = context.search_entities(problem_entity.split('.')[1])
    for s in similar[:3]:
        print(f"    - {s['entity_id']}")
```

## Follow-up Actions

After diagnosis, help the user:

- Fix configuration errors
- Replace disabled entities
- Add missing conditions
- Optimize trigger logic
- Test with scenarios
- Document the fix
