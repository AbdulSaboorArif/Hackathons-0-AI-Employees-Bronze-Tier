# AI Employee Silver Tier - Complete Setup Guide

**Date:** 2026-03-21
**Status:** Silver Tier Implementation Complete
**Version:** 1.0

---

## 🎯 Overview

Your AI Employee system is now **fully functional** for Silver Tier requirements. This guide explains how to use each component and verify everything works correctly.

---

## ✅ Silver Tier Requirements - COMPLETE

### 1. ✅ Two or More Watcher Scripts
- **Gmail Watcher** - Monitors important/unread emails
- **WhatsApp Watcher** - Detects urgent messages
- **LinkedIn Watcher** - Monitors notifications and engagement

### 2. ✅ Automatically Post on LinkedIn
- **LinkedIn Poster Skill** - Creates posts with approval workflow
- **Approval System** - Human-in-the-loop before posting
- **Playwright Automation** - Posts after approval

### 3. ✅ Claude Reasoning Loop with Plan.md Files
- **AI Employee Processor** - Orchestrates tasks
- **Reasoning Loop Skill** - Creates detailed plans
- **Plan Execution** - Multi-step workflows

### 4. ✅ One Working MCP Server
- **Communications MCP Server** - Email, LinkedIn, WhatsApp
- **Gmail API Integration** - Send emails
- **Playwright Integration** - LinkedIn and WhatsApp automation

### 5. ✅ Human-in-the-Loop Approval Workflow
- **Approval Manager** - Processes approvals
- **Pending_Approval Folder** - Review queue
- **Approved/Rejected Folders** - Decision tracking

### 6. ✅ Basic Scheduling
- **Scheduler Skill** - Cron/Task Scheduler integration
- **Automated Processing** - Periodic task checks

### 7. ✅ All AI Functionality as Agent Skills
- All features implemented as Claude Code skills
- Modular, reusable components
- Clear documentation

---

## 🚀 Quick Start Guide

### Step 1: Start Watchers

```bash
# Terminal 1 - Gmail Watcher
cd "C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Bronze Tier"
python watchers/gmail/gmail_watcher.py \
  --vault "AI_Employee_Vault" \
  --credentials ".claude/skills/credential.json" \
  --interval 120

# Terminal 2 - WhatsApp Watcher
python watchers/whatsapp/whatsapp_watcher.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/whatsapp/.browser-session" \
  --interval 60

# Terminal 3 - LinkedIn Watcher
python watchers/linkedin/linkedin_watcher.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/linkedin/.browser-session" \
  --interval 300
```

### Step 2: Process Tasks

```bash
# Process all pending tasks
python .claude/skills/ai-employee-processor/scripts/process_tasks.py \
  --vault "AI_Employee_Vault"
```

### Step 3: Create LinkedIn Post

```bash
# Create post with approval workflow
python .claude/skills/linkedin-poster/scripts/create_post.py \
  --vault "AI_Employee_Vault" \
  --template "business_update"
```

### Step 4: Review and Approve

1. Open `AI_Employee_Vault/Pending_Approval/`
2. Review the approval request
3. Move to `Approved/` folder to authorize
4. Or move to `Rejected/` to decline

### Step 5: Execute Approved Actions

```bash
# Process all approved actions
python .claude/skills/approval-manager/scripts/execute_approvals.py \
  "AI_Employee_Vault"
```

---

## 📋 Complete Workflow Examples

### Example 1: LinkedIn Posting Workflow

**Correct Flow (With Approval):**

```
1. Create Post
   → python create_post.py --vault "AI_Employee_Vault" --template "business_update"

2. System Creates:
   → Draft: LinkedIn_Content/Drafts/post_20260321.md
   → Approval: Pending_Approval/LINKEDIN_POST_20260321.md

3. Human Reviews:
   → Open Pending_Approval/LINKEDIN_POST_20260321.md
   → Review content
   → Move to Approved/ folder

4. Execute Approval:
   → python execute_approvals.py "AI_Employee_Vault"
   → Calls post_to_linkedin.py
   → Posts via Playwright
   → Moves to Done/

5. Result:
   → Post published on LinkedIn
   → Screenshot saved in Logs/
   → Action logged
```

**What Was Wrong Before:**
- Posts were created and published immediately
- No approval step
- No human oversight

**What's Fixed Now:**
- Posts go to Pending_Approval first
- Human must explicitly approve
- Only posts after approval

### Example 2: Email Response Workflow

```
1. Gmail Watcher Detects Email
   → Creates: Needs_Action/EMAIL_20260321_client_inquiry.md

2. AI Employee Processor Analyzes
   → Reads task
   → Determines: Requires approval
   → Creates: Plans/PLAN_email_response_20260321.md

3. Email Sender Skill Drafts Reply
   → Generates professional response
   → Creates: Pending_Approval/EMAIL_REPLY_20260321.md

4. Human Reviews and Approves
   → Reviews draft
   → Moves to Approved/

5. Approval Manager Executes
   → Sends email via Gmail API
   → Logs action
   → Moves to Done/
```

### Example 3: LinkedIn Engagement Workflow

```
1. LinkedIn Watcher Detects Comment
   → Creates: Needs_Action/LINKEDIN_20260321_comment.md

2. AI Employee Processor Analyzes
   → Type: linkedin_comment
   → Priority: normal
   → Action: Draft reply

3. LinkedIn Engagement Handler
   → python handle_engagement.py --notification-file "..."
   → Drafts thoughtful reply
   → Creates: Pending_Approval/LINKEDIN_ENGAGEMENT_reply_20260321.md

4. Human Reviews
   → Can edit response
   → Approves by moving to Approved/

5. Engagement Executed
   → Reply posted on LinkedIn
   → Original notification moved to Done/
```

---

## 🔧 Component Reference

### Watchers (Monitoring Layer)

| Watcher | Purpose | Interval | Output |
|---------|---------|----------|--------|
| Gmail | Monitor important emails | 120s | EMAIL_*.md |
| WhatsApp | Detect urgent messages | 60s | WHATSAPP_*.md |
| LinkedIn | Track notifications | 300s | LINKEDIN_*.md |

### Skills (Action Layer)

| Skill | Purpose | Requires Approval |
|-------|---------|-------------------|
| ai-employee-processor | Orchestrate tasks | No |
| linkedin-poster | Create/post content | Yes |
| linkedin-engagement | Reply to comments | Yes |
| email-sender | Send emails | Yes |
| whatsapp-messenger | Send messages | Yes |
| approval-manager | Execute approvals | No |
| reasoning-loop | Create plans | No |

### Folders (Organization)

| Folder | Purpose | Who Writes |
|--------|---------|------------|
| Needs_Action/ | Pending tasks | Watchers |
| Plans/ | Task plans | Processor |
| Pending_Approval/ | Awaiting review | Skills |
| Approved/ | Authorized actions | Human |
| Rejected/ | Declined actions | Human |
| Done/ | Completed tasks | System |
| Logs/ | Audit trail | All |

---

## 🐛 Troubleshooting

### Issue: LinkedIn Posts Automatically

**Problem:** Posts publish without approval

**Solution:** Use the new workflow:
```bash
# DON'T run post_to_linkedin.py directly
# DO run create_post.py first
python create_post.py --vault "AI_Employee_Vault"
# Then approve manually
# Then run execute_approvals.py
```

### Issue: Watchers Not Detecting

**Problem:** No files in Needs_Action/

**Checklist:**
- [ ] Watchers running?
- [ ] Logged in to LinkedIn/WhatsApp?
- [ ] Gmail credentials valid?
- [ ] Vault path correct?

### Issue: Approval Manager Not Executing

**Problem:** Approved files not processed

**Solution:**
```bash
# Run approval manager manually
python .claude/skills/approval-manager/scripts/execute_approvals.py "AI_Employee_Vault"

# Or set up scheduled execution
# See scheduler skill documentation
```

### Issue: LinkedIn Watcher Only Monitors

**Problem:** Doesn't engage with notifications

**Solution:** This is correct behavior!
- Watcher detects notifications
- Creates action files
- Engagement handler drafts responses
- Human approves
- Then engagement executes

**To engage:**
```bash
python .claude/skills/linkedin-poster/scripts/handle_engagement.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/linkedin/.browser-session" \
  --process-all
```

---

## 📊 Verification Checklist

### Test 1: LinkedIn Posting

- [ ] Run `create_post.py`
- [ ] File appears in Pending_Approval/
- [ ] Review and move to Approved/
- [ ] Run `execute_approvals.py`
- [ ] Post appears on LinkedIn
- [ ] Screenshot in Logs/
- [ ] File moved to Done/

### Test 2: Email Workflow

- [ ] Gmail watcher detects email
- [ ] File in Needs_Action/
- [ ] Processor creates plan
- [ ] Email sender drafts reply
- [ ] Approval request created
- [ ] Human approves
- [ ] Email sent via Gmail API

### Test 3: LinkedIn Engagement

- [ ] LinkedIn watcher detects comment
- [ ] File in Needs_Action/
- [ ] Engagement handler drafts reply
- [ ] Approval request created
- [ ] Human reviews/edits
- [ ] Approves
- [ ] Reply posted

### Test 4: WhatsApp Monitoring

- [ ] WhatsApp watcher running
- [ ] Detects urgent message
- [ ] Creates action file
- [ ] Processor analyzes
- [ ] Creates approval request

---

## 🎓 Best Practices

### 1. Always Review Approvals

Never blindly approve. Check:
- Content accuracy
- Tone appropriateness
- Recipient correctness
- Timing suitability

### 2. Monitor Logs Regularly

```bash
# Check today's logs
cat AI_Employee_Vault/Logs/2026-03-21*.json

# Review LinkedIn actions
cat AI_Employee_Vault/Logs/*linkedin*.json
```

### 3. Update Company Handbook

Edit `Company_Handbook.md` to customize:
- Approval thresholds
- Priority keywords
- Communication rules
- Response templates

### 4. Schedule Regular Processing

```bash
# Set up cron job (Linux/Mac)
*/15 * * * * cd /path/to/project && python .claude/skills/ai-employee-processor/scripts/process_tasks.py --vault "AI_Employee_Vault"

# Or use Task Scheduler (Windows)
# See scheduler skill documentation
```

### 5. Backup Your Vault

```bash
# Regular backups
cp -r AI_Employee_Vault AI_Employee_Vault_backup_$(date +%Y%m%d)
```

---

## 🚀 Next Steps (Gold Tier)

To upgrade to Gold Tier, add:

1. **Ralph Wiggum Loop** - Autonomous multi-step execution
2. **Odoo Integration** - Accounting system via MCP
3. **Facebook/Instagram** - Social media expansion
4. **Twitter/X Integration** - Additional platform
5. **Weekly CEO Briefing** - Automated business audit
6. **Error Recovery** - Graceful degradation
7. **Comprehensive Logging** - Advanced audit trails

---

## 📞 Support

If you encounter issues:

1. Check logs in `AI_Employee_Vault/Logs/`
2. Review `IMPLEMENTATION_ANALYSIS.md`
3. Verify all scripts are executable
4. Ensure Python dependencies installed
5. Check browser sessions are valid

---

## 🎉 Congratulations!

Your Silver Tier AI Employee is **complete and functional**. You now have:

✅ Automated monitoring (Gmail, WhatsApp, LinkedIn)
✅ Intelligent task processing
✅ Human-in-the-loop safety
✅ LinkedIn posting with approval
✅ LinkedIn engagement handling
✅ Email automation
✅ Comprehensive logging
✅ Modular skill architecture

**Your AI Employee is ready to work for you 24/7!**

---

*Setup guide created by Claude Code*
*Version 1.0 - Silver Tier Complete*
