---
description: Search for entities by name, domain, area, or device class
---

You are running the **Find Entities** workflow using the Home Assistant Agent System.

Your task is to help the user discover and understand available entities.

## Usage

The user can search for entities in various ways:

```
/find-entities motion sensors in the kitchen
/find-entities climate controls at the office
/find-entities battery sensors
/find-entities all lights in bedroom
```

## Implementation

```python
from agents.orchestrator import OrchestratorAgent
from agents.shared_context import SharedContext

# Initialize
context = SharedContext()
orchestrator = OrchestratorAgent(context)

# Parse user query
query = "<user's search terms>"

# Extract filters from query
domain = None  # e.g., 'light', 'sensor', 'binary_sensor'
area = None    # e.g., 'kitchen', 'bedroom'
device_class = None  # e.g., 'motion', 'temperature'

# Run entity discovery
result = orchestrator.run(
    workflow='find_entities',
    query=query,
    domain=domain,
    area=area
)

# Present results
print(f"🔍 Found {result.data['count']} entities\n")

for entity in result.data['entities'][:20]:  # Show top 20
    area_str = f" ({entity['area']})" if entity.get('area') else ""
    status = "❌ disabled" if entity.get('disabled') else "✅"
    print(f"  {status} {entity['entity_id']}{area_str}")
    print(f"     {entity['name']}")
    if entity.get('device_class'):
        print(f"     Device class: {entity['device_class']}")
    print()
```

## Search Patterns

Help users with natural language queries:

- "motion sensors" → domain=binary_sensor, device_class=motion
- "kitchen lights" → domain=light, area=kitchen
- "office climate" → domain=climate, area=office
- "all battery sensors" → device_class=battery
- "temperature sensors" → domain=sensor, device_class=temperature

## Context-Aware Suggestions

When the user is creating an automation, suggest relevant entities:

```python
# For triggers
result = orchestrator.run(
    workflow='find_entities',
    context='trigger',
    query=query
)

# For conditions
result = orchestrator.run(
    workflow='find_entities',
    context='condition',
    query=query
)

# For actions
result = orchestrator.run(
    workflow='find_entities',
    context='action',
    query=query
)
```

## Detailed Entity Info

For specific entity lookups:

```python
result = orchestrator.run(
    workflow='find_entities',
    entity_id='binary_sensor.home_kitchen_motion'
)

entity = result.data['entity']
print(f"Entity: {entity['entity_id']}")
print(f"Name: {entity['name']}")
print(f"Area: {entity['area']}")
print(f"Device class: {entity['device_class']}")
print(f"Platform: {entity['platform']}")
print(f"Disabled: {entity['disabled']}")

print(f"\n📝 Used in automations:")
for auto in result.data['used_in_automations']:
    print(f"  - {auto}")

print(f"\n⚡ Capabilities:")
caps = result.data['capabilities']
if caps['can_trigger']:
    print("  ✅ Can be used as trigger")
if caps['can_condition']:
    print("  ✅ Can be used in conditions")
if caps['can_action']:
    print("  ✅ Can be controlled in actions")
```

## User Assistance

- Explain entity naming convention (location_room_device_sensor)
- Suggest similar entities if query doesn't match
- Show device classes for better understanding
- Indicate disabled entities
- Show which automations already use an entity
