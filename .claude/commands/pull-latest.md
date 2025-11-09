# Pull Latest Configuration from Home Assistant

Sync the latest configuration from the Home Assistant instance to local development environment.

## Workflow:

1. **Check for Local Changes**:
   - Run: `git status`
   - Warn if there are uncommitted local changes
   - Ask user if they want to:
     - Commit local changes first
     - Stash local changes
     - Proceed anyway (will be overwritten)
     - Abort operation

2. **Pull Configuration**:
   - Execute: `make pull`
   - This runs rsync to download config from HA instance
   - Excludes sensitive files (.storage files with tokens, secrets)
   - Show what files were updated

3. **Validate Downloaded Config**:
   - Automatically run validation suite
   - Execute: `source venv/bin/activate && python tools/run_tests.py`
   - Report validation results

4. **Report Changes**:
   - Show git diff of what changed
   - Highlight:
     - New files added
     - Modified files
     - Deleted files
   - Explain what might have caused changes (new devices, modified automations, etc.)

5. **Suggest Next Steps**:
   - Review changes and verify they make sense
   - Commit the pulled changes if desired
   - Note any validation issues that need fixing

## Use Cases:

**When to use this command:**
- After making changes directly in Home Assistant UI
- After adding new devices/integrations
- Before starting development (to ensure sync)
- Periodically to stay in sync with HA instance

**What gets pulled:**
- configuration.yaml and all included files
- automations.yaml
- scripts.yaml
- scenes.yaml
- customize.yaml
- Entity registry data (.storage/core.entity_registry)
- Other non-sensitive config files

**What doesn't get pulled (excluded):**
- secrets.yaml (contains sensitive data)
- .storage/ authentication files
- Temporary files and caches

## Safety Notes:

- Always check for local changes first
- Pulling will overwrite local modifications
- Consider committing local work before pulling
- Validation ensures pulled config is valid

## Output Format:

```
🔍 Checking for local changes...
   ⚠️  You have uncommitted changes in:
   - config/automations.yaml

   Options:
   1. Commit changes first
   2. Stash changes
   3. Overwrite (lose local changes)
   4. Abort

📥 Pulling configuration from Home Assistant...
   Downloaded: config/automations.yaml (modified)
   Downloaded: config/.storage/core.entity_registry (modified)

🧪 Validating downloaded configuration...
   ✅ All validations passed

📊 Changes summary:
   - 2 automations added
   - 1 script modified
   - 3 new entities registered

✅ Pull complete! Local config is now in sync.
```
