---
name: approval-manager
description: |
  Manage human-in-the-loop approval workflow for sensitive actions. Monitors pending
  approvals, executes approved actions, and logs all decisions. Use this skill when
  you need to process approval requests, execute approved tasks, or review pending
  actions requiring human oversight.
---

# Approval Manager

Human-in-the-loop approval workflow for safe autonomous operations.

## Core Workflow

1. **Monitor** /Pending_Approval folder for new requests
2. **Present** approval requests to user
3. **Execute** approved actions via appropriate MCP/skill
4. **Log** all approval decisions
5. **Handle** rejections and timeouts

## Usage

```bash
# Process pending approvals
/approval-manager

# Or invoke directly
claude "Check for pending approvals and execute approved actions"
claude "Show all pending approval requests"
```

## What This Skill Does

### Approval Monitoring
- Watches /Pending_Approval folder
- Detects new approval requests
- Tracks approval status
- Handles approval timeouts

### Action Execution
- Executes approved emails via email-sender
- Posts approved LinkedIn content via linkedin-poster
- Sends approved WhatsApp messages via whatsapp-messenger
- Processes approved payments (Gold tier)

### Decision Logging
- Records all approval decisions
- Maintains audit trail
- Tracks approval times
- Identifies patterns

### Timeout Handling
- Detects expired approval requests
- Moves expired items to /Expired folder
- Notifies user of missed approvals
- Suggests default actions

## Folder Structure

```
/Vault
├── /Pending_Approval      # New approval requests
├── /Approved              # User-approved actions (ready to execute)
├── /Rejected              # User-rejected actions
├── /Expired               # Timed-out approvals
└── /Executed              # Successfully executed actions
```

## Approval Request Format

All approval requests follow this standard format:

```markdown
# /Pending_Approval/ACTION_TYPE_description_timestamp.md
---
type: approval_request
action: email_send | linkedin_post | whatsapp_send | payment
created: 2026-03-15T10:00:00Z
expires: 2026-03-15T18:00:00Z
priority: low | normal | high | urgent
status: pending
auto_approve: false
---

## Action Details
[Specific details about what will be done]

## Context
[Why this action is needed]

## Safety Checks
[Automated validation results]

## To Approve
Move this file to /Approved folder.

## To Edit
Modify the action details above, then move to /Approved.

## To Reject
Move this file to /Rejected folder with reason.
```

## Approval Types

### Email Approval

```markdown
# /Pending_Approval/EMAIL_client_invoice_2026-03-15.md
---
type: approval_request
action: email_send
to: client@example.com
subject: Invoice for March 2026
attachments: ["/Vault/Invoices/2026-03_Client.pdf"]
created: 2026-03-15T10:00:00Z
expires: 2026-03-15T18:00:00Z
priority: normal
---

## Email Content

Hi Client A,

Please find attached your invoice for March 2026.

Amount: $1,500
Due date: April 15, 2026

Best regards,
Your Name

## Safety Checks
✅ Recipient is known contact
✅ Professional tone
✅ Attachment exists and is valid
✅ No sensitive data exposed

## To Approve
Move this file to /Approved folder.
```

### LinkedIn Post Approval

```markdown
# /Pending_Approval/LINKEDIN_POST_2026-03-15.md
---
type: approval_request
action: linkedin_post
created: 2026-03-15T09:00:00Z
expires: 2026-03-15T12:00:00Z
priority: normal
scheduled_time: 2026-03-15T10:00:00Z
---

## Post Content

🚀 Excited to share our latest project success!

We just completed a major milestone for Client A, delivering a custom solution that increased their efficiency by 40%.

Key takeaways:
• Clear communication is essential
• Iterative development works
• Client feedback drives success

What's your experience with agile project delivery?

#ProjectManagement #Success #BusinessGrowth

## Engagement Strategy
- Best time: 10:00 AM Tuesday
- Target: Business owners, project managers
- Expected reach: 500-1000

## Safety Checks
✅ Professional content
✅ No client confidential info
✅ Appropriate hashtags
✅ Engaging call-to-action

## To Approve
Move this file to /Approved folder.
```

### WhatsApp Message Approval

```markdown
# /Pending_Approval/WHATSAPP_client_a_2026-03-15.md
---
type: approval_request
action: whatsapp_send
to: Client A
phone: +1234567890
created: 2026-03-15T11:00:00Z
expires: 2026-03-15T13:00:00Z
priority: high
---

## Message Content

Hi Client A! I'll send you the March invoice right away. You should receive it via email within the next hour. Let me know if you need anything else!

## Context
- Responding to urgent invoice request
- Client is high priority
- Invoice is ready to send

## Safety Checks
✅ Professional tone
✅ Accurate information
✅ Timely response
✅ No sensitive data

## To Approve
Move this file to /Approved folder.
```

## Execution Process

When a file is moved to /Approved:

```python
# approval_executor.py
import yaml
from pathlib import Path

def execute_approval(approval_file):
    """Execute an approved action"""

    # Parse approval file
    with open(approval_file) as f:
        content = f.read()
        metadata = yaml.safe_load(content.split('---')[1])
        body = content.split('---')[2]

    action_type = metadata['action']

    # Route to appropriate executor
    if action_type == 'email_send':
        result = execute_email(metadata, body)
    elif action_type == 'linkedin_post':
        result = execute_linkedin_post(metadata, body)
    elif action_type == 'whatsapp_send':
        result = execute_whatsapp(metadata, body)
    else:
        raise ValueError(f"Unknown action type: {action_type}")

    # Log execution
    log_execution(approval_file, result)

    # Move to executed folder
    move_to_executed(approval_file, result)

    return result

def execute_email(metadata, body):
    """Execute approved email via email-sender skill"""
    # Extract email content from body
    # Call email-sender skill
    # Return result
    pass

def execute_linkedin_post(metadata, body):
    """Execute approved LinkedIn post via linkedin-poster skill"""
    # Extract post content from body
    # Call linkedin-poster skill
    # Return result
    pass

def execute_whatsapp(metadata, body):
    """Execute approved WhatsApp message via whatsapp-messenger skill"""
    # Extract message content from body
    # Call whatsapp-messenger skill
    # Return result
    pass
```

## Approval Dashboard

Generate a summary of pending approvals:

```markdown
# /Vault/Dashboard.md (Approval Section)

## Pending Approvals (3)

### 🔴 Urgent
- **WhatsApp to Client A** - Invoice request response
  - Created: 2 hours ago
  - Expires: In 1 hour
  - [View](/Pending_Approval/WHATSAPP_client_a_2026-03-15.md)

### 🟡 Normal Priority
- **Email to Client B** - Project proposal
  - Created: 30 minutes ago
  - Expires: In 7 hours
  - [View](/Pending_Approval/EMAIL_client_b_proposal_2026-03-15.md)

- **LinkedIn Post** - Project success story
  - Created: 1 hour ago
  - Expires: In 2 hours
  - [View](/Pending_Approval/LINKEDIN_POST_2026-03-15.md)

## Recent Decisions (Last 24h)

### ✅ Approved (5)
- Email to Client A - Invoice sent successfully
- LinkedIn post - Published, 23 likes
- WhatsApp to Lead B - Sent, awaiting response
- Email to Client C - Status update sent
- LinkedIn post - Published, 15 likes

### ❌ Rejected (1)
- Email to Unknown Contact - Spam/unsolicited

### ⏰ Expired (0)
```

## Timeout Handling

When approval requests expire:

```python
# timeout_handler.py
from datetime import datetime
from pathlib import Path

def check_expired_approvals():
    """Check for and handle expired approval requests"""

    pending_dir = Path('/Vault/Pending_Approval')
    expired_dir = Path('/Vault/Expired')
    now = datetime.now()

    for approval_file in pending_dir.glob('*.md'):
        metadata = parse_metadata(approval_file)
        expires = datetime.fromisoformat(metadata['expires'])

        if now > expires:
            # Move to expired folder
            expired_file = expired_dir / approval_file.name
            approval_file.rename(expired_file)

            # Log expiration
            log_expiration(approval_file, metadata)

            # Notify user
            notify_expired_approval(metadata)

            # Take default action if configured
            if metadata.get('default_action') == 'reject':
                handle_rejection(expired_file, 'Expired - auto-rejected')
            elif metadata.get('default_action') == 'approve':
                # Only for low-risk actions
                if metadata.get('priority') == 'low':
                    handle_approval(expired_file)
```

## Approval Analytics

Track approval patterns:

```markdown
# /Logs/Approval_Analytics_2026-03.md
---
period: March 2026
total_requests: 127
approved: 115
rejected: 8
expired: 4
---

## Approval Statistics

### By Action Type
- Email: 78 requests (72 approved, 4 rejected, 2 expired)
- LinkedIn: 32 requests (30 approved, 2 rejected, 0 expired)
- WhatsApp: 17 requests (13 approved, 2 rejected, 2 expired)

### By Priority
- Urgent: 15 requests (100% approved, avg time: 8 min)
- High: 34 requests (97% approved, avg time: 22 min)
- Normal: 68 requests (88% approved, avg time: 2.5 hours)
- Low: 10 requests (80% approved, avg time: 6 hours)

### Response Times
- Average approval time: 1.8 hours
- Fastest approval: 3 minutes
- Slowest approval: 7.2 hours
- Expired rate: 3.1%

### Rejection Reasons
- Incorrect information: 3
- Wrong recipient: 2
- Timing not appropriate: 2
- Content needs revision: 1

## Insights
- Urgent requests are approved quickly and reliably
- Email approvals have highest volume
- Low priority items have higher expiration rate
- Consider extending timeout for low priority items
```

## Batch Approval

For multiple similar approvals:

```markdown
# /Pending_Approval/BATCH_weekly_social_posts.md
---
type: batch_approval
action: linkedin_post
count: 5
created: 2026-03-15T08:00:00Z
expires: 2026-03-15T18:00:00Z
---

## Batch: Weekly Social Media Posts

### Post 1 - Monday
[Content...]

### Post 2 - Tuesday
[Content...]

### Post 3 - Wednesday
[Content...]

### Post 4 - Thursday
[Content...]

### Post 5 - Friday
[Content...]

## To Approve All
Move this file to /Approved folder.

## To Approve Individually
Create separate approval files for each post.

## To Reject All
Move this file to /Rejected folder.
```

## Configuration

Edit Company_Handbook.md to customize approval rules:

```markdown
## Approval Workflow Rules

### Auto-Approve (No Human Review)
- Simple confirmations (Yes, OK, Thanks)
- Routine status updates to known contacts
- Scheduled reports

### Require Approval
- All emails to new contacts
- All LinkedIn posts
- All WhatsApp messages with business content
- Any financial transactions
- Bulk communications (>3 recipients)

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

## Notification System

Alert user of pending approvals:

```python
# notification.py
def notify_pending_approval(approval):
    """Notify user of new approval request"""

    priority = approval['priority']
    action = approval['action']

    # Desktop notification
    if priority in ['urgent', 'high']:
        send_desktop_notification(
            title=f"⚠️ {priority.upper()} Approval Needed",
            message=f"{action} requires your review",
            urgency='critical' if priority == 'urgent' else 'normal'
        )

    # Email notification (for urgent only)
    if priority == 'urgent':
        send_email_notification(approval)

    # Update dashboard
    update_dashboard_approval_count()
```

## Silver Tier Capabilities

✅ Monitor /Pending_Approval folder
✅ Execute approved actions via appropriate skills
✅ Log all approval decisions
✅ Handle approval timeouts
✅ Track approval analytics
✅ Support multiple action types
✅ Batch approval support
✅ Configurable approval rules

## Future Enhancements (Gold Tier)

- Mobile app for approval management
- Voice approval via phone call
- AI-powered risk assessment
- Approval delegation workflows
- Smart approval recommendations
- Integration with calendar for context
- Multi-level approval chains

## Troubleshooting

**Approvals not executing:**
- Check /Approved folder permissions
- Verify executor scripts are working
- Review execution logs
- Test individual skills manually

**Timeout not working:**
- Verify timeout checker is running
- Check system clock accuracy
- Review timeout configuration
- Ensure cron job is active

**Missing notifications:**
- Check notification settings
- Verify email/desktop notification setup
- Review notification logs
- Test notification system

## Security Considerations

- Approval files should not contain passwords
- Limit who can move files to /Approved
- Audit all approval decisions
- Monitor for approval bypasses
- Regular review of auto-approve rules
- Encrypt sensitive approval content

## Best Practices

### For Users
- Review approvals promptly
- Provide rejection reasons
- Edit content when needed
- Monitor approval analytics
- Adjust timeouts based on patterns

### For System
- Clear, concise approval requests
- Accurate safety checks
- Appropriate timeout values
- Detailed execution logging
- Regular cleanup of old approvals

---
*Part of the Silver Tier AI Employee implementation*
