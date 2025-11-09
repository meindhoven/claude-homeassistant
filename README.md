# Home Assistant Configuration Management with Claude Code

A comprehensive system for managing Home Assistant configurations with automated validation, testing, and deployment - all enhanced by Claude Code for natural language automation creation.

[![](https://github.com/user-attachments/assets/e4bb0179-a649-42d6-98f1-d8c29d5e84a3)](https://youtu.be/70VUzSw15-4)
Click to play

## 🌟 Features

### 🤖 Multi-Agent Development System (NEW!)
- **10 Specialized AI Agents**: Orchestrator + 9 specialized agents for complete HA development lifecycle
- **Natural Language Automation**: Describe what you want, get production-ready YAML
- **Intelligent Entity Discovery**: Context-aware entity search with capability explanations
- **Dashboard Design**: Create user-friendly dashboards with UX/accessibility best practices
- **Automated Testing**: Simulate scenarios before deployment to catch edge cases
- **Auto-Documentation**: Generates markdown docs, entity maps, and changelogs
- **Best Practices Enforcement**: Security, performance, and pattern analysis
- **Intelligent Debugging**: Systematic diagnosis with specific fix suggestions
- **Refactoring Analysis**: Detects duplicates, suggests optimizations

### 🛡️ Core Safety Features
- **Multi-Layer Validation**: YAML syntax, entity references, official HA validation
- **Pre-Deployment Testing**: Test automations before pushing to HA
- **Safe Deployments**: Pre-push validation blocks invalid configs
- **Automated Hooks**: Validation runs automatically on file changes
- **Entity Registry Integration**: Real-time validation against your actual HA setup
### Claude Code Integration (Enhanced)
- **⚡ Custom Slash Commands**: 10 workflow commands for common tasks (`/validate-config`, `/create-automation`, `/safe-deploy`)
- **🤖 AI-Powered Automation Creation**: Write automations in plain English with guided entity discovery
- **📚 Comprehensive Documentation**: Best practices, workflow patterns, and context-specific guides
- **🔌 MCP Server Support**: Optional direct Home Assistant API integration for real-time queries
- **📖 Multi-Level Documentation**: Context-specific CLAUDE.md files in tools/, config/, and hooks/

### Validation & Safety
- **🛡️ Multi-Layer Validation**: YAML syntax, entity references, and official HA validation
- **🔄 Safe Deployments**: Pre-push validation blocks invalid configs from reaching HA
- **⚡ Automated Hooks**: Validation runs automatically on file changes
- **📊 Entity Registry Integration**: Real-time validation against your actual HA setup

### Developer Experience
- **🔍 Entity Discovery**: Advanced tools to explore and search available entities
- **🎨 Code Quality**: Automated formatting and linting for Python validators
- **📝 Workflow Patterns**: TDD, Explore→Plan→Code→Commit, and more
- **🔧 Context Management**: Guidelines for efficient Claude Code sessions

## 🚀 Quick Start

This repository provides a complete framework for managing Home Assistant configurations with Claude Code. Here's how it works:

### Repository Structure
- **Template Configs**: The `config/` folder contains sanitized example configurations (no secrets)
- **Validation Tools**: The `tools/` folder has all validation scripts
- **Management Commands**: The `Makefile` contains pull/push commands
- **Development Setup**: `pyproject.toml` and other dev files for tooling

### User Workflow

#### 1. Clone Repository
```bash
git clone git@github.com:philippb/claude-homeassistant.git
cd claude-homeassistant
make setup  # Creates Python venv and installs dependencies
```

#### 2. Configure Connection
Copy the example environment file and configure your settings:
```bash
cp .env.example .env
# Edit .env with your actual Home Assistant details
```

The `.env` file should contain:
```bash
# Home Assistant Configuration
HA_TOKEN=your_home_assistant_token
HA_URL=http://your_homeassistant_host:8123

# SSH Configuration for rsync operations
HA_HOST=your_homeassistant_host
HA_REMOTE_PATH=/config/

# Local Configuration (optional - defaults provided)
LOCAL_CONFIG_PATH=config/
BACKUP_DIR=backups
VENV_PATH=venv
TOOLS_PATH=tools
```

Set up SSH access to your Home Assistant instance.

**Recommended**: Install the [Advanced SSH & Web Terminal](https://github.com/hassio-addons/addon-ssh) add-on for Home Assistant, which provides excellent SSH/SFTP access needed for the rsync operations in this project.

#### 3. Pull Your Real Configuration
```bash
make pull  # Downloads YOUR actual HA config, overwriting template files
```

**Important**: This step replaces the template `config/` folder with your real Home Assistant configuration files.

#### 4. Work with Your Configuration
- Edit your real configs locally with full validation
- Use Claude Code to create automations in natural language
- Validation hooks automatically check syntax and entity references

#### 5. Push Changes Back
```bash
make push  # Uploads changes back to your HA instance (with validation)
```

### How It Works

1. **Template Start**: You begin with example configs showing proper structure
2. **Real Data**: First `make pull` overwrites templates with your actual HA setup
3. **Local Development**: Edit real configs locally with validation safety
4. **Safe Deployment**: `make push` validates before uploading to prevent broken configs

This gives you a complete development environment while only modifying your HA instance when completed.

---

## 🤖 Multi-Agent System (NEW!)

This repository includes a comprehensive **10-agent system** that transforms Home Assistant automation development with AI-powered, guided workflows.

### What It Does

- **Natural Language Automation**: Describe what you want in plain English, get production-ready YAML
- **Intelligent Entity Discovery**: "Find motion sensors in the kitchen" - understands context
- **Automated Testing**: Simulates scenarios before deployment to catch edge cases
- **Auto-Documentation**: Generates markdown docs, entity maps, and changelogs
- **Best Practices Enforcement**: Security, performance, and pattern analysis built-in
- **Dashboard Design**: Creates user-friendly dashboards with UX/accessibility best practices

### Quick Start with Agents

Use slash commands for guided workflows:

```bash
/create-automation        # Complete workflow: discovery → design → validate → test → document
/find-entities motion sensors in the kitchen
/review-automations       # Analyze all automations for improvements
/debug-automation         # Systematic debugging with specific fixes
/design-dashboard         # Create accessible, user-friendly dashboards
```

### Example Workflow

```
User: /create-automation "Turn on kitchen lights when motion detected after sunset"

System:
  Step 1: Finding entities... ✓ Found 3 relevant entities
  Step 2: Designing automation... ✓ Created YAML configuration
  Step 3: Best practices review... ⚠️ Add timeout to prevent lights staying on
  Step 4: Validation... ✓ All checks passed
  Step 5: Testing... ✓ Tested 2 scenarios, identified 1 edge case
  Step 6: Documentation... ✓ Generated docs/automations/lighting/kitchen_motion_lights.md

✅ Automation ready! Recommendations: [high] Add auto-off timeout
```

### Complete Agent Documentation

**📖 [Complete Agent System Guide](docs/AGENT_SYSTEM_GUIDE.md)** - Full user guide with:
- All 10 agents and their capabilities
- Available workflows and API reference
- Examples and best practices
- Troubleshooting guide

---

## ⚙️ Prerequisites

### Make Command

This project uses `make` commands for configuration management. If you don't have `make` installed:

**macOS:**
```bash
xcode-select --install  # Installs Command Line Tools including make
```

**Windows:**
- **Option 1**: Use WSL (Windows Subsystem for Linux) - recommended
- **Option 2**: Install via Chocolatey: `choco install make`
- **Option 3**: Use Git Bash (includes make)
- **Option 4**: Install MinGW-w64

**Alternative**: If you can't install `make`, you can run the underlying commands directly by checking the `Makefile` for the actual command syntax.

## 📁 Project Structure

```
├── agents/                # Multi-agent system (NEW!)
│   ├── base_agent.py     # Abstract base class for all agents
│   ├── shared_context.py # Centralized state management
│   ├── orchestrator.py   # Master coordinator
│   ├── creation/         # Entity Discovery & Automation Designer
│   ├── validation/       # Validation & Testing agents
│   ├── analysis/         # Best Practices & Refactoring
│   └── documentation/    # Documentation generation
├── docs/                 # Generated documentation (NEW!)
│   ├── AGENT_SYSTEM_GUIDE.md  # Complete agent system guide
│   ├── automations/      # Per-automation documentation
│   │   ├── lighting/
│   │   ├── climate/
│   │   └── security/
│   └── entities/         # Entity relationship maps
├── config/               # Home Assistant configuration files
│   ├── configuration.yaml
│   ├── automations.yaml
│   ├── scripts.yaml
│   └── .storage/        # Entity registry (pulled from HA)
├── tools/               # Validation scripts
│   ├── run_tests.py     # Main test suite runner
│   ├── yaml_validator.py  # YAML syntax validation
│   ├── reference_validator.py # Entity reference validation
│   ├── ha_official_validator.py # Official HA validation
│   └── entity_explorer.py # Entity discovery tool
├── .claude-code/        # Claude Code project settings
│   ├── commands/        # Slash commands for agents (NEW!)
│   │   ├── create-automation.md
│   │   ├── review-automations.md
│   │   ├── find-entities.md
│   │   └── debug-automation.md
│   ├── hooks/           # Automated validation hooks
│   └── settings.json    # Project configuration
├── tests/               # Agent system tests (NEW!)
│   └── test_agent_system.py
├── .env.example         # Environment configuration template
├── venv/                # Python virtual environment
├── Makefile             # Management commands
└── CLAUDE.md            # Claude Code instructions + agent docs
```

## 🛠️ Available Commands

### Agent System Commands (NEW!)
```bash
# Use natural language to work with automations
/create-automation              # Create new automation with guided workflow
/review-automations            # Comprehensive analysis of all automations
/find-entities <query>         # Natural language entity search
/debug-automation              # Debug failing automations

# Example entity searches
/find-entities motion sensors in the kitchen
/find-entities climate controls at the office
/find-entities all battery sensors
```

### Configuration Management
```bash
make pull      # Pull latest config from Home Assistant
make push      # Push local config to HA (with validation)
make backup    # Create timestamped backup
make validate  # Run all validation tests
```

### Entity Discovery
```bash
make entities                           # Show entity summary
make entities ARGS='--domain climate'   # Climate entities only
make entities ARGS='--search motion'    # Search for motion sensors
make entities ARGS='--area kitchen'     # Kitchen entities only
make entities ARGS='--full'            # Complete detailed output
```

### Individual Validators
```bash
. venv/bin/activate
python tools/yaml_validator.py         # YAML syntax only
python tools/reference_validator.py    # Entity references only
python tools/ha_official_validator.py  # Official HA validation
```

## 🔧 Validation System

The system provides three layers of validation:

### 1. YAML Syntax Validation
- Validates YAML syntax with HA-specific tags (`!include`, `!secret`, `!input`)
- Checks file encoding (UTF-8 required)
- Validates basic HA file structures

### 2. Entity Reference Validation
- Verifies all entity references exist in your HA instance
- Checks device and area references
- Warns about disabled entities
- Extracts entities from Jinja2 templates

### 3. Official HA Validation
- Uses Home Assistant's own validation tools
- Most comprehensive check available
- Catches integration-specific issues

## 🤖 Claude Code Integration

### Multi-Agent Automation Development

The agent system provides a complete development workflow:

**Simple Usage - Slash Commands:**
```bash
/create-automation
# Describe: "Turn off all lights at midnight on weekdays"
# System: Creates, validates, tests, and documents the automation
```

**Complete Workflow Includes:**
1. **Entity Discovery** - Finds all relevant lights automatically
2. **Automation Design** - Generates production-ready YAML
3. **Best Practices Review** - Checks security and performance
4. **Validation** - 3-layer validation ensures correctness
5. **Testing** - Simulates scenarios before deployment
6. **Documentation** - Auto-generates markdown documentation

**Result:**
```yaml
- id: weekday_midnight_lights_off
  alias: "Weekday Midnight Lights Off"
  description: "Turn off all lights at midnight on weekdays"
  trigger:
    - platform: time
      at: "00:00:00"
  condition:
    - condition: time
      weekday: [mon, tue, wed, thu, fri]
  action:
    - service: light.turn_off
      target:
        entity_id: all
  mode: single
```

**Plus:** Recommendations for improvements, edge case warnings, and comprehensive documentation
This project implements [Anthropic's Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) for optimal AI-assisted development.

### Slash Commands (Quick Actions)

Use natural language commands for common workflows:

```bash
# AI-Powered Workflows (Agent System)
/create-automation    # Guided automation creation with entity discovery, validation, and testing
/find-entities        # Natural language entity search ("motion sensors in kitchen")
/review-automations   # Comprehensive analysis of all automations
/debug-automation     # Systematic debugging with specific fix suggestions
/design-dashboard     # Create user-friendly dashboards with UX best practices

# Configuration Management
/validate-config      # Run complete validation suite (YAML + entities + official HA)
/safe-deploy         # Validate, backup, and push to Home Assistant (safest method)
/pull-latest         # Sync latest config from Home Assistant instance
/backup-config       # Create timestamped backup

# Utilities
/fix-yaml            # Auto-fix YAML formatting issues
/troubleshoot        # Diagnose configuration issues with step-by-step guidance
```

Simply type a slash command in Claude Code chat to start the workflow.

### Workflow Patterns

**Explore → Plan → Code → Commit** (Recommended):
1. **Explore**: Use `/find-entities` to discover available devices
2. **Plan**: Break down into steps, identify edge cases
3. **Code**: Implement with validation hooks catching errors
4. **Commit**: Save with clear, descriptive messages

**Test-Driven Development** (For validators):
1. Write tests first based on expected behavior
2. Verify tests fail (red)
3. Implement feature iteratively
4. Tests pass (green)
5. Refactor and commit

See `CLAUDE.md` for complete workflow documentation.

### MCP Server Integration (Optional but Recommended)

Enable direct Home Assistant API access during Claude sessions using **hass-mcp**.

**Quick Setup:**
```bash
# 1. Copy the template
cp .mcp.json.example .mcp.json

# 2. Edit .mcp.json with your HA URL and long-lived access token
# Replace: "http://your_homeassistant_host:8123"
# Replace: "your_long_lived_access_token_here"

# 3. Restart Claude Code
```

**Template (.mcp.json.example):**
```json
{
  "mcpServers": {
    "homeassistant": {
      "command": "uvx",
      "args": ["hass-mcp"],
      "env": {
        "HA_URL": "http://your_homeassistant_host:8123",
        "HA_TOKEN": "your_long_lived_access_token_here"
      },
      "disabled": false
    }
  }
}
```

**Benefits**:
- Query entity states in real-time (is sensor responding?)
- Call HA services directly for testing automations
- Validate entities against live instance
- Debug automations with current state ("why isn't this triggering?")
- Check battery levels and sensor health
- Verify entities are online before deploying

**Security**: `.mcp.json` is in `.gitignore` and never committed.

See `CLAUDE.md` → "MCP Server Configuration" for detailed setup instructions.

### Automated Validation Hooks

Four hooks ensure code quality and configuration safety:

1. **Post-Edit HA Validation**: Runs after editing YAML files in `config/`
2. **Post-Edit Python Quality**: Formats and lints Python code in `tools/`
3. **YAML Formatter**: Auto-formats YAML files
4. **Pre-Push Validation**: Blocks invalid configs from being pushed (critical!)

### Context-Specific Documentation

Claude automatically loads relevant documentation when working in specific directories:

- **`tools/CLAUDE.md`** - Validator development guide (TDD, patterns, debugging)
- **`config/CLAUDE.md`** - HA configuration best practices (syntax, patterns, examples)
- **`.claude-code/hooks/CLAUDE.md`** - Hook development guide (patterns, testing)

### Entity Naming Convention

Standardized naming for multi-location deployments:

**Format: `location_room_device_sensor`**

Examples:
```
binary_sensor.home_basement_motion_battery
media_player.office_kitchen_sonos
climate.home_living_room_heatpump
```

The agent system understands this convention and suggests entities accordingly.
### Natural Language Automation Creation

**Example workflow**:

```
User: "Turn off all lights at midnight on weekdays"

Claude:
1. Uses /find-entities to find light entities
2. Asks for clarification on which lights
3. Generates YAML automation:
```

```yaml
- id: weekday_midnight_lights_off
  alias: "Weekday Midnight Lights Off"
  description: "Turn off all lights at midnight on weekdays"
  mode: single
  trigger:
    - platform: time
      at: "00:00:00"
  condition:
    - condition: time
      weekday: [mon, tue, wed, thu, fri]
  action:
    - service: light.turn_off
      target:
        entity_id: all
```

```
4. Validates configuration automatically
5. Ready to deploy with /safe-deploy
```

## 📊 Entity Discovery

The entity explorer helps you understand what's available:

```bash
# Find all motion sensors
. venv/bin/activate && python tools/entity_explorer.py --search motion

# Show all climate controls
. venv/bin/activate && python tools/entity_explorer.py --domain climate

# Kitchen devices only
. venv/bin/activate && python tools/entity_explorer.py --area kitchen
```

## 🔒 Security & Best Practices

- **Secrets Management**: `secrets.yaml` is excluded from validation
- **SSH Authentication**: Uses SSH keys for secure HA access
- **No Credentials Stored**: Repository contains no sensitive data
- **Pre-Push Validation**: Prevents broken configs from reaching HA
- **Backup System**: Automatic timestamped backups before changes

## 🐛 Troubleshooting

### Validation Errors
1. Check YAML syntax first: `. venv/bin/activate && python tools/yaml_validator.py`
2. Verify entity references: `. venv/bin/activate && python tools/reference_validator.py`
3. Check HA logs if official validation fails

### SSH Connection Issues
1. Test connection: `ssh your_homeassistant_host`
2. Check SSH key permissions: `chmod 600 ~/.ssh/your_key`
3. Verify SSH config in `~/.ssh/config`

### Missing Dependencies
```bash
. venv/bin/activate
pip install homeassistant voluptuous pyyaml jsonschema requests
```

## 🔧 Configuration

### Environment Variables
Configure via `.env` file in project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Available variables:
```bash
# Home Assistant Configuration
HA_TOKEN=your_home_assistant_token       # HA API token
HA_URL=http://your_homeassistant_host:8123  # HA instance URL

# SSH Configuration for rsync operations
HA_HOST=your_homeassistant_host          # SSH hostname for HA
HA_REMOTE_PATH=/config/                  # Remote config path

# Local Configuration (optional - defaults provided)
LOCAL_CONFIG_PATH=config/                # Local config directory
BACKUP_DIR=backups                       # Backup directory
VENV_PATH=venv                          # Python virtual environment path
TOOLS_PATH=tools                        # Tools directory
```

### Claude Code Settings
Located in `.claude-code/settings.json`:
```json
{
  "hooks": {
    "enabled": true,
    "posttooluse": [".claude-code/hooks/posttooluse-ha-validation.sh"],
    "pretooluse": [".claude-code/hooks/pretooluse-ha-push-validation.sh"]
  },
  "validation": {
    "enabled": true,
    "auto_run": true,
    "block_invalid_push": true
  }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all validations pass
5. Submit a pull request

## 📄 License

Apache 2.0

## 📖 Best Practices for Claude Code

This project implements Anthropic's recommended best practices. See `CLAUDE.md` for comprehensive documentation.

### Quick Tips

**✅ DO:**
- Use slash commands for common workflows (`/create-automation`, `/validate-config`)
- Explore entities before writing automations (`/find-entities`)
- Be specific in instructions (edge cases, success criteria, constraints)
- Use `/clear` between unrelated tasks to manage context
- Commit frequently with descriptive messages
- Follow the Explore → Plan → Code → Commit pattern

**❌ DON'T:**
- Give vague instructions like "fix the automation" or "make it better"
- Skip validation before deploying
- Edit files without understanding the naming convention
- Let Claude Code sessions become unfocused (use `/clear`)
- Push configurations without testing

### Workflow Examples

**Creating an automation**:
```
1. /find-entities motion          # Find available motion sensors
2. /find-entities light           # Find lights to control
3. /create-automation             # Guided automation creation
4. /validate-config               # Ensure correctness
5. git add + commit               # Save work
6. /safe-deploy                   # Deploy to HA safely
```

**Developing a new validator**:
```
1. Write tests first (TDD approach)
2. Run pytest - verify tests fail
3. Implement validator
4. Iterate until tests pass
5. Python quality hooks run automatically
6. Commit with clear message
```

### Documentation Structure

- **`README.md`** (this file) - Quick start and overview
- **`CLAUDE.md`** - Complete Claude Code guide (workflows, MCP, best practices)
- **`tools/CLAUDE.md`** - Validator development guide
- **`config/CLAUDE.md`** - HA configuration reference
- **`.claude-code/hooks/CLAUDE.md`** - Hook development guide

## 🙏 Acknowledgments

- [Home Assistant](https://home-assistant.io) for the amazing platform
- [Claude Code](https://claude.ai) and [Anthropic](https://www.anthropic.com/) for AI-powered development
- [Anthropic's Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) for workflow guidance
- The HA community for validation best practices

---

## 🎯 Getting Started with Agents

1. **Clone and Setup** - Follow the Quick Start instructions above
2. **Pull Your Config** - Run `make pull` to sync your HA configuration
3. **Try the Agent System** - Use `/create-automation` to create your first automation
4. **Explore** - Use `/find-entities` to discover what's available
5. **Review** - Run `/review-automations` to analyze your existing setup
6. **Learn More** - Read the [Complete Agent System Guide](docs/AGENT_SYSTEM_GUIDE.md)

## 📚 Additional Resources

- **[Agent System Guide](docs/AGENT_SYSTEM_GUIDE.md)** - Comprehensive user guide with examples
- **[CLAUDE.md](CLAUDE.md)** - Complete project instructions and agent documentation
- **[Slash Command Guides](.claude-code/commands/)** - Detailed usage for each command

---

**Ready to revolutionize your Home Assistant automation workflow?** Start by describing what you want in plain English and let the agent system handle the rest - from design to testing to documentation! 🚀🤖
**Ready to revolutionize your Home Assistant automation workflow?**

1. Clone this repository
2. Configure your `.env` file
3. Pull your HA config with `make pull`
4. Type `/create-automation` in Claude Code
5. Describe your automation in plain English

Let Claude Code handle the rest! 🚀
