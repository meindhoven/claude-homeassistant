# Claude Code Hooks - Development Guide

This directory contains hooks that run automatically during Claude Code sessions.

## What Are Hooks?

Hooks are shell scripts that execute at specific points in the Claude Code workflow:
- **`posttooluse`** - Runs after Claude uses a tool (Edit, Write, etc.)
- **`pretooluse`** - Runs before Claude uses a tool
- **`userpromptsub mit`** - Runs when user submits a prompt

They enable automatic validation, formatting, and quality checks.

## Current Hooks

### `posttooluse-ha-validation.sh`
**Triggers**: After Edit/Write/MultiEdit/NotebookEdit
**Target**: YAML files in `config/` directory
**Purpose**: Validates Home Assistant configuration after edits

**What it does**:
1. Detects YAML file edits in config/
2. Activates Python venv
3. Runs `tools/run_tests.py` (full validation suite)
4. Reports validation results
5. **Does not block** - warns but allows Claude to continue

**When it runs**:
```bash
# User or Claude edits config/automations.yaml
# Hook automatically runs:
🔍 Running Home Assistant configuration validation...
✅ YAML syntax: PASSED
✅ Entity references: PASSED
✅ Official HA validation: PASSED
✅ Home Assistant configuration validation passed!
```

### `posttooluse-python-quality.sh`
**Triggers**: After any tool use
**Target**: Python files in `tools/` directory
**Purpose**: Ensures code quality for validation tools

**What it does**:
1. Detects Python file modifications
2. Runs Black formatting (auto-fixes)
3. Runs isort (import sorting)
4. Runs flake8 (style checking)
5. Runs pylint (code analysis - warnings only)
6. Runs mypy (type checking - warnings only)
7. Runs pytest (if tests exist)

**Code quality checks**:
- ✅ **Black**: Auto-formats code to PEP8 (88 char lines)
- ✅ **isort**: Sorts imports consistently
- ✅ **flake8**: Style enforcement (blocks on errors)
- ⚠️ **pylint**: Code analysis (non-blocking)
- ⚠️ **mypy**: Type checking (non-blocking)
- ✅ **pytest**: Runs test suite (blocks on failures)

### `yaml-formatter.sh`
**Triggers**: After YAML file edits
**Purpose**: Auto-formats YAML files
**Features**:
- Fixes indentation (2 spaces)
- Removes trailing whitespace
- Ensures proper line endings

### `pretooluse-ha-push-validation.sh`
**Triggers**: Before Bash commands matching push/deploy
**Purpose**: Blocks invalid configurations from being pushed

**What it does**:
1. Detects `make push` or deployment commands
2. Runs complete validation suite
3. **Blocks command** if validation fails
4. Allows command if validation passes

**Critical**: This prevents broken configs from reaching HA!

## Hook Development Guidelines

### File Requirements

**1. Executable permissions**:
```bash
chmod +x .claude-code/hooks/your-hook.sh
```

**2. Shebang line**:
```bash
#!/bin/bash
```

**3. Exit codes**:
- `exit 0` - Success, continue workflow
- `exit 1` - Error, block operation (use carefully!)

### Environment Variables

Claude Code provides these variables to hooks:

- `$CLAUDE_TOOL_NAME` - Tool that was used (Edit, Write, Bash, etc.)
- `$CLAUDE_TOOL_ARGS` - Arguments passed to the tool
- `$CLAUDE_WORK_DIR` - Working directory
- `$CLAUDE_FILE_PATH` - Path to affected file (if applicable)

**Example usage**:
```bash
if [[ "$CLAUDE_TOOL_NAME" == "Edit" ]]; then
    if [[ "$CLAUDE_TOOL_ARGS" =~ config/.*\.yaml ]]; then
        echo "YAML file edited, running validation..."
    fi
fi
```

### Best Practices

#### 1. Be Selective
Only run hooks when relevant:
```bash
# Good - check if this is a HA project first
if [ ! -f "config/configuration.yaml" ]; then
    exit 0  # Not a HA project, skip silently
fi
```

#### 2. Fast Execution
Hooks should complete quickly (<2 seconds):
- Cache expensive operations
- Only validate changed files
- Run intensive checks in background if needed

#### 3. Clear Output
Use colored output and emojis for clarity:
```bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}✅ Validation passed!${NC}"
echo -e "${RED}❌ Validation failed!${NC}"
echo -e "${YELLOW}⚠️  Warning: ...${NC}"
```

#### 4. Non-Blocking by Default
Only block for critical issues:
```bash
# Warn but allow
if [ $validation_result -ne 0 ]; then
    echo "⚠️  Validation failed, but continuing..."
    exit 0  # Don't block
fi

# Block critical issues
if [[ "$CLAUDE_TOOL_ARGS" =~ "make push" ]]; then
    if [ $validation_result -ne 0 ]; then
        echo "❌ Cannot push invalid config!"
        exit 1  # Block push
    fi
fi
```

#### 5. Error Handling
```bash
set -e  # Exit on error

# Or handle errors explicitly
if ! command_that_might_fail; then
    echo "Error occurred, but continuing..."
    exit 0
fi
```

## Hook Patterns

### Pattern 1: Conditional Validation
```bash
#!/bin/bash
# Only validate specific file types

if [[ "$CLAUDE_TOOL_NAME" == "Edit" || "$CLAUDE_TOOL_NAME" == "Write" ]]; then
    if [[ "$CLAUDE_TOOL_ARGS" =~ \.yaml$ ]]; then
        echo "🔍 Validating YAML..."
        yamllint "$file_path"
    fi
fi
```

### Pattern 2: Auto-Formatting
```bash
#!/bin/bash
# Auto-format Python files after edit

if [[ "$CLAUDE_TOOL_ARGS" =~ \.py$ ]]; then
    echo "🎨 Formatting Python code..."
    black "$file_path"
    isort "$file_path"
    echo "✅ Formatted"
fi
```

### Pattern 3: Pre-Command Blocking
```bash
#!/bin/bash
# Block dangerous commands

if [[ "$CLAUDE_TOOL_NAME" == "Bash" ]]; then
    if [[ "$CLAUDE_TOOL_ARGS" =~ "rm -rf /" ]]; then
        echo "❌ Dangerous command blocked!"
        exit 1
    fi
fi
```

### Pattern 4: Context-Aware Validation
```bash
#!/bin/bash
# Only run expensive checks during deployment

if [[ "$CLAUDE_TOOL_ARGS" =~ "deploy" ]]; then
    echo "🚀 Running full test suite before deployment..."
    pytest
    if [ $? -ne 0 ]; then
        echo "❌ Tests failed, blocking deployment"
        exit 1
    fi
fi
```

## Testing Hooks

### Manual Testing
```bash
# Simulate hook execution
cd /path/to/project
export CLAUDE_TOOL_NAME="Edit"
export CLAUDE_TOOL_ARGS="config/automations.yaml"
.claude-code/hooks/posttooluse-ha-validation.sh
```

### Debug Mode
Add debug output:
```bash
set -x  # Print each command
echo "DEBUG: Tool=$CLAUDE_TOOL_NAME Args=$CLAUDE_TOOL_ARGS"
```

### Test with Claude
1. Make a change that should trigger hook
2. Observe hook output in Claude Code
3. Verify behavior matches expectations

## Hook Configuration

Hooks are configured in `.claude-code/settings.json`:

```json
{
  "hooks": {
    "enabled": true,
    "posttooluse": [
      ".claude-code/hooks/yaml-formatter.sh",
      ".claude-code/hooks/posttooluse-ha-validation.sh",
      ".claude-code/hooks/posttooluse-python-quality.sh"
    ],
    "pretooluse": [
      ".claude-code/hooks/pretooluse-ha-push-validation.sh"
    ]
  }
}
```

### Order Matters
Hooks run in the order listed:
1. Formatting hooks first (modify files)
2. Validation hooks second (check results)

### Disabling Hooks Temporarily
```json
{
  "hooks": {
    "enabled": false  // Disables all hooks
  }
}
```

Or comment out specific hooks:
```json
{
  "hooks": {
    "posttooluse": [
      // ".claude-code/hooks/expensive-hook.sh",  // Disabled
      ".claude-code/hooks/quick-hook.sh"          // Active
    ]
  }
}
```

## Common Use Cases

### Auto-format on Save
```bash
#!/bin/bash
if [[ "$CLAUDE_TOOL_ARGS" =~ \.(py|js|ts)$ ]]; then
    # Format based on file type
    case "$file_path" in
        *.py) black "$file_path" ;;
        *.js) prettier --write "$file_path" ;;
        *.ts) prettier --write "$file_path" ;;
    esac
fi
```

### Run Tests After Changes
```bash
#!/bin/bash
if [[ "$CLAUDE_TOOL_ARGS" =~ tools/.*\.py$ ]]; then
    echo "🧪 Running tests..."
    pytest tests/ -x  # Stop on first failure
fi
```

### Prevent Committing Secrets
```bash
#!/bin/bash
if [[ "$CLAUDE_TOOL_NAME" == "Bash" ]] && [[ "$CLAUDE_TOOL_ARGS" =~ "git commit" ]]; then
    if grep -r "password\|secret\|api_key" .; then
        echo "❌ Potential secrets detected! Please remove before committing."
        exit 1
    fi
fi
```

### Update Documentation
```bash
#!/bin/bash
# Auto-update README when tools are added
if [[ "$CLAUDE_TOOL_ARGS" =~ tools/.*\.py$ ]]; then
    echo "📝 Updating documentation..."
    ./generate-docs.sh
fi
```

## Debugging Hook Issues

### Hook Not Running
1. Check `settings.json` - is hook listed and enabled?
2. Check file permissions: `ls -la .claude-code/hooks/`
3. Check shebang: `head -1 .claude-code/hooks/your-hook.sh`
4. Check for syntax errors: `bash -n .claude-code/hooks/your-hook.sh`

### Hook Running Too Often
Add conditions to make it more selective:
```bash
# Before: Runs for every file
if [[ "$CLAUDE_TOOL_NAME" == "Edit" ]]; then
    validate_everything
fi

# After: Only for YAML in config/
if [[ "$CLAUDE_TOOL_NAME" == "Edit" ]] && [[ "$CLAUDE_TOOL_ARGS" =~ config/.*\.yaml$ ]]; then
    validate_yaml
fi
```

### Hook Blocking Incorrectly
Change exit code to not block:
```bash
# Before: Blocks on any error
exit 1

# After: Warns but continues
echo "⚠️  Warning: validation failed"
exit 0
```

## Advanced Techniques

### Async Hooks
For long-running tasks:
```bash
#!/bin/bash
# Run expensive operation in background
(
    sleep 2
    run_expensive_validation
    notify-send "Validation complete"
) &

# Hook returns immediately
exit 0
```

### Conditional Blocking
```bash
#!/bin/bash
# Strict mode in production, relaxed in development
if [[ "$ENVIRONMENT" == "production" ]]; then
    # Block on any validation failure
    run_validation || exit 1
else
    # Warn but continue
    run_validation || echo "⚠️  Validation failed (development mode)"
fi
```

### Hook Chaining
```bash
#!/bin/bash
# Call another hook
.claude-code/hooks/format-code.sh
if [ $? -eq 0 ]; then
    .claude-code/hooks/validate-code.sh
fi
```

## Resources

- [Claude Code Hooks Documentation](https://docs.claude.com/claude-code/hooks)
- [Bash Best Practices](https://www.gnu.org/software/bash/manual/)
- Project hooks: See existing hooks in this directory for examples

## Quick Reference

### Hook Types
- `posttooluse` - After tool execution (validation, formatting)
- `pretooluse` - Before tool execution (blocking dangerous ops)
- `userpromptsub mit` - After user input (context processing)

### Common Variables
- `$CLAUDE_TOOL_NAME` - Which tool was used
- `$CLAUDE_TOOL_ARGS` - Tool arguments (often contains file path)
- `$PWD` - Current working directory

### Exit Codes
- `0` - Success, continue
- `1` - Error, block operation
- Other - Treated as error

### Testing
```bash
# Test hook syntax
bash -n hook.sh

# Run hook manually
./hook.sh

# Debug hook
bash -x hook.sh
```
