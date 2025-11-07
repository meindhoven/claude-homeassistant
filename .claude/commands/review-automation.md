# Review and Improve Existing Automation

Analyze an existing Home Assistant automation and suggest improvements.

## What to do:

1. **Select Automation**:
   - Ask user which automation to review (by name or ID)
   - Or list available automations from `config/automations.yaml`
   - Read the full automation configuration

2. **Comprehensive Analysis**:

   **A. Functionality Review:**
   - Explain what the automation does in plain English
   - Describe trigger conditions
   - Describe action sequence
   - Note any conditions or templating logic

   **B. Best Practices Check:**
   - ✅ Has unique ID?
   - ✅ Has descriptive alias?
   - ✅ Triggers are appropriate?
   - ✅ Conditions are necessary?
   - ✅ Actions are efficient?
   - ✅ Uses mode setting if needed (single/restart/queued/parallel)?

   **C. Entity Validation:**
   - Verify all referenced entities exist
   - Check entity naming follows convention
   - Warn about disabled entities
   - Suggest better entity choices if available

   **D. Reliability:**
   - Check for race conditions
   - Identify timing issues
   - Review template complexity
   - Check for potential infinite loops

   **E. Performance:**
   - Identify unnecessary triggers
   - Suggest consolidation opportunities
   - Review condition efficiency
   - Check for excessive API calls

3. **Suggest Improvements**:

   For each issue found, provide:
   - **What's wrong**: Clear explanation
   - **Why it matters**: Impact on reliability/performance/maintainability
   - **How to fix**: Specific code changes
   - **Priority**: Critical / Important / Nice-to-have

4. **Offer Enhancements**:
   - Additional conditions to prevent false triggers
   - Better error handling
   - Notifications for tracking
   - Alternative approaches
   - Related automations that might conflict

5. **Show Before/After**:
   - Present original automation
   - Present improved version
   - Highlight specific changes
   - Explain benefits of each change

## Review Checklist:

- [ ] Automation has clear purpose
- [ ] ID and alias are descriptive
- [ ] Triggers are appropriate and efficient
- [ ] Conditions prevent unwanted executions
- [ ] Actions achieve desired result
- [ ] All entities exist and are enabled
- [ ] No race conditions or timing issues
- [ ] Templates are correct and tested
- [ ] Mode setting is appropriate
- [ ] Error handling is adequate
- [ ] Comments explain complex logic
- [ ] Follows naming conventions

## Common Issues to Look For:

1. **Multiple time-based triggers**: Can often be consolidated
2. **Missing mode setting**: May cause overlapping executions
3. **No conditions**: Automation might run too frequently
4. **Hardcoded values**: Should use input_number or variables
5. **Complex templates**: Could be simplified or split
6. **Missing delays**: Actions might happen too quickly
7. **No notifications**: Hard to debug when it runs
8. **Disabled entities**: Automation won't work properly

## Example Output:

```
📋 Reviewing Automation: "Turn off lights at midnight"

🔍 Current Functionality:
This automation turns off all lights at midnight every day.

Trigger: Time pattern at 00:00:00
Actions: Turn off light.living_room, light.kitchen, light.bedroom

✅ Strengths:
- Has unique ID and clear alias
- Simple and straightforward logic
- All entities exist

⚠️ Issues Found:

1. [IMPORTANT] No weekday condition
   - Automation runs every day including weekends
   - Might want different schedules for weekdays/weekends
   - Add condition to check day of week

2. [NICE-TO-HAVE] Hardcoded entity list
   - Adding new lights requires editing automation
   - Consider using area-based targeting
   - Or use a group

3. [NICE-TO-HAVE] No confirmation
   - Hard to verify automation ran
   - Consider adding notification or log entry

🔧 Suggested Improvements:
[Shows before/after code with improvements]

Would you like me to apply these improvements?
```

## Important:

- Be thorough but not pedantic
- Focus on meaningful improvements
- Explain the "why" behind suggestions
- Respect user's intent - don't change functionality without asking
- Always validate after making changes

## Cross-File Analysis

Many automations depend on entities or configurations defined in other files. Always check these relationships:

### 1. Script References

If automation calls scripts, verify they exist and are correct:

**Check in automation:**
```yaml
action:
  - service: script.secure_home
```

**Verify in config/scripts.yaml:**
```bash
# Read config/scripts.yaml
# Look for: secure_home:
# Verify parameters match
```

**What to check:**
- ✅ Script exists in scripts.yaml
- ✅ Script has required parameters
- ✅ Script actions are still valid
- ⚠️ Warn if script is complex or might fail
- 💡 Suggest improvements to script if needed

### 2. Helper Entity Dependencies

If automation uses input helpers, verify configuration:

**Check in automation:**
```yaml
data:
  brightness_pct: "{{ states('input_number.living_room_brightness') | int }}"
```

**Verify in config/configuration.yaml:**
```bash
# Read config/configuration.yaml
# Look for: input_number: section
# Find: living_room_brightness:
# Check min/max/step values
```

**What to check:**
- ✅ Helper entity is defined
- ✅ Min/max ranges are appropriate
- ✅ Default value makes sense
- ✅ Unit of measurement is correct
- 💡 Suggest better defaults if needed

### 3. Scene References

If automation activates scenes:

**Check in automation:**
```yaml
action:
  - service: scene.turn_on
    target:
      entity_id: scene.movie_mode
```

**Verify in config/scenes.yaml:**
```bash
# Read config/scenes.yaml
# Look for: movie_mode:
# Check entity states defined
```

**What to check:**
- ✅ Scene exists
- ✅ Scene includes expected entities
- ✅ State values are reasonable
- ⚠️ Warn about conflicts with other scenes

### 4. Customization Dependencies

If automation relies on customized entities:

**Check in automation:**
```yaml
# Automation might expect specific:
# - friendly names
# - device classes
# - icons
# - hidden states
```

**Verify in config/customize.yaml:**
```bash
# Read config/customize.yaml
# Check entity customizations
```

**What to check:**
- ✅ Customizations exist
- ✅ Device classes are correct
- ⚠️ Warn if customization affects automation logic

### 5. Conflicting Automations

Check for automations that might interfere:

**What to check:**
- 🔍 Search config/automations.yaml for:
  - Same entity_id in triggers
  - Same service calls to same entities
  - Opposite actions (one turns on, another turns off)
  - Same time triggers

**Common conflicts:**
```yaml
# Automation 1: Turns lights on at sunset
- id: lights_on_sunset
  trigger:
    - platform: sun
      event: sunset
  action:
    - service: light.turn_on
      entity_id: light.living_room

# Automation 2: Turns same lights off at 6pm
- id: lights_off_evening
  trigger:
    - platform: time
      at: "18:00:00"  # Might be around sunset!
  action:
    - service: light.turn_off
      entity_id: light.living_room
```

**Resolution:**
- Identify time overlaps
- Suggest condition to prevent conflicts
- Recommend consolidation if appropriate

### 6. Referenced Groups

If automation uses groups:

**Check in automation:**
```yaml
target:
  entity_id: group.all_downstairs_lights
```

**Verify in config/groups.yaml or configuration.yaml:**
```bash
# Read group configuration
# Verify group exists and members are valid
```

**What to check:**
- ✅ Group exists
- ✅ Group members exist
- ✅ Group type is appropriate
- 💡 Suggest area-based targeting if better

## Multi-File Review Workflow

When reviewing an automation, follow this process:

```
1. Read the automation (config/automations.yaml)
   ↓
2. Identify dependencies:
   - Scripts? → Read config/scripts.yaml
   - Helpers? → Read config/configuration.yaml
   - Scenes? → Read config/scenes.yaml
   - Groups? → Read config/groups.yaml or configuration.yaml
   ↓
3. Verify each dependency:
   - Exists?
   - Correctly configured?
   - Still valid?
   ↓
4. Check for conflicts:
   - Search automations.yaml for similar triggers
   - Identify timing overlaps
   - Find opposite actions
   ↓
5. Report findings:
   - List all files checked
   - Note any issues in dependencies
   - Warn about conflicts
   - Suggest consolidation opportunities
   ↓
6. Recommend improvements:
   - Fix broken references
   - Update deprecated patterns
   - Consolidate duplicates
   - Add missing validations
```

## Example Multi-File Review

```
📋 Reviewing Automation: "Movie Mode at Night"

📂 Files analyzed:
- config/automations.yaml (primary)
- config/scenes.yaml (scene reference)
- config/scripts.yaml (notification script)
- config/configuration.yaml (input_datetime helper)

🔍 Current Configuration:

Automation triggers at time specified by input_datetime.movie_time,
activates scene.movie_mode, and calls script.notify_movie_start.

✅ Dependencies verified:
- scene.movie_mode exists in scenes.yaml
- script.notify_movie_start exists in scripts.yaml
- input_datetime.movie_time defined in configuration.yaml

⚠️ Cross-file issues found:

1. [IMPORTANT] Scene includes obsolete entity
   File: config/scenes.yaml, line 45
   Issue: scene.movie_mode references light.old_tv_backlight
   Impact: Scene activation will fail
   Fix: Remove obsolete entity or update to new entity name

2. [NICE-TO-HAVE] Script could be simplified
   File: config/scripts.yaml, line 120
   Issue: notify_movie_start has complex logic
   Suggestion: Use notify service directly in automation

3. [IMPORTANT] Conflicting automation detected
   File: config/automations.yaml, line 78
   Conflict: "Lights off at 9pm" runs at same time as movie mode
   Impact: Lights turn off immediately after movie mode activates
   Fix: Add condition to skip if movie mode is active

🔧 Recommended changes across files:
[Shows specific changes for each file]

Would you like me to apply these fixes?
```
