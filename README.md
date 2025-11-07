# Home Assistant Configuration Management with Claude Code

A comprehensive system for managing Home Assistant configurations with automated validation, testing, and deployment - all enhanced by Claude Code for natural language automation creation.

[![](https://github.com/user-attachments/assets/e4bb0179-a649-42d6-98f1-d8c29d5e84a3)](https://youtu.be/70VUzSw15-4)
Click to play

## 🌟 Features

### 🤖 Multi-Agent Development System (NEW!)
- **8 Specialized AI Agents**: Orchestrator + 7 specialized agents for complete automation lifecycle
- **Natural Language Automation**: Describe what you want, get production-ready YAML
- **Intelligent Entity Discovery**: Context-aware entity search with capability explanations
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

## 🤖 Multi-Agent System

This repository includes a comprehensive **8-agent system** that transforms Home Assistant automation development with intelligent, guided workflows.

### The Agent Team

**🎯 Orchestrator Agent** - Master coordinator managing all workflows and routing requests to specialized agents

**🔍 Entity Discovery Agent** - Context-aware entity search with natural language understanding
- Find entities by description: "motion sensors in the kitchen"
- Get entity capabilities and usage information
- Context-aware suggestions for triggers, conditions, and actions

**🏗️ Automation Designer Agent** - Converts natural language to production-ready YAML
- Describe automations in plain English
- Automatically discovers required entities
- Generates complete trigger/condition/action configurations

**✅ Validation Agent** - 3-layer validation with intelligent error parsing
- YAML syntax validation
- Entity reference validation
- Official Home Assistant validation
- Explains errors and suggests specific fixes

**🧪 Testing Agent** - Simulates automations before deployment
- Tests multiple scenarios
- Identifies edge cases
- Dry-run capabilities prevent surprises

**📚 Documentation Agent** - Auto-generates comprehensive documentation
- Markdown files for each automation
- Entity relationship maps
- Maintains changelogs automatically

**🎓 Best Practices Agent** - Enforces quality standards
- Security review (exposed secrets, unsafe templates)
- Performance analysis
- Naming convention enforcement
- Pattern recognition and anti-pattern detection

**⚡ Refactoring Agent** - Optimizes existing automations
- Detects duplicate logic
- Suggests script extraction
- Identifies consolidation opportunities

### Using the Agent System

#### Slash Commands (Easiest)

```bash
# Create a new automation with guided workflow
/create-automation

# Review all automations for issues and improvements
/review-automations

# Find entities for your automation
/find-entities motion sensors in the kitchen

# Debug a failing automation
/debug-automation
```

#### Programmatic Usage

```python
from agents.orchestrator import OrchestratorAgent
from agents.shared_context import SharedContext

# Initialize the system
context = SharedContext()
orchestrator = OrchestratorAgent(context)

# Create automation from natural language
result = orchestrator.run(
    workflow='create_automation',
    description="Turn on kitchen lights when motion detected after sunset"
)

if result.success:
    print(f"✅ {result.message}")
    automation = result.data['automation']

    # Review recommendations
    for rec in result.recommendations:
        print(f"[{rec['priority']}] {rec['description']}")
```

### Available Workflows

- **create_automation** - Complete creation workflow with entity discovery, design, validation, testing, and documentation
- **review_automations** - Comprehensive analysis of all automations with quality scoring and recommendations
- **debug_automation** - Systematic debugging with entity availability checks and specific fix suggestions
- **find_entities** - Natural language entity discovery with context-aware suggestions
- **validate_config** - Multi-layer validation with intelligent error resolution
- **document_automations** - Auto-generate markdown documentation and entity maps
- **refactor_automations** - Find optimization opportunities and duplicate patterns

### Example: Creating an Automation

```
User: /create-automation

System: What would you like your automation to do?

User: Turn on kitchen lights when motion is detected after sunset

System: 🤖 Creating automation...

Step 1: Finding entities...
  ✓ Found: binary_sensor.home_kitchen_motion
  ✓ Found: light.home_kitchen_ceiling
  ✓ Found: sun.sun

Step 2: Designing automation...
  ✓ Trigger: Motion detected in kitchen
  ✓ Condition: Sun below horizon
  ✓ Action: Turn on kitchen ceiling light

Step 3: Best practices review...
  ⚠️ Recommendation: Add timeout to prevent lights staying on indefinitely

Step 4: Validation...
  ✓ YAML syntax valid
  ✓ Entity references exist
  ✓ Official HA validation passed

Step 5: Testing scenarios...
  ✓ Motion at 2 PM → No action (sun above horizon)
  ✓ Motion at 9 PM → Lights turn on
  ⚠️ No auto-off mechanism detected

Step 6: Documentation generated...
  ✓ Created: docs/automations/lighting/kitchen_motion_lights.md

✅ Automation ready to deploy!

Recommendations:
  [high] Add timeout action to automatically turn off lights
  [medium] Consider brightness adjustment based on time of night
```

### Agent System Benefits

✅ **Faster Development** - Natural language to production automation in seconds
✅ **Higher Quality** - Best practices enforced automatically
✅ **Fewer Errors** - Multi-layer validation catches issues before deployment
✅ **Better Documentation** - Auto-generated docs stay synchronized
✅ **Easy Debugging** - Intelligent diagnosis with specific solutions
✅ **Continuous Improvement** - Refactoring suggestions optimize over time

### Documentation

- **[Complete Agent System Guide](docs/AGENT_SYSTEM_GUIDE.md)** - Comprehensive user guide with examples and workflows
- **[Project Instructions (CLAUDE.md)](CLAUDE.md)** - Detailed agent system documentation and API reference
- **Slash Command Guides** - See `.claude-code/commands/` for detailed usage instructions

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

### Automated Validation Hooks

Two hooks ensure configuration safety:

1. **Post-Edit Hook**: Runs validation after editing YAML files
2. **Pre-Push Hook**: Validates before syncing to HA (blocks if invalid)

### Entity Naming Convention

This system supports standardized entity naming:

**Format: `location_room_device_sensor`**

Examples:
```
binary_sensor.home_basement_motion_battery
media_player.office_kitchen_sonos
climate.home_living_room_heatpump
```

The agent system understands this convention and suggests entities accordingly.

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

## 🙏 Acknowledgments

- [Home Assistant](https://home-assistant.io) for the amazing platform
- [Claude Code](https://claude.ai) for AI-powered development
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
