---
name: email-sender
description: |
  Send emails via Gmail API with approval workflow. Drafts emails, requests approval
  for sensitive communications, and logs all sent messages. Use this skill when you
  need to send emails, reply to messages, or manage email communications with
  human-in-the-loop safety.
---

# Email Sender

Automate email sending with Gmail API integration and approval workflow.

## Core Workflow

1. **Read** email requests from `/Needs_Action` folder
2. **Draft** email content based on context
3. **Create** approval request for review
4. **Send** via Gmail API after approval
5. **Log** all sent emails and update Dashboard

## Usage

```bash
# Process email requests
/email-sender

# Or invoke directly
claude "Send invoice email to client@example.com"
```

## What This Skill Does

### Email Drafting
- Reads email requests from task files
- Generates professional email content
- Follows company communication guidelines
- Includes proper formatting and signatures

### Approval Workflow
- Creates approval requests for all outgoing emails
- Allows review and editing before sending
- Supports bulk email approval
- Tracks approval history

### Email Sending
- Sends via Gmail API (OAuth2)
- Supports attachments
- Handles CC/BCC recipients
- Manages threading and replies

### Logging & Tracking
- Records all sent emails
- Maintains audit trail
- Updates Dashboard with activity
- Creates follow-up tasks if needed

## Gmail API Setup

### Prerequisites

1. Enable Gmail API in Google Cloud Console
2. Create OAuth2 credentials
3. Download credentials.json
4. Authorize the application

### Installation

```bash
# Install required packages
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-tools

# Run authorization flow (first time only)
python3 .claude/skills/email-sender/scripts/authorize.py
```

### Configuration

```json
// .claude/skills/email-sender/config.json
{
  "credentials_path": "/path/to/credentials.json",
  "token_path": "/path/to/token.json",
  "signature": "\n\nBest regards,\nYour Name\nYour Company",
  "max_recipients": 10,
  "require_approval": {
    "new_contacts": true,
    "bulk_emails": true,
    "attachments": true,
    "external_domains": true
  }
}
```

## Email Request Format

Create email requests in `/Needs_Action`:

```markdown
# /Needs_Action/EMAIL_REQUEST_client_invoice.md
---
type: email_request
to: client@example.com
cc:
bcc:
subject: Invoice for January 2026
priority: normal
requires_approval: true
attachments:
  - /Vault/Invoices/2026-01_Client.pdf
---

## Email Body

Hi [Client Name],

Please find attached the invoice for January 2026.

Payment details:
- Amount: $1,500
- Due date: March 30, 2026
- Payment methods: Bank transfer, PayPal

Let me know if you have any questions.

## Context
- Client: Client A
- Project: Website redesign
- Invoice number: INV-2026-001
```

## Approval Request Format

The skill creates approval files:

```markdown
# /Pending_Approval/EMAIL_client_invoice_2026-03-15.md
---
type: approval_request
action: send_email
created: 2026-03-15T10:00:00Z
expires: 2026-03-15T18:00:00Z
status: pending
---

## Email Details

**To:** client@example.com
**Subject:** Invoice for January 2026
**Attachments:** 2026-01_Client.pdf (245 KB)

## Email Content

Hi Client A,

Please find attached the invoice for January 2026.

Payment details:
- Amount: $1,500
- Due date: March 30, 2026
- Payment methods: Bank transfer, PayPal

Let me know if you have any questions.

Best regards,
Your Name
Your Company

---

## Safety Checks
✅ Recipient is known contact
✅ Subject line is professional
✅ Attachment size within limits
⚠️ Contains financial information - review carefully

## To Approve
Move this file to /Approved folder.

## To Edit
Modify the email content above, then move to /Approved.

## To Reject
Move this file to /Rejected folder.
```

## Gmail API Integration

### Python Script Example

```python
# .claude/skills/email-sender/scripts/send_email.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
import os

def send_email(to, subject, body, attachments=None):
    """Send email via Gmail API"""

    # Load credentials
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('gmail', 'v1', credentials=creds)

    # Create message
    message = MIMEMultipart()
    message['To'] = to
    message['Subject'] = subject

    # Add body
    message.attach(MIMEText(body, 'plain'))

    # Add attachments
    if attachments:
        for filepath in attachments:
            with open(filepath, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(filepath)}'
                )
                message.attach(part)

    # Encode and send
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    result = service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    return result

if __name__ == '__main__':
    import sys
    import json

    # Read email details from stdin
    data = json.loads(sys.stdin.read())

    result = send_email(
        to=data['to'],
        subject=data['subject'],
        body=data['body'],
        attachments=data.get('attachments')
    )

    print(json.dumps(result))
```

## Email Templates

### Invoice Email
```markdown
---
template: invoice
---

Hi {{client_name}},

Please find attached the invoice for {{period}}.

Payment details:
- Amount: {{amount}}
- Due date: {{due_date}}
- Payment methods: {{payment_methods}}

Let me know if you have any questions.
```

### Follow-up Email
```markdown
---
template: follow_up
---

Hi {{recipient_name}},

I wanted to follow up on {{subject}}.

{{custom_message}}

Looking forward to hearing from you.
```

### Meeting Request
```markdown
---
template: meeting_request
---

Hi {{recipient_name}},

I'd like to schedule a meeting to discuss {{topic}}.

Proposed times:
- {{option_1}}
- {{option_2}}
- {{option_3}}

Please let me know what works best for you.
```

## Auto-Reply Detection

The skill can detect when emails need replies:

```python
# Check for emails requiring response
def needs_reply(email):
    """Determine if email needs a reply"""

    # Check for questions
    if '?' in email['body']:
        return True

    # Check for action requests
    action_keywords = ['please', 'could you', 'can you', 'need', 'urgent']
    if any(kw in email['body'].lower() for kw in action_keywords):
        return True

    # Check sender importance
    if email['from'] in important_contacts:
        return True

    return False
```

## Email Logging

All sent emails are logged:

```markdown
# /Logs/Email_Log_2026-03-15.md
---
date: 2026-03-15
total_sent: 5
---

## Sent Emails

### 09:30 - Invoice to Client A
- **To:** client@example.com
- **Subject:** Invoice for January 2026
- **Status:** Sent successfully
- **Message ID:** <abc123@mail.gmail.com>
- **Approved by:** Human review

### 11:45 - Follow-up to Lead B
- **To:** lead@company.com
- **Subject:** Re: Project inquiry
- **Status:** Sent successfully
- **Message ID:** <def456@mail.gmail.com>
- **Approved by:** Human review

## Statistics
- Success rate: 100%
- Average approval time: 15 minutes
- Attachments sent: 2
```

## Safety Features

### Recipient Validation
- Verify email format
- Check against known contacts
- Flag external domains
- Prevent typos (similarity check)

### Content Scanning
- Detect sensitive information
- Check for profanity
- Verify links are safe
- Scan attachments for malware

### Rate Limiting
- Max 50 emails per day
- Max 10 emails per hour
- Cooldown after bulk sends
- Alert on unusual patterns

## Configuration in Company_Handbook.md

```markdown
## Email Communication Rules

### Auto-Approve Conditions
- Replies to known contacts
- Routine status updates
- Automated reports

### Always Require Approval
- New contacts
- Bulk emails (>3 recipients)
- Emails with attachments
- Financial communications
- Legal matters

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
```

## Silver Tier Capabilities

✅ Send emails via Gmail API
✅ Draft professional email content
✅ Human-in-the-loop approval workflow
✅ Support attachments
✅ Email logging and audit trail
✅ Template-based email generation
✅ Recipient validation

## Future Enhancements (Gold Tier)

- AI-powered email drafting
- Smart reply suggestions
- Email threading and conversation tracking
- Calendar integration for meeting requests
- CRM integration
- Email analytics and insights

## Troubleshooting

**Authentication failed:**
- Re-run authorization flow
- Check credentials.json is valid
- Verify Gmail API is enabled
- Check token.json permissions

**Email not sending:**
- Check internet connection
- Verify recipient email format
- Check attachment size limits (25MB)
- Review Gmail API quotas

**Approval workflow not working:**
- Verify folder permissions
- Check file naming conventions
- Ensure orchestrator is running
- Review approval timeout settings

## Security Best Practices

- Store credentials outside vault
- Use OAuth2, never passwords
- Rotate tokens regularly
- Enable 2FA on Gmail account
- Monitor for suspicious activity
- Never log email content in plain text

---
*Part of the Silver Tier AI Employee implementation*
