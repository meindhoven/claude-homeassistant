# Dashboard Design Examples

Examples of using the Dashboard Designer Agent to create user-friendly Home Assistant dashboards.

## Example 1: Overview Dashboard

### User Request
"Create an overview dashboard for my home with the most important controls"

### Workflow

```python
from agents.orchestrator import OrchestratorAgent
from agents.shared_context import SharedContext
import yaml

# Initialize
context = SharedContext()
orchestrator = OrchestratorAgent(context)

# Design dashboard
result = orchestrator.run(
    workflow='design_dashboard',
    description='Overview dashboard with lights, climate, security, and weather',
    layout_type='overview'
)

# Check results
if result.success:
    dashboard = result.data['dashboard']
    quality_score = result.data['quality_score']

    print(f"✅ Dashboard created with {result.data['view_count']} views")
    print(f"📊 Quality score: {quality_score}/100")

    # Save to file
    with open('config/lovelace/overview_dashboard.yaml', 'w') as f:
        yaml.dump(dashboard, f, sort_keys=False, allow_unicode=True)

    # Show recommendations
    print("\n💡 Recommendations:")
    for rec in result.recommendations[:5]:
        print(f"  [{rec['priority']}] {rec['description']}")
```

### Output

```
✅ Dashboard created with 5 views
📊 Quality score: 87/100

💡 Recommendations:
  [medium] Add custom theme for visual consistency
  [medium] Test dashboard on mobile devices
  [low] Add badges for quick status at top of overview
  [low] Consider adding welcome/header card to overview
  [medium] Use icons with text labels for status indication
```

### Generated Dashboard Structure

```yaml
title: Home Dashboard
views:
  - title: Overview
    path: overview
    icon: mdi:home
    cards:
      - type: markdown
        content: '# 🏠 Home Overview

          Welcome home!'
      - type: entities
        title: Lights
        entities:
          - light.home_living_room_ceiling
          - light.home_kitchen_ceiling
          - light.home_bedroom_ceiling
      - type: thermostat
        entity: climate.home_living_room_heatpump
      - type: alarm-panel
        entity: alarm_control_panel.home_alarm
      - type: weather-forecast
        entity: weather.home

  - title: Living Room
    path: living_room
    icon: mdi:sofa
    cards:
      - type: entities
        title: Lights
        entities:
          - light.home_living_room_ceiling
          - light.home_living_room_lamp
      - type: thermostat
        entity: climate.home_living_room_heatpump
      - type: media-control
        entity: media_player.home_living_room_sonos
      - type: entities
        title: Sensors
        entities:
          - sensor.home_living_room_temperature
          - sensor.home_living_room_humidity
```

---

## Example 2: Security Dashboard

### User Request
"I want a security dashboard with cameras, alarm, and door sensors"

### Workflow

```python
result = orchestrator.run(
    workflow='design_dashboard',
    description='Security dashboard with cameras, alarm, door sensors, and locks',
    layout_type='security'
)

if result.success:
    dashboard = result.data['dashboard']

    # Show view breakdown
    for view in dashboard['views']:
        card_count = len(view.get('cards', []))
        print(f"{view.get('icon', '📄')} {view['title']}: {card_count} cards")
```

### Output

```
🔒 Security: 7 cards
```

### Generated Security View

```yaml
title: Security
path: security
icon: mdi:shield-home
cards:
  - type: alarm-panel
    entity: alarm_control_panel.home_alarm

  - type: picture-entity
    entity: camera.home_front_door
    camera_view: live

  - type: picture-entity
    entity: camera.home_driveway
    camera_view: live

  - type: entities
    title: Sensors
    entities:
      - binary_sensor.home_front_door
      - binary_sensor.home_back_door
      - binary_sensor.home_garage_door
      - binary_sensor.home_basement_motion

  - type: entities
    title: Locks
    entities:
      - lock.home_front_door_august
```

---

## Example 3: Room-Specific Dashboard

### User Request
"Design a dashboard just for the kitchen"

### Workflow

```python
# Option 1: Let agent discover entities
result = orchestrator.run(
    workflow='design_dashboard',
    description='Kitchen dashboard with lights, climate, and appliances',
    layout_type='room'
)

# Option 2: Specify exact entities
kitchen_entities = [
    'light.home_kitchen_ceiling',
    'light.home_kitchen_under_cabinet',
    'climate.home_kitchen_thermostat',
    'sensor.home_kitchen_temperature',
    'sensor.home_kitchen_humidity',
    'binary_sensor.home_kitchen_motion'
]

result = orchestrator.run(
    workflow='design_dashboard',
    description='Kitchen dashboard',
    entities=kitchen_entities,
    layout_type='room'
)
```

### Generated Kitchen View

```yaml
title: Kitchen
path: kitchen
icon: mdi:silverware-fork-knife
cards:
  - type: entities
    title: Lights
    entities:
      - light.home_kitchen_ceiling
      - light.home_kitchen_under_cabinet

  - type: thermostat
    entity: climate.home_kitchen_thermostat

  - type: entities
    title: Sensors
    entities:
      - sensor.home_kitchen_temperature
      - sensor.home_kitchen_humidity
      - binary_sensor.home_kitchen_motion
```

---

## Example 4: Reviewing Existing Dashboard

### User Request
"Can you review my existing dashboard and suggest improvements?"

### Workflow

```python
# Load existing dashboard
with open('config/lovelace/my_dashboard.yaml', 'r') as f:
    existing_dashboard = yaml.safe_load(f)

# Review for improvements
result = orchestrator.run(
    workflow='review_dashboard',
    dashboard=existing_dashboard,
    review_type='full'  # Options: full, ux, accessibility, design, performance
)

# Show results
print(f"📊 Quality Score: {result.data['quality_score']}/100")
print(f"🔍 Issues: {len(result.errors)}")
print(f"⚠️  Warnings: {len(result.warnings)}")

print("\n🔴 Critical Issues:")
for error in result.errors:
    print(f"  - {error}")

print("\n💡 Recommendations:")
for rec in result.recommendations[:10]:
    priority_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}
    icon = priority_icon.get(rec['priority'], '⚪')
    print(f"  {icon} {rec['description']}")
```

### Example Output

```
📊 Quality Score: 72/100
🔍 Issues: 2
⚠️  Warnings: 5

🔴 Critical Issues:
  - Overview: Too many cards (18)
  - Living Room: Too many cards (16)

💡 Recommendations:
  🟠 Split 'Overview' into multiple views - currently has 18 cards
  🟠 Split 'Living Room' into multiple views - currently has 16 cards
  🟡 Add titles to 3 cards in 'Overview' for better context
  🟡 Add icons to views: Kitchen, Bedroom, Office
  🟡 Consider standardizing card types in 'Overview'
  🟡 Limit camera cards in 'Security' to 4 or less
  🟢 Add header/welcome card to 'Overview' for better visual hierarchy
  🟢 Consider using a custom theme for visual consistency
  🟢 Use consistent spacing and padding between cards
  🟡 Consider using conditional cards to show/hide based on state
```

---

## Example 5: Media Dashboard

### User Request
"Create a dashboard for controlling all my media players"

### Workflow

```python
result = orchestrator.run(
    workflow='design_dashboard',
    description='Media control dashboard with all speakers and TVs',
    layout_type='media'
)
```

### Generated Media View

```yaml
title: Media
path: media
icon: mdi:music
cards:
  - type: media-control
    entity: media_player.home_living_room_sonos

  - type: media-control
    entity: media_player.home_kitchen_sonos

  - type: media-control
    entity: media_player.home_bedroom_sonos

  - type: media-control
    entity: media_player.home_office_sonos
```

---

## Example 6: Climate Dashboard

### User Request
"I want to see all my thermostats and temperature sensors in one place"

### Workflow

```python
result = orchestrator.run(
    workflow='design_dashboard',
    description='Climate dashboard with thermostats and temperature sensors',
    layout_type='climate'
)
```

### Generated Climate View

```yaml
title: Climate
path: climate
icon: mdi:thermostat
cards:
  - type: thermostat
    entity: climate.home_living_room_heatpump

  - type: thermostat
    entity: climate.home_bedroom_heatpump

  - type: entities
    title: Temperature Sensors
    entities:
      - sensor.home_living_room_temperature
      - sensor.home_bedroom_temperature
      - sensor.home_kitchen_temperature
      - sensor.home_office_temperature
```

---

## Best Practices Demonstrated

### 1. Progressive Disclosure
- Overview shows most important items
- Detailed views for specific areas
- Quick actions at top level

### 2. Consistent Card Selection
- Single thermostats use `thermostat` card
- Multiple entities use `entities` card
- Media players use `media-control` card

### 3. Logical Organization
- Related items grouped together
- Appropriate view icons
- Clear titles for context

### 4. Accessibility
- Meaningful titles
- Icons for navigation
- Logical grouping

### 5. Performance
- Limited cameras per view (max 4)
- Reasonable card counts (8-12 per view)
- Efficient card types

---

## Tips for Dashboard Design

1. **Start with Overview**: Create general view first, then add specialized views
2. **Limit Cards**: Keep 8-12 cards per view for best UX
3. **Use Icons**: Visual navigation is faster than text
4. **Group Logically**: Related controls together (all kitchen in one view)
5. **Test Mobile**: Most users access dashboards on phones
6. **Add Context**: Titles help users understand what they're controlling
7. **Iterate**: Start simple, add complexity as needed

---

## Card Type Selection Guide

| Entity Type | Single Entity | Multiple Entities | Best Use |
|-------------|---------------|-------------------|----------|
| Light | `light` | `entities` | Quick toggle vs detailed controls |
| Climate | `thermostat` | `entities` | Temperature control |
| Media Player | `media-control` | `entities` | Playback with album art |
| Camera | `picture-entity` | `grid` | Live feed display |
| Sensor | `sensor` / `gauge` | `entities` | Numeric values |
| Binary Sensor | `entity` | `entities` | Status indication |
| Switch | `button` | `entities` | Actions vs grouped switches |
| Cover | `cover` | `entities` | Blinds/shades with position |
| Lock | `lock` | `entities` | Secure controls |
| Weather | `weather-forecast` | N/A | Weather display |

---

## Common Patterns

### Welcome Card Pattern
```yaml
- type: markdown
  content: |
    # 🏠 Home Dashboard
    Welcome home!
```

### Quick Status Badges
```yaml
- type: entities
  entities:
    - entity: alarm_control_panel.home_alarm
      name: Security
    - entity: climate.home_living_room_heatpump
      name: Climate
    - entity: person.user
      name: Location
```

### Grouped Lights
```yaml
- type: entities
  title: Living Room Lights
  entities:
    - light.home_living_room_ceiling
    - light.home_living_room_lamp_1
    - light.home_living_room_lamp_2
```

### Security Status
```yaml
- type: entities
  title: Security Status
  show_header_toggle: false
  entities:
    - binary_sensor.home_front_door
    - binary_sensor.home_back_door
    - binary_sensor.home_garage_door
    - binary_sensor.home_basement_motion
```

---

Happy dashboard designing! 🎨✨
