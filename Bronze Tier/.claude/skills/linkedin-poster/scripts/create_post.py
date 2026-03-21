#!/usr/bin/env python3
"""
LinkedIn Post Creator
Creates LinkedIn post drafts and approval requests following the Silver Tier workflow
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import argparse

class LinkedInPostCreator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.linkedin_content = self.vault_path / 'LinkedIn_Content' / 'Drafts'
        self.logs_dir = self.vault_path / 'Logs'

        # Create directories if they don't exist
        self.pending_approval.mkdir(parents=True, exist_ok=True)
        self.linkedin_content.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def read_company_handbook(self):
        """Read LinkedIn strategy from Company Handbook"""
        handbook_path = self.vault_path / 'Company_Handbook.md'
        if handbook_path.exists():
            return handbook_path.read_text(encoding='utf-8')
        return ""

    def generate_post_content(self, topic: str = None, template: str = "business_update"):
        """Generate LinkedIn post content based on template"""

        templates = {
            "business_update": """🚀 Exciting update from our team!

We've been working on building an AI Employee system that automates routine tasks while keeping humans in the loop for important decisions.

Key highlights:
• Automated monitoring of emails, WhatsApp, and LinkedIn
• Smart task processing with approval workflows
• 24/7 operation with human oversight
• Built with Claude Code and Obsidian

This is the future of personal productivity - AI that works for you, not instead of you.

What's your experience with AI automation? Let me know in the comments!

#AI #Automation #Productivity #TechInnovation #AIEmployee""",

            "thought_leadership": """💡 After building an AI Employee system, here's what I learned:

The key to successful AI automation isn't replacing humans - it's augmenting them.

Three principles that made our system work:
1. Human-in-the-loop for sensitive decisions
2. Transparent audit trails for all actions
3. Local-first architecture for privacy

The result? 24/7 monitoring and task processing while maintaining full control.

The future isn't AI vs humans. It's AI + humans working together.

What's your take on AI automation? Share your thoughts below!

#ArtificialIntelligence #Leadership #FutureOfWork #TechTrends""",

            "project_showcase": """🎯 Just completed a fascinating project: Building a Personal AI Employee

The challenge: Automate routine tasks without losing human oversight
The solution: An AI system that monitors, processes, and acts - but always asks permission first

Tech stack:
• Claude Code for reasoning
• Obsidian for knowledge management
• Python watchers for monitoring
• MCP servers for external actions

The system now handles:
✅ Email triage and drafting
✅ WhatsApp message monitoring
✅ LinkedIn engagement
✅ Task orchestration

All with human approval for sensitive actions.

Interested in building your own AI Employee? Happy to share insights!

#ProjectShowcase #AIEngineering #Automation #BuildInPublic"""
        }

        if topic:
            # Custom topic - create simple post
            return f"""💡 {topic}

I've been exploring this topic and wanted to share some thoughts with the community.

What's your experience with this? Let me know in the comments!

#Business #Technology #Innovation"""

        return templates.get(template, templates["business_update"])

    def create_draft_post(self, content: str, category: str = "business_update"):
        """Create draft post file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'post_{timestamp}.md'
        filepath = self.linkedin_content / filename

        draft_content = f"""---
type: linkedin_post
category: {category}
status: draft
created: {datetime.now().isoformat()}
---

{content}
"""

        filepath.write_text(draft_content, encoding='utf-8')
        return filepath

    def create_approval_request(self, post_content: str, draft_file: Path):
        """Create approval request in Pending_Approval folder"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'LINKEDIN_POST_{timestamp}.md'
        filepath = self.pending_approval / filename

        approval_content = f"""---
type: approval_request
action: linkedin_post
created: {datetime.now().isoformat()}
expires: {datetime.now().replace(hour=23, minute=59).isoformat()}
status: pending
draft_file: {draft_file.name}
---

## Post Content

{post_content}

## Engagement Strategy

- **Best time to post:** Tuesday-Thursday, 9:00 AM - 11:00 AM
- **Target audience:** Business professionals, entrepreneurs, tech enthusiasts
- **Expected reach:** 500-1500 impressions in first 24 hours
- **Engagement goal:** 20+ reactions, 5+ comments

## LinkedIn Posting Guidelines

✅ Professional tone maintained
✅ Value-focused content (not overly promotional)
✅ Includes relevant hashtags (3-5)
✅ Encourages engagement with question/CTA
✅ Length appropriate (under 3000 characters)

## To Approve

Move this file to `/Approved` folder to authorize posting.

## To Reject

Move this file to `/Rejected` folder or add feedback below.

## Feedback (Optional)

<!-- Add any changes or feedback here before approving -->

---
*Approval required before posting to LinkedIn*
*This ensures all public content aligns with your brand and messaging*
"""

        filepath.write_text(approval_content, encoding='utf-8')
        return filepath

    def log_action(self, action: str, details: dict):
        """Log post creation action"""
        log_file = self.logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}_linkedin_actions.json"

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details
        }

        logs = []
        if log_file.exists():
            try:
                content = json.loads(log_file.read_text())
                # Handle both list and dict formats
                if isinstance(content, list):
                    logs = content
                elif isinstance(content, dict):
                    logs = [content]
                else:
                    logs = []
            except:
                logs = []

        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2))

    def create_post(self, topic: str = None, template: str = "business_update"):
        """Main workflow: Create post and approval request"""
        print("=" * 60)
        print("LinkedIn Post Creator")
        print("=" * 60)

        # Generate content
        print(f"\n[*] Generating post content (template: {template})...")
        content = self.generate_post_content(topic, template)

        # Create draft
        print(f"[*] Creating draft post...")
        draft_file = self.create_draft_post(content, template)
        print(f"[OK] Draft saved: {draft_file.name}")

        # Create approval request
        print(f"\n[*] Creating approval request...")
        approval_file = self.create_approval_request(content, draft_file)
        print(f"[OK] Approval request created: {approval_file.name}")

        # Log action
        self.log_action('post_created', {
            'draft_file': str(draft_file),
            'approval_file': str(approval_file),
            'template': template,
            'content_preview': content[:100] + '...'
        })

        print(f"\n{'=' * 60}")
        print("[OK] Post Creation Complete")
        print(f"{'=' * 60}")
        print(f"\n[INFO] Next Steps:")
        print(f"1. Review the post content in: {approval_file}")
        print(f"2. If approved, move to: Approved/ folder")
        print(f"3. If rejected, move to: Rejected/ folder")
        print(f"4. The approval-manager will detect and post after approval")
        print(f"\n[WARNING] IMPORTANT: Post will NOT be published until you approve it!")

        return {
            'success': True,
            'draft_file': str(draft_file),
            'approval_file': str(approval_file),
            'content_preview': content[:200]
        }

def main():
    parser = argparse.ArgumentParser(description='Create LinkedIn post with approval workflow')
    parser.add_argument('--vault', required=True, help='Path to Obsidian vault')
    parser.add_argument('--topic', help='Custom topic for post')
    parser.add_argument('--template', default='business_update',
                       choices=['business_update', 'thought_leadership', 'project_showcase'],
                       help='Post template to use')

    args = parser.parse_args()

    creator = LinkedInPostCreator(args.vault)
    result = creator.create_post(args.topic, args.template)

    # Output JSON for programmatic use
    print(f"\n{json.dumps(result, indent=2)}")

if __name__ == '__main__':
    main()
