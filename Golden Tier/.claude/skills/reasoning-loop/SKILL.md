---
name: reasoning-loop
description: |
  Claude reasoning loop that analyzes tasks, creates detailed Plan.md files, and
  executes multi-step workflows. This is the core reasoning engine that breaks down
  complex tasks into actionable steps with human oversight. Use this skill when you
  need to process complex tasks that require planning and multi-step execution.
---

# Reasoning Loop

The core reasoning engine that creates Plan.md files and executes multi-step workflows.

## Core Workflow

1. **Analyze** task from /Needs_Action
2. **Reason** about approach and requirements
3. **Create** detailed Plan.md in /Plans folder
4. **Execute** steps with checkboxes
5. **Request** approval for sensitive actions
6. **Update** plan as work progresses
7. **Move** to /Done when complete

## Usage

```bash
# Process a task with reasoning loop
/reasoning-loop

# Or invoke directly
claude "Analyze the task in Needs_Action and create a plan"
```

## What This Skill Does

### Task Analysis
- Reads tasks from /Needs_Action folder
- Analyzes complexity and requirements
- Identifies dependencies and risks
- Determines if planning is needed

### Plan Creation
- Creates structured Plan.md files
- Breaks down into actionable steps
- Adds checkboxes for tracking
- Includes context and reasoning

### Execution Management
- Tracks progress through checkboxes
- Requests approvals when needed
- Updates plan with results
- Handles errors and retries

### Completion Handling
- Verifies all steps completed
- Updates Dashboard.md
- Moves files to /Done
- Logs execution summary

## Plan.md File Format

```markdown
# /Plans/PLAN_task_name_YYYY-MM-DD.md
---
created: 2026-03-15T10:00:00Z
task_source: /Needs_Action/TASK_client_invoice.md
status: in_progress
priority: high
estimated_time: 30 minutes
---

## Objective

[Clear statement of what needs to be accomplished]

## Context

[Background information and why this task is needed]

## Analysis

[Claude's reasoning about the task]

Key considerations:
- [Consideration 1]
- [Consideration 2]
- [Consideration 3]

Potential risks:
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

## Execution Plan

### Step 1: [Action description]
- [ ] [Specific sub-task]
- [ ] [Specific sub-task]
**Status:** Pending
**Requires approval:** No

### Step 2: [Action description]
- [ ] [Specific sub-task]
- [ ] [Specific sub-task]
**Status:** Pending
**Requires approval:** Yes
**Approval file:** /Pending_Approval/ACTION_description.md

### Step 3: [Action description]
- [ ] [Specific sub-task]
- [ ] [Specific sub-task]
**Status:** Pending
**Requires approval:** No

## Dependencies

- Step 2 depends on Step 1 completion
- Step 3 depends on Step 2 approval

## Success Criteria

- [ ] All steps completed
- [ ] All approvals obtained
- [ ] Results verified
- [ ] Documentation updated

## Execution Log

### 2026-03-15 10:05 - Step 1 Started
[Details of what was done]

### 2026-03-15 10:15 - Step 1 Completed
[Results and any issues encountered]

### 2026-03-15 10:20 - Step 2 Approval Requested
[Approval request created at /Pending_Approval/...]

## Notes

[Any additional observations or learnings]
```

## Example: Invoice Request Task

### Input Task

```markdown
# /Needs_Action/WHATSAPP_client_a_invoice_request.md
---
type: whatsapp_message
from: Client A
received: 2026-03-15T09:30:00Z
priority: high
keywords: invoice, urgent
---

## Message Content

"Hi, I need the invoice for February urgently. Can you send it today?"

## Context
- Client: Client A
- Last invoice: January 2026
- Outstanding: February 2026
```

### Generated Plan

```markdown
# /Plans/PLAN_client_a_invoice_2026-03-15.md
---
created: 2026-03-15T09:35:00Z
task_source: /Needs_Action/WHATSAPP_client_a_invoice_request.md
status: in_progress
priority: high
estimated_time: 45 minutes
---

## Objective

Generate and send February 2026 invoice to Client A via email, then confirm via WhatsApp.

## Context

Client A requested their February invoice urgently via WhatsApp. They are a high-priority client with consistent payment history. Last invoice (January) was sent on time and paid within 7 days.

## Analysis

This is a routine invoice request but marked urgent. The task requires:
1. Generating the invoice (we have all necessary data)
2. Sending via email (requires approval - financial communication)
3. Confirming via WhatsApp (requires approval - client communication)

Key considerations:
- Client is high priority - fast response expected
- Invoice amount needs verification against project records
- Email and WhatsApp both require approval per Company_Handbook.md
- Should complete within 1 hour to meet "urgent" expectation

Potential risks:
- Invoice amount discrepancy - MITIGATION: Verify against project records
- Email delivery failure - MITIGATION: Confirm receipt before WhatsApp response
- Approval delays - MITIGATION: Mark approvals as high priority

## Execution Plan

### Step 1: Verify Invoice Details
- [x] Check project records for February work
- [x] Calculate total amount: $1,500
- [x] Verify payment terms: Net 30
- [x] Confirm client billing address
**Status:** Completed
**Requires approval:** No

### Step 2: Generate Invoice PDF
- [x] Create invoice document
- [x] Include itemized breakdown
- [x] Add payment instructions
- [x] Save to /Invoices/2026-02_Client_A.pdf
**Status:** Completed
**Requires approval:** No

### Step 3: Send Invoice via Email
- [ ] Draft professional email
- [ ] Attach invoice PDF
- [ ] Request approval
- [ ] Send after approval
**Status:** Pending approval
**Requires approval:** Yes
**Approval file:** /Pending_Approval/EMAIL_client_a_invoice_2026-03-15.md

### Step 4: Confirm via WhatsApp
- [ ] Draft confirmation message
- [ ] Request approval
- [ ] Send after approval
**Status:** Pending (depends on Step 3)
**Requires approval:** Yes
**Approval file:** /Pending_Approval/WHATSAPP_client_a_confirm_2026-03-15.md

### Step 5: Update Records
- [ ] Log invoice sent in accounting records
- [ ] Update Dashboard.md
- [ ] Move task to /Done
**Status:** Pending (depends on Step 4)
**Requires approval:** No

## Dependencies

- Step 3 depends on Step 2 completion
- Step 4 depends on Step 3 approval and execution
- Step 5 depends on Step 4 completion

## Success Criteria

- [x] Invoice amount verified: $1,500
- [ ] Email sent successfully
- [ ] WhatsApp confirmation sent
- [ ] Client acknowledges receipt
- [ ] All files moved to /Done

## Execution Log

### 2026-03-15 09:35 - Plan Created
Analyzed task and created execution plan with 5 steps.

### 2026-03-15 09:40 - Step 1 Completed
Verified invoice details:
- February services: Website maintenance, bug fixes
- Total hours: 30 hours @ $50/hour = $1,500
- Payment terms: Net 30 (due April 15, 2026)

### 2026-03-15 09:45 - Step 2 Completed
Generated invoice PDF:
- File: /Invoices/2026-02_Client_A.pdf
- Size: 245 KB
- Format: Professional template with company branding

### 2026-03-15 09:50 - Step 3 Approval Requested
Created email approval request:
- To: client@example.com
- Subject: February 2026 Invoice - $1,500
- Attachment: Invoice PDF
- Waiting for human approval

### 2026-03-15 10:15 - Step 3 Approved and Executed
Email sent successfully:
- Message ID: <abc123@gmail.com>
- Sent at: 10:15 AM
- Delivery confirmed

### 2026-03-15 10:20 - Step 4 Approval Requested
Created WhatsApp approval request:
- To: Client A
- Message: Confirmation that invoice was sent
- Waiting for human approval

### 2026-03-15 10:25 - Step 4 Approved and Executed
WhatsApp message sent successfully:
- Sent at: 10:25 AM
- Delivered and read

### 2026-03-15 10:30 - Step 5 Completed
Updated records:
- Dashboard.md updated with activity
- Invoice logged in accounting
- All files moved to /Done

## Notes

Total execution time: 55 minutes (slightly over estimate due to approval wait times)

Client responded positively via WhatsApp: "Thanks! Got it."

Learnings:
- Approval wait time was 25 minutes - consider adjusting timeout for high-priority items
- Invoice generation process is smooth and reliable
- Client prefers WhatsApp confirmation over email-only communication
```

## Reasoning Loop Process

### Phase 1: Task Intake

```python
# Pseudo-code for reasoning loop
def process_task(task_file):
    # Read task
    task = read_task(task_file)

    # Analyze complexity
    complexity = analyze_complexity(task)

    if complexity == 'simple':
        # Execute directly without plan
        execute_simple_task(task)
    else:
        # Create plan for complex task
        create_plan(task)
```

### Phase 2: Analysis & Planning

```python
def create_plan(task):
    # Analyze task
    analysis = {
        'objective': extract_objective(task),
        'context': gather_context(task),
        'considerations': identify_considerations(task),
        'risks': assess_risks(task)
    }

    # Break down into steps
    steps = decompose_into_steps(analysis)

    # Identify dependencies
    dependencies = map_dependencies(steps)

    # Determine approval requirements
    for step in steps:
        step['requires_approval'] = needs_approval(step)

    # Create plan file
    plan_file = create_plan_file(analysis, steps, dependencies)

    return plan_file
```

### Phase 3: Execution

```python
def execute_plan(plan_file):
    plan = read_plan(plan_file)

    for step in plan['steps']:
        # Check dependencies
        if not dependencies_met(step):
            continue

        # Execute step
        if step['requires_approval']:
            # Create approval request
            approval_file = create_approval_request(step)

            # Wait for approval
            wait_for_approval(approval_file)

            # Execute after approval
            result = execute_step(step)
        else:
            # Execute directly
            result = execute_step(step)

        # Update plan
        update_plan_progress(plan_file, step, result)

        # Log execution
        log_execution(plan_file, step, result)

    # Mark complete
    complete_plan(plan_file)
```

### Phase 4: Completion

```python
def complete_plan(plan_file):
    # Verify all steps completed
    if not all_steps_completed(plan_file):
        raise IncompleteError("Not all steps completed")

    # Update Dashboard
    update_dashboard(plan_file)

    # Move to Done
    move_to_done(plan_file)

    # Log summary
    log_completion_summary(plan_file)
```

## Integration with Other Skills

### With ai-employee-processor

```markdown
ai-employee-processor reads /Needs_Action
    ↓
Determines task needs planning
    ↓
Calls reasoning-loop skill
    ↓
reasoning-loop creates Plan.md
    ↓
Executes steps, creating approval requests
    ↓
approval-manager processes approvals
    ↓
reasoning-loop completes execution
    ↓
Updates Dashboard and moves to /Done
```

### With approval-manager

```markdown
reasoning-loop identifies step needs approval
    ↓
Creates approval request in /Pending_Approval
    ↓
Pauses execution of that step
    ↓
approval-manager detects approval file
    ↓
Human reviews and approves
    ↓
approval-manager executes approved action
    ↓
reasoning-loop continues with next step
```

## Configuration

Edit Company_Handbook.md to customize:

```markdown
## Reasoning Loop Configuration

### When to Create Plans
- Tasks with >3 steps
- Tasks involving multiple systems
- Tasks with dependencies
- Tasks requiring approvals
- Financial transactions
- Client communications

### Plan Detail Level
- High priority: Detailed steps with sub-tasks
- Normal priority: Standard step breakdown
- Low priority: High-level steps only

### Execution Behavior
- Auto-execute: Simple, safe steps
- Request approval: Sensitive actions
- Pause on error: Wait for human intervention
- Retry on failure: Transient errors (max 3 attempts)
```

## Monitoring Plan Execution

### Check Active Plans

```bash
# List all active plans
ls -la Plans/PLAN_*.md | grep -v "Done"

# View plan status
cat Plans/PLAN_task_name.md | grep "status:"

# Check execution log
cat Plans/PLAN_task_name.md | grep -A 20 "## Execution Log"
```

### Dashboard Integration

Plans are tracked in Dashboard.md:

```markdown
## Active Plans (3)

### High Priority
- **Client A Invoice** - Step 3/5 (Waiting for approval)
  - Created: 2 hours ago
  - [View Plan](/Plans/PLAN_client_a_invoice_2026-03-15.md)

### Normal Priority
- **Weekly Report** - Step 1/3 (In progress)
  - Created: 30 minutes ago
  - [View Plan](/Plans/PLAN_weekly_report_2026-03-15.md)

- **LinkedIn Content** - Step 2/4 (In progress)
  - Created: 1 hour ago
  - [View Plan](/Plans/PLAN_linkedin_content_2026-03-15.md)
```

## Silver Tier Capabilities

✅ Analyze complex tasks automatically
✅ Create detailed Plan.md files with reasoning
✅ Break down into actionable steps with checkboxes
✅ Track dependencies between steps
✅ Request approvals for sensitive actions
✅ Execute steps with progress tracking
✅ Update plans with execution logs
✅ Handle errors and retries
✅ Complete and archive finished plans

## Future Enhancements (Gold Tier)

- Ralph Wiggum loop for autonomous multi-step execution
- Parallel step execution for independent tasks
- Dynamic plan adjustment based on results
- Learning from past plans to improve future planning
- Plan templates for common task types
- Estimated time tracking and optimization

## Troubleshooting

**Plans not being created:**
- Check task complexity threshold
- Verify /Plans folder exists
- Review Company_Handbook.md rules

**Steps not executing:**
- Check dependencies are met
- Verify approvals obtained
- Review execution logs for errors

**Plans stuck in progress:**
- Check for pending approvals
- Review error logs
- Manually complete stuck steps

## Best Practices

### For Users
- Review plans before execution starts
- Respond to approval requests promptly
- Check execution logs for issues
- Provide feedback on plan quality

### For System
- Create clear, actionable steps
- Include sufficient context
- Log all execution details
- Update progress in real-time

---
*Part of the Silver Tier AI Employee implementation*
*Core reasoning engine for multi-step task execution*
