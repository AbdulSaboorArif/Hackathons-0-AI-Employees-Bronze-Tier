# AI Employee System - CORRECT Architecture ✅

## 🎯 Core Principle

**Use ONLY existing components from hackathon architecture:**
- Watchers (Perception)
- Skills (Reasoning + Action)
- Orchestrator (Watcher manager)
- System Scheduler (Automation trigger)

**NO custom automation layers. NO parallel systems.**

---

## 📐 Correct Architecture

```
┌─────────────────────────────────────────────────────────────┐
│           HACKATHON-COMPLIANT ARCHITECTURE                  │
└─────────────────────────────────────────────────────────────┘

PERCEPTION LAYER (Continuous)
┌──────────────────────────────────────┐
│  orchestrator.py                     │
│  ├─ LinkedIn Watcher                │
│  ├─ Gmail Watcher                   │
│  └─ WhatsApp Watcher                │
└──────────────────────────────────────┘
         ↓
    Creates files in: Needs_Action/


REASONING LAYER (Scheduled - Every 5 min)
┌──────────────────────────────────────┐
│  Windows Task Scheduler              │
│  Triggers: claude "/ai-employee-processor" │
└──────────────────────────────────────┘
         ↓
┌──────────────────────────────────────┐
│  /ai-employee-processor skill        │
│  - Reads Needs_Action/               │
│  - Calls /reasoning-loop if needed   │
│  - Creates approval requests         │
└──────────────────────────────────────┘
         ↓
    Creates files in: Pending_Approval/


HUMAN APPROVAL (Manual)
┌──────────────────────────────────────┐
│  User reviews and moves to Approved/ │
└──────────────────────────────────────┘


ACTION LAYER (Scheduled - Every 5 min)
┌──────────────────────────────────────┐
│  Windows Task Scheduler              │
│  Triggers: claude "/approval-manager" │
└──────────────────────────────────────┘
         ↓
┌──────────────────────────────────────┐
│  /approval-manager skill             │
│  - Reads Approved/                   │
│  - Executes via MCP servers          │
│  - Moves to Done/                    │
└──────────────────────────────────────┘
```

---

## 🚀 Complete Setup (3 Steps)

### Step 1: Start Watchers (Perception)

```bash
cd watchers
python orchestrator.py --config config.json
```

**What this does:**
- Runs LinkedIn, Gmail, WhatsApp watchers continuously
- Monitors for new notifications, emails, messages
- Creates action files in `Needs_Action/`

**Keep this running** in a terminal or use process manager (PM2, nohup).

---

### Step 2: Setup Task Scheduler (Reasoning + Action)

**Run as Administrator:**
```powershell
powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1
```

**What this does:**
- Creates scheduled task: `AI_Process_Tasks` (every 5 min)
  - Calls `/ai-employee-processor` skill
  - Processes items in `Needs_Action/`
  - Creates approval requests

- Creates scheduled task: `AI_Execute_Approvals` (every 5 min)
  - Calls `/approval-manager` skill
  - Executes approved actions
  - Moves to `Done/`

**This runs automatically** - no need to keep terminal open.

---

### Step 3: Human-in-the-Loop (Your Role)

**Periodically check:**
```
AI_Employee_Vault/Pending_Approval/
```

**Review and approve:**
1. Read the proposed action
2. If approved: Move file to `Approved/`
3. If rejected: Move file to `Rejected/`

**That's it.** The system handles everything else.

---

## 🔄 Complete Workflow Example

### Example: LinkedIn Comment Detected

**1. Watcher Detects (Continuous)**
```
[LinkedIn Watcher via orchestrator.py]
Detects: New comment on your post
↓
Creates: Needs_Action/LINKEDIN_20260321_comment.md
```

**2. Processor Analyzes (Every 5 min via Task Scheduler)**
```
[Task Scheduler triggers]
Runs: claude "/ai-employee-processor"
↓
[/ai-employee-processor skill]
Reads: Needs_Action/LINKEDIN_20260321_comment.md
Analyzes: Should we reply?
Calls: /reasoning-loop for complex analysis
↓
Creates: Pending_Approval/LINKEDIN_REPLY_20260321.md
```

**3. You Approve (Manual)**
```
[You check Pending_Approval/]
Review: LINKEDIN_REPLY_20260321.md
Decision: Looks good
Action: Move to Approved/
```

**4. System Executes (Every 5 min via Task Scheduler)**
```
[Task Scheduler triggers]
Runs: claude "/approval-manager"
↓
[/approval-manager skill]
Reads: Approved/LINKEDIN_REPLY_20260321.md
Calls: MCP server post_to_linkedin
↓
[MCP Server]
Uses: Playwright automation
Posts: Reply to LinkedIn
↓
Moves: To Done/LINKEDIN_REPLY_20260321_COMPLETED.md
Logs: To Logs/
```

**Total time**: ~10 minutes (5 min to process + 5 min to execute)
**Your time**: 30 seconds (review and approve)

---

## 📋 System Components (What Exists)

### Watchers (Perception)
- `watchers/orchestrator.py` - Runs all watchers
- `watchers/linkedin/linkedin_watcher.py` - Monitors LinkedIn
- `watchers/gmail/gmail_watcher.py` - Monitors Gmail
- `watchers/whatsapp/whatsapp_watcher.py` - Monitors WhatsApp

### Skills (Reasoning + Action)
- `/ai-employee-processor` - Processes tasks
- `/reasoning-loop` - Complex task planning
- `/approval-manager` - Executes approved actions
- `/linkedin-poster` - Creates LinkedIn posts
- `/email-sender` - Sends emails
- `/whatsapp-messenger` - Sends WhatsApp messages

### MCP Servers (External Actions)
- `communications-mcp-server` - Email, LinkedIn, WhatsApp tools

### Automation (Triggers)
- `setup_scheduler.ps1` - Windows Task Scheduler setup
- System cron (Linux/Mac alternative)

---

## ✅ What Was Fixed

### ❌ Wrong Approach (Deleted):
- `autonomous_loop.py` - Custom automation layer
- `start_autonomous.bat` - Startup script
- `stop_autonomous.bat` - Stop script
- Parallel processing system

### ✅ Correct Approach (Using):
- `orchestrator.py` - Existing watcher manager
- Skills - Existing reasoning/action components
- Task Scheduler - System-level automation
- Vault workflow - Existing approval process

---

## 🎓 Key Principles

### 1. Use Existing Components
- ✅ orchestrator.py for watchers
- ✅ Skills for all processing
- ✅ System scheduler for automation
- ❌ No custom automation scripts

### 2. Follow Hackathon Architecture
- Perception → Watchers
- Reasoning → Skills (/ai-employee-processor, /reasoning-loop)
- Action → Skills + MCP (/approval-manager, MCP servers)

### 3. Maintain Human-in-the-Loop
- All sensitive actions require approval
- User moves files to Approved/
- System executes only approved actions

### 4. No Parallel Systems
- One orchestrator for watchers
- One scheduler for skills
- One vault for workflow
- No duplicate automation

---

## 🔧 Management Commands

### View Scheduled Tasks
```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like "AI_*"}
```

### Check Task Status
```powershell
Get-ScheduledTask -TaskName "AI_Process_Tasks" | Get-ScheduledTaskInfo
Get-ScheduledTask -TaskName "AI_Execute_Approvals" | Get-ScheduledTaskInfo
```

### Disable Tasks (Pause System)
```powershell
Disable-ScheduledTask -TaskName "AI_Process_Tasks"
Disable-ScheduledTask -TaskName "AI_Execute_Approvals"
```

### Enable Tasks (Resume System)
```powershell
Enable-ScheduledTask -TaskName "AI_Process_Tasks"
Enable-ScheduledTask -TaskName "AI_Execute_Approvals"
```

### Remove Tasks (Uninstall)
```powershell
Unregister-ScheduledTask -TaskName "AI_Process_Tasks" -Confirm:$false
Unregister-ScheduledTask -TaskName "AI_Execute_Approvals" -Confirm:$false
```

### Check Watcher Status
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep orchestrator
```

---

## 📊 Monitoring

### Check Logs
```bash
# Watcher logs
type AI_Employee_Vault\Logs\LinkedInWatcher.log
type AI_Employee_Vault\Logs\GmailWatcher.log

# Skill execution logs
type AI_Employee_Vault\Logs\autonomous_loop_*.log
```

### Check Vault Status
```bash
# Pending tasks
dir AI_Employee_Vault\Needs_Action

# Pending approvals
dir AI_Employee_Vault\Pending_Approval

# Approved actions
dir AI_Employee_Vault\Approved

# Completed tasks
dir AI_Employee_Vault\Done
```

### Check Dashboard
```bash
# Open in Obsidian or text editor
AI_Employee_Vault\Dashboard.md
```

---

## 🚨 Troubleshooting

### Tasks Not Running
**Check:**
1. Are tasks enabled?
   ```powershell
   Get-ScheduledTask -TaskName "AI_*"
   ```
2. Is Claude Code installed?
   ```bash
   claude --version
   ```
3. Check Task Scheduler logs in Event Viewer

### Watchers Not Detecting
**Check:**
1. Is orchestrator running?
   ```bash
   tasklist | findstr python
   ```
2. Are browser sessions logged in?
3. Check watcher logs in `AI_Employee_Vault/Logs/`

### Approvals Not Executing
**Check:**
1. Files are in `Approved/` folder (not `Pending_Approval/`)
2. Task Scheduler is running the approval-manager task
3. Check execution logs

---

## 📖 Summary

### System Components:
- **Watchers**: Run via `orchestrator.py` (continuous)
- **Processing**: Run via Task Scheduler → `/ai-employee-processor` (every 5 min)
- **Execution**: Run via Task Scheduler → `/approval-manager` (every 5 min)
- **Approval**: Manual (you move files to Approved/)

### No Custom Automation:
- ❌ No autonomous_loop.py
- ❌ No start/stop scripts
- ❌ No parallel systems
- ✅ Only existing components

### Fully Autonomous:
- ✅ Watchers monitor continuously
- ✅ Tasks process automatically
- ✅ Approvals execute automatically
- ✅ You only review and approve

---

**Status**: ✅ CORRECTLY FIXED
**Architecture**: Hackathon-compliant
**Automation**: System scheduler + existing skills
**No new layers**: Using only existing components
