---
name: scheduler
description: |
  Schedule recurring tasks and automated workflows using cron (Linux/Mac) or Task
  Scheduler (Windows). Creates scheduled jobs for daily briefings, weekly audits,
  and periodic task processing. Use this skill when you need to automate recurring
  operations or schedule future actions.
---

# Scheduler

Automate recurring tasks with intelligent scheduling.

## Core Workflow

1. **Define** recurring tasks and schedules
2. **Create** cron jobs or scheduled tasks
3. **Monitor** execution and results
4. **Log** all scheduled operations
5. **Alert** on failures or missed runs

## Usage

```bash
# Set up scheduling
/scheduler

# Or invoke directly
claude "Schedule daily briefing at 8 AM"
claude "Create weekly audit every Monday"
```

## What This Skill Does

### Task Scheduling
- Creates cron jobs (Linux/Mac) or Task Scheduler tasks (Windows)
- Supports one-time and recurring schedules
- Handles multiple time zones
- Manages schedule conflicts

### Automated Workflows
- Daily CEO briefing generation
- Weekly business audits
- Periodic inbox processing
- Regular backup operations

### Monitoring & Alerts
- Tracks execution history
- Detects missed runs
- Alerts on failures
- Provides execution reports

## Schedule Types

### Daily Tasks
```markdown
# Daily CEO Briefing - 8:00 AM
---
schedule: daily
time: 08:00
task: generate_ceo_briefing
enabled: true
---

Generates morning briefing with:
- Yesterday's completed tasks
- Today's priorities
- Revenue updates
- Pending approvals
```

### Weekly Tasks
```markdown
# Weekly Business Audit - Monday 9:00 AM
---
schedule: weekly
day: monday
time: 09:00
task: business_audit
enabled: true
---

Performs comprehensive audit:
- Revenue analysis
- Task completion rates
- Subscription review
- Bottleneck identification
```

### Periodic Tasks
```markdown
# Process Inbox - Every 30 minutes
---
schedule: periodic
interval: 30m
task: process_inbox
enabled: true
---

Checks for new items in:
- /Needs_Action folder
- Email inbox
- WhatsApp messages
```

## Platform-Specific Implementation

### Linux/Mac (Cron)

```bash
# Edit crontab
crontab -e

# Daily briefing at 8 AM
0 8 * * * cd /path/to/vault && claude "Generate daily CEO briefing"

# Weekly audit every Monday at 9 AM
0 9 * * 1 cd /path/to/vault && claude "Run weekly business audit"

# Process inbox every 30 minutes
*/30 * * * * cd /path/to/vault && claude "/ai-employee-processor"

# Hourly LinkedIn check (avoid :00 minute - use :07 for load distribution)
7 * * * * cd /path/to/vault && claude "Check LinkedIn for engagement"
```

### Windows (Task Scheduler)

```powershell
# Create daily briefing task
$action = New-ScheduledTaskAction -Execute "claude" -Argument "Generate daily CEO briefing" -WorkingDirectory "C:\path\to\vault"
$trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM
Register-ScheduledTask -TaskName "AI_Employee_Daily_Briefing" -Action $action -Trigger $trigger

# Create weekly audit task
$action = New-ScheduledTaskAction -Execute "claude" -Argument "Run weekly business audit" -WorkingDirectory "C:\path\to\vault"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9:00AM
Register-ScheduledTask -TaskName "AI_Employee_Weekly_Audit" -Action $action -Trigger $trigger

# Create periodic inbox processing (every 30 minutes)
$action = New-ScheduledTaskAction -Execute "claude" -Argument "/ai-employee-processor" -WorkingDirectory "C:\path\to\vault"
$trigger = New-ScheduledTaskTrigger -Once -At 12:00AM -RepetitionInterval (New-TimeSpan -Minutes 30) -RepetitionDuration ([TimeSpan]::MaxValue)
Register-ScheduledTask -TaskName "AI_Employee_Process_Inbox" -Action $action -Trigger $trigger
```

## Schedule Configuration File

```yaml
# /Vault/Schedules/schedules.yaml
schedules:
  - name: daily_briefing
    description: Generate morning CEO briefing
    schedule: "0 8 * * *"  # 8 AM daily
    command: "claude 'Generate daily CEO briefing'"
    enabled: true
    notify_on_failure: true

  - name: weekly_audit
    description: Comprehensive business audit
    schedule: "0 9 * * 1"  # 9 AM Monday
    command: "claude 'Run weekly business audit'"
    enabled: true
    notify_on_failure: true

  - name: process_inbox
    description: Process pending tasks
    schedule: "*/30 * * * *"  # Every 30 minutes
    command: "claude '/ai-employee-processor'"
    enabled: true
    notify_on_failure: false

  - name: linkedin_engagement
    description: Check LinkedIn activity
    schedule: "7 * * * *"  # Every hour at :07
    command: "claude 'Check LinkedIn for comments and engagement'"
    enabled: true
    notify_on_failure: false

  - name: backup_vault
    description: Backup Obsidian vault
    schedule: "0 0 * * *"  # Midnight daily
    command: "python3 scripts/backup_vault.py"
    enabled: true
    notify_on_failure: true
```

## Cron Expression Guide

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
│ │ │ │ │
* * * * *

Examples:
0 8 * * *        - 8:00 AM every day
0 9 * * 1        - 9:00 AM every Monday
*/30 * * * *     - Every 30 minutes
0 */2 * * *      - Every 2 hours
0 0 1 * *        - First day of every month at midnight
0 0 * * 0        - Every Sunday at midnight
```

## Scheduled Task Templates

### Daily CEO Briefing

```markdown
# Task: Generate Daily CEO Briefing
# Schedule: 8:00 AM daily
# Duration: ~2 minutes

## Actions
1. Read /Done folder for yesterday's completed tasks
2. Read /Needs_Action for today's priorities
3. Check /Accounting for recent transactions
4. Review /Pending_Approval for items needing attention
5. Generate briefing in /Briefings/YYYY-MM-DD_briefing.md
6. Update Dashboard.md with summary

## Output Format
- Executive summary (2-3 sentences)
- Key metrics (revenue, tasks completed)
- Today's priorities (top 5)
- Alerts and bottlenecks
- Proactive suggestions
```

### Weekly Business Audit

```markdown
# Task: Weekly Business Audit
# Schedule: Monday 9:00 AM
# Duration: ~5 minutes

## Actions
1. Analyze last 7 days of transactions
2. Review task completion rates
3. Check subscription usage
4. Identify bottlenecks
5. Calculate weekly revenue
6. Generate audit report
7. Create action items for improvements

## Output Format
- Week overview
- Revenue analysis
- Task metrics
- Subscription audit
- Bottleneck report
- Recommendations
```

### Inbox Processing

```markdown
# Task: Process Inbox
# Schedule: Every 30 minutes
# Duration: ~1 minute

## Actions
1. Scan /Needs_Action folder
2. Prioritize items by urgency
3. Create plans for complex tasks
4. Generate approval requests
5. Update Dashboard
6. Log processing results

## Output Format
- Items processed count
- New plans created
- Approvals requested
- Errors encountered
```

## Execution Logging

```markdown
# /Logs/Scheduler_Log_2026-03-15.md
---
date: 2026-03-15
total_runs: 48
successful: 47
failed: 1
---

## Execution History

### 08:00 - Daily CEO Briefing
**Status:** ✅ Success
**Duration:** 1m 23s
**Output:** /Briefings/2026-03-15_briefing.md
**Notes:** Generated successfully

### 08:30 - Process Inbox
**Status:** ✅ Success
**Duration:** 45s
**Items processed:** 3
**Notes:** 2 plans created, 1 approval requested

### 09:00 - Weekly Business Audit
**Status:** ✅ Success
**Duration:** 4m 12s
**Output:** /Audits/2026-03-15_weekly_audit.md
**Notes:** Identified 2 optimization opportunities

### 09:30 - Process Inbox
**Status:** ❌ Failed
**Duration:** 30s
**Error:** Network timeout connecting to Gmail API
**Notes:** Will retry on next run

## Statistics
- Success rate: 97.9%
- Average duration: 1m 45s
- Most reliable: Daily briefing (100%)
- Needs attention: Gmail API connection
```

## Failure Handling

### Retry Logic

```python
# retry_handler.py
import time
import logging

def execute_with_retry(task, max_attempts=3):
    """Execute scheduled task with retry logic"""

    for attempt in range(max_attempts):
        try:
            result = task.execute()
            log_success(task, result)
            return result

        except TransientError as e:
            if attempt < max_attempts - 1:
                delay = 2 ** attempt  # Exponential backoff
                logging.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s")
                time.sleep(delay)
            else:
                log_failure(task, e)
                notify_human(task, e)
                raise

        except PermanentError as e:
            log_failure(task, e)
            notify_human(task, e)
            raise
```

### Alert Configuration

```markdown
# /Vault/Schedules/alert_config.md
---
alert_settings:
  email: your@email.com
  slack_webhook: https://hooks.slack.com/...
  critical_tasks:
    - daily_briefing
    - weekly_audit
  alert_on:
    - consecutive_failures: 3
    - execution_time_exceeded: 300  # 5 minutes
    - missed_runs: 2
---

## Alert Templates

### Failure Alert
Subject: ⚠️ Scheduled Task Failed: {task_name}
Body: The scheduled task "{task_name}" failed at {timestamp}.
Error: {error_message}
Next scheduled run: {next_run}

### Missed Run Alert
Subject: ⚠️ Scheduled Task Missed: {task_name}
Body: The scheduled task "{task_name}" did not execute at {expected_time}.
Possible causes: System offline, scheduler not running
```

## Schedule Management Commands

```bash
# List all schedules
claude "List all scheduled tasks"

# Enable/disable schedule
claude "Disable daily briefing schedule"
claude "Enable weekly audit schedule"

# Modify schedule
claude "Change daily briefing time to 7 AM"
claude "Run inbox processing every 15 minutes instead of 30"

# Manual execution
claude "Run daily briefing now"
claude "Execute weekly audit immediately"

# View execution history
claude "Show scheduler logs for today"
claude "Show failed scheduled tasks this week"
```

## Best Practices

### Timing Considerations
- Avoid :00 and :30 minutes for load distribution
- Schedule heavy tasks during off-peak hours
- Consider time zones for global operations
- Leave buffer time between dependent tasks

### Resource Management
- Limit concurrent scheduled tasks
- Monitor system resources
- Set execution timeouts
- Clean up old logs regularly

### Reliability
- Test schedules before enabling
- Monitor execution success rates
- Set up failure alerts
- Maintain backup schedules

## Silver Tier Capabilities

✅ Create cron jobs or scheduled tasks
✅ Support daily, weekly, and periodic schedules
✅ Execute automated workflows
✅ Log all executions
✅ Handle failures with retry logic
✅ Alert on critical failures
✅ Cross-platform support (Windows/Linux/Mac)

## Future Enhancements (Gold Tier)

- Dynamic schedule adjustment based on workload
- Dependency management between tasks
- Distributed scheduling across multiple machines
- Advanced failure recovery strategies
- Schedule optimization recommendations
- Integration with calendar for conflict detection

## Troubleshooting

**Scheduled task not running:**
- Verify cron daemon is running (Linux/Mac)
- Check Task Scheduler service (Windows)
- Review cron syntax
- Check file permissions
- Verify working directory path

**Task runs but fails:**
- Check execution logs
- Verify environment variables
- Test command manually
- Review resource availability
- Check network connectivity

**Missed executions:**
- System was offline during scheduled time
- Scheduler service not running
- System clock incorrect
- Task disabled in configuration

## Security Considerations

- Run scheduled tasks with minimal privileges
- Secure credential storage for API access
- Limit network access for scheduled tasks
- Audit scheduled task modifications
- Monitor for unauthorized schedule changes

---
*Part of the Silver Tier AI Employee implementation*
