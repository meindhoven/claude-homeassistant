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
