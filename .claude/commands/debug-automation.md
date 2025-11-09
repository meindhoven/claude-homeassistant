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

2. **Entity Availability** (🔴 **USE MCP HERE**)
   - Do all referenced entities exist? (check registry)
   - Are any entities disabled? (check registry)
   - **Are entities currently available?** (use MCP `homeassistant_get_states`)
   - **What's the current battery status?** (use MCP to get live attributes)
   - **When did entity last update?** (use MCP to get last_updated)
   - **Are sensors actually responding?** (check if state != 'unavailable')

3. **Trigger Testing** (🔴 **USE MCP HERE**)
   - Will triggers actually fire?
   - **Are trigger entities responsive?** (use MCP to verify live state)
   - **What's the current trigger state?** (check if automation would trigger now)
   - Is trigger logic sound?

4. **Condition Testing** (🔴 **USE MCP HERE**)
   - Are conditions reachable?
   - Do condition entities exist?
   - **Would conditions pass right now?** (use MCP to test current state)

5. **Action Testing** (🔴 **USE MCP HERE**)
   - Are target entities controllable?
   - **Are target entities currently available?** (use MCP)
   - Are services available? (use MCP `homeassistant_get_services`)
   - **Can we actually control them?** (check if entity supports the service)

## Using MCP for Live Diagnostics

**CRITICAL**: Always use MCP tools when debugging to check **current, live state**:

```python
# Check if trigger entity is responsive
trigger_entity = "binary_sensor.home_kitchen_motion"
state = homeassistant_get_states(entity_id=trigger_entity)

if state['state'] == 'unavailable':
    print(f"❌ PROBLEM: Trigger entity {trigger_entity} is OFFLINE")
    print(f"   The automation cannot trigger because the sensor isn't responding")
    print(f"   Action: Check sensor battery, connection, or device")
else:
    print(f"✅ Trigger entity is online")
    print(f"   Current state: {state['state']}")
    print(f"   Last updated: {state['last_updated']}")

# Check battery level if available
if 'battery_level' in state.get('attributes', {}):
    battery = state['attributes']['battery_level']
    if battery < 20:
        print(f"⚠️  WARNING: Low battery ({battery}%) - entity may become unavailable soon")
```

```python
# Test if action entity can be controlled
action_entity = "light.home_kitchen_ceiling"
state = homeassistant_get_states(entity_id=action_entity)

if state['state'] == 'unavailable':
    print(f"❌ PROBLEM: Action target {action_entity} is OFFLINE")
    print(f"   The automation will fail to execute")
else:
    print(f"✅ Action target is available")

    # Verify the service is available
    services = homeassistant_get_services()
    light_services = services.get('light', {})

    if 'turn_on' in light_services:
        print(f"✅ Service 'light.turn_on' is available")
    else:
        print(f"❌ Service 'light.turn_on' is NOT available")
```

```python
# Test if automation would trigger RIGHT NOW
current_state = homeassistant_get_states(entity_id=trigger_entity)
trigger_to_state = 'on'  # from automation config

if current_state['state'] == trigger_to_state:
    print(f"🔔 Automation WOULD TRIGGER right now")
    print(f"   {trigger_entity} is currently '{current_state['state']}'")
else:
    print(f"⏸️  Automation would NOT trigger right now")
    print(f"   Current state: '{current_state['state']}' (needs '{trigger_to_state}')")
```

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
