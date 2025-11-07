# Troubleshoot Configuration Issues

Help diagnose and fix Home Assistant configuration validation errors.

## What to do:

1. **Gather Information**:
   - Ask what problem the user is experiencing:
     - Validation errors?
     - Automation not working?
     - Entity not found?
     - YAML syntax issues?
   - Run validation if not already done
   - Check git status for recent changes

2. **Run Comprehensive Diagnostics**:

   **A. YAML Validation:**
   ```bash
   source venv/bin/activate && python tools/yaml_validator.py
   ```
   - Check for syntax errors
   - Identify problematic files and line numbers

   **B. Entity Reference Validation:**
   ```bash
   source venv/bin/activate && python tools/reference_validator.py
   ```
   - Find missing or disabled entities
   - Check for typos in entity names
   - Verify device references

   **C. Official HA Validation:**
   ```bash
   source venv/bin/activate && python tools/ha_official_validator.py
   ```
   - Run Home Assistant's own validation
   - Check integration-specific issues

3. **Analyze Errors**:

   For each error found:
   - **Parse error message**: Extract key information
   - **Identify root cause**: What's actually wrong?
   - **Locate problem**: Which file, line, entity?
   - **Explain impact**: What breaks if not fixed?
   - **Check dependencies**: Are there related issues?

4. **Provide Solutions**:

   For each issue, offer:
   - **Quick fix**: Immediate solution
   - **Explanation**: Why this fixes it
   - **Prevention**: How to avoid in future
   - **Code example**: Show correct syntax

5. **Common Issue Patterns**:

   **Entity Not Found:**
   - Search entity registry for similar names
   - Check if entity was renamed
   - Verify entity exists and is enabled
   - Look for typos (underscore vs dash, singular vs plural)

   **YAML Syntax Error:**
   - Check indentation (must be 2 spaces, not tabs)
   - Verify quote matching
   - Check for special characters
   - Ensure proper list formatting

   **Integration Error:**
   - Check if integration is installed
   - Verify configuration keys
   - Check for deprecated options
   - Review integration documentation

   **Template Error:**
   - Validate Jinja2 syntax
   - Check variable existence
   - Test template in Developer Tools
   - Simplify complex templates

6. **Step-by-Step Resolution**:
   - Fix issues in priority order (critical first)
   - Validate after each fix
   - Confirm issue is resolved
   - Check for cascade effects

7. **Prevention Recommendations**:
   - Suggest workflow improvements
   - Recommend validation before edits
   - Show how hooks prevent issues
   - Share best practices

## Diagnostic Commands:

```bash
# Full validation suite
source venv/bin/activate && python tools/run_tests.py

# Check specific file syntax
source venv/bin/activate && python tools/yaml_validator.py config/automations.yaml

# Find entity information
source venv/bin/activate && python tools/entity_explorer.py --search "entity_name"

# Check entity registry
cat config/.storage/core.entity_registry | grep "entity_id"

# Git diff to see recent changes
git diff config/
```

## Common Error Messages:

### "Entity not found"
```
❌ Error: entity_id 'light.livng_room' not found

🔍 Diagnosis: Typo in entity name (missing 'i' in 'living')

🔧 Fix: Change 'light.livng_room' to 'light.living_room'

💡 Tip: Use /explore-entities to verify entity names
```

### "Invalid YAML"
```
❌ Error: mapping values are not allowed here (line 45)

🔍 Diagnosis: Indentation error or missing colon

🔧 Fix: Check line 45 for proper indentation and syntax

💡 Tip: YAML uses 2-space indentation, not tabs
```

### "Unknown integration"
```
❌ Error: Integration 'my_custom' not found

🔍 Diagnosis: Integration not installed or typo in name

🔧 Fix: Install integration or correct the name

💡 Tip: Check HACS or official integrations list
```

## Output Format:

```
🔍 Running diagnostics...

Found 3 issues:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Issue 1: Entity Reference Error
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: config/automations.yaml
Line: 67
Entity: binary_sensor.basement_motion

Problem: Entity not found in registry

Root Cause: Entity was renamed to 'binary_sensor.home_basement_motion'

Fix: Update line 67:
  entity_id: binary_sensor.home_basement_motion

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 Would you like me to apply these fixes automatically?
```

## Important:

- Be methodical and thorough
- Test fixes one at a time
- Validate after each change
- Explain not just what but why
- Help user learn to prevent future issues
