# AI Employee - Bronze Tier Setup Guide

Welcome to your Personal AI Employee! This guide will help you set up the Bronze Tier foundation.

## Prerequisites

- Python 3.13+ installed
- Claude Code installed and configured
- Obsidian (optional, for viewing the vault)
- Basic command line knowledge

## Installation Steps

### 1. Verify Python Installation

```bash
python --version
# Should show Python 3.13 or higher
```

### 2. Navigate to Project Directory

```bash
cd "C:\Users\dell\Desktop\Hackathon 0 AI Employees"
```

### 3. Verify Folder Structure

Check that these folders exist:
```
AI_Employee_Vault/
├── Inbox/
├── Needs_Action/
├── Done/
├── Plans/
├── Logs/
├── Pending_Approval/
├── Approved/
├── Rejected/
├── Accounting/
└── Briefings/
```

### 4. Review Configuration Files

**Dashboard.md** - Your system status dashboard
```bash
# View in any text editor or Obsidian
notepad AI_Employee_Vault\Dashboard.md
```

**Company_Handbook.md** - Customize your AI's behavior
```bash
notepad AI_Employee_Vault\Company_Handbook.md
```

### 5. Start the File System Watcher

```bash
cd watchers
python filesystem_watcher.py ../AI_Employee_Vault
```

You should see:
```
============================================================
File System Watcher - Bronze Tier
============================================================
Vault: ..\AI_Employee_Vault
Inbox: ..\AI_Employee_Vault\Inbox
Check interval: 30 seconds
============================================================

Watching for new files... (Press Ctrl+C to stop)
```

### 6. Test the System

**In a new terminal window:**

```bash
# Create a test file
echo "This is a test document" > "AI_Employee_Vault\Inbox\test_document.txt"
```

**Check the watcher output** - You should see:
```
Found 1 new item(s)
Created action file: FILE_test_document_20260314_HHMMSS.md
```

**Verify the action file was created:**
```bash
dir AI_Employee_Vault\Needs_Action
```

### 7. Process Tasks with Claude Code

```bash
# From the project root
claude "Read all files in AI_Employee_Vault/Needs_Action and process them according to Company_Handbook.md rules. Create plans if needed and update Dashboard.md"
```

Or use the skill:
```bash
claude /ai-employee-processor
```

### 8. Verify Results

Check these locations:
- `AI_Employee_Vault/Dashboard.md` - Should show updated activity
- `AI_Employee_Vault/Plans/` - May contain plan files
- `AI_Employee_Vault/Done/` - Completed tasks moved here

## Optional: Open in Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Select `AI_Employee_Vault` folder
4. Explore your AI Employee's workspace visually

## Daily Usage

### Morning Routine
1. Start the watcher (if not running)
2. Check Dashboard.md for overnight activity
3. Review Needs_Action/ folder
4. Process tasks with Claude Code

### Adding Tasks
- Drop files in `Inbox/` folder
- Watcher automatically creates action items
- Claude processes them on next run

### Reviewing Work
- Check `Dashboard.md` for summary
- Review `Logs/` for detailed audit trail
- Check `Done/` for completed tasks

## Troubleshooting

### Watcher Won't Start
```bash
# Check Python version
python --version

# Try running with full path
python C:\Users\dell\Desktop\Hackathon 0 AI Employees\watchers\filesystem_watcher.py C:\Users\dell\Desktop\Hackathon 0 AI Employees\AI_Employee_Vault
```

### Files Not Detected
- Ensure files are in `Inbox/` not subfolders
- Check watcher is running (look for console output)
- Verify file permissions

### Claude Can't Read Vault
```bash
# Make sure you're in the right directory
cd "C:\Users\dell\Desktop\Hackathon 0 AI Employees"

# Use absolute paths if needed
claude "Read C:\Users\dell\Desktop\Hackathon 0 AI Employees\AI_Employee_Vault\Dashboard.md"
```

## What's Next?

### Bronze Tier Complete ✅
You now have:
- Working Obsidian vault
- File system watcher
- Claude Code integration
- Basic task processing

### Silver Tier Goals
- Gmail watcher
- MCP servers for external actions
- Human-in-the-loop approval workflow
- Automated scheduling
- LinkedIn integration

### Gold Tier Goals
- Multiple watchers (Gmail, WhatsApp, LinkedIn)
- Full cross-domain integration
- Odoo accounting integration
- Social media automation
- Weekly CEO briefings

## Support

- Review `BRONZE_TIER_COMPLETE.md` for architecture details
- Check `AI_Employee_Vault/README.md` for vault structure
- See `watchers/README.md` for watcher documentation
- Join Wednesday Research Meetings for community support

---
*Bronze Tier Setup Complete - You're ready to build your AI Employee!*
