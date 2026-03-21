# AI Employee - Manual Command Reference

Complete guide for manually running all watchers, skills, and workflows.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Watchers (Monitoring)](#watchers-monitoring)
3. [Skills (Actions)](#skills-actions)
4. [Approval Workflow](#approval-workflow)
5. [Status & Monitoring](#status--monitoring)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Check Python & Dependencies
```bash
# Verify Python version (need 3.13+)
python3 --version

# Verify Playwright is installed
python3 -c "import playwright; print('Playwright OK')"

# Verify Google API libraries
python3 -c "import google.auth; print('Google Auth OK')"
```

### Check Node.js (for MCP servers)
```bash
# Verify Node.js version (need 24+)
node --version
```

---

## Watchers (Monitoring)

### 1. Gmail Watcher
**Purpose**: Monitors Gmail for new important emails

```bash
# Run Gmail watcher (continuous monitoring)
python3 watchers/gmail/gmail_watcher.py \
  --vault "AI_Employee_Vault" \
  --credentials "credential.json" \
  --interval 120

# Single check (test mode)
python3 watchers/gmail/gmail_watcher.py \
  --vault "AI_Employee_Vault" \
  --credentials "credential.json" \
  --interval 120 \
  --once
```

**What it does**:
- Checks Gmail every 120 seconds (2 minutes)
- Detects unread important emails
- Creates action files in `AI_Employee_Vault/Needs_Action/`
- Requires `token.json` (run Gmail OAuth first if missing)

**Stop**: Press `Ctrl+C`

---

### 2. WhatsApp Watcher
**Purpose**: Monitors WhatsApp Web for urgent messages

```bash
# Run WhatsApp watcher (continuous monitoring)
python3 watchers/whatsapp/whatsapp_watcher.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/whatsapp/.browser-session" \
  --interval 60

# Single check (test mode)
python3 test_whatsapp_watcher.py
```

**What it does**:
- Checks WhatsApp Web every 60 seconds
- Detects messages with urgent keywords (urgent, asap, invoice, payment, help)
- Creates action files in `AI_Employee_Vault/Needs_Action/`
- Opens browser window (scan QR code on first run)

**First time setup**: Browser opens → Scan QR code with phone → Session persists

**Stop**: Press `Ctrl+C`

---

### 3. LinkedIn Watcher
**Purpose**: Monitors LinkedIn notifications (if implemented)

```bash
# Run LinkedIn watcher
python3 watchers/linkedin/linkedin_watcher.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/linkedin/.browser-session" \
  --interval 300
```

**What it does**:
- Checks LinkedIn every 300 seconds (5 minutes)
- Detects notifications, messages, connection requests
- Creates action files in `AI_Employee_Vault/Needs_Action/`
<!-- Dont Check Messages and connection  -->
**Stop**: Press `Ctrl+C`

---

### 4. File System Watcher
**Purpose**: Monitors a folder for dropped files

```bash
# Run file system watcher
python3 watchers/filesystem_watcher.py \
  --vault "AI_Employee_Vault" \
  --watch-folder "~/Desktop/AI_Inbox"
```

**What it does**:
- Watches specified folder for new files
- Automatically moves files to `AI_Employee_Vault/Needs_Action/`
- Creates metadata files

**Stop**: Press `Ctrl+C`

---

## Skills (Actions)

### 1. Send Email (Gmail API)
**Purpose**: Send approved emails via Gmail

```bash
# Send a specific email
python3 send_email.py

# Or with custom recipient/subject/body
python3 -c "
from send_email import send_email
send_email(
    to='recipient@example.com',
    subject='Your Subject',
    body='Your message here'
)
"
```

**What it does**:
- Sends email via Gmail API
- Requires `token.json` (OAuth authenticated)
- Logs sent emails to `AI_Employee_Vault/Logs/email_sent_log.json`

**Prerequisites**: Run `python3 authorize_gmail.py` first if no token.json

---

### 2. Post to LinkedIn
**Purpose**: Post approved content to LinkedIn

```bash
# Post from approval file
python3 .claude/skills/linkedin-poster/scripts/post_to_linkedin.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/linkedin/.browser-session" \
  --approval-file "AI_Employee_Vault/Approved/LINKEDIN_POST_YYYYMMDD.md"

# Example with specific file
python3 .claude/skills/linkedin-poster/scripts/post_to_linkedin.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/linkedin/.browser-session" \
  --approval-file "AI_Employee_Vault/Approved/LINKEDIN_POST_20260321_170529.md"
```

**What it does**:
- Opens LinkedIn in browser
- Finds "Start a post" button
- Types content and clicks Post
- Takes screenshot for verification
- Moves file to `Done/` folder
- Logs to `AI_Employee_Vault/Logs/YYYY-MM-DD_linkedin_posts.json`

**Prerequisites**: Must be logged into LinkedIn (session persists)

---

### 3. Send WhatsApp Message
**Purpose**: Send approved messages via WhatsApp Web

```bash
# Send from approval file
python3 .claude/skills/whatsapp-messenger/scripts/send_whatsapp.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/whatsapp/.browser-session" \
  --approval-file "AI_Employee_Vault/Approved/WHATSAPP_REPLY_contact.md"

# Example with test file
python3 .claude/skills/whatsapp-messenger/scripts/send_whatsapp.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/whatsapp/.browser-session" \
  --approval-file "AI_Employee_Vault/Approved/WHATSAPP_TEST_20260321.md"
```

**What it does**:
- Opens WhatsApp Web in browser
- Searches for contact by name
- Types and sends message
- Takes screenshots for verification
- Moves file to `Done/` folder
- Logs to `AI_Employee_Vault/Logs/YYYY-MM-DD_whatsapp_messages.json`

**Prerequisites**: Must be logged into WhatsApp Web (scan QR code on first run)

---

### 4. Process AI Employee Tasks
**Purpose**: Let Claude process tasks from Needs_Action folder

```bash
# Use the ai-employee-processor skill
claude "Process all tasks in Needs_Action folder"

# Or use approval-manager skill
claude "Check for pending approvals and execute approved actions"
```

**What it does**:
- Reads files from `Needs_Action/`
- Creates plans and drafts responses
- Moves items to `Pending_Approval/`
- Waits for human approval

---

## Approval Workflow

### Manual Approval Process

#### 1. Check Pending Approvals
```bash
# List all pending approvals
ls -la AI_Employee_Vault/Pending_Approval/

# View a specific approval
cat AI_Employee_Vault/Pending_Approval/LINKEDIN_POST_20260321.md
```

#### 2. Approve an Action
```bash
# Move to Approved folder
mv "AI_Employee_Vault/Pending_Approval/LINKEDIN_POST_20260321.md" \
   "AI_Employee_Vault/Approved/"

# Or approve multiple at once
mv AI_Employee_Vault/Pending_Approval/*.md AI_Employee_Vault/Approved/
```

#### 3. Reject an Action
```bash
# Move to Rejected folder
mv "AI_Employee_Vault/Pending_Approval/EMAIL_spam.md" \
   "AI_Employee_Vault/Rejected/"
```

#### 4. Execute Approved Actions

**For LinkedIn:**
```bash
python3 .claude/skills/linkedin-poster/scripts/post_to_linkedin.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/linkedin/.browser-session" \
  --approval-file "AI_Employee_Vault/Approved/LINKEDIN_POST_*.md"
```

**For WhatsApp:**
```bash
python3 .claude/skills/whatsapp-messenger/scripts/send_whatsapp.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/whatsapp/.browser-session" \
  --approval-file "AI_Employee_Vault/Approved/WHATSAPP_*.md"
```

**For Email:**
```bash
# Email sending is done via send_email.py
# Modify the script to read from approval file
```

---

## Status & Monitoring

### Check Vault Status
```bash
# Quick status check
echo "=== AI Employee Vault Status ==="
echo "Needs Action: $(ls AI_Employee_Vault/Needs_Action/ 2>/dev/null | wc -l) files"
echo "Pending Approval: $(ls AI_Employee_Vault/Pending_Approval/ 2>/dev/null | wc -l) files"
echo "Approved: $(ls AI_Employee_Vault/Approved/ 2>/dev/null | wc -l) files"
echo "Done: $(ls AI_Employee_Vault/Done/*.md 2>/dev/null | wc -l) tasks"
echo "Executed: $(ls AI_Employee_Vault/Executed/*.md 2>/dev/null | wc -l) actions"
```

### View Recent Logs
```bash
# Email logs
cat AI_Employee_Vault/Logs/email_sent_log.json | python3 -m json.tool

# LinkedIn logs
cat AI_Employee_Vault/Logs/2026-03-21_linkedin_posts.json | python3 -m json.tool

# WhatsApp logs
cat AI_Employee_Vault/Logs/2026-03-21_whatsapp_messages.json | python3 -m json.tool
```

### View Screenshots
```bash
# List recent screenshots
ls -lht AI_Employee_Vault/Logs/*.png | head -10

# Open latest LinkedIn screenshot (Windows)
start AI_Employee_Vault/Logs/linkedin_post_success_*.png

# Open latest WhatsApp screenshot (Windows)
start AI_Employee_Vault/Logs/whatsapp_success_*.png
```

---

## Troubleshooting

### Gmail Authentication Issues
```bash
# Re-authenticate Gmail
python3 authorize_gmail.py

# Check if token exists
ls -la token.json

# Test Gmail connection
python3 -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
creds = Credentials.from_authorized_user_file('token.json')
service = build('gmail', 'v1', credentials=creds)
profile = service.users().getProfile(userId='me').execute()
print(f'Connected as: {profile[\"emailAddress\"]}')
"
```

### Browser Session Issues

**LinkedIn session expired:**
```bash
# Delete session and re-login
rm -rf watchers/linkedin/.browser-session/
# Next run will prompt for login
```

**WhatsApp session expired:**
```bash
# Delete session and re-scan QR code
rm -rf watchers/whatsapp/.browser-session/
# Next run will show QR code
```

### Check Running Processes
```bash
# Check if watchers are running
ps aux | grep "watcher.py"

# Kill a stuck watcher
pkill -f "gmail_watcher.py"
pkill -f "whatsapp_watcher.py"
```

### Clear Processed Messages
```bash
# Archive old Done files
mkdir -p AI_Employee_Vault/Archive/$(date +%Y-%m)
mv AI_Employee_Vault/Done/*.md AI_Employee_Vault/Archive/$(date +%Y-%m)/

# Clean old logs (older than 30 days)
find AI_Employee_Vault/Logs -name "*.json" -mtime +30 -delete
find AI_Employee_Vault/Logs -name "*.png" -mtime +30 -delete
```

---

## Quick Start Commands

### Start All Watchers (in separate terminals)

**Terminal 1 - Gmail:**
```bash
python3 watchers/gmail/gmail_watcher.py \
  --vault "AI_Employee_Vault" \
  --credentials "credential.json" \
  --interval 120
```

**Terminal 2 - WhatsApp:**
```bash
python3 watchers/whatsapp/whatsapp_watcher.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/whatsapp/.browser-session" \
  --interval 60
```

**Terminal 3 - LinkedIn:**
```bash
python3 watchers/linkedin/linkedin_watcher.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/linkedin/.browser-session" \
  --interval 300
```

### Process Everything at Once
```bash
# Let Claude process all pending tasks
claude "Process all tasks in Needs_Action, create approvals, and show me what needs my review"
```

---

## Production Setup (Background Running)

### Using PM2 (Recommended for Linux/Mac)
```bash
# Install PM2
npm install -g pm2

# Start all watchers
pm2 start watchers/gmail/gmail_watcher.py \
  --interpreter python3 \
  --name gmail-watcher \
  -- --vault AI_Employee_Vault --credentials credential.json --interval 120

pm2 start watchers/whatsapp/whatsapp_watcher.py \
  --interpreter python3 \
  --name whatsapp-watcher \
  -- --vault AI_Employee_Vault --session watchers/whatsapp/.browser-session --interval 60

# View status
pm2 status

# View logs
pm2 logs gmail-watcher
pm2 logs whatsapp-watcher

# Stop all
pm2 stop all

# Auto-start on reboot
pm2 save
pm2 startup
```

### Using Task Scheduler (Windows)
```bash
# Create scheduled task for Gmail watcher
schtasks /create /tn "Gmail Watcher" \
  /tr "python3 C:\path\to\watchers\gmail\gmail_watcher.py --vault AI_Employee_Vault --credentials credential.json" \
  /sc onstart /ru SYSTEM

# Create scheduled task for WhatsApp watcher
schtasks /create /tn "WhatsApp Watcher" \
  /tr "python3 C:\path\to\watchers\whatsapp\whatsapp_watcher.py --vault AI_Employee_Vault --session watchers/whatsapp/.browser-session" \
  /sc onstart /ru SYSTEM
```

---

## Summary

**For daily use:**
1. Start watchers in background (PM2 or Task Scheduler)
2. Check `Pending_Approval/` folder periodically
3. Approve/reject items by moving files
4. Watchers and skills handle the rest automatically

**For manual posting:**
- LinkedIn: Use `post_to_linkedin.py` command
- WhatsApp: Use `send_whatsapp.py` command
- Email: Use `send_email.py` script

**For troubleshooting:**
- Check logs in `AI_Employee_Vault/Logs/`
- View screenshots for visual verification
- Re-authenticate if sessions expire

---

*Last updated: 2026-03-21*
*Silver Tier AI Employee System*
