---
description: Design a user-friendly Home Assistant dashboard with best practices
---

You are running the **Design Dashboard** workflow using the Home Assistant Agent System.

Your task is to create a well-designed, user-friendly dashboard following HA best practices.

## Usage

The user wants to create or improve a dashboard. Help them design it with proper UX, accessibility, and visual design.

```
/design-dashboard

User: Create an overview dashboard for my home
User: Design a dashboard for the kitchen
User: I want a security monitoring dashboard
```

## Implementation

```python
from agents.orchestrator import OrchestratorAgent
from agents.shared_context import SharedContext
import yaml

# Initialize
context = SharedContext()
orchestrator = OrchestratorAgent(context)

# Get user's requirements
description = "<user's description of desired dashboard>"

# For specific room/area dashboards
layout_type = "overview"  # or "room", "security", "climate", "media"

# Run dashboard design workflow
result = orchestrator.run(
    workflow='design_dashboard',
    description=description,
    layout_type=layout_type
)

# Present the dashboard
if result.success:
    dashboard = result.data['dashboard']
    quality_score = result.data.get('quality_score', 0)

    print(f"✅ Dashboard designed successfully!")
    print(f"📊 Quality Score: {quality_score}/100")
    print(f"📑 Views: {result.data['view_count']}")
    print()

    # Show dashboard structure
    print("🎨 Dashboard Structure:\n")
    for view in dashboard.get('views', []):
        icon = view.get('icon', '📄')
        title = view.get('title', 'Untitled')
        card_count = len(view.get('cards', []))
        print(f"{icon} {title}: {card_count} cards")

    print()

    # Show recommendations
    if result.recommendations:
        print(f"💡 Recommendations:\n")
        for idx, rec in enumerate(result.recommendations[:10], 1):
            priority_icon = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(rec['priority'], '⚪')
            print(f"  {idx}. {priority_icon} {rec['description']}")
            if rec.get('action'):
                print(f"      → {rec['action']}")

    print()

    # Show YAML configuration
    print("📝 Dashboard Configuration (YAML):\n")
    print("```yaml")
    print(yaml.dump(dashboard, sort_keys=False, allow_unicode=True))
    print("```")

    print()
    print("Would you like me to:")
    print("1. Save this dashboard configuration to a file?")
    print("2. Make adjustments based on recommendations?")
    print("3. Create a different layout type?")
    print("4. Review the dashboard for additional improvements?")

else:
    print(f"❌ Dashboard design failed: {result.message}")
    for error in result.errors:
        print(f"  - {error}")
```

## Layout Types

Help users choose the appropriate layout:

### **Overview** (Default)
- Main dashboard view
- Quick actions and status summary
- Sections: Lights, Climate, Security, Weather
- Best for: Home page with most-used controls

### **Room**
- Single room control
- Sections: Lighting, Climate, Media, Sensors
- Best for: Dedicated room dashboards

### **Security**
- Security and monitoring
- Sections: Alarm, Cameras, Sensors, Locks
- Best for: Security overview

### **Climate**
- Climate and energy management
- Sections: Thermostats, Temperature Sensors, Energy
- Best for: Climate control and monitoring

### **Media**
- Media and entertainment
- Sections: Now Playing, Devices, Favorites
- Best for: Media control center

## Design Process

The workflow performs these steps:

1. **Entity Discovery**
   - Finds relevant entities based on description
   - Groups by area and domain
   - Suggests appropriate entities

2. **Dashboard Design**
   - Creates views based on layout type
   - Selects appropriate card types
   - Organizes cards logically
   - Follows naming conventions

3. **UX & Accessibility Review**
   - Checks information overload
   - Reviews visual hierarchy
   - Validates accessibility standards
   - Ensures responsive design
   - Calculates quality score

## Best Practices Applied

The agent system automatically applies:

### UX Principles
- ✅ Progressive disclosure (important info first)
- ✅ Visual hierarchy (clear primary/secondary content)
- ✅ Consistency (similar items look similar)
- ✅ Immediate feedback
- ✅ Error prevention

### Accessibility
- ✅ Meaningful labels
- ✅ Icon + text for status (not color alone)
- ✅ Touch-friendly targets (44x44px minimum)
- ✅ Readable text sizes
- ✅ Keyboard navigation support

### Design
- ✅ Consistent card types within views
- ✅ Proper grouping of related items
- ✅ Visual breathing room
- ✅ Icons for navigation
- ✅ Appropriate card limits per view

### Performance
- ✅ Reasonable card counts
- ✅ Optimized camera card usage
- ✅ Conditional cards when appropriate

## Common Patterns

### Creating Overview Dashboard

```python
result = orchestrator.run(
    workflow='design_dashboard',
    description='Overview dashboard with lights, climate, and security',
    layout_type='overview'
)
```

### Room-Specific Dashboard

```python
result = orchestrator.run(
    workflow='design_dashboard',
    description='Kitchen dashboard with lights, climate, and appliances',
    layout_type='room'
)
```

### Security Dashboard

```python
result = orchestrator.run(
    workflow='design_dashboard',
    description='Security dashboard with cameras, alarm, and door sensors',
    layout_type='security'
)
```

### Custom Entity Selection

```python
# Specify exact entities to include
entities = [
    'light.home_living_room_ceiling',
    'climate.home_living_room_heatpump',
    'media_player.home_living_room_sonos',
    'sensor.home_living_room_temperature'
]

result = orchestrator.run(
    workflow='design_dashboard',
    description='Living room dashboard',
    entities=entities,
    layout_type='room'
)
```

## Reviewing Existing Dashboard

To review an existing dashboard configuration:

```python
# Load existing dashboard
with open('config/lovelace/dashboard.yaml', 'r') as f:
    dashboard = yaml.safe_load(f)

# Review for improvements
result = orchestrator.run(
    workflow='review_dashboard',
    dashboard=dashboard,
    review_type='full'  # or 'ux', 'accessibility', 'design', 'performance'
)

print(f"📊 Quality Score: {result.data['quality_score']}/100")
print(f"\n🔍 Issues Found: {len(result.errors)}")
print(f"⚠️  Warnings: {len(result.warnings)}")

for rec in result.recommendations:
    print(f"  • {rec['description']}")
```

## Optimization Tips

After designing, suggest these improvements:

1. **Too Many Cards**
   - Split into multiple views
   - Use grid cards for grouping
   - Consider conditional cards

2. **Inconsistent Design**
   - Standardize card types
   - Use consistent titles
   - Add view icons

3. **Poor Performance**
   - Limit camera cards (max 4 per view)
   - Use lazy loading
   - Reduce total card count

4. **Accessibility Issues**
   - Add meaningful titles
   - Use icons with text labels
   - Ensure proper contrast

## Card Type Selection Guide

Help users understand which card to use:

| Entity Domain | Single Entity | Multiple Entities | Best Use |
|---------------|---------------|-------------------|----------|
| light | light | entities/grid | Quick toggles vs detailed controls |
| climate | thermostat | entities | Temperature control |
| media_player | media-control | entities | Playback with album art |
| camera | picture-entity | grid | Live feed display |
| sensor | sensor/gauge | entities | Numeric values |
| binary_sensor | entity | entities | Status indication |
| switch | button | entities | Actions vs grouped switches |
| cover | cover | entities | Blinds/shades with position |
| lock | lock | entities | Secure controls |
| weather | weather-forecast | N/A | Weather display |

## Example Interaction

```
User: Create a dashboard for my home

Agent: I'll design an overview dashboard for you with the most important controls.

🎨 Dashboard designed with 5 views - Quality score: 87/100

📑 Views:
  🏠 Overview: 8 cards (welcome, lights, climate, security, weather)
  🛏️  Bedroom: 6 cards (lights, climate, media, sensors)
  🍳 Kitchen: 5 cards (lights, climate, appliances)
  🔒 Security: 7 cards (alarm, cameras, door sensors, locks)
  ☁️  Climate: 4 cards (thermostats, temperature sensors)

💡 Recommendations:
  1. 🟡 Add custom theme for better visual consistency
  2. 🟡 Consider adding badges for quick status at top
  3. 🟢 Test on mobile devices for responsive design

Would you like me to:
1. Save this dashboard?
2. Adjust based on recommendations?
3. Focus on a specific room?
```

## Saving Dashboard

After user approves, save the configuration:

```python
# Save to dashboard file
dashboard_path = 'config/lovelace/dashboard.yaml'

with open(dashboard_path, 'w') as f:
    yaml.dump(dashboard, f, sort_keys=False, allow_unicode=True)

print(f"✅ Dashboard saved to {dashboard_path}")
print("\nNext steps:")
print("1. Go to HA → Settings → Dashboards")
print("2. Add new dashboard")
print("3. Choose 'Edit in YAML'")
print("4. Paste the configuration")
print("5. Save and enjoy your new dashboard!")
```

## Interactive Refinement

Offer to refine based on user feedback:

```
User: Can you make the living room view more detailed?

Agent: I'll redesign the living room view with more cards...

[Runs design workflow for specific room with more entities]

✅ Updated living room view with 12 cards
  - Added individual light controls (was grouped)
  - Added humidity sensor
  - Added media favorites
  - Split climate into thermostat + sensors

💡 Note: View now has 12 cards (recommended max: 10)
Consider if all cards are necessary or create a "Living Room Details" sub-view.
```

## Tips for Users

Explain these dashboard design principles:

1. **Start Simple**: Begin with overview, add detail as needed
2. **Group Logically**: Related controls together
3. **Use Icons**: Visual navigation is faster
4. **Limit Cards**: 8-12 cards per view ideal
5. **Test Mobile**: Most users view on phones
6. **Add Context**: Titles help understanding
7. **Iterate**: Start basic, improve over time

---

The dashboard design agent helps create professional, user-friendly dashboards that follow Home Assistant best practices! 🎨✨
