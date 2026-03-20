# Silver Tier - AI Employee Skills

Advanced automation capabilities for your Personal AI Employee.

## Overview

Silver Tier transforms your Bronze Tier foundation into a **Functional Assistant** with:

- 📧 **Email automation** via Gmail API
- 💼 **LinkedIn posting** for business development
- 💬 **WhatsApp messaging** via Web automation
- ⏰ **Intelligent scheduling** for recurring tasks
- ✅ **Approval workflow** for safe autonomous operations

## Skills Included

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| **linkedin-poster** | Automate LinkedIn presence | Post generation, engagement tracking, lead detection |
| **email-sender** | Send emails with safety | Gmail API, approval workflow, templates |
| **whatsapp-messenger** | Manage WhatsApp comms | Message monitoring, auto-replies, lead detection |
| **scheduler** | Automate recurring tasks | Cron jobs, daily briefings, weekly audits |
| **approval-manager** | Human-in-the-loop safety | Approval workflow, action execution, logging |

## Quick Start

### 1. Prerequisites

Ensure Bronze Tier is complete:
```bash
# Verify Bronze Tier skills exist
ls .claude/skills/ai-employee-processor
ls .claude/skills/browsing-with-playwright
```

### 2. Setup (3-4 hours)

Follow the detailed setup guide:
```bash
# Read setup instructions
cat SILVER_TIER_SETUP.md
```

Key setup steps:
1. Gmail API authorization
2. WhatsApp Web login via Playwright
3. LinkedIn login via Playwright
4. Configure scheduled tasks
5. Update Company_Handbook.md

### 3. Test Skills

```bash
# Test email sending
claude "Draft test email to yourself"

# Test LinkedIn posting
claude "Create LinkedIn post about Silver Tier completion"

# Test WhatsApp messaging
claude "Draft WhatsApp message to test contact"

# Test scheduler
claude "Generate daily CEO briefing"

# Test approval workflow
claude "/approval-manager"
```

## Usage Examples

### Send Invoice Email

```bash
# Create email request
claude "Send invoice email to client@example.com with attachment /Vault/Invoices/2026-03.pdf"

# Review approval in /Pending_Approval
# Move to /Approved when ready

# Execute approved action
claude "/approval-manager"
```

### Post to LinkedIn

```bash
# Generate post
claude "Create LinkedIn post about our latest project success"

# Review in /Pending_Approval
# Edit if needed, then move to /Approved

# Publish
claude "/approval-manager"
```

### Respond to WhatsApp

```bash
# Check for urgent messages
claude "/whatsapp-messenger"

# Review drafted replies in /Pending_Approval
# Approve by moving to /Approved

# Send messages
claude "/approval-manager"
```

### Schedule Daily Briefing

```bash
# Set up daily briefing at 8 AM
claude "Schedule daily CEO briefing at 8:00 AM"

# Verify schedule
crontab -l  # Linux/Mac
Get-ScheduledTask  # Windows
```

## Folder Structure

```
AI_Employee_Vault/
├── Needs_Action/          # Incoming tasks
├── Plans/                 # Task plans
├── Pending_Approval/      # Actions awaiting approval
├── Approved/              # Approved actions (ready to execute)
├── Rejected/              # Rejected actions
├── Expired/               # Timed-out approvals
├── Executed/              # Completed actions
├── Done/                  # Completed tasks
├── Logs/                  # Activity logs
├── LinkedIn_Content/      # LinkedIn posts and analytics
│   ├── Drafts/
│   └── Analytics/
├── Schedules/             # Schedule configurations
├── Briefings/             # Daily briefings
├── Audits/                # Weekly audits
├── Dashboard.md           # Real-time overview
└── Company_Handbook.md    # Rules and configuration
```

## Configuration

### Company_Handbook.md

Configure behavior by editing sections:

```markdown
## Email Communication Rules
- Auto-approve conditions
- Approval requirements
- Response time targets

## WhatsApp Communication Rules
- Priority keywords
- Business hours
- Response times

## LinkedIn Strategy
- Posting frequency
- Content mix
- Target audience

## Approval Workflow Rules
- Timeout settings
- Default actions
- Delegation rules
```

## Daily Workflow

### Morning (8:00 AM)
1. ✅ Review daily briefing in Dashboard.md
2. ✅ Check /Pending_Approval folder
3. ✅ Approve/reject pending actions

### Throughout Day
1. 🔄 Watchers detect new messages/tasks
2. 🤖 AI processes and creates approval requests
3. 👤 Review and approve as needed
4. ⚡ Approved actions execute automatically

### Evening (6:00 PM)
1. 📊 Review Dashboard.md for day's activity
2. ✅ Process any pending approvals
3. 📝 Check logs for errors

### Weekly (Monday 9:00 AM)
1. 📈 Review weekly audit report
2. ✅ Approve optimization suggestions
3. 📅 Plan week's content

## Monitoring

### Check System Health

```bash
# View recent activity
cat Dashboard.md

# Check scheduler logs
cat Logs/Scheduler_Log_$(date +%Y-%m-%d).md

# Check approval analytics
cat Logs/Approval_Analytics_$(date +%Y-%m).md

# Verify Playwright server
python3 .claude/skills/browsing-with-playwright/scripts/verify.py
```

### Key Metrics

Track these metrics weekly:
- Email response time (target: < 2 hours)
- WhatsApp response time (target: < 30 minutes)
- Approval processing time (target: < 1 hour)
- Automation rate (target: > 70%)
- Error rate (target: < 5%)

## Troubleshooting

### Skills Not Working

```bash
# Verify skills are registered
claude --list-skills

# Check skill files exist
ls -la .claude/skills/*/SKILL.md

# Restart Claude Code
```

### Playwright Issues

```bash
# Restart server
bash .claude/skills/browsing-with-playwright/scripts/stop-server.sh
bash .claude/skills/browsing-with-playwright/scripts/start-server.sh

# Verify server
python3 .claude/skills/browsing-with-playwright/scripts/verify.py
```

### Gmail API Issues

```bash
# Re-authorize
python3 authorize_gmail.py

# Test connection
python3 test_email.py
```

### Scheduler Issues

```bash
# Check cron jobs (Linux/Mac)
crontab -l

# Check Task Scheduler (Windows)
Get-ScheduledTask | Where-Object {$_.TaskName -like "AI_Employee*"}

# View scheduler logs
cat Logs/Scheduler_Log_*.md
```

## Security

### Credentials Management

```bash
# Store credentials in .env
cat > .env << 'EOF'
GMAIL_CREDENTIALS_PATH=/path/to/credentials.json
GMAIL_TOKEN_PATH=/path/to/token.pickle
PLAYWRIGHT_SERVER_URL=http://localhost:8808
EOF

# Secure .env file
chmod 600 .env

# Verify .gitignore
cat .gitignore | grep -E "\.env|credentials|token"
```

### Approval Workflow

All sensitive actions require approval:
- ✅ Emails to new contacts
- ✅ All LinkedIn posts
- ✅ WhatsApp messages with business content
- ✅ Bulk communications
- ✅ Financial transactions

## Performance

### Optimization Tips

1. **Reduce approval bottlenecks:**
   - Review approval analytics
   - Adjust auto-approve rules for routine tasks
   - Set appropriate timeouts

2. **Improve response times:**
   - Monitor watcher performance
   - Optimize schedule intervals
   - Reduce processing overhead

3. **Enhance reliability:**
   - Enable failure alerts
   - Implement retry logic
   - Regular credential rotation

## Next Steps

### Week 1: Stabilization
- Run all skills daily
- Monitor for errors
- Adjust configurations
- Gather metrics

### Week 2: Optimization
- Review approval analytics
- Optimize schedules
- Refine Company_Handbook.md rules
- Improve templates

### Week 3: Enhancement
- Add custom templates
- Create additional schedules
- Expand priority contacts
- Fine-tune approval timeouts

### Week 4: Gold Tier Preparation
- Review Gold Tier requirements
- Plan Facebook/Instagram integration
- Consider Odoo accounting setup
- Prepare for advanced features

## Resources

### Documentation
- [SILVER_TIER_COMPLETE.md](SILVER_TIER_COMPLETE.md) - Overview and architecture
- [SILVER_TIER_SETUP.md](SILVER_TIER_SETUP.md) - Detailed setup guide
- [Claude Code Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

### Individual Skill Docs
- [linkedin-poster/SKILL.md](.claude/skills/linkedin-poster/SKILL.md)
- [email-sender/SKILL.md](.claude/skills/email-sender/SKILL.md)
- [whatsapp-messenger/SKILL.md](.claude/skills/whatsapp-messenger/SKILL.md)
- [scheduler/SKILL.md](.claude/skills/scheduler/SKILL.md)
- [approval-manager/SKILL.md](.claude/skills/approval-manager/SKILL.md)

### External Resources
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Playwright Documentation](https://playwright.dev)
- [Cron Expression Guide](https://crontab.guru)

### Support
- GitHub Issues: https://github.com/anthropics/claude-code/issues
- Wednesday Research Meetings: Every Wednesday 10:00 PM
- Zoom: https://us06web.zoom.us/j/87188707642

## Submission

Ready to submit your Silver Tier project?

1. **Create demo video** (5-10 minutes) showing:
   - Email sending workflow
   - LinkedIn posting
   - WhatsApp messaging
   - Approval workflow
   - Scheduled tasks in action

2. **Document your setup:**
   - README.md with architecture overview
   - Setup instructions
   - Security disclosure
   - Lessons learned

3. **Submit via form:**
   - https://forms.gle/JR9T1SJq5rmQyGkGA

## License

This is part of the Personal AI Employee Hackathon 0.
See main documentation for details.

---

**Status:** Silver Tier Complete ✅
**Estimated Time:** 20-30 hours
**Next Goal:** Gold Tier 🎯

*You've built a functional AI Employee capable of multi-channel communication, intelligent scheduling, and safe autonomous operations. Excellent work!*
