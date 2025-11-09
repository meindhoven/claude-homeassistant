# Home Assistant Configuration Management

This repository manages Home Assistant configuration files with automated validation, testing, and deployment.

## 📚 Documentation Structure

This file contains **Claude Code-specific guidance** for working on this project. For specific topics, see:

- **Home Assistant Configuration**: See [config/CLAUDE.md](config/CLAUDE.md) for HA config guidelines, automation examples, and entity naming conventions
- **Validation Tool Development**: See [tools/CLAUDE.md](tools/CLAUDE.md) for developing validators with TDD
- **Hook Development**: See [.claude-code/hooks/CLAUDE.md](.claude-code/hooks/CLAUDE.md) for hook patterns and testing
- **Agent System**: See [docs/AGENT_SYSTEM_GUIDE.md](docs/AGENT_SYSTEM_GUIDE.md) for complete agent documentation
- **General Overview**: See [README.md](README.md) for quick start and project overview

## Slash Commands (Quick Actions)

Use these slash commands for common workflows:

### Getting Started
- `/primer` - Comprehensive repository analysis to prime Claude on the codebase (recommended for new sessions)
- `/tree` - Visualize repository structure

### AI-Powered Workflows (Agent System)
- `/create-automation` - Guided automation creation with entity discovery, validation, and testing
- `/create-automation-prp` - Advanced automation creation using PRP framework for complex automations (one-pass implementation)
- `/find-entities` - Natural language entity search ("motion sensors in kitchen")
- `/review-automations` - Comprehensive analysis of all automations
- `/debug-automation` - Systematic debugging with specific fix suggestions
- `/design-dashboard` - Create user-friendly dashboards with UX best practices

### Configuration Management
- `/validate-config` - Run complete validation suite (YAML + entities + official HA)
- `/safe-deploy` - Validate, backup, and push to Home Assistant (safest deployment method)
- `/pull-latest` - Sync latest config from Home Assistant instance
- `/backup-config` - Create timestamped backup

### Utilities
- `/fix-yaml` - Auto-fix YAML formatting issues
- `/troubleshoot` - Diagnose configuration issues with step-by-step guidance

Simply type the slash command (e.g., `/validate-config`) to start the workflow.

## Best Practices for Working with Claude Code

### Recommended Workflow Patterns

#### 1. Explore → Plan → Code → Commit

The most effective workflow for feature development:

**Start of session**: Run `/primer` to establish comprehensive repository context (recommended for new Claude Code sessions)

1. **Explore**: Research the codebase first
   - Use `/tree` to visualize repository structure (if needed)
   - Use `/find-entities` to discover available devices
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
   - Follow naming conventions (see config/CLAUDE.md)

4. **Commit**: Save work with context
   - Write clear, descriptive commit messages
   - Explain the "why" not just the "what"
   - Commit logical units of work
   - Push to remote when ready

**Example:**
```
User: "Add automation to turn off all lights when I leave"

START: /primer                  # Prime Claude on codebase (new session)

1. EXPLORE:
   /find-entities person         # Find person/device_tracker entities
   /find-entities lights          # Find all light entities
   Read config/automations.yaml   # Check existing patterns

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

**Details**: See [tools/CLAUDE.md](tools/CLAUDE.md) for complete TDD workflow

#### 3. Visual Iteration (for dashboards/UI)

For Home Assistant dashboard/Lovelace configurations:

1. **Provide design mock** or describe desired layout
2. **Implement UI code** in Lovelace YAML using `/design-dashboard`
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

4. **Document Cross-File Dependencies**
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

**More Details**: See [config/CLAUDE.md](config/CLAUDE.md) for HA-specific multi-file patterns

### Code Quality and Development Standards

Maintain high code quality and consistency across the project with these standards.

#### File Size Limits

Keep files manageable and maintainable by following these limits:

**Python Files:**
- **Maximum file size**: 500 lines
- **Maximum function size**: 50 lines
- **Maximum class size**: 100 lines

**YAML Files:**
- **Automation files**: Keep individual automations under 100 lines
- **Configuration files**: Break large configs into separate files using `!include`

**Why:**
- Easier to understand and review
- Faster to navigate and edit
- Simpler to test individual components
- Reduces merge conflicts
- Easier to refactor

**Enforcement:**
For Python tools, consider adding pre-commit hooks to check file sizes. See [tools/CLAUDE.md](tools/CLAUDE.md) for implementation guidance.

#### Search and File Discovery

**ALWAYS use ripgrep (`rg`) instead of `grep` or `find`** for better performance:

**✅ Search with ripgrep:**
```bash
# Search for pattern in files
rg "pattern" config/

# Search with context (3 lines before/after)
rg -C 3 "motion" config/automations.yaml

# Search specific file types
rg "climate" -t yaml

# Find files by pattern
rg --files -g "*.yaml" config/

# Case-insensitive search
rg -i "SENSOR" config/
```

**❌ Avoid grep and find:**
```bash
# Don't use grep
grep -r "pattern" config/

# Don't use find
find config/ -name "*.yaml"
```

**Benefits of ripgrep:**
- 10-100x faster than grep
- Respects .gitignore by default
- Better default output formatting
- Built-in file type filtering
- Unicode support

**Note**: The Grep tool in Claude Code uses ripgrep internally, so prefer using that tool over manual bash commands.

#### Conventional Commit Format

Use conventional commit format for clear, searchable git history:

**Format:**
```
<type>(<scope>): <subject>

<optional body>

<optional footer>
```

**Types:**
- `feat` - New feature or automation
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Formatting, whitespace (no code change)
- `refactor` - Code restructuring (no behavior change)
- `test` - Adding or updating tests
- `chore` - Maintenance tasks, dependencies

**Scopes (examples for this project):**
- `automation` - Automation changes
- `validation` - Validator tool changes
- `agent` - Agent system changes
- `config` - Configuration file changes
- `hook` - Hook changes
- `docs` - Documentation updates

**Examples:**
```bash
# New automation
git commit -m "feat(automation): Add motion-based lighting for kitchen"

# Bug fix in validator
git commit -m "fix(validation): Handle missing entity gracefully in reference validator"

# Documentation update
git commit -m "docs(hooks): Add troubleshooting section for validation hooks"

# Refactoring
git commit -m "refactor(agent): Extract entity discovery logic to separate function"

# Multiple files (use body for details)
git commit -m "feat(automation): Add climate schedule with configurable settings

- configuration.yaml: Added input_number helpers for temperature
- scripts.yaml: Created reusable climate control script
- automations.yaml: Added schedule-based automation

These files must be deployed together."
```

**Benefits:**
- Easy to scan git history for specific changes
- Automated changelog generation possible
- Clear understanding of change impact
- Better collaboration in team environments

**Current Practice**: You're already following this pattern informally. This formalizes it for consistency.

#### Line Length

**Maximum line length: 100 characters** (for all files)

**Python:**
- Enforced by Ruff formatter in tools/
- Use black-compatible style

**YAML:**
- Break long lines with proper indentation
- Use multi-line strings with `|` or `>` for long text

**Markdown:**
- Prefer breaking at sentence boundaries
- Code blocks can exceed 100 characters if needed

**Why 100 characters:**
- Fits on modern displays without horizontal scrolling
- Works well with side-by-side diffs
- Compatible with GitHub code review interface
- Balances readability with conciseness

#### Naming Conventions Summary

**Python (in tools/):**
```python
# Variables and functions: snake_case
entity_id = "sensor.home_kitchen_motion"
def validate_entity_reference():

# Classes: PascalCase
class EntityValidator:

# Constants: UPPER_SNAKE_CASE
MAX_FILE_SIZE = 500

# Private members: _leading_underscore
def _internal_helper():
```

**YAML (in config/):**
```yaml
# Entity IDs: domain.{scope}_{area}_{device}_{measurement}
sensor.home_kitchen_motion
light.office_bedroom_ceiling

# Automation IDs: lowercase with underscores
automation.kitchen_motion_lights

# Helper entities: descriptive with underscores
input_number.kitchen_light_brightness
```

**More Details**: See [config/CLAUDE.md](config/CLAUDE.md) for complete entity naming conventions.

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

The MCP server configuration is stored in `.mcp.json` (not tracked in git for security).

**Template file:** `.mcp.json.example` (committed to repository)

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

**Configuration Details:**
- `command: "uvx"` - Uses uvx to run the hass-mcp package (auto-installs if needed)
- `args: ["hass-mcp"]` - The MCP server package name
- `HA_URL` - Your Home Assistant URL (replace with your actual URL)
- `HA_TOKEN` - Your Home Assistant long-lived access token (replace with actual token)
- `disabled: false` - MCP server is enabled by default

**Security Note:**
- `.mcp.json` is in `.gitignore` and will NOT be committed
- This keeps your credentials secure and private

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

2. **Create your MCP configuration:**
   ```bash
   # Copy the template
   cp .mcp.json.example .mcp.json
   ```

3. **Generate Long-Lived Access Token:**
   - Open Home Assistant web interface
   - Navigate to: Profile → Security (bottom left corner → your profile)
   - Scroll to "Long-Lived Access Tokens" section
   - Click "Create Token"
   - Give it a name (e.g., "Claude MCP")
   - Copy the token immediately (you can't view it again!)

4. **Edit .mcp.json with your credentials:**
   ```bash
   # Open .mcp.json in your editor
   # Replace the following values:
   ```

   **Before:**
   ```json
   "HA_URL": "http://your_homeassistant_host:8123",
   "HA_TOKEN": "your_long_lived_access_token_here"
   ```

   **After (example):**
   ```json
   "HA_URL": "http://homeassistant.local:8123",
   "HA_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   ```

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
✅ Use /find-entities before creating automations
✅ Verify entities exist in registry
✅ Check Home Assistant docs when unsure
✅ Search existing automations for patterns
✅ Use MCP to check live entity states when debugging
✅ Use MCP to verify entities are online before deploying

❌ Don't guess entity names
❌ Don't assume services exist
❌ Don't skip entity discovery phase
❌ Don't assume entities are online without checking via MCP
```

#### MCP (Model Context Protocol) Best Practices
```markdown
✅ Use MCP for live state queries (homeassistant_get_states)
✅ Use MCP when debugging ("why isn't this triggering?")
✅ Check battery levels via MCP before trusting sensors
✅ Verify entities are available (state != 'unavailable')
✅ Test services exist before using (homeassistant_get_services)
✅ Use MCP to simulate automation execution

❌ Don't use MCP for discovering ALL entities (use entity registry files)
❌ Don't use MCP for metadata (area, device_class - use registry)
❌ Don't skip entity discovery - MCP supplements, doesn't replace
```

**When to use MCP vs Files:**
- **Files (entity registry)**: Discovery, metadata, disabled entities, relationships
- **MCP (live API)**: Current state, availability, battery levels, testing, debugging
- **Best**: Use BOTH - files for discovery, MCP for state verification

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

**More Details**: See [.claude-code/hooks/CLAUDE.md](.claude-code/hooks/CLAUDE.md) for complete hook documentation

## 🤖 Multi-Agent Development System

This repository includes a comprehensive **multi-agent system** for intelligent Home Assistant automation development.

**For complete agent documentation**, see:
- **[docs/AGENT_SYSTEM_GUIDE.md](docs/AGENT_SYSTEM_GUIDE.md)** - Complete user guide with examples, workflows, and API reference

### Quick Overview

The agent system provides:
- **10 Specialized Agents**: Entity discovery, automation design, validation, testing, documentation, best practices, refactoring, and dashboard design
- **Natural Language Automation**: Describe what you want, get production-ready YAML
- **Automated Testing**: Simulate scenarios before deployment
- **Auto-Documentation**: Generates docs, entity maps, and changelogs
- **Best Practices Enforcement**: Security, performance, and pattern analysis

### Getting Started with Agents

Use slash commands for guided workflows:

```bash
# Create new automation
/create-automation

# Review all automations
/review-automations

# Find entities
/find-entities motion sensors in the kitchen

# Debug automation
/debug-automation

# Design dashboard
/design-dashboard
```

**Learn More**: See [docs/AGENT_SYSTEM_GUIDE.md](docs/AGENT_SYSTEM_GUIDE.md)

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

**Note**: All python tools need to be run with `source venv/bin/activate && python <tool_path>`

## Project Structure

- `config/` - Contains all Home Assistant configuration files (synced from HA instance)
- `tools/` - Validation and testing scripts
- `agents/` - Multi-agent system for automation development
- `venv/` - Python virtual environment with dependencies
- `temp/` - Temporary directory for Claude to write and test code before moving to final locations
- `Makefile` - Commands for pulling/pushing configuration
- `.mcp.json` - Model Context Protocol server configuration
- `.claude-code/` - Project-specific Claude Code settings and hooks
  - `commands/` - Custom slash commands
  - `hooks/` - Validation hooks that run automatically
  - `settings.json` - Project configuration

## Validation System

This project includes comprehensive validation to prevent invalid configurations:

1. **YAML Syntax Validation** - Ensures proper YAML syntax with HA-specific tags
2. **Entity Reference Validation** - Checks that all referenced entities/devices exist
3. **Official HA Validation** - Uses Home Assistant's own validation tools

### Automated Validation Hooks

- **Post-Edit Hook**: Runs validation after editing any YAML files in `config/`
- **Pre-Push Hook**: Validates configuration before pushing to Home Assistant
- **Blocks invalid pushes**: Prevents uploading broken configurations

**More Details**: See [.claude-code/hooks/CLAUDE.md](.claude-code/hooks/CLAUDE.md)

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
- ✅ **Multi-Agent System**: AI-powered automation development

## Important Notes

- **Never push without validation**: The hooks prevent this, but be aware
- **Blueprint files** use `!input` tags which are normal and expected
- **Secrets are skipped** during validation for security
- **SSH access required** for pull/push operations
- **Python venv required** for validation tools
- **Entity naming convention**: See [config/CLAUDE.md](config/CLAUDE.md) for details

## Troubleshooting

### Validation Fails
1. Check YAML syntax errors first
2. Verify entity references exist in `.storage/` files
3. Run individual validators to isolate issues
4. Check HA logs if official validation fails
5. Use `/troubleshoot` for guided diagnostics

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
