---
description: Create automation using Product Requirements Prompt (PRP) framework for one-pass implementation
---

Create a comprehensive automation using the **PRP (Product Requirements Prompt) framework**. This approach emphasizes thorough research and context gathering before implementation to achieve "one-pass implementation success."

## Overview

The PRP framework reduces iteration cycles by ensuring comprehensive context is gathered upfront. Rather than vague requirements, you'll create a detailed blueprint with all necessary context, patterns, validation gates, and error handling.

## Phase 1: Research and Context Gathering

### 1.1 Entity Discovery
Use `/find-entities` to discover relevant entities:

```bash
# Example searches:
/find-entities motion sensors in kitchen
/find-entities climate entities
/find-entities person tracking
```

**Document:**
- Exact entity IDs (e.g., `binary_sensor.home_kitchen_motion`)
- Current states (via MCP if available)
- Attributes needed (battery_level, temperature, etc.)
- Entity availability (is it online and responding?)

### 1.2 Pattern Research
Search existing automations for similar patterns:

```bash
# Search for similar automation patterns
rg "motion" config/automations.yaml
rg "climate" config/automations.yaml
rg "person.*state" config/automations.yaml
```

**Document:**
- Similar automation patterns found
- Trigger structures used
- Condition patterns
- Action sequences
- Error handling approaches

### 1.3 Service Documentation
Verify services exist and understand their parameters:

**Via MCP (if available):**
```python
# Use homeassistant_get_services tool
# Example: Check light.turn_on parameters
```

**Via Home Assistant docs:**
- https://www.home-assistant.io/integrations/
- Service call parameters
- Supported features

**Document:**
- Services needed (e.g., `light.turn_on`, `climate.set_temperature`)
- Required parameters
- Optional parameters
- Response types

### 1.4 Live State Verification
**CRITICAL**: Use MCP to verify entities before creating automation:

```python
# Check entity availability
state = homeassistant_get_states(entity_id="binary_sensor.home_kitchen_motion")

# Verify:
- state['state'] != 'unavailable'  # Entity is online
- battery_level > 20%  # For battery devices
- last_changed is recent  # Entity is updating
```

**Document:**
- Which entities are currently online
- Battery levels for battery-powered devices
- Last update timestamps
- Any entities that need attention before deployment

### 1.5 User Clarification
Ask specific questions about requirements:

**Trigger Questions:**
- What should trigger this automation?
- Should it run on state change, time, event, or other?
- Any specific conditions for the trigger (e.g., only during certain hours)?

**Condition Questions:**
- What conditions must be met?
- Are there time-based conditions?
- State-based conditions?
- Should multiple conditions use AND or OR logic?

**Action Questions:**
- What should happen when triggered?
- Should actions run in sequence or parallel?
- Are there delays between actions?
- What should happen if an action fails?

**Edge Case Questions:**
- What if an entity is unavailable?
- What if multiple people trigger simultaneously?
- What should happen on HA restart?
- Should state be restored after interruption?

## Phase 2: Blueprint Creation

### 2.1 Requirements Document

Create a structured requirements document:

```markdown
## Automation: [Clear, Descriptive Name]

### Purpose
[One-sentence description of what this automation does and why]

### Entities Involved
**Triggers:**
- entity_id: [exact ID]
- platform: [state/time/event/etc.]
- current_state: [from MCP]
- availability: [online/offline]

**Conditions:**
- entity_id: [exact ID]
- condition_type: [state/time/numeric_state/etc.]
- current_state: [from MCP]

**Actions:**
- service: [exact service name]
- entity_id: [exact ID]
- parameters: [specific values]
- current_state: [from MCP]

### Trigger Logic
[Detailed explanation with specific values]

### Condition Logic
[Detailed explanation with AND/OR relationships]

### Action Sequence
1. [First action with parameters]
2. [Second action with parameters]
3. [etc.]

### Edge Cases
- **Entity unavailable:** [How to handle]
- **State conflict:** [How to handle]
- **Timing issues:** [How to handle]
- **Multiple triggers:** [How to handle]

### Similar Patterns Found
[Reference to existing automations with similar structure]
```

### 2.2 Pseudocode Implementation

Write pseudocode before YAML:

```
TRIGGER:
  IF binary_sensor.home_kitchen_motion changes to 'on'
  AND time is after sunset

CONDITION:
  IF light.kitchen is 'off'
  AND person.home is 'home'

ACTION:
  1. Turn on light.kitchen with brightness 80%
  2. Wait 5 minutes
  3. IF binary_sensor.home_kitchen_motion is 'off'
     THEN turn off light.kitchen
     ELSE extend timer by 5 minutes

ERROR HANDLING:
  IF light.kitchen is unavailable:
    - Log error
    - Send notification
    - Skip action gracefully
```

### 2.3 File Planning

Determine which files need modification:

**Single-file automation:**
- config/automations.yaml only

**Multi-file automation:**
- config/configuration.yaml (for helper entities like input_number)
- config/scripts.yaml (for reusable script)
- config/automations.yaml (for automation)

**Document dependency order:**
1. Create helpers first (configuration.yaml)
2. Create scripts second (scripts.yaml)
3. Create automation last (automations.yaml)

## Phase 3: Implementation

### 3.1 YAML Generation

Generate the actual YAML following discovered patterns:

```yaml
- id: 'unique_id_here'
  alias: "Clear Descriptive Name"
  description: "One-sentence purpose"

  trigger:
    # [Implement trigger from blueprint]

  condition:
    # [Implement conditions from blueprint]

  action:
    # [Implement action sequence from blueprint]

  mode: single  # or restart/queued/parallel based on requirements
```

### 3.2 Helper Entities (if needed)

If the automation needs configurable values:

```yaml
# In config/configuration.yaml
input_number:
  kitchen_light_brightness:
    name: "Kitchen Light Brightness"
    min: 0
    max: 100
    step: 5
    initial: 80
    unit_of_measurement: "%"
```

### 3.3 Reusable Scripts (if needed)

For complex action sequences used by multiple automations:

```yaml
# In config/scripts.yaml
kitchen_motion_lights:
  alias: "Kitchen Motion Lights"
  sequence:
    - service: light.turn_on
      target:
        entity_id: light.kitchen
      data:
        brightness_pct: "{{ states('input_number.kitchen_light_brightness') | int }}"
```

## Phase 4: Validation Gates

### 4.1 Pre-Deployment Validation

Run complete validation suite:

```bash
# All validations
/validate-config

# Or manually:
make validate
```

**Must pass:**
- YAML syntax validation
- Entity reference validation
- Official HA validation

### 4.2 Test Scenarios

Define specific test scenarios:

```markdown
## Test Plan

### Scenario 1: Normal Operation
1. Trigger condition: [specific action to trigger]
2. Expected state before: [entity states]
3. Expected state after: [entity states]
4. Expected actions: [what should happen]

### Scenario 2: Edge Case - Entity Unavailable
1. Trigger condition: [specific action]
2. Entity state: unavailable
3. Expected behavior: [graceful handling]

### Scenario 3: Edge Case - Multiple Triggers
1. Trigger condition: [rapid triggers]
2. Expected behavior: [based on mode setting]
```

### 4.3 MCP-Based Testing

If MCP is available, simulate scenarios:

```python
# Verify automation would trigger correctly
current_state = homeassistant_get_states(entity_id="trigger_entity")
print(f"Current state: {current_state['state']}")
print(f"Would trigger: {current_state['state'] == 'expected_value'}")

# Test service calls
homeassistant_call_service(
    domain="light",
    service="turn_on",
    service_data={
        "entity_id": "light.kitchen",
        "brightness_pct": 80
    }
)
```

## Phase 5: Confidence Assessment

### 5.1 Confidence Score (1-10)

Rate confidence that automation will work on first try:

**10/10 - Extremely Confident:**
- All entities verified online via MCP
- Similar patterns found and tested
- All edge cases handled
- Complete validation passed
- Test scenarios successful

**7-9/10 - Confident:**
- Most entities verified
- Pattern found but not identical
- Main edge cases handled
- Validation passed

**4-6/10 - Moderate:**
- Some entities not verified
- Pattern similar but requires adaptation
- Some edge cases not handled
- Validation passed with warnings

**1-3/10 - Low:**
- Entities not verified
- New pattern, no reference
- Edge cases unclear
- Validation issues

### 5.2 Risk Assessment

Document potential risks:

```markdown
## Risk Assessment

**High Risk:**
- [Entity X is battery-powered with 15% battery - may go offline]

**Medium Risk:**
- [No similar pattern found - new trigger type]

**Low Risk:**
- [All entities online and responding]

**Mitigation:**
- [Replace battery before deployment]
- [Test trigger manually before enabling]
- [Monitor for first 24 hours]
```

## Phase 6: Deployment

### 6.1 Safe Deployment

Use `/safe-deploy` for validated deployment:

```bash
/safe-deploy
```

Or manual deployment with validation:

```bash
make validate  # Ensure passing
make push      # Deploy to HA
```

### 6.2 Post-Deployment Monitoring

**First 24 hours:**
- Monitor automation in HA UI (Settings → Automations & Scenes)
- Check logbook for execution history
- Verify trigger conditions are being met
- Confirm actions are executing as expected

**Via MCP (if available):**
```python
# Check automation state
automation_state = homeassistant_get_states(entity_id="automation.your_automation")
print(f"State: {automation_state['state']}")
print(f"Last triggered: {automation_state['attributes'].get('last_triggered')}")
```

### 6.3 Iteration (if needed)

If issues are found:
1. Document the specific failure
2. Update the requirements document
3. Modify implementation
4. Re-run validation
5. Re-deploy

## Success Criteria

A complete PRP-based automation includes:

- ✅ Comprehensive entity discovery with live state verification
- ✅ Similar pattern research and references
- ✅ Detailed requirements document
- ✅ Pseudocode implementation
- ✅ Edge case identification and handling
- ✅ Complete YAML implementation
- ✅ Validation gates (all passing)
- ✅ Test scenarios defined
- ✅ Confidence score with justification
- ✅ Risk assessment with mitigation
- ✅ Post-deployment monitoring plan

## Benefits of PRP Approach

**Compared to ad-hoc automation creation:**

- 🎯 **Higher first-pass success rate**: Thorough research reduces iterations
- 🔍 **Better edge case handling**: Systematic identification prevents issues
- 📚 **Reusable patterns**: Documentation helps future automations
- 🛡️ **Lower deployment risk**: Validation and testing before deployment
- 📖 **Better documentation**: Requirements document serves as reference
- 🔧 **Easier debugging**: Clear understanding of expected behavior

## When to Use PRP

**Use PRP for:**
- Complex automations with multiple conditions/actions
- Critical automations (security, climate, safety)
- Automations involving multiple files
- New patterns not yet established
- Automations with many edge cases

**Use regular `/create-automation` for:**
- Simple single-trigger, single-action automations
- Well-established patterns
- Quick prototypes for testing
- Automations with minimal edge cases

## Example: Complete PRP Workflow

See [config/CLAUDE.md](../../config/CLAUDE.md) for complete example of PRP-based automation creation.

## Related Commands

- `/find-entities` - Discover entities (Phase 1.1)
- `/validate-config` - Run validation (Phase 4.1)
- `/safe-deploy` - Deploy with validation (Phase 6.1)
- `/debug-automation` - Troubleshoot after deployment (Phase 6.3)
- `/create-automation` - Simpler workflow for basic automations
