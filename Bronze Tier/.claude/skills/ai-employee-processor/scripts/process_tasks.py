#!/usr/bin/env python3
"""
AI Employee Task Processor
Core orchestrator that reads Needs_Action, analyzes tasks, and triggers appropriate skills
This is the "brain" that connects watchers → skills → actions
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import argparse
import subprocess

class AIEmployeeProcessor:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans = self.vault_path / 'Plans'
        self.done = self.vault_path / 'Done'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.logs_dir = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        self.handbook = self.vault_path / 'Company_Handbook.md'

        # Create directories
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.plans.mkdir(parents=True, exist_ok=True)
        self.done.mkdir(parents=True, exist_ok=True)
        self.pending_approval.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def read_handbook_rules(self):
        """Read Company Handbook for decision rules"""
        if self.handbook.exists():
            return self.handbook.read_text(encoding='utf-8')
        return ""

    def analyze_task(self, task_file: Path):
        """Analyze task file and determine type and priority"""
        content = task_file.read_text(encoding='utf-8')

        # Parse frontmatter
        metadata = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()

        # Determine task type from filename or metadata
        task_type = metadata.get('type', 'unknown')
        if 'EMAIL_' in task_file.name:
            task_type = 'email'
        elif 'WHATSAPP_' in task_file.name:
            task_type = 'whatsapp_message'
        elif 'LINKEDIN_' in task_file.name:
            task_type = 'linkedin_notification'
        elif 'FILE_' in task_file.name:
            task_type = 'file_drop'

        # Determine priority
        priority = metadata.get('priority', 'normal')

        # Check for urgent keywords
        urgent_keywords = ['urgent', 'asap', 'emergency', 'critical', 'help', 'invoice', 'payment']
        if any(kw in content.lower() for kw in urgent_keywords):
            priority = 'high'

        return {
            'file': task_file,
            'type': task_type,
            'priority': priority,
            'metadata': metadata,
            'content': content
        }

    def requires_approval(self, task_type: str, task_info: dict):
        """Determine if task requires human approval"""
        # Read handbook rules
        handbook = self.read_handbook_rules()

        # Always require approval for:
        approval_types = [
            'email',  # Sending emails
            'whatsapp_message',  # Sending WhatsApp
            'linkedin_post',  # Posting to LinkedIn
            'payment',  # Financial transactions
        ]

        if task_type in approval_types:
            return True

        # Check for financial keywords
        financial_keywords = ['payment', 'invoice', 'transfer', 'bank', '$', 'usd', 'eur']
        content = task_info.get('content', '').lower()
        if any(kw in content for kw in financial_keywords):
            return True

        return False

    def determine_action(self, task_info: dict):
        """Determine what action to take for this task"""
        task_type = task_info['type']
        priority = task_info['priority']

        actions = {
            'email': {
                'skill': 'email-sender',
                'action': 'draft_reply',
                'requires_approval': True
            },
            'whatsapp_message': {
                'skill': 'whatsapp-messenger',
                'action': 'draft_reply',
                'requires_approval': True
            },
            'linkedin_notification': {
                'skill': 'linkedin-engagement',
                'action': 'analyze_and_respond',
                'requires_approval': True
            },
            'linkedin_comment': {
                'skill': 'linkedin-engagement',
                'action': 'draft_reply',
                'requires_approval': True
            },
            'linkedin_connection_request': {
                'skill': 'linkedin-engagement',
                'action': 'review_profile',
                'requires_approval': True
            },
            'file_drop': {
                'skill': 'file-processor',
                'action': 'analyze_and_categorize',
                'requires_approval': False
            }
        }

        return actions.get(task_type, {
            'skill': 'manual-review',
            'action': 'review_required',
            'requires_approval': True
        })

    def create_simple_plan(self, task_info: dict, action: dict):
        """Create a simple plan for straightforward tasks"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        task_name = task_info['file'].stem
        plan_file = self.plans / f"PLAN_{task_name}_{timestamp}.md"

        plan_content = f"""---
created: {datetime.now().isoformat()}
task_source: {task_info['file'].name}
task_type: {task_info['type']}
priority: {task_info['priority']}
status: pending
---

## Objective

Process {task_info['type']} task: {task_info['file'].name}

## Task Details

**Type:** {task_info['type']}
**Priority:** {task_info['priority']}
**Source:** {task_info['file'].name}

## Recommended Action

**Skill:** {action['skill']}
**Action:** {action['action']}
**Requires Approval:** {'Yes' if action['requires_approval'] else 'No'}

## Execution Steps

### Step 1: Analyze Task
- [x] Read task file
- [x] Determine task type: {task_info['type']}
- [x] Assess priority: {task_info['priority']}
- [x] Check approval requirements: {'Required' if action['requires_approval'] else 'Not required'}

### Step 2: Execute Action
- [ ] Trigger {action['skill']} skill
- [ ] Perform {action['action']}
{'- [ ] Request human approval' if action['requires_approval'] else '- [ ] Execute directly'}

### Step 3: Complete
- [ ] Verify action completed
- [ ] Update Dashboard
- [ ] Move to Done folder

## Notes

Created by AI Employee Processor
"""

        plan_file.write_text(plan_content, encoding='utf-8')
        return plan_file

    def log_processing(self, task_info: dict, action: dict, result: str):
        """Log task processing"""
        log_file = self.logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}_task_processing.json"

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'task_file': task_info['file'].name,
            'task_type': task_info['type'],
            'priority': task_info['priority'],
            'action': action,
            'result': result
        }

        logs = []
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text())
            except:
                logs = []

        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2))

    def update_dashboard(self, summary: dict):
        """Update Dashboard.md with processing summary"""
        if not self.dashboard.exists():
            return

        dashboard_content = self.dashboard.read_text(encoding='utf-8')

        # Update last check time
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Add recent activity
        activity_line = f"- **[{datetime.now().strftime('%H:%M')}]** 🤖 Processed {summary['processed']} tasks"

        # Simple update - append to recent activity section
        if '## Recent Activity' in dashboard_content:
            parts = dashboard_content.split('## Recent Activity')
            if len(parts) == 2:
                # Insert new activity at the top of the list
                activity_section = parts[1].split('\n', 1)
                new_dashboard = (
                    parts[0] +
                    '## Recent Activity\n' +
                    activity_line + '\n' +
                    (activity_section[1] if len(activity_section) > 1 else '')
                )
                self.dashboard.write_text(new_dashboard, encoding='utf-8')

    def process_task(self, task_file: Path):
        """Process a single task"""
        print(f"\n{'='*60}")
        print(f"Processing: {task_file.name}")
        print(f"{'='*60}")

        # Analyze task
        task_info = self.analyze_task(task_file)
        print(f"📋 Type: {task_info['type']}")
        print(f"⚡ Priority: {task_info['priority']}")

        # Determine action
        action = self.determine_action(task_info)
        print(f"🎯 Action: {action['action']} via {action['skill']}")
        print(f"🔒 Approval: {'Required' if action['requires_approval'] else 'Not required'}")

        # Create plan
        plan_file = self.create_simple_plan(task_info, action)
        print(f"📝 Plan created: {plan_file.name}")

        # For now, we create the plan and log
        # In full implementation, we would trigger the skill here
        result = 'plan_created'

        if action['requires_approval']:
            print(f"⏳ Task requires human approval - waiting for user action")
            result = 'awaiting_approval'
        else:
            print(f"✅ Task can be auto-processed")
            result = 'ready_for_execution'

        # Log processing
        self.log_processing(task_info, action, result)

        return {
            'task': task_file.name,
            'type': task_info['type'],
            'priority': task_info['priority'],
            'action': action,
            'plan': plan_file.name,
            'result': result
        }

    def process_all_tasks(self):
        """Process all tasks in Needs_Action folder"""
        print("=" * 60)
        print("AI Employee Task Processor")
        print("=" * 60)

        # Get all task files
        task_files = list(self.needs_action.glob('*.md'))

        if not task_files:
            print("\n✅ No pending tasks to process")
            return {
                'processed': 0,
                'results': []
            }

        print(f"\n📋 Found {len(task_files)} task(s) to process\n")

        results = []
        for task_file in task_files:
            try:
                result = self.process_task(task_file)
                results.append(result)
            except Exception as e:
                print(f"❌ Error processing {task_file.name}: {e}")
                results.append({
                    'task': task_file.name,
                    'result': 'error',
                    'error': str(e)
                })

        # Summary
        print(f"\n{'='*60}")
        print("Processing Summary")
        print(f"{'='*60}")
        print(f"Total processed: {len(results)}")
        print(f"Plans created: {sum(1 for r in results if 'plan' in r)}")
        print(f"Awaiting approval: {sum(1 for r in results if r.get('result') == 'awaiting_approval')}")
        print(f"Ready for execution: {sum(1 for r in results if r.get('result') == 'ready_for_execution')}")
        print(f"Errors: {sum(1 for r in results if r.get('result') == 'error')}")

        # Update dashboard
        self.update_dashboard({
            'processed': len(results),
            'timestamp': datetime.now().isoformat()
        })

        return {
            'processed': len(results),
            'results': results
        }

def main():
    parser = argparse.ArgumentParser(description='AI Employee Task Processor')
    parser.add_argument('--vault', required=True, help='Path to Obsidian vault')

    args = parser.parse_args()

    processor = AIEmployeeProcessor(args.vault)
    result = processor.process_all_tasks()

    # Output JSON for programmatic use
    print(f"\n{json.dumps(result, indent=2)}")

if __name__ == '__main__':
    main()
