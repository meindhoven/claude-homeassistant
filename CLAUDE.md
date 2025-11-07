# Home Assistant Configuration Management

This repository manages Home Assistant configuration files with automated validation, testing, and deployment.

## Slash Commands (Quick Actions)

Use these slash commands for common workflows:

### Core Workflows
- `/validate-config` - Run complete validation suite
- `/create-automation` - Guided automation creation with entity discovery
- `/explore-entities` - Interactive entity discovery and search
- `/safe-deploy` - Validate, backup, and push to Home Assistant
- `/pull-latest` - Sync latest config from Home Assistant

### Utilities
- `/backup-config` - Create timestamped backup
- `/fix-yaml` - Auto-fix YAML formatting issues
- `/review-automation` - Analyze and improve existing automation
- `/troubleshoot` - Diagnose configuration issues
- `/entity-search` - Quick entity lookup with filters

Simply type the slash command (e.g., `/validate-config`) to start the workflow.

## Best Practices for Working with Claude Code

### Recommended Workflow Patterns

#### 1. Explore → Plan → Code → Commit

The most effective workflow for feature development:

1. **Explore**: Research the codebase first
   - Use `/explore-entities` to discover available devices
   - Read relevant configuration files
   - Check existing automations for patterns
   - Search for similar implementations

2. **Plan**: Create a detailed plan before coding
   - Use extended thinking modes ("think hard" for complex tasks)
   - Break down into smaller, manageable steps
   - Identify potential issues early
   - Document assumptions and decisions

3. **Code**: Implement systematically
   - Follow one step at a time
   - Use validation hooks to catch errors immediately
   - Test incrementally rather than all at once
   - Follow naming conventions and best practices

4. **Commit**: Save work with context
   - Write clear, descriptive commit messages
   - Explain the "why" not just the "what"
   - Commit logical units of work
   - Push to remote when ready

**Example:**
```
User: "Add automation to turn off all lights when I leave"

1. EXPLORE:
   /entity-search             # Find person/device_tracker entities
   /entity-search             # Find all light entities
   Read config/automations.yaml  # Check existing patterns

2. PLAN:
   - Trigger: person.home changes to "away"
   - Condition: None (always run when leaving)
   - Action: Turn off all lights by area
   - Consider: What if multiple people? Need to check all person states

3. CODE:
   /create-automation         # Use guided workflow
   /validate-config          # Ensure it's correct

4. COMMIT:
   git add + commit with clear message about the automation's purpose
```

#### 2. Test-Driven Development (TDD)

For validation tools and Python scripts:

1. **Write tests first** based on expected inputs/outputs
   ```bash
   # Example: Adding new validator feature
   1. Write test cases in tests/test_new_validator.py
   2. Run pytest - verify tests fail (red)
   3. Commit failing tests
   4. Implement feature
   5. Run pytest iteratively until passing (green)
   6. Refactor if needed
   7. Commit working implementation
   ```

2. **Verify tests fail first**: Ensures tests are actually testing something
3. **Commit tests separately**: Makes review easier
4. **Iterate until green**: Small incremental changes
5. **Use subagents for verification**: Get objective review of implementation

**Benefits:**
- Catches edge cases early
- Documents expected behavior
- Prevents regression
- Makes refactoring safer

#### 3. Visual Iteration (for dashboards/UI)

For Home Assistant dashboard/Lovelace configurations:

1. **Provide design mock** or describe desired layout
2. **Implement UI code** in Lovelace YAML
3. **Take screenshot** of result (if possible)
4. **Iterate 2-3 times** for quality improvements
5. **Commit** final version

### Instruction Specificity

**Vague instructions lead to suboptimal results.** Be specific about requirements, constraints, and edge cases.

#### ❌ Vague Instructions (Avoid)

```
"Add tests for the validator"
"Fix the automation"
"Make it better"
"Update the script"
```

#### ✅ Specific Instructions (Use These)

```
"Write pytest tests for reference_validator.py covering:
 - Valid entity references (should pass)
 - Missing entities (should error with entity_id in message)
 - Disabled entities (should warn, not error)
 - Jinja2 template extraction (test {{ states.light.kitchen }} pattern)
 - Avoid mocking the entity registry - use test fixtures"

"Fix the 'lights off at midnight' automation to:
 - Only run on weekdays (Mon-Fri)
 - Exclude bedroom lights (people might be reading)
 - Add a 30-second delay between turning off each room
 - Send notification when complete"

"Optimize the entity_explorer.py script:
 - Add caching for entity registry (currently reads on every search)
 - Implement fuzzy matching for entity names
 - Sort results by relevance score, not alphabetically
 - Target: Search should complete in <100ms for 500+ entities"
```

**Guidelines:**
- Specify **edge cases** to handle
- Define **success criteria** clearly
- Mention **constraints** (performance, compatibility, style)
- State what to **avoid** (mocking, certain patterns, etc.)
- Provide **examples** when helpful

### Context Management

Long sessions can accumulate irrelevant context. Manage it actively:

#### When to Use `/clear`

- ✅ After completing a major feature
- ✅ When switching to unrelated task
- ✅ If responses become unfocused or repetitive
- ✅ Before starting a new automation project
- ✅ After resolving a complex debugging session

#### Keeping Context Focused

1. **Use GitHub Issues**: For multi-step projects, track in issues rather than long conversations
2. **Use TODO lists**: Break complex tasks into trackable items
3. **Session planning**: Start sessions with clear goals
4. **Regular commits**: Commit frequently to externalize progress

#### Example Context Management

```
# Good session flow:
/create-automation → work on automation → /validate-config → commit → /clear
/create-automation → work on new automation → /validate-config → commit → /clear

# Instead of:
/create-automation → automation 1 → automation 2 → automation 3 → troubleshoot
→ fix issues → add features → debug more → ... (long unfocused session)
```

### Multi-Claude Workflows (Advanced)

For complex projects, consider running multiple Claude instances:

1. **Parallel Development**:
   - Instance 1: Writes automation
   - Instance 2: Reviews code quality
   - Use git worktrees for independent work

2. **Test Verification**:
   - Instance 1: Implements feature
   - Instance 2: Verifies implementation isn't overfitting to tests

3. **Simultaneous Tasks**:
   - Instance 1: Working on automations
   - Instance 2: Updating documentation
   - Instance 3: Refactoring validators

**Setup**: Use separate terminal windows or tmux panes, each with its own Claude Code session.

## MCP Server Configuration

### What is MCP?

**Model Context Protocol (MCP)** is a protocol that allows Claude to communicate directly with external services during sessions. For Home Assistant, this enables:

- ✅ **Real-time entity queries**: Check current state of devices without parsing files
- ✅ **Service calls**: Test automations by calling HA services directly
- ✅ **Live validation**: Verify entities exist against running HA instance
- ✅ **State inspection**: Debug automations with live state data
- ✅ **Direct API access**: Full Home Assistant API available to Claude

### Available Options

#### Option 1: Official Home Assistant MCP (HA 2025.2+)

Home Assistant 2025.2+ includes built-in MCP server support:
- Exposed at `/api/mcp` endpoint
- OAuth authentication support
- Access control via exposed entities page
- Full Assist API integration

**Setup:**
1. Ensure Home Assistant 2025.2 or later
2. Enable "Model Context Protocol Server" integration
3. Configure exposed entities for Claude access
4. Use your HA URL + `/api/mcp` as endpoint

#### Option 2: Community MCP Servers

Several community implementations available:

**allenporter/mcp-server-home-assistant** (Recommended)
- Full WebSocket API support
- Entity state queries and service calls
- Active development and maintenance
- Install: `uvx mcp-server-home-assistant`

**Other options:**
- `tevonsb/homeassistant-mcp` - Alternative implementation
- `voska/hass-mcp` - Docker-focused approach

### Configuration

The `.mcp.json` file in the project root provides two pre-configured servers (both disabled by default):

```json
{
  "mcpServers": {
    "homeassistant": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-homeassistant"],
      "env": {
        "HOME_ASSISTANT_URL": "${HA_URL}",
        "HOME_ASSISTANT_TOKEN": "${HA_TOKEN}"
      },
      "disabled": true
    },
    "homeassistant-community": {
      "command": "uvx",
      "args": ["mcp-server-home-assistant", "-v"],
      "env": {
        "HOME_ASSISTANT_WEB_SOCKET_URL": "${HA_URL}/api/websocket",
        "HOME_ASSISTANT_API_TOKEN": "${HA_TOKEN}"
      },
      "disabled": true
    }
  }
}
```

### Setup Instructions

1. **Ensure Prerequisites:**
   ```bash
   # For npx-based server (Option 1):
   npm --version  # Requires Node.js

   # For uvx-based server (Option 2):
   pip install uv  # Or: curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Configure Environment:**
   Your `.env` file already contains the required variables:
   ```bash
   HA_TOKEN=your_home_assistant_long_lived_access_token
   HA_URL=http://your_homeassistant_host:8123
   ```

3. **Generate Token (if not done):**
   - Go to Home Assistant → Profile → Security
   - Scroll to "Long-Lived Access Tokens"
   - Click "Create Token"
   - Copy token to `.env` file as `HA_TOKEN`

4. **Enable MCP Server:**
   Edit `.mcp.json` and change `"disabled": true` to `"disabled": false` for your chosen server.

5. **Restart Claude Code:**
   Close and reopen Claude Code for MCP configuration to take effect.

6. **Verify Connection:**
   Ask Claude to query an entity:
   ```
   "What's the current state of my living room lights?"
   ```

### Usage Examples

Once configured, you can interact with Home Assistant directly:

**Query Entity States:**
```
User: What's the temperature in the office?
Claude: [Queries sensor.office_living_room_temperature via MCP]
        The office is currently 72°F.
```

**Test Services:**
```
User: Turn on the kitchen lights to 50% brightness
Claude: [Calls light.turn_on service via MCP]
        Kitchen lights set to 50% brightness.
```

**Validate Automations:**
```
User: Check if binary_sensor.home_basement_motion exists
Claude: [Queries entity registry via MCP]
        Yes, that entity exists and is currently "off".
```

**Debug Automations:**
```
User: Why isn't my automation triggering?
Claude: [Checks entity states via MCP]
        The person.home entity shows "home" not "away".
        The automation trigger expects state change to "away".
```

### Benefits for This Project

1. **Faster Development**: No need to pull configs to check entity states
2. **Live Debugging**: See real-time state during automation development
3. **Validation**: Verify entities exist without parsing `.storage` files
4. **Testing**: Test automations by calling services directly
5. **Exploration**: Discover entities interactively during sessions

### Troubleshooting

**MCP not connecting:**
- Verify HA_URL and HA_TOKEN in `.env`
- Check Home Assistant is accessible from your machine
- Try `curl $HA_URL/api/` (should return 200 with API message)
- Check Claude Code logs for MCP connection errors

**Permission errors:**
- Ensure token has necessary permissions
- For official integration, check exposed entities settings
- Token must be "Long-Lived Access Token" not temporary

**Command not found:**
- For `npx`: Install Node.js from nodejs.org
- For `uvx`: Install uv via `pip install uv`
- Verify command in terminal before enabling in `.mcp.json`

### Security Notes

- MCP gives Claude direct API access to Home Assistant
- Tokens are read from `.env` (never committed to git)
- Use `.mcp.json` for team-shared configs
- Create `.mcp.local.json` for personal overrides (add to .gitignore)
- Consider read-only tokens for development

### Advanced: Custom MCP Servers

You can create project-specific MCP servers for:
- Custom validation logic
- Project-specific automation patterns
- Integration with other tools
- See: https://modelcontextprotocol.io/docs

## Project Structure

- `config/` - Contains all Home Assistant configuration files (synced from HA instance)
- `tools/` - Validation and testing scripts
- `venv/` - Python virtual environment with dependencies
- `temp/` - Temporary directory for Claude to write and test code before moving to final locations
- `Makefile` - Commands for pulling/pushing configuration
- `.mcp.json` - Model Context Protocol server configuration (see MCP Server Configuration section)
- `.claude/` - Claude Code slash commands
  - `commands/` - Custom workflow commands (see Slash Commands above)
- `.claude-code/` - Project-specific Claude Code settings and hooks
  - `hooks/` - Validation hooks that run automatically
  - `settings.json` - Project configuration

## Available Commands

### Configuration Management
- `make pull` - Pull latest config from Home Assistant instance
- `make push` - Push local config to Home Assistant (with validation)
- `make backup` - Create backup of current config
- `make validate` - Run all validation tests

### Validation Tools
- `python tools/run_tests.py` - Run complete validation suite
- `python tools/yaml_validator.py` - YAML syntax validation only
- `python tools/reference_validator.py` - Entity/device reference validation
- `python tools/ha_official_validator.py` - Official HA configuration validation

### Entity Discovery Tools
- `make entities` - Explore available Home Assistant entities
- `python tools/entity_explorer.py` - Entity registry parser and explorer
  - `--search TERM` - Search entities by name, ID, or device class
  - `--domain DOMAIN` - Show entities from specific domain (e.g., climate, sensor)
  - `--area AREA` - Show entities from specific area
  - `--full` - Show complete detailed output

## Validation System

This project includes comprehensive validation to prevent invalid configurations:

1. **YAML Syntax Validation** - Ensures proper YAML syntax with HA-specific tags
2. **Entity Reference Validation** - Checks that all referenced entities/devices exist
3. **Official HA Validation** - Uses Home Assistant's own validation tools

### Automated Validation Hooks

- **Post-Edit Hook**: Runs validation after editing any YAML files in `config/`
- **Pre-Push Hook**: Validates configuration before pushing to Home Assistant
- **Blocks invalid pushes**: Prevents uploading broken configurations

## Home Assistant Instance Details

- **Host**: Configure in Makefile `HA_HOST` variable
- **User**: Configure SSH access as needed
- **SSH Key**: Configure SSH key authentication
- **Config Path**: /config/ (standard HA path)
- **Version**: Compatible with Home Assistant Core 2024.x+

## Entity Registry

The system tracks entities across these domains:
- alarm_control_panel, binary_sensor, button, camera, climate
- device_tracker, event, image, light, lock, media_player
- number, person, scene, select, sensor, siren, switch
- time, tts, update, vacuum, water_heater, weather, zone

## Development Workflow

1. **Pull Latest**: `make pull` to sync from HA
2. **Edit Locally**: Modify files in `config/` directory
3. **Auto-Validation**: Hooks automatically validate on edits
4. **Test Changes**: `make validate` for full test suite
5. **Deploy**: `make push` to upload (blocked if validation fails)

## Key Features

- ✅ **Safe Deployments**: Pre-push validation prevents broken configs
- ✅ **Entity Validation**: Ensures all references point to real entities
- ✅ **Entity Discovery**: Advanced tools to explore and search available entities
- ✅ **Official HA Tools**: Uses Home Assistant's own validation
- ✅ **YAML Support**: Handles HA-specific tags (!include, !secret, !input)
- ✅ **Comprehensive Testing**: Multiple validation layers
- ✅ **Automated Hooks**: Validation runs automatically on file changes

## Important Notes

- **Never push without validation**: The hooks prevent this, but be aware
- **Blueprint files** use `!input` tags which are normal and expected
- **Secrets are skipped** during validation for security
- **SSH access required** for pull/push operations
- **Python venv required** for validation tools

## Troubleshooting

### Validation Fails
1. Check YAML syntax errors first
2. Verify entity references exist in `.storage/` files
3. Run individual validators to isolate issues
4. Check HA logs if official validation fails

### SSH Issues
1. Verify SSH key permissions: `chmod 600 ~/.ssh/your_key`
2. Test connection: `ssh your_homeassistant_host`
3. Check SSH config in `~/.ssh/config`

### Missing Dependencies
1. Activate venv: `source venv/bin/activate`
2. Install requirements: `pip install homeassistant voluptuous pyyaml`

## Security

- **SSH keys** are used for secure access
- **Secrets.yaml** is excluded from validation (contains sensitive data)
- **No credentials** are stored in this repository
- **Access tokens** in config are for authorized integrations

This system ensures you can confidently manage Home Assistant configurations with Claude while maintaining safety and reliability.

## Entity Naming Convention

This Home Assistant setup uses a **standardized entity naming convention** for multi-location deployments:

### **Format: `location_room_device_sensor`**

**Structure:**
- **location**: `home`, `office`, `cabin`, etc.
- **room**: `basement`, `kitchen`, `living_room`, `main_bedroom`, `guest_bedroom`, `driveway`, etc.
- **device**: `motion`, `heatpump`, `sonos`, `lock`, `vacuum`, `water_heater`, `alarm`, etc.
- **sensor**: `battery`, `tamper`, `status`, `temperature`, `humidity`, `door`, `running`, etc.

### **Examples:**
```
binary_sensor.home_basement_motion_battery
binary_sensor.home_basement_motion_tamper
media_player.home_kitchen_sonos
media_player.office_main_bedroom_sonos
climate.home_living_room_heatpump
climate.office_living_room_thermostat
lock.home_front_door_august
sensor.office_driveway_camera_battery
vacuum.home_roborock
vacuum.office_roborock
```

### **Benefits:**
- **Clear location identification** - no ambiguity between properties
- **Consistent structure** - easy to predict entity names
- **Automation-friendly** - simple to target location-specific devices
- **Scalable** - supports additional locations or rooms

### **Implementation:**
- All location-based entities follow this convention
- Legacy entities have been systematically renamed
- New entities should follow this pattern
- Vendor prefixes (aquanta_, august_, etc.) are replaced with descriptive device names

### **Claude Code Integration:**
- **Always explore first**: Use entity discovery tools before writing automations (see "Explore → Plan → Code → Commit" workflow above)
- **Ask for clarification**: When multiple choices exist for sensors or devices, always ask the user
- **Follow naming convention**: Use the `location_room_device_sensor` pattern when suggesting entity names
- **Be specific**: Follow instruction specificity guidelines (see Best Practices section)
- **Validate early**: Use hooks and validation commands frequently
- **Manage context**: Use `/clear` between unrelated tasks (see Context Management above)

## Important Technical Notes

- All python tools need to be run with  `source venv/bin/activate && python <tool_path>`
- Validation hooks run automatically but can be manually triggered with `/validate-config`
- Use slash commands for common workflows - they include built-in validation and safety checks

---

# 🤖 Multi-Agent Development System

This repository now includes a **comprehensive multi-agent system** for intelligent Home Assistant automation development. The agent system provides guided workflows for creating, validating, testing, and documenting automations with confidence.

## Agent System Overview

The system consists of 8 specialized agents coordinated by an Orchestrator:

### **1. Orchestrator Agent** (Master Coordinator)
- Routes requests to appropriate specialists
- Manages complex multi-agent workflows
- Consolidates results from multiple agents
- Handles error recovery and state management

### **2. Entity Discovery Agent** (Explorer)
- Context-aware entity search
- Natural language entity discovery
- Shows entity capabilities and usage
- Suggests relevant entities for automation context

### **3. Automation Designer Agent** (Architect)
- Converts natural language to YAML
- Builds triggers, conditions, and actions
- Pattern recognition and templates
- Generates complete automation configurations

### **4. Validation Agent** (Quality Controller)
- 3-layer validation (YAML, references, official HA)
- Intelligent error parsing and explanations
- Specific fix suggestions
- Conflict detection

### **5. Testing Agent** (QA Engineer)
- Simulates automations before deployment
- Tests multiple scenarios
- Identifies edge cases
- Provides dry-run capabilities

### **6. Documentation Agent** (Librarian)
- Auto-generates markdown documentation
- Creates entity relationship maps
- Maintains changelogs
- Keeps documentation synchronized

### **7. Best Practices Agent** (Advisor)
- Security review
- Performance analysis
- Naming convention enforcement
- Pattern recognition and anti-pattern detection

### **8. Refactoring Agent** (Optimizer)
- Detects duplicate logic
- Suggests script extraction
- Optimizes performance
- Consolidates similar automations

## Quick Start with Agents

### Using Slash Commands

The easiest way to use the agent system is through slash commands:

```bash
# Create new automation with guided workflow
/create-automation

# Find entities for your automation
/find-entities motion sensors in the kitchen

# Review all automations for issues
/review-automations

# Debug a failing automation
/debug-automation
```

### Programmatic Usage

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

# Check results
if result.success:
    automation = result.data['automation']
    print(f"✅ {result.message}")

    # Review recommendations
    for rec in result.recommendations:
        print(f"[{rec['priority']}] {rec['description']}")
```

## Available Workflows

The Orchestrator provides these complete workflows:

### **create_automation**
Complete workflow for creating new automations:
1. Entity Discovery (find relevant entities)
2. Automation Design (create YAML)
3. Best Practices Review
4. Validation (all layers)
5. Testing (scenarios)
6. Documentation (generate docs)

```python
orchestrator.run(
    workflow='create_automation',
    description="Turn on lights when door opens"
)
```

### **review_automations**
Comprehensive review of all automations:
1. Best Practices Review
2. Refactoring Analysis
3. Validation Check
4. Generate Report

```python
orchestrator.run(workflow='review_automations')
```

### **debug_automation**
Debug failing automations:
1. Validate configuration
2. Check entity availability
3. Test trigger conditions
4. Simulate execution
5. Provide diagnosis

```python
orchestrator.run(
    workflow='debug_automation',
    automation=problematic_automation
)
```

### **find_entities**
Discover entities by natural language:

```python
orchestrator.run(
    workflow='find_entities',
    query='motion sensors',
    domain='binary_sensor',
    area='kitchen',
    context='trigger'  # For context-aware suggestions
)
```

### **validate_config**
Run comprehensive validation:

```python
orchestrator.run(
    workflow='validate_config',
    validation_type='full',  # or 'yaml', 'references', 'official'
    file_path='config/automations.yaml'  # optional
)
```

### **document_automations**
Generate documentation:

```python
orchestrator.run(
    workflow='document_automations',
    doc_type='all'  # or 'automation', 'entity_map', 'changelog', 'index'
)
```

### **refactor_automations**
Find optimization opportunities:

```python
orchestrator.run(
    workflow='refactor_automations',
    refactor_type='all'  # or 'duplicates', 'scripts', 'optimize', 'consolidate'
)
```

## Agent System Directory Structure

```
claude-homeassistant/
├── agents/                        # Agent system (NEW!)
│   ├── __init__.py               # Package initialization
│   ├── base_agent.py             # Abstract base class for all agents
│   ├── shared_context.py         # Shared state management
│   ├── orchestrator.py           # Master coordinator
│   ├── creation/                 # Creation agents
│   │   ├── entity_discovery.py   # Entity search and discovery
│   │   └── automation_designer.py # Automation creation
│   ├── validation/               # Validation agents
│   │   ├── validation_agent.py   # Configuration validation
│   │   └── testing_agent.py      # Scenario testing
│   ├── analysis/                 # Analysis agents
│   │   ├── best_practices.py     # Best practices review
│   │   └── refactoring.py        # Optimization analysis
│   └── documentation/            # Documentation agents
│       └── documentation_agent.py # Doc generation
├── docs/                         # Generated documentation (NEW!)
│   ├── AGENT_SYSTEM_GUIDE.md    # Complete user guide
│   ├── automations/             # Per-automation docs
│   │   ├── lighting/
│   │   ├── climate/
│   │   ├── security/
│   │   └── general/
│   ├── entities/                # Entity documentation
│   │   └── entity_map.md
│   └── changelog.md             # Automation changelog
├── .claude-code/
│   └── commands/                # Slash commands (NEW!)
│       ├── create-automation.md
│       ├── review-automations.md
│       ├── find-entities.md
│       └── debug-automation.md
└── config/                      # HA configuration (existing)
```

## Using Individual Agents

Access specific agents directly through the orchestrator:

```python
orchestrator = OrchestratorAgent(context)

# Get specific agent
entity_agent = orchestrator.get_agent('entity_discovery')
validation_agent = orchestrator.get_agent('validation')
testing_agent = orchestrator.get_agent('testing')

# Use agent directly
result = entity_agent.run(
    query='motion sensors',
    domain='binary_sensor'
)

# List all available agents
for agent_info in orchestrator.list_agents():
    print(f"{agent_info['name']}: {agent_info['description']}")
```

## Shared Context System

The SharedContext provides centralized state management:

```python
context = SharedContext()

# Access registries
entities = context.get_entities()
devices = context.get_devices()
areas = context.get_areas()

# Search and validate
results = context.search_entities("kitchen")
exists = context.entity_exists('light.home_kitchen_ceiling')

# Get specific entity
entity = context.get_entity('binary_sensor.home_kitchen_motion')

# Load automations
automations = context.get_automations()
automation = context.get_automation('kitchen_motion_lights')

# Configuration paths
automations_path = context.get_automations_path()
config_path = context.get_config_path('automations.yaml')

# Inter-agent communication
context.send_message('agent1', 'agent2', {'key': 'value'})
messages = context.get_messages('agent2')

# Shared data storage
context.set_data('key', value)
value = context.get_data('key')
```

## Agent Result Format

All agents return standardized `AgentResult` objects:

```python
result = agent.run(**kwargs)

# Check success
if result.success:
    print(f"✅ {result.message}")
else:
    print(f"❌ {result.message}")

# Access data
data = result.data
automation = result.data.get('automation')

# Review errors and warnings
for error in result.errors:
    print(f"Error: {error}")

for warning in result.warnings:
    print(f"Warning: {warning}")

# Get recommendations
for rec in result.recommendations:
    priority = rec['priority']  # critical, high, medium, low
    description = rec['description']
    action = rec.get('action')
    print(f"[{priority}] {description}")
    if action:
        print(f"  Action: {action}")
```

## Best Practices with Agents

### 1. Always Start with Entity Discovery

Before creating automations, explore available entities:

```python
# Find relevant entities
result = orchestrator.run(
    workflow='find_entities',
    query='motion',
    area='kitchen'
)

# Review options
for entity in result.data['entities']:
    print(f"{entity['entity_id']}: {entity['name']}")
    if entity.get('relevance_reason'):
        print(f"  → {entity['relevance_reason']}")
```

### 2. Use Complete Workflows

The orchestrator workflows ensure nothing is missed:

```python
# Good: Use complete workflow
result = orchestrator.run(
    workflow='create_automation',
    description="..."
)

# Less ideal: Manual agent coordination
# (only for advanced custom workflows)
```

### 3. Review All Recommendations

Agents provide intelligent suggestions - review them:

```python
if result.recommendations:
    for rec in result.recommendations:
        if rec['priority'] in ['critical', 'high']:
            print(f"⚠️ {rec['description']}")
            # Consider implementing before deployment
```

### 4. Test Before Deploying

Always test automations before pushing to HA:

```python
# Testing is included in create_automation workflow
# Or run separately:
testing_result = orchestrator.get_agent('testing').run(
    automation=automation,
    test_type='full'
)

# Review edge cases
for warning in testing_result.warnings:
    print(f"Edge case: {warning}")
```

### 5. Keep Documentation Updated

Auto-generate docs as you go:

```python
# Documentation is included in create_automation workflow
# Or update manually:
doc_result = orchestrator.get_agent('documentation').run(
    automation=automation,
    doc_type='automation',
    update_existing=True
)
```

## Integrating Agents with Existing Workflow

The agent system integrates seamlessly:

```
Traditional Workflow:
1. make pull
2. Edit automations.yaml manually
3. make validate
4. make push

Enhanced Agent Workflow:
1. make pull
2. /create-automation (agents design + validate + test)
3. Review recommendations
4. Save to automations.yaml
5. make push (pre-push validation still runs)
```

## Troubleshooting the Agent System

### "No module named 'agents'"

```bash
# Ensure you're in the project root
cd /home/user/claude-homeassistant

# Python needs to find the agents module
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### "SharedContext not initialized"

```python
# Always create context first
from agents.shared_context import SharedContext
context = SharedContext()

# Then create orchestrator
from agents.orchestrator import OrchestratorAgent
orchestrator = OrchestratorAgent(context)
```

### "Entity registry not found"

```bash
# Pull latest config to get registry files
make pull

# Verify registry files exist
ls -la config/.storage/core.entity_registry
```

### "Agent workflow failed"

```python
# Check result details
if not result.success:
    print(f"Failure: {result.message}")
    print(f"Errors: {result.errors}")

    # Check data for partial results
    if result.data:
        print(f"Partial data: {result.data}")
```

## Advanced: Creating Custom Workflows

You can create custom workflows by combining agents:

```python
def custom_workflow(description: str):
    """Custom workflow: Create + Optimize + Test + Document"""

    context = SharedContext()
    orchestrator = OrchestratorAgent(context)

    # Step 1: Design
    design_result = orchestrator.get_agent('automation_designer').run(
        description=description
    )
    automation = design_result.data['automation']

    # Step 2: Optimize
    practices_result = orchestrator.get_agent('best_practices').run(
        automation=automation,
        review_type='full'
    )

    # Step 3: Apply high-priority recommendations
    for rec in practices_result.recommendations:
        if rec['priority'] == 'high':
            automation = apply_recommendation(automation, rec)

    # Step 4: Validate
    val_result = orchestrator.get_agent('validation').run(
        automation=automation
    )

    # Step 5: Test
    test_result = orchestrator.get_agent('testing').run(
        automation=automation,
        test_type='full'
    )

    # Step 6: Document
    doc_result = orchestrator.get_agent('documentation').run(
        automation=automation,
        doc_type='automation'
    )

    return {
        'automation': automation,
        'validation': val_result,
        'testing': test_result,
        'documentation': doc_result
    }
```

## Documentation

- **[Agent System Guide](docs/AGENT_SYSTEM_GUIDE.md)** - Complete user guide with examples
- **[Agent API Reference](docs/AGENT_API.md)** - Detailed API documentation (coming soon)
- **Slash Commands** - See `.claude-code/commands/` for usage guides

## Agent System Benefits

✅ **Confidence**: Test automations before deployment
✅ **Quality**: Best practices enforced automatically
✅ **Speed**: Natural language to working automation
✅ **Safety**: Multi-layer validation prevents errors
✅ **Maintainability**: Auto-generated documentation
✅ **Intelligence**: Context-aware suggestions
✅ **Learning**: Agents explain best practices

## Next Steps

1. **Try it out**: Use `/create-automation` to create your first automation
2. **Review existing**: Run `/review-automations` to analyze current automations
3. **Explore entities**: Use `/find-entities` to discover what's available
4. **Read the guide**: See `docs/AGENT_SYSTEM_GUIDE.md` for comprehensive documentation

The agent system is designed to make Home Assistant automation development safer, faster, and more enjoyable! 🏠✨
