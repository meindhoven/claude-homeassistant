---
description: Visualize repository structure with tree command
---

Visualize the repository structure to understand the codebase organization.

## Basic Structure (3 levels)

Run the following command to show the repository structure:

```bash
tree -L 3 -I 'venv|__pycache__|.git|*.pyc|.pytest_cache|*.egg-info' --dirsfirst
```

## Explanation

Provide a brief explanation of the key directories and their purposes:

### Top-Level Structure
- **config/** - Home Assistant configuration files (synced with HA instance)
- **tools/** - Validation and testing scripts (Python)
- **agents/** - Multi-agent system for automation development
- **docs/** - Comprehensive documentation
- **.claude-code/** - Claude Code settings, commands, and hooks
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
- **.claude-code/hooks/CLAUDE.md** - Hook patterns and testing
- **docs/AGENT_SYSTEM_GUIDE.md** - Complete agent system documentation

### Claude Code Configuration (.claude-code/)
- **commands/** - Custom slash commands
- **hooks/** - Validation hooks (pre/post tool use)
- **settings.json** - Project configuration and tool allowlist

## Advanced Options

If you need more detail in specific areas:

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

## Usage

Run `/tree` anytime you need to visualize the repository structure or explain organization to someone new to the codebase.

This is particularly useful:
- At the start of a session (after `/primer`)
- When explaining the codebase
- When looking for where to add new files
- When understanding project organization
