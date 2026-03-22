# Instagram Watcher

Monitors Instagram for DMs, comments, and engagement opportunities.

## Features

- Monitors Instagram direct messages
- Checks for notifications
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

2. **Setup Instagram Session** (one-time):
```bash
# Run the Instagram poster setup to create session
python ../.claude/skills/instagram-poster/scripts/setup_instagram_session.py
```

3. **Start Watcher**:
```bash
python instagram/instagram_watcher.py \
  --vault "../AI_Employee_Vault" \
  --session "instagram/.browser-session" \
  --interval 300
```

## Usage

### Command Line Arguments
- `--vault` (required): Path to AI Employee Vault
- `--session` (required): Path to browser session directory
- `--interval` (optional): Check interval in seconds (default: 300)

### Example
```bash
python instagram/instagram_watcher.py \
  --vault "../AI_Employee_Vault" \
  --session "instagram/.browser-session" \
  --interval 300
```

## Monitored Keywords

The watcher detects messages containing:
- urgent
- help
- question
- inquiry
- interested
- price
- buy

## Output

Creates files in `AI_Employee_Vault/Needs_Action/` with format:
```
INSTAGRAM_DIRECT_MESSAGE_ig_dm_20260321_235959.md
INSTAGRAM_NOTIFICATION_ig_notif_20260321_235959.md
```

## Logs

Logs are written to:
- `AI_Employee_Vault/Logs/InstagramWatcher.log`

## Troubleshooting

**Session expired**:
```bash
# Re-run setup
python ../.claude/skills/instagram-poster/scripts/setup_instagram_session.py
```

**No DMs detected**:
- Check if logged in
- Verify keywords match your use case
- Check logs for errors

**Watcher stops**:
- Check logs for errors
- Verify Instagram UI hasn't changed
- Restart watcher
