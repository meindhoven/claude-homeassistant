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
