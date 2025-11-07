# Home Assistant Configuration Guidelines

This directory contains your Home Assistant configuration files synced from your HA instance.

## Directory Structure

```
config/
├── configuration.yaml     # Main configuration file
├── automations.yaml      # Automation definitions
├── scripts.yaml          # Reusable scripts
├── scenes.yaml           # Scene definitions
├── customize.yaml        # Entity customizations
├── secrets.yaml          # Sensitive data (not synced)
├── blueprints/           # Automation blueprints
│   └── automation/
└── .storage/             # Entity registry and state (not committed)
    └── core.entity_registry  # Used for validation
```

## Important Rules

### ⚠️ Read-Only Files

**NEVER edit these files directly** - they're managed by Home Assistant:
- `.storage/*` - Entity registry, auth, integrations
- `*.conf` - Integration-specific configs
- `automations.yaml` (if using UI editor)

### ✅ Safe to Edit

These files can be edited in this repository:
- `configuration.yaml` - Main config
- `scripts.yaml` - Custom scripts
- `scenes.yaml` - Scene definitions
- Blueprint files in `blueprints/`
- Any files in `packages/` (if using)

### 🔒 Secrets Management

- `secrets.yaml` is **never** committed to git
- Use `!secret` tag for sensitive values
- Example: `api_key: !secret openweather_api_key`
- Validation skips files using `!secret`

## Entity Naming Convention

This instance uses: **`location_room_device_sensor`**

### Examples:
```yaml
# Binary sensors
binary_sensor.home_basement_motion
binary_sensor.office_living_room_motion_battery

# Climate controls
climate.home_living_room_heatpump
climate.office_main_bedroom_thermostat

# Media players
media_player.home_kitchen_sonos
media_player.office_bedroom_sonos

# Lights
light.home_living_room_main
light.office_kitchen_overhead
```

### Parts:
- **location**: `home`, `office`, `cabin`, etc.
- **room**: `basement`, `kitchen`, `living_room`, `main_bedroom`
- **device**: `motion`, `heatpump`, `sonos`, `overhead`
- **sensor**: `battery`, `temperature`, `status`

## Writing Automations

### Basic Structure

```yaml
- id: unique_automation_id
  alias: "Human Readable Name"
  description: "What this automation does"
  trigger:
    - platform: state
      entity_id: binary_sensor.home_basement_motion
      to: 'on'
  condition:
    - condition: state
      entity_id: sun.sun
      state: 'below_horizon'
  action:
    - service: light.turn_on
      target:
        entity_id: light.home_basement_main
      data:
        brightness_pct: 100
```

### Best Practices

**1. Always include ID and alias**:
```yaml
- id: basement_motion_lights
  alias: "Basement Motion Activated Lights"
```

**2. Use meaningful descriptions**:
```yaml
  description: "Turn on basement lights when motion detected after sunset"
```

**3. Add mode setting** for automations that might overlap:
```yaml
  mode: single  # or: restart, queued, parallel
```

**4. Use templates for dynamic behavior**:
```yaml
  action:
    - service: light.turn_on
      data:
        brightness_pct: >
          {% if is_state('sun.sun', 'above_horizon') %}
            50
          {% else %}
            100
          {% endif %}
```

**5. Add delays for sequential actions**:
```yaml
  action:
    - service: light.turn_off
      target:
        entity_id: light.home_living_room_main
    - delay:
        seconds: 30
    - service: light.turn_off
      target:
        entity_id: light.home_kitchen_main
```

## Common Patterns

### Time-Based Automation
```yaml
- id: weekday_lights_off
  alias: "Weekday Midnight Lights Off"
  trigger:
    - platform: time
      at: "00:00:00"
  condition:
    - condition: time
      weekday:
        - mon
        - tue
        - wed
        - thu
        - fri
  action:
    - service: light.turn_off
      target:
        entity_id: all
```

### State-Based with Duration
```yaml
- id: no_motion_lights_off
  alias: "Basement Lights Off After 5 Min No Motion"
  trigger:
    - platform: state
      entity_id: binary_sensor.home_basement_motion
      to: 'off'
      for:
        minutes: 5
  action:
    - service: light.turn_off
      target:
        entity_id: light.home_basement_main
```

### Multi-Entity Targeting
```yaml
  action:
    - service: light.turn_off
      target:
        entity_id:
          - light.home_living_room_main
          - light.home_kitchen_main
          - light.home_bedroom_main
```

### Area-Based Targeting
```yaml
  action:
    - service: light.turn_off
      target:
        area_id: living_room
```

### Notification Action
```yaml
  action:
    - service: notify.mobile_app_iphone
      data:
        title: "Motion Detected"
        message: "Basement motion sensor triggered at {{ now().strftime('%H:%M') }}"
```

## YAML Syntax Rules

### Indentation
- **Always use 2 spaces** (never tabs)
- Be consistent throughout file

### Lists
```yaml
# Two valid formats:

# Dash format (preferred for clarity)
entity_id:
  - light.living_room
  - light.kitchen

# Inline format (compact)
entity_id: [light.living_room, light.kitchen]
```

### Strings
```yaml
# Quote when containing special characters
at: "00:00:00"
message: "It's time to leave!"

# Quote for numbers starting with zero
id: "0123"

# No quotes for simple values
state: on
```

### Home Assistant Specific Tags

**!include** - Include external files:
```yaml
automation: !include automations.yaml
script: !include scripts.yaml
```

**!secret** - Reference secrets:
```yaml
api_key: !secret openweather_key
```

**!input** - Blueprint inputs:
```yaml
entity_id: !input motion_sensor
```

## Validation Workflow

### Before Editing
1. Pull latest config: `make pull`
2. Check current validation: `make validate`

### After Editing
1. **Automatic validation** runs via hooks
2. **Manual validation**: `make validate` or `/validate-config`
3. Fix any errors before pushing

### Before Deploying
1. Run `/safe-deploy` slash command, or:
2. `make backup` - Create backup
3. `make validate` - Final check
4. `make push` - Deploy to HA

## Common Validation Errors

### Entity Not Found
```
ERROR: Entity 'light.livng_room' not found
```
**Fix**: Check spelling, use `/entity-search` to find correct name

### YAML Syntax Error
```
ERROR: mapping values are not allowed here (line 45)
```
**Fix**: Check indentation, colons, and list formatting

### Invalid Service
```
ERROR: Service 'light.tun_on' does not exist
```
**Fix**: Correct service name (should be `light.turn_on`)

### Missing Required Field
```
ERROR: required key not provided @ data['entity_id']
```
**Fix**: Add missing required field to configuration

## Integration-Specific Notes

### Climate Entities
```yaml
- service: climate.set_temperature
  target:
    entity_id: climate.home_living_room_heatpump
  data:
    temperature: 72
    hvac_mode: heat
```

### Media Players
```yaml
- service: media_player.play_media
  target:
    entity_id: media_player.home_kitchen_sonos
  data:
    media_content_type: music
    media_content_id: "spotify:playlist:..."
```

### Covers (Blinds/Shades)
```yaml
- service: cover.set_cover_position
  target:
    entity_id: cover.home_living_room_blinds
  data:
    position: 50  # 0 = closed, 100 = open
```

## Testing Configurations

### Check Config Without Restarting
```bash
# From HA CLI or SSH
ha core check
```

### Reload Specific Components
Most components support reload without restart:
```yaml
# automation.yaml
service: automation.reload

# script.yaml
service: script.reload

# scene.yaml
service: scene.reload
```

## Working with Claude Code

### Discovery First
Before writing automations:
```
/entity-search motion           # Find motion sensors
/entity-search climate          # Find thermostats
/explore-entities               # Interactive discovery
```

### Use Slash Commands
- `/create-automation` - Guided automation creation
- `/review-automation` - Analyze existing automation
- `/validate-config` - Check before deploying
- `/safe-deploy` - Backup and push safely

### Entity Discovery with MCP
If MCP is enabled, Claude can query live states:
```
"What's the current temperature in the office?"
"Is the basement motion sensor working?"
"Show me all lights that are currently on"
```

## Troubleshooting

### Automation Not Triggering

**Check trace**:
- Go to HA → Settings → Automations & Scenes
- Click on automation → "Trace" tab
- See why condition/trigger failed

**Common issues**:
- Entity state is different than expected
- Condition preventing execution
- Automation disabled
- Trigger time zone issues

### Configuration Not Loading

**Check HA logs**:
```bash
# View logs
ha core logs

# Or from UI
Settings → System → Logs
```

### Entity Unavailable

**Possible causes**:
- Integration offline/disconnected
- Entity disabled
- Entity was renamed/removed
- Network connectivity issues

## Resources

- [Home Assistant Documentation](https://www.home-assistant.io/docs/)
- [Automation Documentation](https://www.home-assistant.io/docs/automation/)
- [Template Documentation](https://www.home-assistant.io/docs/configuration/templating/)
- [Service Calls](https://www.home-assistant.io/docs/scripts/service-calls/)

## Quick Reference

### Common Services
- `light.turn_on` / `light.turn_off`
- `switch.turn_on` / `switch.turn_off`
- `climate.set_temperature`
- `cover.open_cover` / `cover.close_cover`
- `media_player.play_media`
- `notify.{service}` (platform-specific)
- `homeassistant.reload_core_config`
- `automation.reload`
- `script.reload`

### Common Conditions
- `condition: state` - Entity in specific state
- `condition: numeric_state` - Numeric comparison
- `condition: time` - Time-based condition
- `condition: sun` - Sunrise/sunset
- `condition: zone` - Location-based
- `condition: template` - Jinja2 template

### Common Triggers
- `platform: state` - Entity state changes
- `platform: time` - Specific time
- `platform: time_pattern` - Recurring pattern
- `platform: sun` - Sunrise/sunset
- `platform: webhook` - Webhook trigger
- `platform: mqtt` - MQTT message
- `platform: event` - HA event
