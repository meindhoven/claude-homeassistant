---
description: Review all automations for issues and improvement opportunities
---

You are running the **Review Automations** workflow using the Home Assistant Agent System.

Your task is to comprehensively review all existing automations and provide actionable recommendations.

## Workflow Steps

Execute the complete review workflow:

1. **Load Automations**: Load all automations from config/automations.yaml
2. **Best Practices Review**: Check each automation for security, performance, naming issues
3. **Refactoring Analysis**: Find duplicates, script extraction opportunities
4. **Validation**: Ensure all configurations are valid
5. **Generate Report**: Summarize findings with prioritized recommendations

## Implementation

```python
from agents.orchestrator import OrchestratorAgent
from agents.shared_context import SharedContext

# Initialize
context = SharedContext()
orchestrator = OrchestratorAgent(context)

# Run review workflow
result = orchestrator.run(workflow='review_automations')

# Present comprehensive report
print(result.message)
print(f"\n📊 Summary:")
print(f"  Automations reviewed: {result.data['automations_reviewed']}")
print(f"  Average quality score: {result.data['summary']['average_quality_score']:.1f}/100")
print(f"  Validation: {'✅ Passed' if result.data['summary']['validation_passed'] else '❌ Failed'}")

print(f"\n🔧 Top Recommendations:")
for idx, rec in enumerate(result.recommendations[:10], 1):
    priority_icon = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    }.get(rec['priority'], '⚪')
    print(f"  {idx}. {priority_icon} {rec['description']}")
```

## Report Sections

Present findings in these categories:

1. **Security Issues** (Critical priority)
2. **Performance Problems** (High priority)
3. **Refactoring Opportunities** (Medium priority)
4. **Naming Inconsistencies** (Low priority)
5. **Documentation Gaps** (Low priority)

## User Actions

After presenting the report, ask the user:
- Which issues would you like me to fix?
- Should I implement the refactoring suggestions?
- Would you like me to document all automations?
