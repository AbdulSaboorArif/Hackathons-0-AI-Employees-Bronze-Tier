# Watchers - AI Employee Perception Layer

Watchers are the "senses" of your AI Employee. They continuously monitor various sources and create actionable items in the vault.

## Bronze Tier Watcher

### File System Watcher
Monitors the `Inbox/` folder for new files and creates action items.

**Features:**
- Detects new files in Inbox folder
- Creates detailed action files in Needs_Action/
- Identifies file types and suggests actions
- Runs continuously with configurable check interval

**Usage:**
```bash
cd watchers
python filesystem_watcher.py ../AI_Employee_Vault
```

**How it works:**
1. Watches the `Inbox/` folder every 30 seconds
2. When a new file appears, creates a markdown file in `Needs_Action/`
3. The action file contains file metadata and suggested next steps
4. Claude Code can then process these action files

**Testing:**
1. Start the watcher
2. Drop any file into `AI_Employee_Vault/Inbox/`
3. Check `AI_Employee_Vault/Needs_Action/` for the generated action file

## Architecture

```
File dropped in Inbox/
        ↓
FileSystemWatcher detects it
        ↓
Creates FILE_*.md in Needs_Action/
        ↓
Claude Code processes the action file
        ↓
Moves completed task to Done/
```

## Future Watchers (Silver/Gold Tier)

- **Gmail Watcher**: Monitors email for important messages
- **WhatsApp Watcher**: Monitors WhatsApp Web for urgent messages
- **Finance Watcher**: Monitors bank transactions and financial data
- **Calendar Watcher**: Monitors upcoming events and deadlines

## Process Management

For production use, run watchers with a process manager:

```bash
# Using PM2 (recommended)
pm2 start filesystem_watcher.py --interpreter python3 --name "fs-watcher"
pm2 save
pm2 startup

# Or using nohup (simple)
nohup python filesystem_watcher.py ../AI_Employee_Vault > watcher.log 2>&1 &
```

## Configuration

Edit the watcher parameters in the script:
- `check_interval`: Seconds between checks (default: 30)
- `vault_path`: Path to your Obsidian vault

---
*Part of the Bronze Tier AI Employee implementation*
