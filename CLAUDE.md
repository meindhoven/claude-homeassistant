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

#### 4. Multi-File Workflows

Many Home Assistant features require coordinated changes across multiple files. Handle these systematically:

**Common Multi-File Patterns:**

**Pattern 1: Automation with Helper Entities**
```
Request: "Create automation with adjustable brightness"

Files to modify:
1. config/configuration.yaml - Define input_number helper
2. config/automations.yaml - Reference helper in automation

Workflow:
→ Read both files to understand current structure
→ Add helper entity definition first
→ Create automation referencing the helper
→ Validate both files
→ Test that helper appears in UI
→ Commit both changes together
```

**Pattern 2: Automation with Reusable Script**
```
Request: "Secure home when leaving (multiple actions)"

Files to modify:
1. config/scripts.yaml - Create reusable script
2. config/automations.yaml - Call script from automation

Benefits:
→ Script can be reused by multiple automations
→ Script can be triggered manually from UI
→ Easier to test and maintain
→ Changes to script affect all automations using it
```

**Pattern 3: Complex Scene with Automation**
```
Request: "Movie mode that dims lights and adjusts thermostat"

Files to modify:
1. config/scenes.yaml - Define scene with all entity states
2. config/automations.yaml - Automation to activate scene
3. config/automations.yaml - Automation to restore previous state

Workflow:
→ Create scene with desired states
→ Create activation automation
→ Create restoration automation
→ Validate scene activates correctly
→ Test that restoration works
```

**Pattern 4: Integration Configuration**
```
Request: "Add weather integration"

Files to modify:
1. config/configuration.yaml - Add integration config
2. config/secrets.yaml - Store API key
3. config/automations.yaml - Create weather-based automation

Security:
→ NEVER commit secrets.yaml
→ Use !secret tag in configuration.yaml
→ Validate without exposing secrets
```

**Best Practices for Multi-File Changes:**

1. **Plan the Dependency Graph**
   ```
   Before editing, identify:
   - Which files need changes?
   - What's the dependency order?
   - Which entities reference which?
   - What could break if one fails?
   ```

2. **Edit in Dependency Order**
   ```
   Good order:
   1. Base configs (configuration.yaml)
   2. Shared resources (scripts.yaml, scenes.yaml)
   3. Consumers (automations.yaml)

   Why: Ensures references exist before they're used
   ```

3. **Validate Incrementally**
   ```
   After each file edit:
   → Run validation
   → Check for new errors
   → Fix before moving to next file

   Result: Isolate errors to specific changes
   ```

4. **Use Slash Commands for Multi-File Workflows**
   ```
   /create-automation - Automatically handles multi-file needs
   /review-automation - Checks cross-file dependencies
   /safe-deploy - Validates all related files together
   ```

5. **Document Cross-File Dependencies**
   ```
   In commit messages:
   "Add brightness automation with helper input

   - configuration.yaml: Added input_number helper
   - automations.yaml: Added automation using helper

   These files must be deployed together."
   ```

**Common Multi-File Pitfalls:**

❌ **Editing files in wrong order**
```
Bad: Create automation first, add helper second
Result: Validation fails, automation references non-existent entity
Good: Add helper first, then create automation
```

❌ **Forgetting to validate all changed files**
```
Bad: Validate only automations.yaml
Result: Syntax error in configuration.yaml breaks HA restart
Good: Run full validation suite (all files)
```

❌ **Partial commits**
```
Bad: Commit automation without helper
Result: Broken automation in git history
Good: Commit all related changes together
```

❌ **Assuming entities exist**
```
Bad: Reference script.secure_home without checking
Result: Automation fails silently at runtime
Good: Read scripts.yaml first to verify it exists
```

**Multi-File Workflow Example:**

```
User: "Create automation to adjust thermostat based on occupancy
       with configurable temperature settings"

Claude's approach:
1. PLAN multi-file changes:
   - configuration.yaml: input_number for temperatures
   - automations.yaml: occupancy-based automation

2. READ existing files:
   - Check configuration.yaml structure
   - Check current automations
   - Find occupancy sensors

3. EDIT in order:
   a. configuration.yaml - Add helpers:
      - input_number.occupied_temp
      - input_number.unoccupied_temp
   b. automations.yaml - Add automation referencing helpers

4. VALIDATE after each edit:
   - After helpers: Check YAML syntax
   - After automation: Check entity references

5. TEST logic:
   - Verify helpers appear in UI
   - Check automation triggers correctly
   - Confirm template renders properly

6. COMMIT together:
   "Add occupancy-based thermostat automation

   - configuration.yaml: Temperature input helpers
   - automations.yaml: Occupancy automation

   Helpers allow UI adjustment without editing YAML."
```

**When to Use Multi-File Patterns:**

✅ **Use scripts** when:
- Same actions used by multiple automations
- Actions are complex and benefit from abstraction
- You want manual triggering capability

✅ **Use helpers** when:
- Values need UI adjustment
- Settings should persist across restarts
- Multiple automations share configuration

✅ **Use scenes** when:
- Setting multiple entity states together
- Wanting quick state restoration
- Creating mood/mode presets

✅ **Use groups** when:
- Controlling multiple entities as one
- Simplifying automation targets
- Creating logical entity collections

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

## Personal Configuration (CLAUDE.local.md)

### Customizing Claude's Behavior

While this project provides comprehensive team-wide documentation via CLAUDE.md and subdirectory guides, **you can personalize Claude's behavior** for your own development style without affecting the shared configuration.

**CLAUDE.local.md** is a personal configuration file that:
- ✅ **Overrides team defaults** with your personal preferences
- ✅ **Never committed to git** (in .gitignore)
- ✅ **Automatically loaded** by Claude Code alongside shared CLAUDE.md
- ✅ **Supports all markdown features** - sections, code blocks, lists, examples

### Creating Your Personal Configuration

**Quick Start:**
```bash
# Copy the template to create your personal config
cp CLAUDE.local.md.template CLAUDE.local.md

# Edit with your preferences
# (Use your preferred editor)
```

The template includes sections for:
- **Development Preferences**: Your typical workflow patterns
- **Environment Setup**: Your Home Assistant URL, areas of focus, special entities
- **Coding Style**: Python/YAML style preferences
- **Communication**: How you prefer Claude to respond (detail level, explanations, emojis)
- **Tool Usage**: Which tools you use frequently
- **Personal Automations**: What you're currently working on
- **MCP Preferences**: Whether you use MCP and how

### Benefits

**For Individual Developers:**
- Claude remembers your coding style preferences
- Adapts communication style to your preference (concise vs verbose)
- Knows which entities and areas you typically work with
- Understands your current projects for more relevant assistance
- Respects your workflow preferences (e.g., "always ask before deploying")

**For Teams:**
- Each team member can have different preferences
- Shared CLAUDE.md provides team standards
- Personal CLAUDE.local.md customizes without conflicts
- No merge conflicts from personal preferences

### Example Use Cases

**Scenario 1: Different Detail Preferences**
```markdown
# In your CLAUDE.local.md
## Communication Preferences
- Detail level: Concise
- Explanations: Only when asked
- Code comments: Minimal
```

**Scenario 2: Project-Specific Context**
```markdown
# In your CLAUDE.local.md
## What I'm Currently Working On
- Migrating all motion sensor automations to new Z-Wave sensors
- Working primarily with: binary_sensor.home_*_motion entities
- Areas: basement, garage, driveway
- Always test motion automations manually before deploying
```

**Scenario 3: Personal Constraints**
```markdown
# In your CLAUDE.local.md
## Personal Notes
- Always confirm before deploying climate automations (expensive if wrong!)
- I'm learning HA, so please explain Jinja2 templates when using them
- Prefer entity_id over friendly names in automations
```

### Privacy and Security

**Safe to include:**
- Your specific entity names (e.g., `climate.office_bedroom_thermostat`)
- Areas you work in
- Personal workflow preferences
- Current project context
- Skill level and learning goals

**Avoid including:**
- Passwords or API tokens (use `.env` for those)
- Personal identifying information
- Detailed physical security layouts
- Home address or location details

**Note**: CLAUDE.local.md is in `.gitignore` and will never be committed, but it may still appear in local backups.

### Template Reference

See **CLAUDE.local.md.template** for a complete example with:
- All available sections
- Example configurations
- Usage tips
- Best practices

**The template is comprehensive** - you don't need to fill out every section, just the ones relevant to your workflow.

## MCP Server Configuration

### What is MCP?

**Model Context Protocol (MCP)** is a protocol that allows Claude to communicate directly with external services during sessions. For Home Assistant, this enables:

- ✅ **Real-time entity queries**: Check current state of devices without parsing files
- ✅ **Service calls**: Test automations by calling HA services directly
- ✅ **Live validation**: Verify entities exist against running HA instance
- ✅ **State inspection**: Debug automations with live state data
- ✅ **Direct API access**: Full Home Assistant API available to Claude

### MCP Server Implementation

This project uses **hass-mcp** (`voska/hass-mcp`), a community MCP server implementation that provides:

- ✅ **Full Home Assistant API access** via standard REST API
- ✅ **Entity state queries** and service calls
- ✅ **Simple configuration** with minimal dependencies
- ✅ **Easy installation** via `uvx` (no Docker required)
- ✅ **Active development** and community support

**Why hass-mcp:**
- Works with any Home Assistant version (no need for HA 2025.2+)
- Lightweight and fast
- Uses standard Home Assistant API (compatible with all HA installations)
- Simple environment variable configuration

**Alternative Options:**
- `allenporter/mcp-server-home-assistant` - WebSocket-based implementation
- `tevonsb/homeassistant-mcp` - Alternative REST implementation
- Built-in HA MCP (requires HA 2025.2+) - Native integration via `/api/mcp`

### Configuration

The `.mcp.json` file in the project root contains the MCP server configuration:

```json
{
  "mcpServers": {
    "homeassistant": {
      "command": "uvx",
      "args": ["hass-mcp"],
      "env": {
        "HA_URL": "${HA_URL}",
        "HA_TOKEN": "${HA_TOKEN}"
      },
      "disabled": false
    }
  }
}
```

**Configuration Details:**
- `command: "uvx"` - Uses uvx to run the hass-mcp package (auto-installs if needed)
- `args: ["hass-mcp"]` - The MCP server package name
- `HA_URL` - Your Home Assistant URL (from `.env` file)
- `HA_TOKEN` - Your Home Assistant long-lived access token (from `.env` file)
- `disabled: false` - MCP server is enabled by default

### Setup Instructions

1. **Install uvx (if not already installed):**
   ```bash
   # Using pip:
   pip install uv

   # Or using the official installer:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Verify installation:
   uvx --version
   ```

2. **Configure Environment Variables:**
   Ensure your `.env` file contains the required variables:
   ```bash
   HA_TOKEN=your_home_assistant_long_lived_access_token
   HA_URL=http://your_homeassistant_host:8123
   ```

3. **Generate Long-Lived Access Token (if not done):**
   - Open Home Assistant web interface
   - Navigate to: Profile → Security (bottom left corner → your profile)
   - Scroll to "Long-Lived Access Tokens" section
   - Click "Create Token"
   - Give it a name (e.g., "Claude MCP")
   - Copy the token immediately (you can't view it again!)
   - Add to `.env` file as `HA_TOKEN=<your_token>`

4. **Verify Configuration:**
   The MCP server is already configured and enabled in `.mcp.json`. No changes needed unless you want to disable it.

5. **Restart Claude Code:**
   Close and reopen Claude Code to load the MCP configuration.

6. **Test the Connection:**
   Ask Claude to query an entity:
   ```
   "What's the current state of my living room lights?"
   ```

   Or verify connectivity:
   ```
   "List all my climate entities"
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

**Command not found (uvx):**
- Install uv: `pip install uv` or use the official installer
- Verify installation: `uvx --version`
- Ensure uv is in your PATH
- Try manual installation: `uv tool install hass-mcp`

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

## Tool Configuration and Allowlist

### Understanding Tool Permissions

Claude Code uses various tools to interact with your codebase. This project has configured a **tool allowlist** that enables Claude to work efficiently without requiring manual approval for each operation.

**Why Tool Allowlists Matter:**
- ⚡ **Faster workflows**: Claude can read, edit, and validate files immediately
- 🔒 **Safety through hooks**: Validation hooks catch errors regardless of tool permissions
- 🎯 **Focused development**: No interruptions for routine operations
- 📊 **Transparent operations**: All tool usage is logged and can be reviewed

### Pre-Approved Tools

These tools are configured in `.claude-code/settings.json` and don't require explicit approval:

#### File Operations
- **Read** - Read files to understand codebase
- **Edit** - Modify existing files (always reads first)
- **Write** - Create new files when necessary
- **Glob** - Find files matching patterns
- **Grep** - Search code for specific content

#### Task Management
- **Task** - Launch specialized agents for complex operations
- **TodoWrite** - Track progress with TODO lists
- **ExitPlanMode** - Complete planning phase

#### Execution
- **Bash** - Run terminal commands (git, make, validation tools)
- **BashOutput** - Monitor output from background processes
- **KillShell** - Stop background processes

#### Research
- **WebFetch** - Fetch documentation and resources
- **WebSearch** - Search for solutions and information

#### Specialized
- **NotebookEdit** - Edit Jupyter notebooks
- **Skill** - Execute project-specific skills

#### MCP (Model Context Protocol)
- **mcp__homeassistant__get_entity** - Query single entity state
- **mcp__homeassistant__get_entities** - Query multiple entity states
- **mcp__homeassistant__call_service** - Call Home Assistant services
- **mcp__homeassistant__get_states** - Get all entity states
- **mcp__homeassistant__list_entities** - List available entities
- **mcp__homeassistant__list_services** - List available services
- **mcp__homeassistant__get_config** - Get Home Assistant configuration

### Project-Specific Tool Guidance

Based on this project's needs, Claude follows these tool usage patterns:

#### File Operations Best Practices
```markdown
✅ Always read files before editing
✅ Use Edit for modifying existing files (preserves formatting)
✅ Run validation after config changes
✅ Prefer incremental changes over large rewrites

❌ Don't use Write for existing files (use Edit instead)
❌ Don't skip validation after YAML changes
❌ Don't edit .storage/ files (read-only)
```

#### Execution Best Practices
```markdown
✅ Validate before every push (make validate)
✅ Use hooks for automatic validation
✅ Test automations incrementally
✅ Run Python tools with venv activated

❌ Don't push without validation passing
❌ Don't bypass pre-push hooks
❌ Don't run tools without activating venv
```

#### Research Best Practices
```markdown
✅ Use entity_explorer.py before creating automations
✅ Verify entities exist in registry
✅ Check Home Assistant docs when unsure
✅ Search existing automations for patterns

❌ Don't guess entity names
❌ Don't assume services exist
❌ Don't skip entity discovery phase
```

#### MCP Best Practices
```markdown
✅ Use MCP to query live entity states
✅ Verify entity existence against running HA instance
✅ Test service calls before adding to automations
✅ Use get_entities for batch queries
✅ Check entity states when debugging automations

❌ Don't rely solely on config files for entity info
❌ Don't call services that modify state without asking
❌ Don't assume MCP is available (check .env configured)
```

### Safety Through Hooks

While tools are pre-approved, **validation hooks ensure safety**:

1. **Post-Edit Validation** (`.claude-code/hooks/posttooluse-ha-validation.sh`)
   - Runs after YAML edits in `config/`
   - Validates syntax, entities, and HA config
   - Non-blocking - warns but allows work to continue

2. **Pre-Push Validation** (`.claude-code/hooks/pretooluse-ha-push-validation.sh`)
   - Runs before `make push` or deployment
   - **Blocking** - prevents invalid configs from reaching HA
   - Ensures only validated configs are deployed

3. **Python Quality Checks** (`.claude-code/hooks/posttooluse-python-quality.sh`)
   - Runs after Python file edits
   - Auto-formats with Black and isort
   - Runs linting and type checking

**Result**: Fast development + Safe deployments

### Customizing Tool Configuration

The tool configuration is in `.claude-code/settings.json`:

```json
{
  "tools": {
    "allowlist": {
      "file_operations": ["Read", "Edit", "Write", "Glob", "Grep"],
      "task_management": ["Task", "TodoWrite", "ExitPlanMode"],
      "execution": ["Bash", "BashOutput", "KillShell"],
      "research": ["WebFetch", "WebSearch"],
      "notebook": ["NotebookEdit"],
      "project_specific": ["Skill"]
    },
    "guidance": {
      "file_operations": {
        "always_read_before_edit": true,
        "use_validation_after_changes": true,
        "prefer_edit_over_write": true
      },
      "execution": {
        "validate_before_push": true,
        "use_hooks_for_safety": true,
        "test_incrementally": true
      },
      "research": {
        "use_entity_explorer_before_automations": true,
        "verify_entity_existence": true,
        "check_ha_docs_when_unsure": true
      }
    }
  }
}
```

**To modify**:
1. Edit `.claude-code/settings.json`
2. Add/remove tools from allowlist
3. Update guidance flags as needed
4. Changes take effect immediately

### Personal Tool Preferences

If you have personal tool preferences different from the team, use **CLAUDE.local.md**:

```markdown
# In your CLAUDE.local.md
## Personal Tool Allowlist
**Custom permissions:**
- Always ask before running Bash commands that modify git history
- Auto-approve all Read operations
- Prefer verbose output for Bash commands
```

### Benefits of This Configuration

**For This Project:**
- ✅ Automatic validation after every edit
- ✅ Blocked invalid pushes to Home Assistant
- ✅ Fast iteration on automations
- ✅ Safe experimentation with configs
- ✅ Entity validation without manual checks

**For Development Workflow:**
- ✅ Claude can read docs and examples freely
- ✅ Edits are validated immediately by hooks
- ✅ Git operations require explicit confirmation (not in allowlist)
- ✅ Dangerous operations (force push, rm -rf) are never auto-approved

### Monitoring Tool Usage

All tool usage is logged and visible in Claude Code's interface. Review logs to:
- Understand what Claude did during a session
- Debug issues with file edits or validation
- Learn Claude's problem-solving approach
- Verify no unintended changes were made

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
