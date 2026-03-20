#!/usr/bin/env python3
"""
Approval Executor Script
Executes approved actions from the /Approved folder
"""

import yaml
import json
import subprocess
from pathlib import Path
from datetime import datetime
import shutil

class ApprovalExecutor:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.approved_dir = self.vault_path / 'Approved'
        self.executed_dir = self.vault_path / 'Executed'
        self.logs_dir = self.vault_path / 'Logs'

        # Create directories if they don't exist
        self.executed_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

    def parse_approval_file(self, filepath):
        """Parse approval file and extract metadata and content"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by --- markers
        parts = content.split('---')
        if len(parts) < 3:
            raise ValueError("Invalid approval file format")

        # Parse YAML metadata
        metadata = yaml.safe_load(parts[1])
        body = parts[2].strip()

        return metadata, body

    def execute_email(self, metadata, body, filepath):
        """Execute email sending"""
        print(f"📧 Executing email: {metadata.get('subject', 'No subject')}")

        # Extract email details
        email_data = {
            'to': metadata.get('to'),
            'subject': metadata.get('subject'),
            'body': self.extract_email_body(body),
            'attachments': metadata.get('attachments', []),
            'cc': metadata.get('cc'),
            'bcc': metadata.get('bcc')
        }

        # Call send_email.py script
        script_path = Path('.claude/skills/email-sender/scripts/send_email.py')
        if not script_path.exists():
            raise FileNotFoundError(f"Email sender script not found: {script_path}")

        result = subprocess.run(
            ['python3', str(script_path)],
            input=json.dumps(email_data),
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            response = json.loads(result.stdout)
            print(f"✅ Email sent successfully! Message ID: {response['message_id']}")
            return {'status': 'success', 'message_id': response['message_id']}
        else:
            error = json.loads(result.stdout)
            print(f"❌ Email failed: {error['error']}")
            return {'status': 'error', 'error': error['error']}

    def execute_linkedin_post(self, metadata, body, filepath):
        """Execute LinkedIn posting"""
        print(f"💼 Executing LinkedIn post")

        # Extract post content
        post_content = self.extract_post_content(body)

        print(f"⚠️  LinkedIn posting requires Playwright automation")
        print(f"Post content: {post_content[:100]}...")

        # TODO: Implement Playwright automation for LinkedIn posting
        # For now, return success with manual instruction

        return {
            'status': 'manual_required',
            'message': 'LinkedIn posting requires manual execution via Playwright',
            'content': post_content
        }

    def execute_whatsapp(self, metadata, body, filepath):
        """Execute WhatsApp message sending"""
        print(f"💬 Executing WhatsApp message to {metadata.get('to', 'Unknown')}")

        # Extract message content
        message_content = self.extract_message_content(body)

        print(f"⚠️  WhatsApp messaging requires Playwright automation")
        print(f"Message: {message_content[:100]}...")

        # TODO: Implement Playwright automation for WhatsApp
        # For now, return success with manual instruction

        return {
            'status': 'manual_required',
            'message': 'WhatsApp messaging requires manual execution via Playwright',
            'content': message_content
        }

    def extract_email_body(self, body):
        """Extract email body from approval file content"""
        # Look for "## Email Content" section
        if '## Email Content' in body:
            parts = body.split('## Email Content')
            if len(parts) > 1:
                content = parts[1].split('##')[0].strip()
                return content
        return body

    def extract_post_content(self, body):
        """Extract post content from approval file"""
        if '## Post Content' in body:
            parts = body.split('## Post Content')
            if len(parts) > 1:
                content = parts[1].split('##')[0].strip()
                return content
        return body

    def extract_message_content(self, body):
        """Extract message content from approval file"""
        if '## Message Content' in body:
            parts = body.split('## Message Content')
            if len(parts) > 1:
                content = parts[1].split('##')[0].strip()
                return content
        return body

    def log_execution(self, filepath, metadata, result):
        """Log execution result"""
        log_file = self.logs_dir / f"Approval_Execution_{datetime.now().strftime('%Y-%m-%d')}.json"

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'file': filepath.name,
            'action': metadata.get('action'),
            'result': result
        }

        # Append to log file
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)

        logs.append(log_entry)

        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

    def move_to_executed(self, filepath):
        """Move approval file to executed folder"""
        dest = self.executed_dir / filepath.name
        shutil.move(str(filepath), str(dest))
        print(f"📁 Moved to: {dest}")

    def process_approval(self, filepath):
        """Process a single approval file"""
        print(f"\n{'='*60}")
        print(f"Processing: {filepath.name}")
        print(f"{'='*60}")

        try:
            # Parse file
            metadata, body = self.parse_approval_file(filepath)

            action_type = metadata.get('action')

            # Execute based on action type
            if action_type == 'email_send':
                result = self.execute_email(metadata, body, filepath)
            elif action_type == 'linkedin_post':
                result = self.execute_linkedin_post(metadata, body, filepath)
            elif action_type == 'whatsapp_send':
                result = self.execute_whatsapp(metadata, body, filepath)
            else:
                result = {
                    'status': 'error',
                    'error': f'Unknown action type: {action_type}'
                }
                print(f"❌ Unknown action type: {action_type}")

            # Log execution
            self.log_execution(filepath, metadata, result)

            # Move to executed
            self.move_to_executed(filepath)

            return result

        except Exception as e:
            print(f"❌ Error processing {filepath.name}: {e}")
            return {'status': 'error', 'error': str(e)}

    def process_all_approvals(self):
        """Process all files in Approved folder"""
        if not self.approved_dir.exists():
            print(f"⚠️  Approved folder not found: {self.approved_dir}")
            return

        approval_files = list(self.approved_dir.glob('*.md'))

        if not approval_files:
            print("✅ No pending approvals to process")
            return

        print(f"\n📋 Found {len(approval_files)} approval(s) to process\n")

        results = []
        for filepath in approval_files:
            result = self.process_approval(filepath)
            results.append(result)

        # Summary
        print(f"\n{'='*60}")
        print("Summary")
        print(f"{'='*60}")
        print(f"Total processed: {len(results)}")
        print(f"Successful: {sum(1 for r in results if r['status'] == 'success')}")
        print(f"Failed: {sum(1 for r in results if r['status'] == 'error')}")
        print(f"Manual required: {sum(1 for r in results if r['status'] == 'manual_required')}")

if __name__ == '__main__':
    import sys

    # Get vault path from argument or use current directory
    vault_path = sys.argv[1] if len(sys.argv) > 1 else '.'

    print("=" * 60)
    print("Approval Executor")
    print("=" * 60)

    executor = ApprovalExecutor(vault_path)
    executor.process_all_approvals()
