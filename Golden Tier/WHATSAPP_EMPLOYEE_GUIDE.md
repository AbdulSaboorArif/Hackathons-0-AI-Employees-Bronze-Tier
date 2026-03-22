# WhatsApp Employee - Complete Setup Guide

## Overview
The WhatsApp employee monitors WhatsApp Web for urgent messages, drafts replies, requests approval, and sends responses automatically.

## Components

### 1. WhatsApp Watcher
**Location**: `watchers/whatsapp/whatsapp_watcher.py`

**What it does**:
- Monitors WhatsApp Web every 60 seconds
- Detects messages with urgent keywords (urgent, asap, invoice, payment, help, etc.)
- Creates action files in `/Needs_Action` folder
- Uses persistent browser session (login once, stays logged in)

**How to run**:
```bash
python3 watchers/whatsapp/whatsapp_watcher.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/whatsapp/.browser-session" \
  --interval 60
```

**First time setup**:
1. Run the watcher
2. Browser window opens showing WhatsApp Web
3. Scan QR code with your phone
4. Session persists - no need to scan again

### 2. WhatsApp Message Sender
**Location**: `.claude/skills/whatsapp-messenger/scripts/send_whatsapp.py`

**What it does**:
- Sends approved messages via WhatsApp Web
- Searches for contact by name
- Types and sends the message
- Takes screenshots for verification
- Logs all sent messages

**How to use**:
```bash
python3 .claude/skills/whatsapp-messenger/scripts/send_whatsapp.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/whatsapp/.browser-session" \
  --approval-file "AI_Employee_Vault/Approved/WHATSAPP_reply_client.md"
```

## Complete Workflow

### Step 1: Watcher Detects Urgent Message
```
WhatsApp message received: "Hi, I need the invoice urgently!"
↓
Watcher detects keyword: "invoice", "urgently"
↓
Creates: /Needs_Action/WHATSAPP_20260321_Client_A.md
```

### Step 2: AI Drafts Reply
```
Claude reads the message
↓
Drafts professional reply
↓
Creates: /Pending_Approval/WHATSAPP_REPLY_Client_A.md
```

### Step 3: Human Approval
```
You review the draft reply
↓
Move file to /Approved folder
↓
Triggers sending workflow
```

### Step 4: Automated Sending
```
Sender script executes
↓
Opens WhatsApp Web
↓
Searches for contact
↓
Sends message
↓
Moves to /Done folder
```

## Approval File Format

When creating a WhatsApp reply for approval:

```markdown
---
type: whatsapp_reply
to: Client A
recipient: Client A
created: 2026-03-21T19:00:00Z
status: pending
---

## Message

Hi Client A!

I'll send you the invoice right away. You should receive it within the next hour.

Let me know if you need anything else!

Best regards,
Abdul Saboor Arif

## Context
- Original message: "Hi, I need the invoice urgently!"
- Detected keywords: invoice, urgently
- Priority: high
```

## Urgent Keywords

The watcher detects these keywords as urgent:
- urgent, asap, emergency, help
- invoice, payment, due, deadline
- problem, issue, error, broken
- meeting, call, now, immediately

## Testing the Workflow

### Test 1: Manual Message Detection
```bash
# Run single check
python3 test_whatsapp_watcher.py
```

### Test 2: Create Test Approval
```bash
# Create a test approval file
cat > AI_Employee_Vault/Pending_Approval/WHATSAPP_TEST.md << 'EOF'
---
type: whatsapp_reply
to: Test Contact
recipient: Test Contact
---

## Message

This is a test message from the AI Employee system.
EOF

# Move to Approved
mv AI_Employee_Vault/Pending_Approval/WHATSAPP_TEST.md AI_Employee_Vault/Approved/

# Send it
python3 .claude/skills/whatsapp-messenger/scripts/send_whatsapp.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/whatsapp/.browser-session" \
  --approval-file "AI_Employee_Vault/Approved/WHATSAPP_TEST.md"
```

## Continuous Operation

To run the watcher continuously in the background:

### Windows (using Task Scheduler)
```bash
# Create scheduled task that runs on startup
schtasks /create /tn "WhatsApp Watcher" /tr "python3 C:\path\to\watchers\whatsapp\whatsapp_watcher.py --vault AI_Employee_Vault --session watchers/whatsapp/.browser-session" /sc onstart
```

### Linux/Mac (using PM2)
```bash
# Install PM2
npm install -g pm2

# Start watcher
pm2 start watchers/whatsapp/whatsapp_watcher.py \
  --interpreter python3 \
  --name whatsapp-watcher \
  -- --vault AI_Employee_Vault --session watchers/whatsapp/.browser-session

# Save and auto-start on reboot
pm2 save
pm2 startup
```

## Security Notes

1. **Session Security**: The browser session contains your WhatsApp login. Keep the `.browser-session` folder secure.

2. **Message Privacy**: All messages are logged in `/Logs` folder. Review and clean periodically.

3. **Approval Required**: All outgoing messages require human approval by default. Never bypass this for sensitive communications.

4. **Rate Limiting**: Don't send too many messages too quickly to avoid WhatsApp restrictions.

## Troubleshooting

**Problem**: QR code not appearing
- Solution: Make sure browser window is visible (headless=False)
- Check if WhatsApp Web is accessible in your region

**Problem**: Contact not found
- Solution: Make sure contact name matches exactly as shown in WhatsApp
- Try using phone number instead: "+1234567890"

**Problem**: Message not sending
- Solution: Check screenshots in `/Logs` folder to see what went wrong
- Verify WhatsApp Web UI hasn't changed (selectors may need updating)

**Problem**: Session expired
- Solution: Delete `.browser-session` folder and scan QR code again

## Integration with Approval Manager

The approval-manager skill can automatically execute approved WhatsApp messages:

```python
# In approval-manager script
if approval_file.name.startswith('WHATSAPP_'):
    result = subprocess.run([
        'python3',
        '.claude/skills/whatsapp-messenger/scripts/send_whatsapp.py',
        '--vault', vault_path,
        '--session', 'watchers/whatsapp/.browser-session',
        '--approval-file', str(approval_file)
    ])
```

## Silver Tier Requirements ✅

- ✅ WhatsApp watcher monitoring for urgent messages
- ✅ Automated message sending via Playwright
- ✅ Human-in-the-loop approval workflow
- ✅ Logging and audit trail
- ✅ Persistent session (login once)

---

**Status**: WhatsApp employee fully functional and ready for Silver Tier demonstration.
