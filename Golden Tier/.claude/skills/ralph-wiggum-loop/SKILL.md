# Ralph Wiggum Loop Skill

**Description**: Autonomous multi-step task completion using Stop hook pattern. Keeps Claude working until task moves to /Done folder.

## Concept

The Ralph Wiggum loop is a Stop hook that intercepts Claude's exit and re-injects the prompt if the task isn't complete. Named after the Simpsons character who famously said "I'm helping!" - it keeps the AI working autonomously until the job is done.

## How It Works

1. **Orchestrator creates state file** with task prompt
2. **Claude works on task** (read, think, plan, execute)
3. **Claude tries to exit** after completing work
4. **Stop hook checks**: Is task file in /Done?
5. **YES** → Allow exit (task complete)
6. **NO** → Block exit, re-inject prompt (loop continues)
7. **Repeat** until complete or max iterations reached

## Setup

1. **Create Stop Hook**:
```bash
mkdir -p .claude/hooks
```

2. **Configure in settings.json**:
```json
{
  "hooks": {
    "stop": {
      "command": "python",
      "args": [".claude/hooks/ralph_wiggum_stop.py"],
      "enabled": true
    }
  }
}
```

3. **Test the Loop**:
```bash
python scripts/start_ralph_loop.py \
  --vault "../../AI_Employee_Vault" \
  --task "Process all files in Needs_Action" \
  --max-iterations 10
```

## Stop Hook Implementation

The hook checks for completion signals:

**Method 1: Promise-based (Simple)**
```python
# Claude outputs completion signal
print("<promise>TASK_COMPLETE</promise>")
```

**Method 2: File movement (Advanced - Recommended)**
```python
# Hook detects when task file moves to /Done
if task_file_in_done_folder():
    allow_exit()
else:
    re_inject_prompt()
```

## State File Format

The orchestrator creates a state file to track the loop:

```json
{
  "task_id": "process_inbox_20260321",
  "prompt": "Process all files in Needs_Action folder",
  "created": "2026-03-21T20:00:00Z",
  "max_iterations": 10,
  "current_iteration": 1,
  "completion_check": "file_movement",
  "target_file": "AI_Employee_Vault/Needs_Action/TASK_*.md",
  "done_folder": "AI_Employee_Vault/Done/"
}
```

## Usage Patterns

### Pattern 1: Process Inbox
```python
# Start loop to process all pending tasks
start_ralph_loop(
    prompt="Process all files in Needs_Action, create plans, and move to Done",
    completion_check="folder_empty",
    target_folder="AI_Employee_Vault/Needs_Action"
)
```

### Pattern 2: Multi-Step Task
```python
# Complex task requiring multiple steps
start_ralph_loop(
    prompt="Create invoice for Client A, send via email, log to Odoo",
    completion_check="file_movement",
    target_file="AI_Employee_Vault/Plans/PLAN_invoice_client_a.md"
)
```

### Pattern 3: Weekly Audit
```python
# Autonomous weekly business audit
start_ralph_loop(
    prompt="Generate CEO briefing, analyze revenue, identify bottlenecks",
    completion_check="promise",
    max_iterations=5
)
```

## Safety Features

### Max Iterations
Prevents infinite loops:
```python
max_iterations = 10  # Stop after 10 attempts
```

### Timeout
Prevents hanging:
```python
timeout_minutes = 30  # Stop after 30 minutes
```

### Error Detection
Stops on repeated failures:
```python
if same_error_3_times:
    stop_loop_and_alert()
```

### Human Override
User can stop loop anytime:
```bash
# Create stop signal file
touch .claude/hooks/STOP_RALPH_LOOP
```

## Integration with Orchestrator

The orchestrator manages Ralph loops:

```python
# orchestrator.py
def start_autonomous_task(task_file):
    # Create state file
    state = create_state_file(task_file)

    # Start Claude with Ralph loop
    subprocess.run([
        'claude',
        '--prompt', state['prompt'],
        '--hook-enabled', 'stop'
    ])

    # Monitor completion
    while not is_complete(state):
        time.sleep(5)

    # Cleanup
    cleanup_state_file(state)
```

## Monitoring

Track loop progress:

```bash
# View current state
cat .claude/hooks/ralph_state.json

# View loop log
tail -f .claude/hooks/ralph_loop.log
```

## Troubleshooting

**Loop never exits**:
- Check completion condition
- Verify file paths
- Review Claude's output
- Check max iterations

**Loop exits too early**:
- Task not actually complete
- Completion check too lenient
- File moved prematurely

**Infinite loop**:
- Max iterations not set
- Completion condition never met
- Bug in Stop hook logic

**Performance issues**:
- Reduce max iterations
- Add delays between iterations
- Optimize task complexity

## Best Practices

1. **Clear Completion Criteria**: Define exactly when task is done
2. **Reasonable Max Iterations**: Usually 5-10 is sufficient
3. **Monitor First Runs**: Watch the loop to ensure it works correctly
4. **Graceful Degradation**: Handle errors without crashing
5. **Audit Logging**: Log all loop activity for review

## Advanced: Nested Loops

For complex workflows:

```python
# Main loop: Process all inbox items
start_ralph_loop(
    prompt="Process all Needs_Action items",
    completion_check="folder_empty"
)

# Each item may trigger sub-loop:
# - Create plan (sub-loop 1)
# - Execute plan (sub-loop 2)
# - Verify completion (sub-loop 3)
```

## Security Considerations

⚠️ **Important**:
- Ralph loops run autonomously
- Always set max iterations
- Monitor first runs closely
- Use for trusted tasks only
- Review logs regularly
- Have kill switch ready

## Resources

- [Claude Code Hooks Documentation](https://docs.anthropic.com/claude-code/hooks)
- [Ralph Wiggum Reference Implementation](https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum)
