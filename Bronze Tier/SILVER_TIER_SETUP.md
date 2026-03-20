# Silver Tier Setup Guide

Complete setup instructions for Silver Tier AI Employee capabilities.

## Prerequisites

Before starting, ensure you have completed Bronze Tier:
- ✅ Obsidian vault with folder structure
- ✅ Claude Code installed and working
- ✅ ai-employee-processor skill functional
- ✅ browsing-with-playwright skill functional

## Estimated Setup Time: 3-4 hours

---

## Step 1: Gmail API Setup (45 minutes)

### 1.1 Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing
3. Enable Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### 1.2 Create OAuth2 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Configure consent screen if prompted:
   - User Type: External
   - App name: "AI Employee"
   - Add your email as test user
4. Application type: "Desktop app"
5. Download credentials.json

### 1.3 Install Python Dependencies

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-tools
```

### 1.4 Authorize Application

Create authorization script:

```python
# authorize_gmail.py
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authorize():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    print("Authorization successful!")

if __name__ == '__main__':
    authorize()
```

Run: `python authorize_gmail.py`

### 1.5 Test Email Sending

```python
# test_email.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import pickle

def send_test_email():
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText('Test email from AI Employee')
    message['To'] = 'your@email.com'
    message['Subject'] = 'Test Email'

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    result = service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    print(f"Email sent! Message ID: {result['id']}")

if __name__ == '__main__':
    send_test_email()
```

---

## Step 2: WhatsApp Web Setup (30 minutes)

### 2.1 Start Playwright Server

```bash
# Start with persistent browser context
npx @playwright/mcp@latest --port 8808 --shared-browser-context &
```

### 2.2 Login to WhatsApp Web

```bash
# Navigate to WhatsApp Web
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_navigate \
  -p '{"url": "https://web.whatsapp.com"}'

# Take screenshot to see QR code
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_take_screenshot \
  -p '{"type": "png", "fullPage": true}'
```

### 2.3 Scan QR Code

1. Open screenshot file
2. Open WhatsApp on your phone
3. Go to Settings > Linked Devices
4. Scan QR code from screenshot

### 2.4 Verify Login

```bash
# Wait for login to complete
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_wait_for \
  -p '{"text": "Chats", "time": 30000}'

# Take screenshot to verify
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_take_screenshot \
  -p '{"type": "png", "fullPage": true}'
```

---

## Step 3: LinkedIn Setup (30 minutes)

### 3.1 Login to LinkedIn

```bash
# Navigate to LinkedIn
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_navigate \
  -p '{"url": "https://www.linkedin.com"}'

# Get page snapshot to find login elements
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_snapshot -p '{}'
```

### 3.2 Manual Login

Use the snapshot output to identify login form elements, then:

```bash
# Type email
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_type \
  -p '{"element": "Email input", "ref": "e10", "text": "your@email.com"}'

# Type password
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_type \
  -p '{"element": "Password input", "ref": "e12", "text": "yourpassword"}'

# Click sign in
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_click \
  -p '{"element": "Sign in button", "ref": "e15"}'
```

### 3.3 Verify Login

```bash
# Wait for home page
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_wait_for \
  -p '{"text": "Home", "time": 10000}'
```

---

## Step 4: Scheduler Setup (30 minutes)

### 4.1 Linux/Mac (Cron)

```bash
# Open crontab editor
crontab -e

# Add these lines (adjust paths):
# Daily briefing at 8 AM
0 8 * * * cd /path/to/vault && /usr/local/bin/claude "Generate daily CEO briefing" >> /path/to/logs/briefing.log 2>&1

# Weekly audit every Monday at 9 AM
0 9 * * 1 cd /path/to/vault && /usr/local/bin/claude "Run weekly business audit" >> /path/to/logs/audit.log 2>&1

# Process inbox every 30 minutes
*/30 * * * * cd /path/to/vault && /usr/local/bin/claude "/ai-employee-processor" >> /path/to/logs/processor.log 2>&1

# Save and exit
```

### 4.2 Windows (Task Scheduler)

Create PowerShell script:

```powershell
# setup_scheduler.ps1

# Daily briefing
$action = New-ScheduledTaskAction -Execute "claude" -Argument "Generate daily CEO briefing" -WorkingDirectory "C:\path\to\vault"
$trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM
Register-ScheduledTask -TaskName "AI_Employee_Daily_Briefing" -Action $action -Trigger $trigger -Description "Generate morning CEO briefing"

# Weekly audit
$action = New-ScheduledTaskAction -Execute "claude" -Argument "Run weekly business audit" -WorkingDirectory "C:\path\to\vault"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9:00AM
Register-ScheduledTask -TaskName "AI_Employee_Weekly_Audit" -Action $action -Trigger $trigger -Description "Weekly business audit"

# Process inbox
$action = New-ScheduledTaskAction -Execute "claude" -Argument "/ai-employee-processor" -WorkingDirectory "C:\path\to\vault"
$trigger = New-ScheduledTaskTrigger -Once -At 12:00AM -RepetitionInterval (New-TimeSpan -Minutes 30) -RepetitionDuration ([TimeSpan]::MaxValue)
Register-ScheduledTask -TaskName "AI_Employee_Process_Inbox" -Action $action -Trigger $trigger -Description "Process inbox every 30 minutes"

Write-Host "Scheduled tasks created successfully!"
```

Run as Administrator: `powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1`

### 4.3 Verify Schedules

Linux/Mac:
```bash
crontab -l
```

Windows:
```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like "AI_Employee*"}
```

---

## Step 5: Vault Folder Structure (15 minutes)

Create additional folders for Silver Tier:

```bash
cd /path/to/AI_Employee_Vault

# Create Silver Tier folders
mkdir -p Pending_Approval
mkdir -p Approved
mkdir -p Rejected
mkdir -p Expired
mkdir -p Executed
mkdir -p LinkedIn_Content/Drafts
mkdir -p LinkedIn_Content/Analytics
mkdir -p Schedules
mkdir -p Briefings
mkdir -p Audits
```

---

## Step 6: Configuration Files (30 minutes)

### 6.1 Update Company_Handbook.md

Add these sections:

```markdown
## Email Communication Rules

### Auto-Approve Conditions
- Replies to known contacts
- Routine status updates
- Automated reports

### Always Require Approval
- All emails to new contacts
- All LinkedIn posts
- All WhatsApp messages with business content
- Bulk emails (>3 recipients)
- Financial communications

### Email Signature
Best regards,
[Your Name]
[Your Title]
[Your Company]
[Contact Info]

### Response Time Targets
- Urgent: Within 2 hours
- Normal: Within 24 hours
- Low priority: Within 3 days

## WhatsApp Communication Rules

### Priority Keywords
urgent, asap, emergency, help, invoice, payment, due, deadline

### Response Time Targets
- Urgent keywords: Within 15 minutes
- Priority contacts: Within 30 minutes
- Regular messages: Within 2 hours
- After hours: Next business day

### Business Hours
- Monday-Friday: 9:00 AM - 6:00 PM
- Saturday: 10:00 AM - 2:00 PM
- Sunday: Closed (emergency only)

### Out of Office Message
"Thanks for your message! I'm currently unavailable but will respond within [timeframe]. For urgent matters, please call [phone number]."

## LinkedIn Strategy

### Brand Voice
- Professional but approachable
- Focus on practical value
- Share real experiences

### Target Audience
- Business owners
- Entrepreneurs
- [Your specific audience]

### Posting Frequency
- Minimum: 3 posts per week
- Optimal: 1 post per day
- Maximum: 2 posts per day

### Best Times to Post
- Tuesday-Thursday: 9:00 AM - 11:00 AM
- Tuesday-Wednesday: 12:00 PM - 1:00 PM

### Content Mix (80/20 Rule)
- 80% Value: Tips, insights, industry news
- 20% Promotion: Services, products, offers

### Topics to Cover
- Industry insights
- Project case studies
- Tips and best practices
- Company updates

### Topics to Avoid
- Politics
- Controversial subjects
- Overly promotional content

## Approval Workflow Rules

### Approval Timeouts
- Urgent: 2 hours
- High: 4 hours
- Normal: 8 hours
- Low: 24 hours

### Default Actions on Timeout
- Urgent: Notify immediately, no default action
- High: Notify, no default action
- Normal: Auto-reject
- Low: Auto-reject

### Approval Delegation
- Manager can approve: All actions
- Assistant can approve: Routine emails, social posts
- System can auto-approve: Confirmations, status updates
```

### 6.2 Create Priority Contacts List

```markdown
# /Vault/WhatsApp_Contacts.md
---
priority_contacts:
  - name: Client A
    phone: +1234567890
    priority: high
    auto_respond: false
    notes: Major client, always requires approval

  - name: Client B
    phone: +0987654321
    priority: medium
    auto_respond: true
    notes: Regular client, routine updates can auto-respond

  - name: Partner Company
    phone: +1122334455
    priority: high
    auto_respond: false
    notes: Business partner, important communications
---
```

### 6.3 Create LinkedIn Content Templates

```markdown
# /Vault/LinkedIn_Content/templates.md

## Business Update Template
---
type: linkedin_post
category: business_update
---

🚀 Exciting news from [Your Business]!

[Main announcement or update]

Key highlights:
• [Benefit 1]
• [Benefit 2]
• [Benefit 3]

[Call to action]

#YourIndustry #BusinessGrowth #Innovation

---

## Thought Leadership Template
---
type: linkedin_post
category: thought_leadership
---

💡 [Insightful question or statement]

After [X years/months] in [industry], I've learned that:

[Key insight 1]
[Key insight 2]
[Key insight 3]

What's your experience with this? Let me know in the comments!

#Leadership #Industry #ProfessionalDevelopment
```

---

## Step 7: Security Setup (20 minutes)

### 7.1 Create .env File

```bash
# Create .env in vault root
cat > .env << 'EOF'
# Gmail API
GMAIL_CREDENTIALS_PATH=/path/to/credentials.json
GMAIL_TOKEN_PATH=/path/to/token.pickle

# Playwright
PLAYWRIGHT_SERVER_URL=http://localhost:8808

# Security
DRY_RUN=false
MAX_EMAILS_PER_DAY=50
MAX_WHATSAPP_PER_HOUR=30

# Notifications
ALERT_EMAIL=your@email.com
EOF
```

### 7.2 Add to .gitignore

```bash
cat >> .gitignore << 'EOF'
# Credentials
.env
credentials.json
token.pickle
token.json

# Browser sessions
.playwright/
browser_data/

# Logs
*.log
Logs/*.json
EOF
```

---

## Step 8: Testing (30 minutes)

### 8.1 Test Email Sending

```bash
claude "Draft an email to test@example.com with subject 'Test Email' and body 'This is a test'"
# Check /Pending_Approval for approval request
# Move to /Approved
claude "/approval-manager"
# Verify email was sent
```

### 8.2 Test LinkedIn Posting

```bash
claude "Create a LinkedIn post about completing Silver Tier setup"
# Check /Pending_Approval
# Move to /Approved
claude "/approval-manager"
# Verify post on LinkedIn
```

### 8.3 Test WhatsApp Messaging

```bash
# Send yourself a test message on WhatsApp with keyword "urgent"
# Wait for watcher to detect (if running)
# Or manually create task:
claude "Draft a WhatsApp reply to [Your Name] saying 'Test successful'"
# Check /Pending_Approval
# Move to /Approved
claude "/approval-manager"
```

### 8.4 Test Scheduler

```bash
# Manually trigger scheduled task
claude "Generate daily CEO briefing"
# Check /Briefings for output

claude "Run weekly business audit"
# Check /Audits for output
```

---

## Step 9: Launch Watchers (Optional - Gold Tier)

For continuous monitoring, create watcher scripts:

```python
# gmail_watcher.py
# See watcher examples in documentation
```

```python
# whatsapp_watcher.py
# See watcher examples in documentation
```

Start with process manager:
```bash
pm2 start gmail_watcher.py --interpreter python3
pm2 start whatsapp_watcher.py --interpreter python3
pm2 save
```

---

## Verification Checklist

- [ ] Gmail API authorized and tested
- [ ] WhatsApp Web logged in and persistent
- [ ] LinkedIn logged in and persistent
- [ ] Scheduled tasks created and verified
- [ ] Vault folder structure complete
- [ ] Company_Handbook.md updated
- [ ] .env file created and secured
- [ ] .gitignore updated
- [ ] All skills tested successfully
- [ ] Approval workflow functional

---

## Troubleshooting

### Gmail API Issues
- **403 Forbidden:** Check OAuth consent screen, enable Gmail API
- **Token expired:** Delete token.pickle and re-authorize
- **Import errors:** Reinstall google packages

### Playwright Issues
- **Server not responding:** Restart with `npx @playwright/mcp@latest --port 8808 --shared-browser-context`
- **Session expired:** Re-scan QR codes
- **Element not found:** Run browser_snapshot to get current refs

### Scheduler Issues
- **Tasks not running:** Check cron daemon or Task Scheduler service
- **Wrong working directory:** Verify paths in cron/task
- **Permission denied:** Check file permissions

---

## Next Steps

1. Run for 1 week to gather data
2. Review approval analytics
3. Optimize schedules based on patterns
4. Adjust Company_Handbook.md rules
5. Consider advancing to Gold Tier

---

**Setup Complete!** Your Silver Tier AI Employee is ready to operate.

For support, join Wednesday Research Meetings at 10:00 PM:
https://us06web.zoom.us/j/87188707642
