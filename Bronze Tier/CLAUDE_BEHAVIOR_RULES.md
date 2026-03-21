# Claude Behavior Rules - Use Existing Code, Don't Duplicate ⚠️

## ✅ What This Document Is About

**Python scripts ARE necessary and MUST exist.**

**The problem**: Claude keeps creating NEW scripts instead of USING existing ones.

---

## 🎯 The Core Rule

**ALWAYS use existing skills, watchers, and scripts.**

**ONLY create new scripts when:**
1. Nothing exists yet for that functionality
2. User explicitly asks for a new script
3. Absolutely necessary to fulfill the task

**Write MINIMAL code when creating new scripts.**

---

## ✅ Correct Behavior Examples

### Example 1: LinkedIn Posting

**User asks**: "Post to LinkedIn about our new product"

**❌ WRONG (What Claude was doing):**
```python
# Creating new file: linkedin_post_new.py
from playwright.sync_api import sync_playwright

def post_to_linkedin(content):
    # 50 lines of code...
```

**✅ RIGHT (What Claude should do):**
```bash
# Use existing skill
/linkedin-poster
```

**Why**: The `/linkedin-poster` skill already exists. No need to create new script.

---

### Example 2: Running LinkedIn Watcher

**User asks**: "Start the LinkedIn watcher"

**❌ WRONG:**
```python
# Creating new file: start_linkedin_watcher.py
import subprocess
subprocess.run(['python', 'watchers/linkedin/linkedin_watcher.py'])
```

**✅ RIGHT:**
```bash
# Use existing watcher script
python watchers/linkedin/linkedin_watcher.py --vault "AI_Employee_Vault" --session "watchers/linkedin/.browser-session" --interval 300
```

**Why**: The watcher script already exists at `watchers/linkedin/linkedin_watcher.py`. Just run it.

---

### Example 3: Fixing a Bug

**User says**: "The LinkedIn post button isn't clicking"

**❌ WRONG:**
```python
# Creating new file: fixed_linkedin_post.py
# Entire new implementation...
```

**✅ RIGHT:**
```python
# Modify existing file: .claude/skills/communications-mcp-server/test_linkedin_post.py
# Change only the broken part:

# OLD CODE (line 112-118)
post_button_selectors = [
    'button:has-text("Post")',
    '.share-actions__primary-action',
]

# NEW CODE (line 112-125)
post_button_selectors = [
    'button.share-actions__primary-action:has-text("Post")',
    'button[aria-label*="Post"]',
    'button:has-text("Post"):visible',
    '.share-actions__primary-action',
]
```

**Why**: Fix the existing file, don't create a new one.

---

## 📋 What Already Exists (USE THESE)

### Skills (Use via /skill-name)
- `/linkedin-poster` - Post to LinkedIn
- `/email-sender` - Send emails
- `/whatsapp-messenger` - Send WhatsApp messages
- `/ai-employee-processor` - Process tasks
- `/approval-manager` - Execute approved actions
- `/reasoning-loop` - Complex task planning
- `/scheduler` - Schedule recurring tasks

### Watchers (Run these scripts)
- `python watchers/linkedin/linkedin_watcher.py` - Monitor LinkedIn
- `python watchers/gmail/gmail_watcher.py` - Monitor Gmail
- `python watchers/whatsapp/whatsapp_watcher.py` - Monitor WhatsApp
- `python watchers/filesystem_watcher.py` - Monitor Inbox folder
- `python watchers/orchestrator.py` - Run all watchers

### MCP Servers (Already implemented)
- `.claude/skills/communications-mcp-server/communications-mcp-server.js`
- Tools: `send_email`, `post_to_linkedin`, `send_whatsapp`

---

## 🔄 Correct Workflow

### When User Asks to Do Something:

1. **Check**: Does a skill exist for this?
   - YES → Use the skill (`/skill-name`)
   - NO → Go to step 2

2. **Check**: Does a watcher/script exist for this?
   - YES → Run the existing script
   - NO → Go to step 3

3. **Check**: Can I modify existing code to do this?
   - YES → Modify existing file
   - NO → Go to step 4

4. **Ask user**: "No existing code found. Should I create a new script?"
   - User says YES → Create MINIMAL new script
   - User says NO → Find alternative approach

---

## 🎯 Real-World Scenarios

### Scenario 1: "Post to LinkedIn"
```bash
# ✅ Use existing skill
/linkedin-poster

# ❌ Don't create new script
# linkedin_post_v2.py
```

### Scenario 2: "Start monitoring LinkedIn"
```bash
# ✅ Run existing watcher
python watchers/linkedin/linkedin_watcher.py --vault "AI_Employee_Vault" --session "watchers/linkedin/.browser-session" --interval 300

# ❌ Don't create new script
# start_linkedin_monitor.py
```

### Scenario 3: "Send an email"
```bash
# ✅ Use existing skill
/email-sender

# ❌ Don't create new script
# send_email_now.py
```

### Scenario 4: "Fix the Post button selector"
```python
# ✅ Modify existing file
# Edit: .claude/skills/communications-mcp-server/test_linkedin_post.py
# Change lines 112-118 only

# ❌ Don't create new file
# fixed_linkedin_post.py
```

### Scenario 5: "Process tasks in Needs_Action"
```bash
# ✅ Use existing skill
/ai-employee-processor

# ❌ Don't create new script
# process_tasks.py
```

---

## 🚨 When to Create New Scripts

### ✅ Create new script ONLY when:

1. **Truly new functionality**
   - Example: User wants to monitor Twitter (no Twitter watcher exists)
   - Create: `watchers/twitter/twitter_watcher.py`

2. **New skill requested**
   - Example: User wants Instagram posting (no Instagram skill exists)
   - Create: `.claude/skills/instagram-poster/`

3. **Test/debug scripts**
   - Example: Testing a specific API endpoint
   - Create: `test_api.py` (temporary, for debugging)

4. **User explicitly requests**
   - User: "Create a script to backup the vault"
   - Create: `backup_vault.py`

### ❌ Don't create new script when:

1. Skill already exists → Use the skill
2. Watcher already exists → Run the watcher
3. Similar code exists → Modify existing code
4. Can be done via vault workflow → Use vault folders
5. MCP tool exists → Use MCP tool

---

## 📝 Code Creation Guidelines

### When you MUST create new code:

1. **Keep it MINIMAL**
   - Only essential functionality
   - No unnecessary features
   - No over-engineering

2. **Follow existing patterns**
   - Use same structure as existing watchers/skills
   - Import from base classes
   - Follow naming conventions

3. **Document clearly**
   - Add comments explaining purpose
   - Include usage examples
   - Note dependencies

4. **Ask first if unsure**
   - "Should I create a new script for this?"
   - "Or should I modify existing code?"

---

## 🎓 Learning from Past Mistakes

### Mistake 1: Creating duplicate LinkedIn posting scripts
**What happened**: Created `linkedin_post.py`, `post_to_linkedin.py`, `linkedin_automation.py`
**What exists**: `/linkedin-poster` skill already does this
**Lesson**: Check for existing skills first

### Mistake 2: Creating new watcher scripts
**What happened**: Created `new_linkedin_watcher.py`
**What exists**: `watchers/linkedin/linkedin_watcher.py` already exists
**Lesson**: Check watchers/ directory first

### Mistake 3: Creating standalone automation scripts
**What happened**: Created `send_email.py`, `post_linkedin.py`
**What exists**: Skills and MCP servers already handle this
**Lesson**: Use the skill system, not standalone scripts

---

## ✅ Quick Decision Flowchart

```
User asks to do something
        ↓
Does a skill exist? ──YES──→ Use /skill-name
        ↓ NO
Does a watcher exist? ──YES──→ Run python watchers/...
        ↓ NO
Does similar code exist? ──YES──→ Modify existing file
        ↓ NO
Ask user: "Create new script?" ──YES──→ Create MINIMAL script
        ↓ NO
Find alternative approach
```

---

## 📊 Summary

### ✅ DO:
- Use existing skills via `/skill-name`
- Run existing watchers via `python watchers/...`
- Modify existing files to fix bugs
- Create MINIMAL code when necessary
- Ask user before creating new scripts

### ❌ DON'T:
- Create duplicate scripts
- Create new scripts when skills exist
- Create new watchers when they exist
- Over-engineer solutions
- Bypass existing architecture

---

## 🎯 The Golden Rule

**"Use what exists. Create only when nothing exists. Keep it minimal."**

---

**Status**: ✅ CLARIFIED
**Date**: 2026-03-21
**Issue**: #3 Claude Creating New Scripts
**Solution**: Use existing skills/watchers/scripts. Only create new code when absolutely necessary and keep it minimal.
