# CEO Briefing Skill

**Description**: Generate weekly Monday Morning CEO Briefing with revenue analysis, task completion, bottlenecks, and proactive suggestions.

## Capabilities

- Analyze completed tasks from /Done folder
- Calculate revenue from Odoo accounting
- Identify bottlenecks and delays
- Generate proactive cost optimization suggestions
- Create executive summary reports
- Track business metrics and KPIs

## Setup

1. **Install Dependencies**:
```bash
cd .claude/skills/ceo-briefing
pip install -r requirements.txt
```

2. **Configure Odoo Connection**:
```bash
cp .env.example .env
# Edit .env with your Odoo credentials
```

3. **Test Generation**:
```bash
python scripts/generate_briefing.py \
  --vault "../../AI_Employee_Vault" \
  --date-from "2026-03-15" \
  --date-to "2026-03-21"
```

## Briefing Components

### 1. Executive Summary
- Overall week performance
- Key achievements
- Critical issues

### 2. Revenue Analysis
- Weekly revenue total
- Month-to-date progress
- Comparison to targets
- Revenue by customer

### 3. Task Completion
- Tasks completed this week
- Tasks in progress
- Overdue tasks
- Completion rate

### 4. Bottleneck Analysis
- Tasks that took longer than expected
- Blocked tasks
- Resource constraints
- Process inefficiencies

### 5. Proactive Suggestions
- Cost optimization opportunities
- Subscription audit
- Process improvements
- Upcoming deadlines

## Scheduled Generation

Use with scheduler skill for automatic weekly briefings:

```bash
# Windows Task Scheduler
python scripts/schedule_briefing.py --platform windows

# Linux/Mac cron
python scripts/schedule_briefing.py --platform unix
```

Default schedule: Sunday 7:00 PM (ready for Monday morning)

## Briefing Template

Generated briefings follow this structure:

```markdown
---
generated: 2026-03-21T19:00:00Z
period: 2026-03-15 to 2026-03-21
week_number: 12
---

# Monday Morning CEO Briefing

## Executive Summary
[High-level overview]

## Revenue
- **This Week**: $X,XXX
- **MTD**: $X,XXX (XX% of target)
- **Trend**: [On track / Behind / Ahead]

## Completed Tasks
- [x] Task 1
- [x] Task 2

## Bottlenecks
| Task | Expected | Actual | Delay |
|------|----------|--------|-------|
| ... | ... | ... | ... |

## Proactive Suggestions
### Cost Optimization
- [Suggestion 1]

### Upcoming Deadlines
- [Deadline 1]
```

## Integration with Business Goals

The briefing reads from `AI_Employee_Vault/Business_Goals.md`:

```markdown
---
last_updated: 2026-03-21
review_frequency: weekly
---

## Q1 2026 Objectives

### Revenue Target
- Monthly goal: $10,000
- Current MTD: $4,500

### Key Metrics to Track
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Client response time | < 24 hours | > 48 hours |
| Invoice payment rate | > 90% | < 80% |
```

## Odoo Integration

Briefing pulls data from Odoo:
- Posted invoices (revenue)
- Customer payments
- Outstanding invoices
- Expense tracking

## Usage in Claude Code

```python
# Trigger briefing generation
from datetime import datetime, timedelta

# Calculate last week
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

# Generate briefing
briefing = generate_ceo_briefing(
    vault_path="AI_Employee_Vault",
    date_from=start_date.strftime("%Y-%m-%d"),
    date_to=end_date.strftime("%Y-%m-%d")
)

# Save to Briefings folder
briefing_file = f"AI_Employee_Vault/Briefings/{end_date.strftime('%Y-%m-%d')}_Monday_Briefing.md"
with open(briefing_file, 'w') as f:
    f.write(briefing)
```

## Customization

Edit `scripts/briefing_template.py` to customize:
- Metrics tracked
- Alert thresholds
- Report sections
- Formatting

## Security

- Briefings contain sensitive business data
- Store in vault (not public)
- Review before sharing
- Redact sensitive info if needed

## Troubleshooting

**No revenue data**:
- Check Odoo connection
- Verify invoices are posted
- Check date range

**Missing tasks**:
- Ensure tasks moved to /Done
- Check file format
- Verify date metadata

**Incorrect calculations**:
- Verify Business_Goals.md format
- Check Odoo data accuracy
- Review date ranges

## Resources

- [Business Goals Template](../../AI_Employee_Vault/Business_Goals.md)
- [Odoo Revenue Reports](https://www.odoo.com/documentation/19.0/applications/finance/accounting/reporting.html)
