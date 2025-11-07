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
