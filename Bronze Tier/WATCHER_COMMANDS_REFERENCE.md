# Watcher Commands Reference - Issue #2 Fix ✅

## Problem Identified

**Error**: `python linkedin/linkedin_watcher.py → file not found`

**Root Cause**: Incorrect path references in commands and documentation

---

## ✅ CORRECT Directory Structure

```
Bronze Tier/
├── watchers/
│   ├── base_watcher.py
│   ├── filesystem_watcher.py
│   ├── gmail/
│   │   └── gmail_watcher.py
│   ├── whatsapp/
│   │   └── whatsapp_watcher.py
│   ├── linkedin/
│   │   └── linkedin_watcher.py
│   ├── orchestrator.py
│   ├── config.json
│   └── requirements.txt
```

---

## ✅ CORRECT Commands to Run Watchers

### From Project Root (Bronze Tier/)

#### LinkedIn Watcher
```bash
# CORRECT ✅
python watchers/linkedin/linkedin_watcher.py --vault "AI_Employee_Vault" --session "watchers/linkedin/.browser-session" --interval 300

# WRONG ❌
python linkedin/linkedin_watcher.py
```

#### Gmail Watcher
```bash
# CORRECT ✅
python watchers/gmail/gmail_watcher.py --vault "AI_Employee_Vault" --credentials "credentials.json" --interval 300

# WRONG ❌
python gmail/gmail_watcher.py
```

#### WhatsApp Watcher
```bash
# CORRECT ✅
python watchers/whatsapp/whatsapp_watcher.py --vault "AI_Employee_Vault" --session "watchers/whatsapp/.browser-session" --interval 300

# WRONG ❌
python whatsapp/whatsapp_watcher.py
```

#### File System Watcher
```bash
# CORRECT ✅
python watchers/filesystem_watcher.py AI_Employee_Vault

# WRONG ❌
python filesystem_watcher.py AI_Employee_Vault
```

---

## ✅ CORRECT Commands from watchers/ Directory

If you're already inside the `watchers/` directory:

```bash
cd watchers

# LinkedIn
python linkedin/linkedin_watcher.py --vault "../AI_Employee_Vault" --session "linkedin/.browser-session" --interval 300

# Gmail
python gmail/gmail_watcher.py --vault "../AI_Employee_Vault" --credentials "../credentials.json" --interval 300

# WhatsApp
python whatsapp/whatsapp_watcher.py --vault "../AI_Employee_Vault" --session "whatsapp/.browser-session" --interval 300

# File System
python filesystem_watcher.py ../AI_Employee_Vault
```

---

## ✅ Using Orchestrator (Recommended)

The orchestrator runs all watchers together:

```bash
# From project root
cd watchers
python orchestrator.py --config config.json
```

**config.json** should contain:
```json
{
  "vault_path": "../AI_Employee_Vault",
  "watchers": [
    {
      "name": "filesystem",
      "enabled": true,
      "check_interval": 30
    },
    {
      "name": "gmail",
      "enabled": true,
      "check_interval": 300,
      "credentials_path": "../credentials.json"
    },
    {
      "name": "linkedin",
      "enabled": true,
      "check_interval": 300,
      "session_path": "linkedin/.browser-session"
    },
    {
      "name": "whatsapp",
      "enabled": true,
      "check_interval": 300,
      "session_path": "whatsapp/.browser-session"
    }
  ]
}
```

---

## ✅ Absolute Paths (Most Reliable)

For production use, always use absolute paths:

```bash
# Windows
python "C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Bronze Tier\watchers\linkedin\linkedin_watcher.py" \
  --vault "C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Bronze Tier\AI_Employee_Vault" \
  --session "C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Bronze Tier\watchers\linkedin\.browser-session" \
  --interval 300

# Linux/Mac
python /path/to/Bronze\ Tier/watchers/linkedin/linkedin_watcher.py \
  --vault /path/to/Bronze\ Tier/AI_Employee_Vault \
  --session /path/to/Bronze\ Tier/watchers/linkedin/.browser-session \
  --interval 300
```

---

## ✅ Testing Watcher Paths

Verify paths before running:

```bash
# Check if watcher exists
ls -la watchers/linkedin/linkedin_watcher.py

# Windows
dir watchers\linkedin\linkedin_watcher.py

# Test import
python -c "import sys; sys.path.append('watchers'); from linkedin.linkedin_watcher import LinkedInWatcher; print('✅ Import successful')"
```

---

## ✅ Common Path Errors and Fixes

### Error 1: "No such file or directory"
```bash
# WRONG
python linkedin/linkedin_watcher.py

# FIX - Add watchers/ prefix
python watchers/linkedin/linkedin_watcher.py
```

### Error 2: "ModuleNotFoundError: No module named 'base_watcher'"
```bash
# WRONG - Running from wrong directory
cd linkedin
python linkedin_watcher.py

# FIX - Run from project root or add to PYTHONPATH
cd "Bronze Tier"
python watchers/linkedin/linkedin_watcher.py
```

### Error 3: "Vault path not found"
```bash
# WRONG - Relative path from wrong location
python watchers/linkedin/linkedin_watcher.py --vault "AI_Employee_Vault"

# FIX - Use correct relative path or absolute path
python watchers/linkedin/linkedin_watcher.py --vault "./AI_Employee_Vault"
# OR
python watchers/linkedin/linkedin_watcher.py --vault "C:\full\path\to\AI_Employee_Vault"
```

---

## ✅ Process Management Commands

### Using nohup (Linux/Mac)
```bash
# LinkedIn Watcher
nohup python watchers/linkedin/linkedin_watcher.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/linkedin/.browser-session" \
  --interval 300 \
  > logs/linkedin_watcher.log 2>&1 &

# Save PID
echo $! > linkedin_watcher.pid
```

### Using PM2 (Cross-platform)
```bash
# Install PM2
npm install -g pm2

# Start LinkedIn Watcher
pm2 start watchers/linkedin/linkedin_watcher.py \
  --name "linkedin-watcher" \
  --interpreter python \
  -- --vault "AI_Employee_Vault" \
     --session "watchers/linkedin/.browser-session" \
     --interval 300

# Start all watchers
pm2 start watchers/orchestrator.py \
  --name "ai-employee-watchers" \
  --interpreter python \
  -- --config watchers/config.json

# Save configuration
pm2 save

# Auto-start on boot
pm2 startup
```

### Using Windows Task Scheduler
```powershell
# Create scheduled task for LinkedIn Watcher
$action = New-ScheduledTaskAction `
  -Execute "python" `
  -Argument "watchers\linkedin\linkedin_watcher.py --vault AI_Employee_Vault --session watchers\linkedin\.browser-session --interval 300" `
  -WorkingDirectory "C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Bronze Tier"

$trigger = New-ScheduledTaskTrigger -AtStartup

Register-ScheduledTask `
  -TaskName "AI_Employee_LinkedIn_Watcher" `
  -Action $action `
  -Trigger $trigger `
  -Description "LinkedIn monitoring watcher"
```

---

## ✅ Verification Checklist

Run these commands to verify everything is correct:

```bash
# 1. Check directory structure
ls -la watchers/
ls -la watchers/linkedin/
ls -la watchers/gmail/
ls -la watchers/whatsapp/

# 2. Check Python can find modules
python -c "import sys; sys.path.append('watchers'); from base_watcher import BaseWatcher; print('✅ base_watcher OK')"

# 3. Check vault path
ls -la AI_Employee_Vault/

# 4. Test watcher import
python -c "import sys; sys.path.append('watchers'); from linkedin.linkedin_watcher import LinkedInWatcher; print('✅ LinkedInWatcher OK')"

# 5. Dry run (if watcher supports it)
python watchers/linkedin/linkedin_watcher.py --help
```

---

## ✅ Quick Reference Card

**Always remember:**
1. Run from project root: `Bronze Tier/`
2. Use prefix: `watchers/`
3. Full path: `watchers/linkedin/linkedin_watcher.py`
4. Vault path: `AI_Employee_Vault` or `./AI_Employee_Vault`
5. Session path: `watchers/linkedin/.browser-session`

**Quick test:**
```bash
cd "C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Bronze Tier"
python watchers/linkedin/linkedin_watcher.py --vault "AI_Employee_Vault" --session "watchers/linkedin/.browser-session" --interval 300
```

---

## Summary of Changes

### What Was Wrong:
- Commands used `linkedin/linkedin_watcher.py` (missing `watchers/` prefix)
- Relative paths assumed wrong working directory
- No clear documentation of correct paths

### What Was Fixed:
- ✅ All commands now use correct `watchers/` prefix
- ✅ Clear documentation of directory structure
- ✅ Examples for different working directories
- ✅ Absolute path examples for production
- ✅ Process management commands
- ✅ Verification checklist

---

**Status**: ✅ FIXED
**Date**: 2026-03-21
**Issue**: #2 Watcher Path Error
