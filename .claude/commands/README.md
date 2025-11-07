# Claude Code Slash Commands

This directory contains custom slash commands for Home Assistant configuration management with Claude Code.

## Available Commands

### Core Workflow Commands

1. **`/validate-config`** - Run complete validation suite
   - YAML syntax validation
   - Entity reference validation
   - Official HA validation
   - Comprehensive error reporting

2. **`/create-automation`** - Create new automation with guidance
   - Entity discovery and confirmation
   - YAML generation following best practices
   - Automatic validation
   - Follows naming conventions

3. **`/explore-entities`** - Interactive entity discovery
   - Search by domain, area, or keyword
   - View entity details and attributes
   - Understand available devices

4. **`/safe-deploy`** - Validate and push to Home Assistant
   - Pre-flight checks
   - Complete validation
   - Automatic backup
   - Safe deployment with verification

5. **`/pull-latest`** - Sync from Home Assistant
   - Check for local changes
   - Pull remote configuration
   - Validate downloaded config
   - Show changes summary

### Utility Commands

6. **`/backup-config`** - Create timestamped backup
   - Manual backup creation
   - View backup history
   - Disk space reporting

7. **`/fix-yaml`** - Fix YAML formatting issues
   - Auto-fix indentation
   - Quote correction
   - Trailing space removal
   - Encoding fixes

8. **`/review-automation`** - Review and improve automation
   - Functionality analysis
   - Best practices check
   - Performance optimization
   - Before/after comparison

9. **`/troubleshoot`** - Diagnose configuration issues
   - Comprehensive diagnostics
   - Error analysis
   - Step-by-step resolution
   - Prevention recommendations

10. **`/entity-search`** - Quick entity lookup
    - Fast targeted search
    - Multiple filter options
    - Usage examples
    - Related entity suggestions

## Usage

Simply type the slash command in Claude Code chat:

```
/validate-config
/create-automation
/entity-search
```

Claude will execute the workflow defined in the corresponding markdown file.

## How It Works

Each `.md` file contains detailed instructions for Claude on:
- What information to gather
- Which tools and scripts to run
- How to present results
- Error handling procedures
- Best practices to follow

## Customization

You can:
- Edit existing commands to match your workflow
- Add new commands by creating `.md` files
- Remove commands by deleting `.md` files
- Create personal commands in `.claude-local/commands/` (not synced)

## Command Naming Convention

- Use lowercase with hyphens
- Be descriptive but concise
- Match common user intentions
- Group related commands logically

## Best Practices

1. **Commands are workflows**: Not just shortcuts, but guided processes
2. **Include validation**: Always verify before destructive operations
3. **Provide context**: Explain what's happening at each step
4. **Handle errors**: Graceful error handling and clear error messages
5. **Be interactive**: Ask for confirmation on important decisions

## Related Files

- `.claude-code/settings.json` - Project settings and hooks
- `CLAUDE.md` - Project documentation for Claude
- `.claude-code/hooks/` - Validation hooks

## Documentation

For more information on Claude Code slash commands, see:
https://docs.claude.com/claude-code
