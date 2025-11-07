## Home Assistant Agent System - User Guide

Welcome to the HA Agent System! This guide will help you make the most of the intelligent agent-based development workflow.

## 🎯 What is the Agent System?

The Agent System is a multi-agent AI architecture that helps you create, test, validate, and document Home Assistant automations with confidence. Think of it as having a team of specialists working together to ensure your automations are high-quality, secure, and maintainable.

## 🤖 The Agent Team

### **Orchestrator Agent** (The Coordinator)
- Manages complex workflows
- Routes requests to appropriate specialists
- Consolidates results
- Provides unified interface

### **Entity Discovery Agent** (The Explorer)
- Finds entities by natural language
- Context-aware suggestions
- Shows entity capabilities
- Identifies similar entities

### **Automation Designer Agent** (The Architect)
- Converts natural language to YAML
- Builds triggers, conditions, actions
- Understands patterns and templates
- Suggests improvements

### **Validation Agent** (The Quality Controller)
- 3-layer validation (YAML, references, official HA)
- Intelligent error parsing
- Specific fix suggestions
- Conflict detection

### **Testing Agent** (The QA Engineer)
- Simulates automations before deployment
- Tests multiple scenarios
- Identifies edge cases
- Prevents unexpected behavior

### **Documentation Agent** (The Librarian)
- Auto-generates markdown docs
- Creates entity relationship maps
- Maintains changelogs
- Keeps documentation synchronized

### **Best Practices Agent** (The Advisor)
- Security review
- Performance analysis
- Naming convention enforcement
- Pattern recognition

### **Refactoring Agent** (The Optimizer)
- Detects duplicate logic
- Suggests script extraction
- Optimizes performance
- Consolidates similar automations

---

## 🚀 Quick Start

### 1. Creating Your First Automation

Use the `/create-automation` command:

```
/create-automation

User: Turn on kitchen lights when motion is detected after sunset

System: 🤖 Creating automation...

Step 1: Finding entities...
  ✓ Found: binary_sensor.home_kitchen_motion
  ✓ Found: light.home_kitchen_ceiling
  ✓ Found: sun.sun

Step 2: Designing automation...
  ✓ Trigger: Motion detected
  ✓ Condition: Sun below horizon
  ✓ Action: Turn on light

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

Would you like me to:
1. Add the recommended timeout?
2. Deploy to Home Assistant?
3. Make other modifications?
```

### 2. Finding Entities

Use the `/find-entities` command:

```
/find-entities motion sensors in the kitchen

🔍 Found 2 entities

✅ binary_sensor.home_kitchen_motion (Kitchen)
   PIR Motion Sensor - Battery 95%
   Device class: motion

✅ binary_sensor.home_kitchen_motion_occupancy (Kitchen)
   Occupancy Sensor
   Device class: occupancy

💡 Suggestion:
  - Use 'home_kitchen_motion' for door entry detection
  - Use 'home_kitchen_motion_occupancy' for sustained presence
```

### 3. Reviewing Automations

Use the `/review-automations` command:

```
/review-automations

📊 Reviewing 23 automations...

Summary:
  ✓ Average quality score: 82/100
  ✓ Validation: All passed
  🔧 Refactoring opportunities: 5

🔴 Critical (1):
  1. Security: Remove hardcoded token in 'notify_on_door_open'

🟠 High Priority (3):
  1. Extract duplicate motion light pattern (used in 5 automations)
  2. Fix inefficient polling in 'temperature_monitor'
  3. Add availability check to 'garage_door_control'

🟡 Medium Priority (7):
  1. Consolidate 3 similar time-based lighting automations
  2. Document 5 undocumented automations
  ...

Would you like me to fix any of these issues?
```

### 4. Debugging Automations

Use the `/debug-automation` command:

```
/debug-automation

User: My kitchen lights automation isn't working

🔍 Debugging 'Kitchen Motion Lights'...

Configuration: ✅ Valid
Entities: ❌ Issues found
Triggers: ✅ Valid

🚨 Issues Found:

1. Entity 'binary_sensor.home_kitchen_motion' is disabled
   - Battery level: 5% (critically low)
   - Last update: 3 days ago
   - Status: Offline

💡 Solutions:

1. Replace battery in kitchen motion sensor
2. Re-enable entity in Home Assistant:
   - Settings → Devices & Services
   - Find device → Enable entity
3. Alternative: Use binary_sensor.home_kitchen_motion_occupancy instead
   (Currently active, battery 87%)

Would you like me to update the automation to use the alternative sensor?
```

---

## 📋 Common Workflows

### Creating Automation from Scratch

```python
from agents.orchestrator import OrchestratorAgent
from agents.shared_context import SharedContext

# Initialize
context = SharedContext()
orchestrator = OrchestratorAgent(context)

# Create automation
result = orchestrator.run(
    workflow='create_automation',
    description="Turn on living room lights at sunset if someone is home"
)

# Check result
if result.success:
    automation = result.data['automation']
    print(f"✅ Created: {automation['alias']}")

    # Review recommendations
    for rec in result.recommendations:
        print(f"[{rec['priority']}] {rec['description']}")

    # Write to file if user approves
    if user_approves:
        save_automation(automation)
```

### Validating Configuration

```python
# Run full validation
result = orchestrator.run(
    workflow='validate_config',
    validation_type='full'
)

if not result.success:
    print("❌ Validation failed:")
    for error in result.errors:
        print(f"  - {error}")

    # Get fix suggestions
    for rec in result.recommendations:
        print(f"💡 {rec['description']}")
```

### Finding and Using Entities

```python
# Search for entities
result = orchestrator.run(
    workflow='find_entities',
    query='temperature',
    domain='sensor',
    area='bedroom'
)

# Show results
for entity in result.data['entities']:
    print(f"{entity['entity_id']}: {entity['name']}")

# Get specific entity details
result = orchestrator.run(
    workflow='find_entities',
    entity_id='sensor.home_bedroom_temperature'
)

entity = result.data['entity']
print(f"Device class: {entity['device_class']}")
print(f"Capabilities: {entity['capabilities']}")
print(f"Used in: {entity['used_in_automations']}")
```

### Refactoring Automations

```python
# Analyze all automations
result = orchestrator.run(
    workflow='refactor_automations',
    refactor_type='all'
)

# Show opportunities
summary = result.data['summary']
print(f"Duplicate patterns: {summary['duplicate_patterns']}")
print(f"Script opportunities: {summary['script_opportunities']}")
print(f"Optimizations: {summary['optimizations']}")

# Get specific recommendations
for rec in result.recommendations:
    if rec['priority'] == 'high':
        print(f"🟠 {rec['description']}")
```

---

## 🎓 Best Practices

### 1. Always Use Entity Discovery First

Before creating automations, explore available entities:

```
/find-entities [what you're looking for]
```

This ensures you use the correct entity IDs and understand what's available.

### 2. Review Recommendations

The agents provide intelligent recommendations. Always review them before deploying:

- 🔴 Critical: Security issues, must fix
- 🟠 High: Performance or reliability issues
- 🟡 Medium: Best practices and optimizations
- 🟢 Low: Nice-to-haves and refinements

### 3. Test Before Deploying

The Testing Agent runs scenarios. Review the results:

```
✓ Scenario 1: Motion at 2 PM → No action
✓ Scenario 2: Motion at 9 PM → Lights on
⚠️ Edge case: No timeout, lights stay on indefinitely
```

Address warnings before deployment.

### 4. Document as You Go

The Documentation Agent auto-generates docs. Keep them updated:

```python
# After creating/modifying automation
orchestrator.run(
    workflow='document_automations',
    automation=updated_automation
)
```

### 5. Regular Reviews

Run periodic reviews to maintain quality:

```
/review-automations  # Monthly or after major changes
```

---

## 🔧 Advanced Usage

### Custom Workflows

You can combine agents for custom workflows:

```python
# Custom workflow: Create + Optimize + Document
context = SharedContext()

# Step 1: Create
designer = AutomationDesignerAgent(context)
design_result = designer.run(description="...")
automation = design_result.data['automation']

# Step 2: Optimize
best_practices = BestPracticesAgent(context)
bp_result = best_practices.run(automation=automation)

# Apply recommendations
if bp_result.recommendations:
    automation = apply_recommendations(automation, bp_result.recommendations)

# Step 3: Validate
validation = ValidationAgent(context)
val_result = validation.run(automation=automation)

# Step 4: Document
documentation = DocumentationAgent(context)
doc_result = documentation.run(automation=automation)
```

### Accessing Individual Agents

```python
orchestrator = OrchestratorAgent(context)

# Get specific agent
entity_agent = orchestrator.get_agent('entity_discovery')
result = entity_agent.run(query="motion sensors")

# List all agents
for agent_info in orchestrator.list_agents():
    print(f"{agent_info['name']}: {agent_info['description']}")
```

### Using Shared Context

The SharedContext stores state across agents:

```python
context = SharedContext()

# Access registries
entities = context.get_entities()
devices = context.get_devices()
areas = context.get_areas()

# Search
results = context.search_entities("kitchen")

# Check entity existence
if context.entity_exists('light.kitchen'):
    entity = context.get_entity('light.kitchen')

# Get automations
automations = context.get_automations()
automation = context.get_automation('kitchen_motion_lights')

# Inter-agent communication
context.send_message('agent1', 'agent2', {'data': 'value'})
messages = context.get_messages('agent2')

# Shared data
context.set_data('key', value)
value = context.get_data('key')
```

---

## 🐛 Troubleshooting

### "Agent failed to load registries"

**Cause**: Entity registry files not found

**Solution**:
```bash
# Pull latest config from HA
make pull

# Verify files exist
ls config/.storage/core.entity_registry
```

### "Validation tools not found"

**Cause**: Tools directory not in path

**Solution**:
```bash
# Activate venv
source venv/bin/activate

# Install dependencies
pip install homeassistant voluptuous pyyaml
```

### "Context not initialized"

**Cause**: SharedContext not passed to agent

**Solution**:
```python
# Always create context first
context = SharedContext()

# Pass to orchestrator
orchestrator = OrchestratorAgent(context)
```

### "Entity not found"

**Cause**: Entity doesn't exist or is disabled

**Solution**:
```
/find-entities [entity name]

# Check status and find alternatives
# Use debug workflow to diagnose
/debug-automation
```

---

## 📚 Additional Resources

- [CLAUDE.md](../CLAUDE.md) - Project instructions for Claude Code
- [Agent API Reference](./AGENT_API.md) - Detailed API documentation
- [Best Practices Guide](./best_practices/automation_patterns.md) - Automation patterns
- [Entity Naming Convention](./entities/naming_convention.md) - Naming standards

---

## 🎉 Examples

Check out the example workflows in `docs/examples/`:

- `creating_motion_light.md` - Complete motion-activated light
- `debugging_failed_automation.md` - Debugging walkthrough
- `refactoring_duplicates.md` - Extract common patterns
- `batch_documentation.md` - Document all automations

---

**Need Help?**

The agent system is designed to be interactive and helpful. Don't hesitate to:

1. Ask questions: "How do I...?"
2. Request explanations: "Why is this recommended?"
3. Try workflows: Use slash commands to explore
4. Experiment: The validation layer keeps you safe

Happy automating! 🏠✨
