# Explore Home Assistant Entities

Interactive entity discovery to help understand what's available in the Home Assistant instance.

## What to do:

1. **Ask what the user wants to find**:
   - Specific device type? (lights, sensors, switches, climate, etc.)
   - Specific location? (home, office, specific room)
   - Specific functionality? (motion, temperature, battery, etc.)

2. **Run entity explorer** with appropriate filters:
   ```bash
   source venv/bin/activate && python tools/entity_explorer.py [OPTIONS]
   ```

   Options:
   - `--domain DOMAIN` - Filter by domain (sensor, binary_sensor, light, switch, climate, etc.)
   - `--area AREA` - Filter by area/location
   - `--search TERM` - Search by keyword
   - `--full` - Show complete details

3. **Present results clearly**:
   - Group by domain or location
   - Show entity_id, friendly name, and current state (if available)
   - Highlight relevant attributes (device_class, unit_of_measurement, etc.)
   - Note any disabled entities

4. **Provide context**:
   - Explain the naming convention: `location_room_device_sensor`
   - Suggest related entities that might be useful
   - If searching for automations, suggest which entities would work well together

## Example Usage Patterns:

**Finding climate controls:**
```bash
source venv/bin/activate && python tools/entity_explorer.py --domain climate
```

**Finding motion sensors:**
```bash
source venv/bin/activate && python tools/entity_explorer.py --search motion
```

**Finding kitchen devices:**
```bash
source venv/bin/activate && python tools/entity_explorer.py --area kitchen
```

## Important:

- Parse the entity registry data from `config/.storage/core.entity_registry`
- Show practical, actionable information
- Help users understand what they have available
- Suggest automation ideas based on discovered entities
