# Quick Entity Search

Fast entity lookup with filters for finding specific Home Assistant entities.

## What to do:

1. **Understand Search Intent**:
   - Ask user what they're looking for if not specified
   - Determine best search approach:
     - By domain (sensor, light, switch, climate, etc.)
     - By area/location (kitchen, bedroom, office, etc.)
     - By keyword (motion, temperature, battery, etc.)
     - By device class (motion, door, temperature, etc.)

2. **Execute Targeted Search**:

   **Search by domain:**
   ```bash
   source venv/bin/activate && python tools/entity_explorer.py --domain DOMAIN
   ```

   **Search by area:**
   ```bash
   source venv/bin/activate && python tools/entity_explorer.py --area AREA
   ```

   **Search by keyword:**
   ```bash
   source venv/bin/activate && python tools/entity_explorer.py --search KEYWORD
   ```

   **Detailed view:**
   ```bash
   source venv/bin/activate && python tools/entity_explorer.py --full --search KEYWORD
   ```

3. **Present Results**:
   - Show entity_id (the actual identifier to use)
   - Show friendly name (human-readable name)
   - Show domain (entity type)
   - Show area/location if available
   - Show device_class if relevant
   - Highlight disabled entities with warning

4. **Provide Context**:
   - Explain the naming convention being used
   - Show related entities that might be useful
   - Suggest common use cases for found entities
   - Note any relevant attributes (units, states, etc.)

5. **Enable Quick Actions**:
   - Offer to create automation with found entity
   - Show example usage in YAML
   - Suggest complementary entities

## Common Search Scenarios:

### "Find all motion sensors"
```bash
source venv/bin/activate && python tools/entity_explorer.py --domain binary_sensor --search motion
```

### "Find kitchen devices"
```bash
source venv/bin/activate && python tools/entity_explorer.py --search kitchen
```

### "Find all climate controls"
```bash
source venv/bin/activate && python tools/entity_explorer.py --domain climate
```

### "Find temperature sensors"
```bash
source venv/bin/activate && python tools/entity_explorer.py --domain sensor --search temperature
```

### "Find entities in office"
```bash
source venv/bin/activate && python tools/entity_explorer.py --area office
```

## Entity Domains Reference:

Common domains to search:
- **sensor**: Temperature, humidity, battery, power, etc.
- **binary_sensor**: Motion, door, window, occupancy, etc.
- **light**: All lighting controls
- **switch**: Smart switches and outlets
- **climate**: Thermostats, HVAC, heat pumps
- **cover**: Blinds, shades, garage doors
- **lock**: Smart locks
- **media_player**: Sonos, TV, speakers
- **camera**: Security cameras
- **vacuum**: Robot vacuums
- **alarm_control_panel**: Security systems
- **device_tracker**: Presence detection
- **person**: Person entities
- **zone**: Location zones

## Output Format:

```
🔍 Searching for: motion sensors

Found 8 entities:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏠 Home - Basement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

binary_sensor.home_basement_motion
  Name: Home Basement Motion
  Device Class: motion
  State: off

binary_sensor.home_basement_motion_battery
  Name: Home Basement Motion Battery
  Device Class: battery
  State: 85%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 Office - Living Room
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

binary_sensor.office_living_room_motion
  Name: Office Living Room Motion
  Device Class: motion
  State: on
  ⚠️  Currently triggered!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Usage Examples:

In automations:
  trigger:
    - platform: state
      entity_id: binary_sensor.home_basement_motion
      to: 'on'

In conditions:
  condition: state
  entity_id: binary_sensor.home_basement_motion
  state: 'on'

Would you like to create an automation using any of these entities?
```

## Tips for Users:

- **Be specific**: Narrow searches save time
- **Check naming**: Entities follow `location_room_device_sensor` format
- **Multiple searches**: Try different keywords if first search doesn't find it
- **Full details**: Add `--full` flag for complete information
- **Combine filters**: Use domain + keyword for precise results

## Important:

- Parse entity registry from `config/.storage/core.entity_registry`
- Handle case-insensitive searches
- Show actual entity_id values (what to use in YAML)
- Warn about disabled entities (won't work in automations)
- Suggest alternatives if search returns no results
- Always format entity names correctly for copy-paste use
