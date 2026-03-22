---
name: whatsapp-messenger
description: |
  Send and monitor WhatsApp messages via WhatsApp Web automation. Detects urgent
  messages, drafts replies, and manages client communications. Use this skill when
  you need to respond to WhatsApp messages, send updates to clients, or monitor
  conversations for business opportunities.
---

# WhatsApp Messenger

Automate WhatsApp communication via WhatsApp Web with Playwright.

## Core Workflow

1. **Monitor** WhatsApp Web for new messages
2. **Detect** urgent keywords and priority contacts
3. **Draft** appropriate responses
4. **Request** approval for sensitive messages
5. **Send** via Playwright automation
6. **Log** all conversations

## Usage

```bash
# Process WhatsApp messages
/whatsapp-messenger

# Or invoke directly
claude "Check WhatsApp for urgent messages and draft replies"
```

## What This Skill Does

### Message Monitoring
- Watches for unread messages
- Detects urgent keywords (urgent, asap, payment, invoice, help)
- Prioritizes messages from important contacts
- Creates action items in /Needs_Action

### Response Drafting
- Generates contextual replies
- Follows company communication style
- Includes relevant information
- Maintains professional tone

### Message Sending
- Sends via WhatsApp Web automation
- Supports text messages
- Can send media (images, documents)
- Handles group messages

### Conversation Tracking
- Logs all interactions
- Tracks response times
- Identifies potential leads
- Creates follow-up tasks

## WhatsApp Web Setup

### Prerequisites

1. WhatsApp account with active phone number
2. Playwright browser automation
3. Persistent browser session for login persistence

### First-Time Setup

```bash
# 1. Start Playwright server with persistent context
npx @playwright/mcp@latest --port 8808 --shared-browser-context &

# 2. Navigate to WhatsApp Web
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_navigate \
  -p '{"url": "https://web.whatsapp.com"}'

# 3. Scan QR code with your phone (first time only)
# Take screenshot to see QR code
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_take_screenshot \
  -p '{"type": "png", "fullPage": true}'

# 4. Wait for login to complete
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_wait_for \
  -p '{"text": "Chats", "time": 30000}'
```

### Session Persistence

The browser context persists between runs, so you only need to scan the QR code once.

## Message Detection

### Urgent Keywords
```python
URGENT_KEYWORDS = [
    'urgent', 'asap', 'emergency', 'help',
    'invoice', 'payment', 'due', 'deadline',
    'problem', 'issue', 'error', 'broken',
    'meeting', 'call', 'now', 'immediately'
]
```

### Priority Contacts
```markdown
# /Vault/WhatsApp_Contacts.md
---
priority_contacts:
  - name: Client A
    phone: +1234567890
    priority: high
    auto_respond: false
  - name: Client B
    phone: +0987654321
    priority: medium
    auto_respond: true
---
```

## Message Request Format

When urgent messages are detected:

```markdown
# /Needs_Action/WHATSAPP_client_a_2026-03-15.md
---
type: whatsapp_message
from: Client A
phone: +1234567890
received: 2026-03-15T10:30:00Z
priority: high
keywords: invoice, urgent
status: pending
---

## Message Content

"Hi, I need the invoice for last month urgently. Can you send it today?"

## Context
- Client: Client A
- Last interaction: 2026-03-10
- Outstanding invoices: 1 (February 2026)
- Relationship: Active client, 6 months

## Suggested Response

"Hi Client A! I'll send you the February invoice right away. You should receive it within the next hour. Let me know if you need anything else!"

## Actions Required
- [ ] Generate February invoice
- [ ] Send invoice via email
- [ ] Confirm receipt with client
```

## Approval Workflow

For sensitive messages, approval is required:

```markdown
# /Pending_Approval/WHATSAPP_REPLY_client_a_2026-03-15.md
---
type: approval_request
action: send_whatsapp
to: Client A
phone: +1234567890
created: 2026-03-15T10:35:00Z
expires: 2026-03-15T12:00:00Z
status: pending
---

## Message to Send

"Hi Client A! I'll send you the February invoice right away. You should receive it within the next hour. Let me know if you need anything else!"

## Context
- Responding to urgent invoice request
- Client is high priority
- Invoice is ready to send

## Safety Checks
✅ Professional tone
✅ Accurate information
✅ Appropriate response time
✅ No sensitive data in message

## To Approve
Move this file to /Approved folder.

## To Edit
Modify the message above, then move to /Approved.

## To Reject
Move this file to /Rejected folder.
```

## Sending Messages via Playwright

```bash
# 1. Get current page state
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_snapshot -p '{}'

# 2. Search for contact
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_click \
  -p '{"element": "Search input box", "ref": "e10"}'

python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_type \
  -p '{"element": "Search input", "ref": "e10", "text": "Client A"}'

# 3. Click on contact
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_click \
  -p '{"element": "Client A chat", "ref": "e15"}'

# 4. Type message
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_type \
  -p '{"element": "Message input", "ref": "e20", "text": "Your message here"}'

# 5. Send message
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_click \
  -p '{"element": "Send button", "ref": "e25"}'

# 6. Verify sent
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_wait_for \
  -p '{"text": "Your message here", "time": 5000}'
```

## Message Templates

### Invoice Request Response
```markdown
---
template: invoice_request
---

Hi {{client_name}}! I'll send you the {{period}} invoice right away. You should receive it within the next hour. Let me know if you need anything else!
```

### Payment Confirmation
```markdown
---
template: payment_confirmation
---

Hi {{client_name}}, I've received your payment of {{amount}} for {{invoice_number}}. Thank you! Your receipt will be sent via email shortly.
```

### Meeting Confirmation
```markdown
---
template: meeting_confirmation
---

Hi {{client_name}}, confirmed! Our meeting is scheduled for {{date}} at {{time}}. Looking forward to it!
```

### General Inquiry Response
```markdown
---
template: general_inquiry
---

Hi {{client_name}}, thanks for reaching out! {{custom_response}} Let me know if you have any other questions.
```

## Conversation Logging

All WhatsApp interactions are logged:

```markdown
# /Logs/WhatsApp_Log_2026-03-15.md
---
date: 2026-03-15
total_messages: 12
urgent_messages: 3
---

## Conversations

### 10:30 - Client A (Urgent)
**Received:** "Hi, I need the invoice for last month urgently. Can you send it today?"
**Sent:** "Hi Client A! I'll send you the February invoice right away. You should receive it within the next hour. Let me know if you need anything else!"
**Status:** Sent successfully
**Response time:** 5 minutes
**Approved by:** Human review

### 11:45 - Lead B
**Received:** "What are your rates for web design?"
**Sent:** "Hi! Our web design packages start at $2,500. I can send you a detailed proposal. Would you like to schedule a call to discuss your project?"
**Status:** Sent successfully
**Response time:** 8 minutes
**Approved by:** Human review

## Lead Indicators
- 2 new inquiries about services
- 1 payment confirmation
- 3 follow-up tasks created

## Response Time Stats
- Average: 6.5 minutes
- Fastest: 3 minutes
- Slowest: 15 minutes
```

## Auto-Response Rules

Configure in Company_Handbook.md:

```markdown
## WhatsApp Communication Rules

### Auto-Approve Conditions
- Simple confirmations (Yes, OK, Thanks)
- Status updates to known clients
- Routine check-ins

### Always Require Approval
- New contacts
- Financial discussions
- Pricing information
- Meeting scheduling
- Problem resolution

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
```

## Lead Detection

The skill identifies potential business opportunities:

```python
LEAD_INDICATORS = [
    'pricing', 'rates', 'cost', 'quote', 'proposal',
    'interested', 'looking for', 'need help with',
    'can you', 'do you offer', 'services',
    'project', 'work together', 'hire'
]

def is_potential_lead(message):
    """Detect if message indicates business opportunity"""
    text = message['text'].lower()
    return any(indicator in text for indicator in LEAD_INDICATORS)
```

When leads are detected:

```markdown
# /Needs_Action/LEAD_whatsapp_2026-03-15.md
---
type: lead
source: whatsapp
contact: Unknown Contact
phone: +1122334455
received: 2026-03-15T14:20:00Z
priority: high
---

## Lead Message

"Hi, I'm looking for someone to design a website for my new business. What are your rates?"

## Lead Qualification
- Service interest: Web design
- Budget: Unknown
- Timeline: Unknown
- Decision maker: Likely yes (new business owner)

## Recommended Actions
- [ ] Send pricing information
- [ ] Request project details
- [ ] Schedule discovery call
- [ ] Add to CRM
- [ ] Send portfolio examples
```

## Safety Features

### Message Validation
- Check message length (max 4096 characters)
- Verify phone number format
- Prevent spam/bulk messaging
- Rate limiting (max 30 messages/hour)

### Content Filtering
- No sensitive information (passwords, credit cards)
- Professional language only
- No automated marketing messages
- Comply with WhatsApp terms of service

### Privacy Protection
- Never share client information
- Don't discuss other clients
- Secure conversation logs
- Regular log cleanup (90 days)

## Silver Tier Capabilities

✅ Monitor WhatsApp Web for messages
✅ Detect urgent keywords and priority contacts
✅ Draft contextual responses
✅ Human-in-the-loop approval workflow
✅ Send messages via Playwright automation
✅ Log all conversations
✅ Identify potential leads
✅ Track response times

## Future Enhancements (Gold Tier)

- AI-powered response generation
- Multi-language support
- Voice message transcription
- Media file handling (images, documents)
- Group chat management
- Automated follow-ups
- CRM integration

## Troubleshooting

**WhatsApp Web not loading:**
- Check internet connection
- Restart Playwright server
- Clear browser cache
- Re-scan QR code

**Messages not sending:**
- Verify contact exists
- Check message format
- Ensure browser is logged in
- Review rate limits

**Session expired:**
- Re-scan QR code on phone
- Check phone is connected to internet
- Verify WhatsApp app is active

**Automation detected:**
- Add random delays between actions
- Don't send too many messages quickly
- Use human-like typing patterns
- Vary message timing

## Important Notes

⚠️ **WhatsApp Terms of Service:** Automated messaging may violate WhatsApp's terms. Use responsibly and primarily for responding to incoming messages, not bulk outreach.

⚠️ **Account Safety:** Excessive automation can lead to account bans. Always use human-in-the-loop approval and reasonable rate limits.

⚠️ **Privacy:** WhatsApp conversations are end-to-end encrypted. Respect user privacy and comply with data protection regulations.

---
*Part of the Silver Tier AI Employee implementation*
