---
description: Visualize repository structure
---

Visualize the repository structure to understand the codebase organization.

## Method Selection

First, check if `tree` is available:

```bash
command -v tree >/dev/null 2>&1 && echo "✓ tree is installed" || echo "✗ tree not found - using fallback"
```

## Option A: Using tree (if available)

**Basic structure (3 levels):**
```bash
tree -L 3 -I 'venv|__pycache__|.git|*.pyc|.pytest_cache|*.egg-info' --dirsfirst
```

## Option B: Alternative using find (no tree required)

**Basic structure:**
```bash
find . -maxdepth 3 \
  -not -path '*/venv/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/.git/*' \
  -not -path '*/.pytest_cache/*' \
  -not -name '*.pyc' \
  -not -name '*.egg-info' \
  | sort | sed 's|^\./||' | sed 's|/[^/]*$|/|' | sort -u
```

**Or use a simpler hierarchical listing:**
```bash
# Top level
ls -d */ .[!.]* 2>/dev/null | grep -v -E "venv/|\.git/"

# Second level (example: config/)
ls -la config/ | head -20
```

## Explanation

Provide a brief explanation of the key directories and their purposes:

### Top-Level Structure
- **config/** - Home Assistant configuration files (synced with HA instance)
- **tools/** - Validation and testing scripts (Python)
- **agents/** - Multi-agent system for automation development
- **docs/** - Comprehensive documentation
- **.claude/** - Claude Code settings, commands, and hooks
- **venv/** - Python virtual environment (excluded from tree)
- **temp/** - Temporary directory for testing (if exists)

### Configuration Directory (config/)
- **automations.yaml** - Automation definitions
- **scripts.yaml** - Reusable scripts
- **scenes.yaml** - Scene definitions
- **configuration.yaml** - Main configuration
- **.storage/** - Entity registry and HA metadata (read-only)

### Tools Directory (tools/)
- **Validation scripts** - yaml_validator.py, reference_validator.py, ha_official_validator.py
- **Entity discovery** - entity_explorer.py
- **Tests** - tests/ directory with pytest suite

### Agents Directory (agents/)
- **orchestrator_agent.py** - Main agent coordinator
- **Specialized agents** - entity_discovery, automation_designer, validation, etc.

### Documentation Structure
- **CLAUDE.md** (root) - Main Claude Code guidance with cross-references
- **config/CLAUDE.md** - HA configuration guidelines
- **tools/CLAUDE.md** - Validator development with TDD
- **.claude/hooks/CLAUDE.md** - Hook patterns and testing
- **docs/AGENT_SYSTEM_GUIDE.md** - Complete agent system documentation

### Claude Code Configuration (.claude/)
- **commands/** - Custom slash commands
- **hooks/** - Validation hooks (pre/post tool use)
- **settings.json** - Project configuration and tool allowlist

## Advanced Options

### With tree (if available)

**Show more levels (5 levels deep):**
```bash
tree -L 5 -I 'venv|__pycache__|.git|*.pyc|.pytest_cache|*.egg-info' --dirsfirst
```

**Focus on specific directory (e.g., config/):**
```bash
tree config/ -L 3 -I '.storage|__pycache__' --dirsfirst
```

**Show hidden files and directories:**
```bash
tree -La 3 -I 'venv|__pycache__|.git|*.pyc|.pytest_cache|*.egg-info' --dirsfirst
```

**Show file sizes:**
```bash
tree -L 3 -h -I 'venv|__pycache__|.git|*.pyc|.pytest_cache|*.egg-info' --dirsfirst
```

### Without tree (fallback alternatives)

**Show more levels (5 levels deep):**
```bash
find . -maxdepth 5 -not -path '*/venv/*' -not -path '*/__pycache__/*' -not -path '*/.git/*' | sort
```

**Focus on specific directory (e.g., config/):**
```bash
find config/ -maxdepth 3 -not -path '*/.storage/*' | sort
```

**Show with file sizes:**
```bash
find . -maxdepth 3 -not -path '*/venv/*' -not -path '*/.git/*' -exec ls -lh {} \; 2>/dev/null | grep -v "^total"
```

## Installing tree (Optional)

If you want the enhanced visualization that `tree` provides, you can install it:

**macOS:**
```bash
brew install tree
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tree
```

**Windows (via Chocolatey):**
```bash
choco install tree
```

**Windows (via Scoop):**
```bash
scoop install tree
```

## Usage

Run `/tree` anytime you need to visualize the repository structure or explain organization to someone new to the codebase.

This is particularly useful:
- At the start of a session (after `/primer`)
- When explaining the codebase
- When looking for where to add new files
- When understanding project organization

**Note**: This command works with or without `tree` installed - it will automatically use fallback methods if needed.
