# Safe Deploy to Home Assistant

Validate and push local configuration to the Home Assistant instance with safety checks.

## Workflow:

1. **Pre-flight Status Check**:
   - Check git status for uncommitted changes
   - Show what files have been modified
   - Confirm with user that they want to proceed

2. **Run Complete Validation**:
   - Execute: `source venv/bin/activate && python tools/run_tests.py`
   - Check all three validation layers:
     - YAML syntax validation
     - Entity reference validation
     - Official HA validation

3. **Report Validation Results**:
   - ✅ If all validations pass: Proceed to backup
   - ❌ If any validation fails: **STOP** and report errors
   - Provide specific error details and suggested fixes
   - **Never deploy invalid configurations**

4. **Create Backup** (only if validation passed):
   - Execute: `make backup`
   - Confirm backup was created successfully
   - Show backup location and timestamp

5. **Push to Home Assistant** (only if backup succeeded):
   - Execute: `make push`
   - Monitor the rsync operation
   - Report success or any errors

6. **Verify Deployment**:
   - Suggest user verify HA is running correctly
   - Remind them to check HA logs if needed
   - Note that HA may need to be reloaded/restarted depending on changes

7. **Git Commit** (optional but recommended):
   - Ask if user wants to commit the changes
   - Suggest a meaningful commit message based on what changed
   - Commit and offer to push to remote git repository

## Safety Guardrails:

- **NEVER skip validation** - blocked deployments prevent broken HA instances
- **Always backup first** - enables quick rollback if needed
- **Stop on any error** - don't continue deployment if any step fails
- **Confirm destructive operations** - pushing overwrites remote config

## Output Format:

Provide clear status at each step:
```
🔍 Checking current status...
   Modified: config/automations.yaml, config/scripts.yaml

🧪 Running validation suite...
   ✅ YAML syntax: PASSED
   ✅ Entity references: PASSED
   ✅ Official HA validation: PASSED

💾 Creating backup...
   ✅ Backup created: backups/config-20231107-143022.tar.gz

📤 Pushing to Home Assistant...
   ✅ Configuration deployed successfully

✅ Deployment complete! Your changes are now live.
```

## Important:

- This is the ONLY safe way to deploy changes
- Pre-tool-use hook should already be blocking direct pushes
- If user tries to skip validation, warn them strongly against it
