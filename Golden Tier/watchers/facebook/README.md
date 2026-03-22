# Facebook Watcher

Monitors Facebook for notifications, messages, and engagement opportunities.

## Features

- Monitors Facebook notifications
- Checks for unread messages
- Detects urgent keywords
- Creates action files in Needs_Action folder
- Persistent browser session (login once)

## Setup

1. **Install Dependencies**:
```bash
cd watchers
pip install -r requirements.txt
playwright install chromium
```

2. **Setup Facebook Session** (one-time):
```bash
# Run the Facebook poster setup to create session
python ../.claude/skills/facebook-poster/scripts/setup_facebook_session.py
```

3. **Start Watcher**:
```bash
python facebook/facebook_watcher.py \
  --vault "../AI_Employee_Vault" \
  --session "facebook/.browser-session" \
  --interval 300
```

## Usage

### Command Line Arguments
- `--vault` (required): Path to AI Employee Vault
- `--session` (required): Path to browser session directory
- `--interval` (optional): Check interval in seconds (default: 300)

### Example
```bash
python facebook/facebook_watcher.py \
  --vault "../AI_Employee_Vault" \
  --session "facebook/.browser-session" \
  --interval 300
```

## Monitored Keywords

The watcher detects messages containing:
- urgent
- asap
- help
- question
- inquiry
- interested

## Output

Creates files in `AI_Employee_Vault/Needs_Action/` with format:
```
FACEBOOK_NOTIFICATION_fb_notif_20260321_235959.md
FACEBOOK_MESSAGE_fb_msg_20260321_235959.md
```

## Logs

Logs are written to:
- `AI_Employee_Vault/Logs/FacebookWatcher.log`

## Troubleshooting

**Session expired**:
```bash
# Re-run setup
python ../.claude/skills/facebook-poster/scripts/setup_facebook_session.py
```

**No notifications detected**:
- Check if logged in
- Verify keywords match your use case
- Check logs for errors

**Watcher stops**:
- Check logs for errors
- Verify Facebook UI hasn't changed
- Restart watcher
