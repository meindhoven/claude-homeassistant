# Fix YAML Formatting Issues

Automatically fix common YAML formatting problems in Home Assistant configuration files.

## What to do:

1. **Identify Problem Files**:
   - Ask user which files need fixing, or
   - Run validation to find files with issues
   - Check for common problems:
     - Indentation errors
     - Missing quotes
     - Incorrect line breaks
     - Trailing spaces
     - Wrong encoding

2. **Analyze Issues**:
   - Run: `source venv/bin/activate && python tools/yaml_validator.py`
   - Parse error messages to identify specific issues
   - Determine if issues are auto-fixable or need manual intervention

3. **Auto-Fix When Possible**:
   - Use yamllint with auto-fix capabilities
   - Fix indentation (2 spaces, not tabs)
   - Remove trailing whitespace
   - Ensure proper line endings (LF, not CRLF)
   - Fix quote consistency
   - Ensure UTF-8 encoding

4. **Manual Fix Guidance**:
   For issues that need human judgment:
   - Show exact line numbers and context
   - Explain what's wrong
   - Suggest specific corrections
   - Provide before/after examples

5. **Validate After Fixing**:
   - Re-run validation to confirm fixes worked
   - Report remaining issues if any

## Common YAML Issues:

### Indentation Errors
```yaml
# ❌ Wrong (inconsistent indentation)
automation:
  - id: test
  trigger:
    - platform: time

# ✅ Correct (consistent 2-space indentation)
automation:
  - id: test
    trigger:
      - platform: time
```

### Quote Issues
```yaml
# ❌ Wrong (unquoted time values)
at: 00:00:00

# ✅ Correct (quoted time values)
at: "00:00:00"
```

### List Format
```yaml
# ❌ Wrong (inconsistent list format)
entity_id:
  - light.living_room
  light.kitchen

# ✅ Correct (consistent list format)
entity_id:
  - light.living_room
  - light.kitchen
```

## Tools Used:

- `tools/yaml_validator.py` - Detect syntax errors
- `.yamllint.yml` - Linting rules configuration
- `yamllint` - YAML linter (via hook)
- Claude Code's Edit tool - Make corrections

## Workflow:

1. Backup config first (safety)
2. Run validation to identify issues
3. Fix automatically where possible
4. Guide manual fixes for complex issues
5. Validate again
6. Show diff of changes made

## Output Format:

```
🔍 Analyzing YAML files for issues...

Found issues in 2 files:
   ❌ config/automations.yaml (3 issues)
   ❌ config/scripts.yaml (1 issue)

🔧 Fixing automations.yaml...
   ✅ Fixed indentation on line 45
   ✅ Fixed missing quotes on line 67
   ✅ Removed trailing space on line 102

🔧 Fixing scripts.yaml...
   ✅ Fixed list format on line 23

✅ Re-validating...
   All YAML files now pass validation!

📊 Summary:
   Files fixed: 2
   Issues corrected: 4
   Remaining issues: 0
```

## Important:

- Always back up before making changes
- Test complex automations after fixing
- Some issues might need context to fix properly
- Validate after every fix to ensure correctness
