# Create Home Assistant Automation

Guide the user through creating a new Home Assistant automation with proper validation.

## Workflow:

1. **Gather Requirements**: Ask the user to describe what they want to automate in plain English
   - What triggers the automation?
   - What conditions should be checked?
   - What actions should happen?

2. **Discover Entities**:
   - Use `source venv/bin/activate && python tools/entity_explorer.py` to find available entities
   - Search for relevant entities based on the user's description
   - Ask user to confirm which specific entities to use (don't assume if multiple match)
   - Follow the naming convention: `location_room_device_sensor`

3. **Draft Automation**: Create the YAML automation following HA best practices:
   - Meaningful `id` and `alias`
   - Clear trigger configuration
   - Appropriate conditions (if needed)
   - Well-structured actions
   - Include comments explaining the logic

4. **Add to Configuration**:
   - Add the automation to `config/automations.yaml`
   - Use proper YAML formatting and indentation

5. **Validate**: Run validation to ensure:
   - YAML syntax is correct
   - All entity references exist
   - Configuration is valid

6. **Explain**: Describe what the automation does and when it will trigger

## Important:

- **Always explore entities first** - don't guess entity names
- **Ask for clarification** if requirements are ambiguous
- **Follow naming conventions** documented in CLAUDE.md
- **Validate before completing** - never deliver unvalidated automations
- **Be specific** - avoid using "entity.example" placeholders

## Example Interaction:

User: "Turn off living room lights at 11pm on weekdays"

You should:
1. Search for living room light entities
2. Confirm which lights the user wants to control
3. Create automation with time trigger + weekday condition
4. Add to config/automations.yaml
5. Validate the configuration
6. Explain when it will run

## Multi-File Workflows

Some automations require changes to multiple files. Handle these systematically:

### Example 1: Automation with Helper Input

**User Request:** "Create automation to adjust living room brightness based on time of day"

**Multi-file changes needed:**

1. **config/configuration.yaml** - Add input_number helper:
```yaml
input_number:
  living_room_brightness_morning:
    name: "Living Room Morning Brightness"
    min: 0
    max: 100
    step: 5
    unit_of_measurement: "%"
  living_room_brightness_evening:
    name: "Living Room Evening Brightness"
    min: 0
    max: 100
    step: 5
    unit_of_measurement: "%"
```

2. **config/automations.yaml** - Add automation using the helpers:
```yaml
- id: living_room_brightness_schedule
  alias: "Living Room Brightness Schedule"
  trigger:
    - platform: time
      at: "07:00:00"
      id: morning
    - platform: time
      at: "18:00:00"
      id: evening
  action:
    - service: light.turn_on
      target:
        entity_id: light.home_living_room_main
      data:
        brightness_pct: >
          {% if trigger.id == 'morning' %}
            {{ states('input_number.living_room_brightness_morning') | int }}
          {% else %}
            {{ states('input_number.living_room_brightness_evening') | int }}
          {% endif %}
```

**Workflow:**
1. Check if input_number is configured in configuration.yaml
2. Add helper entities if needed
3. Create automation referencing the helpers
4. Validate both files changed
5. Explain how to adjust brightness via UI

### Example 2: Automation with Reusable Script

**User Request:** "Turn off all lights and lock doors when everyone leaves"

**Multi-file changes needed:**

1. **config/scripts.yaml** - Create reusable script:
```yaml
secure_home:
  alias: "Secure Home"
  sequence:
    - service: light.turn_off
      target:
        entity_id: all
    - service: lock.lock
      target:
        entity_id:
          - lock.home_front_door
          - lock.home_back_door
    - service: notify.mobile_app
      data:
        message: "Home secured - all lights off, doors locked"
```

2. **config/automations.yaml** - Add automation calling the script:
```yaml
- id: secure_on_departure
  alias: "Secure Home When Everyone Leaves"
  trigger:
    - platform: state
      entity_id: person.home
      to: 'not_home'
  condition:
    - condition: state
      entity_id: person.office
      state: 'not_home'
  action:
    - service: script.secure_home
```

**Workflow:**
1. Create reusable script in scripts.yaml
2. Create automation that calls the script
3. Validate both files
4. Explain script can be reused by other automations or manually triggered

### Example 3: Automation with Notification Configuration

**User Request:** "Notify me when garage door is left open for 10 minutes"

**Multi-file changes needed:**

1. **config/automations.yaml** - Add automation:
```yaml
- id: garage_door_open_alert
  alias: "Garage Door Left Open Alert"
  trigger:
    - platform: state
      entity_id: binary_sensor.home_garage_door
      to: 'on'
      for:
        minutes: 10
  action:
    - service: notify.mobile_app_iphone
      data:
        title: "Garage Door Alert"
        message: "Garage door has been open for 10 minutes"
        data:
          tag: "garage-door-alert"
          actions:
            - action: "CLOSE_GARAGE"
              title: "Close Garage Door"
```

2. **config/automations.yaml** - Add action handler (separate automation):
```yaml
- id: garage_door_notification_action
  alias: "Handle Garage Door Notification Action"
  trigger:
    - platform: event
      event_type: mobile_app_notification_action
      event_data:
        action: 'CLOSE_GARAGE'
  action:
    - service: cover.close_cover
      target:
        entity_id: cover.home_garage_door
```

**Workflow:**
1. Create alert automation with actionable notification
2. Create action handler automation
3. Validate configuration
4. Explain both automations work together

## Best Practices for Multi-File Changes:

1. **Plan First**: Identify all files that need changes before editing
2. **Edit Sequentially**: Make changes to files in logical order
3. **Validate After Each File**: Catch errors early
4. **Test Relationships**: Verify cross-file references work
5. **Commit Together**: All related changes in one commit
6. **Document Dependencies**: Explain which files depend on each other
