---
description: Comprehensive repository analysis to prime Claude on the codebase
---

Perform a comprehensive analysis of this Home Assistant configuration repository following a **macro-to-micro approach**. This helps establish mental models before diving into specific implementations.

## Analysis Workflow

### 1. Structure Overview
Run `tree -L 2 -I 'venv|__pycache__|.git'` to visualize the project organization.

Identify:
- Top-level directories and their purposes
- Configuration file locations
- Tool and agent locations
- Documentation structure

### 2. Documentation Review
Read the following files in order to establish foundational context:

1. **README.md** - Quick start and project overview
2. **CLAUDE.md** - Claude Code-specific guidance (root)
3. **docs/AGENT_SYSTEM_GUIDE.md** - Complete agent system documentation
4. **config/CLAUDE.md** - Home Assistant configuration guidelines
5. **tools/CLAUDE.md** - Validation tool development
6. **.claude-code/hooks/CLAUDE.md** - Hook patterns and testing

### 3. Entity Registry Analysis
Read **config/.storage/core.entity_registry** to understand:
- Available entities (sensors, lights, climate, etc.)
- Entity naming conventions (e.g., `sensor.home_{area}_{device}_{measurement}`)
- Disabled entities
- Device relationships

### 4. Key Configuration Files
Read these core files to understand the automation system:

1. **config/configuration.yaml** - Main configuration and integrations
2. **config/automations.yaml** - Automation definitions
3. **config/scripts.yaml** - Reusable scripts
4. **config/scenes.yaml** - Scene definitions (if exists)

### 5. Validation System
Review the **tools/** directory structure:

- `yaml_validator.py` - YAML syntax validation
- `reference_validator.py` - Entity/device reference validation
- `ha_official_validator.py` - Official HA validation
- `entity_explorer.py` - Entity discovery tool

Understand the validation pipeline and how hooks trigger it.

### 6. Agent System
Review the **agents/** directory:

- `orchestrator_agent.py` - Main agent coordinator
- Specialized agents (entity_discovery, automation_designer, validation, etc.)
- How agents interact with MCP for live state

### 7. MCP Configuration (if exists)
Check if **.mcp.json** exists (user's personal config):
- MCP server configuration (hass-mcp)
- When to use MCP vs files
- Available MCP tools

## Expected Output

Provide a comprehensive explanation covering:

### Project Structure
- How files and directories organize the codebase
- Separation of concerns (config vs tools vs agents vs documentation)
- Where different types of files live

### Project Purpose
- What problems this repository solves
- Key objectives (safe deployments, validation, automation development)
- How it integrates with Home Assistant

### Key Functionality
- Which specific files drive functionality and their roles
- How validation works (YAML → entities → official HA)
- How the agent system assists automation creation
- How MCP integration provides live state access

### Dependencies
- External libraries (homeassistant, voluptuous, pyyaml)
- Home Assistant instance (SSH access, API access)
- MCP servers (hass-mcp)
- Validation tools and hooks

### Setup and Configuration
- Virtual environment setup (venv/)
- SSH configuration for pull/push
- MCP configuration (.mcp.json)
- Git workflow and hooks

### Development Patterns
- Entity naming conventions
- Multi-file workflow patterns
- TDD for validators
- Agent-assisted automation creation
- When to use MCP vs entity registry files

## Success Criteria

After running this primer, you should be able to:
- Navigate the repository confidently
- Understand the validation pipeline
- Know where to find specific types of information
- Use the agent system effectively
- Follow established patterns for new automations
- Understand when to use MCP vs files

## Usage

Simply run `/primer` at the start of a new session to quickly establish comprehensive context about this Home Assistant configuration repository.
