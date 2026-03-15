---
name: ai-employee-processor
description: |
  Process tasks from the AI Employee vault. Reads items from Needs_Action folder,
  creates plans, and manages task workflow. Use this skill when you need to process
  pending tasks, review action items, or manage the AI Employee workflow.
---

# AI Employee Task Processor

This skill enables Claude Code to act as your AI Employee by processing tasks from the Obsidian vault.

## Core Workflow

1. **Read** items from `/Needs_Action` folder
2. **Analyze** the task and context from Company_Handbook.md
3. **Create** a plan in `/Plans` folder if needed
4. **Execute** or request approval for actions
5. **Move** completed items to `/Done` folder
6. **Update** Dashboard.md with activity

## Usage

```bash
# Process all pending tasks
/ai-employee-processor

# Or invoke directly
claude "Process all items in Needs_Action folder following Company_Handbook rules"
```

## What This Skill Does

### Task Processing
- Reads all .md files in Needs_Action/
- Analyzes each task based on Company_Handbook.md rules
- Determines if immediate action or approval is needed
- Creates detailed plans for multi-step tasks

### Decision Making
- Follows rules from Company_Handbook.md
- Identifies tasks requiring human approval
- Prioritizes based on urgency keywords
- Suggests appropriate next actions

### File Management
- Creates plan files in Plans/ folder
- Moves completed tasks to Done/ folder
- Creates approval requests in Pending_Approval/
- Updates Dashboard.md with latest activity

### Logging
- Records all actions in Logs/ folder
- Maintains audit trail
- Timestamps all operations

## Example Flow

```
1. File dropped in Inbox/
   ↓
2. Watcher creates FILE_*.md in Needs_Action/
   ↓
3. AI Employee Processor reads the task
   ↓
4. Analyzes based on Company_Handbook rules
   ↓
5. Creates PLAN_*.md if multi-step
   ↓
6. Executes safe actions OR creates approval request
   ↓
7. Updates Dashboard.md
   ↓
8. Moves to Done/ when complete
```

## Approval Workflow

For sensitive actions, the processor creates approval files:

```markdown
# /Pending_Approval/ACTION_description.md
---
action: send_email
requires_approval: true
---

## Action Details
[Details of what will be done]

## To Approve
Move this file to /Approved folder

## To Reject
Move this file to /Rejected folder
```

## Configuration

Edit `Company_Handbook.md` to customize:
- Approval thresholds
- Priority keywords
- Communication rules
- Financial limits

## Bronze Tier Capabilities

✅ Read and process files from Needs_Action
✅ Create structured plans
✅ Follow Company_Handbook rules
✅ Update Dashboard
✅ Move completed tasks to Done
✅ Basic logging

## Future Enhancements (Silver/Gold)

- MCP integration for external actions
- Email sending capabilities
- Payment processing with approval
- Social media posting
- Automated scheduling

---
*Part of the Bronze Tier AI Employee implementation*
