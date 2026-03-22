# Twitter Watcher

Monitors Twitter for mentions, DMs, and engagement opportunities.

## Features

- Monitors Twitter notifications
- Checks for mentions
- Monitors direct messages
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

2. **Setup Twitter Session** (one-time):
```bash
# Run the Twitter poster setup to create session
python ../.claude/skills/twitter-poster/scripts/setup_twitter_session.py
```

3. **Start Watcher**:
```bash
python twitter/twitter_watcher.py \
  --vault "../AI_Employee_Vault" \
  --session "twitter/.browser-session" \
  --interval 300
```

## Usage

### Command Line Arguments
- `--vault` (required): Path to AI Employee Vault
- `--session` (required): Path to browser session directory
- `--interval` (optional): Check interval in seconds (default: 300)

### Example
```bash
python twitter/twitter_watcher.py \
  --vault "../AI_Employee_Vault" \
  --session "twitter/.browser-session" \
  --interval 300
```

## Monitored Keywords

The watcher detects messages containing:
- urgent
- help
- question
- inquiry
- interested
- @ (mentions)

## Output

Creates files in `AI_Employee_Vault/Needs_Action/` with format:
```
TWITTER_NOTIFICATION_tw_notif_20260321_235959.md
TWITTER_MENTION_tw_mention_20260321_235959.md
TWITTER_DIRECT_MESSAGE_tw_dm_20260321_235959.md
```

## Logs

Logs are written to:
- `AI_Employee_Vault/Logs/TwitterWatcher.log`

## Troubleshooting

**Session expired**:
```bash
# Re-run setup
python ../.claude/skills/twitter-poster/scripts/setup_twitter_session.py
```

**No mentions detected**:
- Check if logged in
- Verify keywords match your use case
- Check logs for errors

**Watcher stops**:
- Check logs for errors
- Verify Twitter UI hasn't changed
- Restart watcher
