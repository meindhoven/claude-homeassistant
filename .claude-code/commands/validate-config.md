# Validate Home Assistant Configuration

Run the complete validation suite on the current Home Assistant configuration.

## What to do:

1. **Check environment**: Verify that the virtual environment and tools exist
2. **Run validation suite**: Execute `source venv/bin/activate && python tools/run_tests.py`
3. **Report results**: Provide a clear summary of:
   - YAML syntax validation results
   - Entity reference validation results
   - Official HA validation results
   - Any errors or warnings found
4. **Suggest fixes**: If validation fails, analyze errors and suggest specific fixes

## Output Format:

Provide a clear, structured report:
- ✅ Passed checks
- ❌ Failed checks with details
- ⚠️ Warnings that don't block deployment
- 🔧 Specific remediation steps if needed

## Important:

- Run from project root directory
- Ensure venv is activated
- Parse output to identify specific issues (file paths, line numbers, entity names)
- Don't just show raw output - interpret and explain what needs fixing
