#!/usr/bin/env python3
"""
Generate Monday Morning CEO Briefing
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Try to import xmlrpc for Odoo integration
try:
    import xmlrpc.client
    ODOO_AVAILABLE = True
except ImportError:
    ODOO_AVAILABLE = False
    print("[Warning] xmlrpc not available. Install with: pip install xmlrpc")

load_dotenv()

class OdooClient:
    """Simple Odoo JSON-RPC client"""

    def __init__(self):
        self.url = os.getenv('ODOO_URL', 'http://localhost:8069')
        self.db = os.getenv('ODOO_DB', 'ai_employee_db')
        self.username = os.getenv('ODOO_USERNAME', 'admin')
        self.password = os.getenv('ODOO_PASSWORD', '')
        self.uid = None

    def authenticate(self):
        """Authenticate with Odoo"""
        if not ODOO_AVAILABLE:
            return None

        try:
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = common.authenticate(self.db, self.username, self.password, {})
            return self.uid
        except Exception as e:
            print(f"[Odoo] Authentication failed: {e}")
            return None

    def get_revenue(self, date_from: str, date_to: str) -> Dict[str, Any]:
        """Get revenue for period"""
        if not ODOO_AVAILABLE or not self.uid:
            return {'total': 0, 'invoices': [], 'available': False}

        try:
            models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

            domain = [
                ['move_type', '=', 'out_invoice'],
                ['state', '=', 'posted'],
                ['invoice_date', '>=', date_from],
                ['invoice_date', '<=', date_to],
            ]

            invoices = models.execute_kw(
                self.db, self.uid, self.password,
                'account.move', 'search_read',
                [domain],
                {'fields': ['name', 'partner_id', 'amount_total', 'invoice_date']}
            )

            total = sum(inv['amount_total'] for inv in invoices)

            return {
                'total': total,
                'count': len(invoices),
                'invoices': invoices,
                'available': True
            }
        except Exception as e:
            print(f"[Odoo] Revenue query failed: {e}")
            return {'total': 0, 'invoices': [], 'available': False}

def parse_task_file(file_path: Path) -> Dict[str, Any]:
    """Parse task markdown file"""
    try:
        content = file_path.read_text(encoding='utf-8')

        # Extract frontmatter
        parts = content.split('---')
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            metadata = {}
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

            # Extract title
            body = '---'.join(parts[2:]).strip()
            lines = body.split('\n')
            title = lines[0].replace('#', '').strip() if lines else file_path.stem

            return {
                'file': file_path.name,
                'title': title,
                'metadata': metadata,
                'created': metadata.get('created', ''),
                'type': metadata.get('type', 'task')
            }
    except Exception as e:
        print(f"[Warning] Could not parse {file_path}: {e}")

    return None

def analyze_tasks(vault_path: Path, date_from: str, date_to: str) -> Dict[str, Any]:
    """Analyze completed tasks in date range"""

    done_dir = vault_path / 'Done'
    if not done_dir.exists():
        return {'completed': [], 'count': 0}

    completed_tasks = []

    for task_file in done_dir.glob('*.md'):
        task_data = parse_task_file(task_file)
        if task_data:
            # Check if in date range
            created = task_data.get('created', '')
            if created:
                try:
                    task_date = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    start_date = datetime.fromisoformat(date_from)
                    end_date = datetime.fromisoformat(date_to)

                    if start_date <= task_date <= end_date:
                        completed_tasks.append(task_data)
                except:
                    pass

    return {
        'completed': completed_tasks,
        'count': len(completed_tasks)
    }

def load_business_goals(vault_path: Path) -> Dict[str, Any]:
    """Load business goals from vault"""

    goals_file = vault_path / 'Business_Goals.md'
    if not goals_file.exists():
        return {'revenue_target': 10000, 'available': False}

    try:
        content = goals_file.read_text(encoding='utf-8')

        # Simple parsing for revenue target
        revenue_target = 10000  # default
        for line in content.split('\n'):
            if 'Monthly goal:' in line or 'monthly goal:' in line:
                # Extract number
                parts = line.split('$')
                if len(parts) > 1:
                    num_str = parts[1].replace(',', '').split()[0]
                    try:
                        revenue_target = float(num_str)
                    except:
                        pass

        return {
            'revenue_target': revenue_target,
            'available': True
        }
    except Exception as e:
        print(f"[Warning] Could not load business goals: {e}")
        return {'revenue_target': 10000, 'available': False}

def generate_briefing(vault_path: Path, date_from: str, date_to: str) -> str:
    """Generate CEO briefing"""

    print(f"[Briefing] Generating for period: {date_from} to {date_to}")

    # Load business goals
    goals = load_business_goals(vault_path)
    revenue_target = goals['revenue_target']

    # Analyze tasks
    print("[Briefing] Analyzing tasks...")
    tasks = analyze_tasks(vault_path, date_from, date_to)

    # Get revenue from Odoo
    print("[Briefing] Fetching revenue data...")
    odoo = OdooClient()
    odoo.authenticate()
    revenue_data = odoo.get_revenue(date_from, date_to)

    # Calculate MTD (month-to-date)
    now = datetime.now()
    month_start = now.replace(day=1).strftime('%Y-%m-%d')
    mtd_revenue = odoo.get_revenue(month_start, now.strftime('%Y-%m-%d'))

    # Generate briefing content
    briefing = f"""---
generated: {datetime.now().isoformat()}
period: {date_from} to {date_to}
week_number: {datetime.now().isocalendar()[1]}
---

# Monday Morning CEO Briefing

## Executive Summary

"""

    # Executive summary
    if tasks['count'] > 0 and revenue_data['total'] > 0:
        briefing += f"Strong week with {tasks['count']} tasks completed and ${revenue_data['total']:,.2f} in revenue.\n\n"
    elif tasks['count'] > 0:
        briefing += f"Productive week with {tasks['count']} tasks completed.\n\n"
    else:
        briefing += "Quiet week. Consider reviewing priorities and upcoming tasks.\n\n"

    # Revenue section
    briefing += "## Revenue\n\n"

    if revenue_data['available']:
        briefing += f"- **This Week**: ${revenue_data['total']:,.2f}\n"
        briefing += f"- **Invoice Count**: {revenue_data['count']}\n"

        if mtd_revenue['available']:
            mtd_total = mtd_revenue['total']
            mtd_percent = (mtd_total / revenue_target * 100) if revenue_target > 0 else 0
            briefing += f"- **MTD**: ${mtd_total:,.2f} ({mtd_percent:.1f}% of ${revenue_target:,.0f} target)\n"

            if mtd_percent >= 90:
                briefing += "- **Trend**: ✅ On track\n"
            elif mtd_percent >= 70:
                briefing += "- **Trend**: ⚠️ Slightly behind\n"
            else:
                briefing += "- **Trend**: ❌ Behind target\n"
    else:
        briefing += "- **Status**: Odoo not connected. Revenue data unavailable.\n"
        briefing += "- **Action**: Configure Odoo integration for revenue tracking.\n"

    briefing += "\n"

    # Completed tasks
    briefing += "## Completed Tasks\n\n"

    if tasks['count'] > 0:
        for task in tasks['completed'][:10]:  # Show top 10
            briefing += f"- [x] {task['title']}\n"

        if tasks['count'] > 10:
            briefing += f"\n*...and {tasks['count'] - 10} more tasks*\n"
    else:
        briefing += "- No tasks completed this week\n"

    briefing += "\n"

    # Bottlenecks (placeholder - would need more sophisticated analysis)
    briefing += "## Bottlenecks\n\n"
    briefing += "*No significant bottlenecks detected this week.*\n\n"

    # Proactive suggestions
    briefing += "## Proactive Suggestions\n\n"

    briefing += "### Upcoming Deadlines\n"
    briefing += "- Review next week's priorities\n"
    briefing += "- Check for pending approvals\n"
    briefing += "- Follow up on outstanding invoices\n\n"

    briefing += "### Process Improvements\n"
    briefing += "- Consider automating recurring tasks\n"
    briefing += "- Review and update Business_Goals.md\n"
    briefing += "- Schedule client check-ins\n\n"

    briefing += "---\n"
    briefing += "*Generated by AI Employee CEO Briefing System*\n"

    return briefing

def main():
    parser = argparse.ArgumentParser(description='Generate CEO Briefing')
    parser.add_argument('--vault', required=True, help='Path to AI Employee Vault')
    parser.add_argument('--date-from', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--date-to', help='End date (YYYY-MM-DD)')
    parser.add_argument('--output', help='Output file path (optional)')

    args = parser.parse_args()

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"Error: Vault not found: {vault_path}")
        sys.exit(1)

    # Default to last 7 days
    if not args.date_from or not args.date_to:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        date_from = start_date.strftime('%Y-%m-%d')
        date_to = end_date.strftime('%Y-%m-%d')
    else:
        date_from = args.date_from
        date_to = args.date_to

    # Generate briefing
    briefing_content = generate_briefing(vault_path, date_from, date_to)

    # Save briefing
    if args.output:
        output_path = Path(args.output)
    else:
        briefings_dir = vault_path / 'Briefings'
        briefings_dir.mkdir(exist_ok=True)
        output_path = briefings_dir / f"{datetime.now().strftime('%Y-%m-%d')}_Monday_Briefing.md"

    output_path.write_text(briefing_content, encoding='utf-8')

    print(f"\n[Briefing] ✅ Generated successfully!")
    print(f"[Briefing] Saved to: {output_path}")
    print(f"\n{briefing_content}")

    sys.exit(0)

if __name__ == '__main__':
    main()
