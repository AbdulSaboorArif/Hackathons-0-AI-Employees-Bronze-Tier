#!/usr/bin/env python3
"""
Golden Tier Verification Script
Checks all components are properly installed and configured
"""

import sys
import subprocess
from pathlib import Path
import json

def check_command(cmd, name):
    """Check if a command is available"""
    try:
        result = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=5)
        print(f"[OK] {name}: Available")
        return True
    except:
        print(f"[FAIL] {name}: Not found")
        return False

def check_file(path, name):
    """Check if a file exists"""
    if Path(path).exists():
        print(f"[OK] {name}: Found")
        return True
    else:
        print(f"[FAIL] {name}: Missing")
        return False

def check_directory(path, name):
    """Check if a directory exists"""
    if Path(path).exists() and Path(path).is_dir():
        print(f"[OK] {name}: Found")
        return True
    else:
        print(f"[FAIL] {name}: Missing")
        return False

def check_docker():
    """Check if Docker is running"""
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"[OK] Docker: Running")
            return True
        else:
            print(f"[FAIL] Docker: Not running")
            return False
    except:
        print(f"[FAIL] Docker: Not available")
        return False

def check_odoo():
    """Check if Odoo is accessible"""
    try:
        import urllib.request
        response = urllib.request.urlopen('http://localhost:8069', timeout=5)
        print(f"[OK] Odoo: Accessible at http://localhost:8069")
        return True
    except:
        print(f"[FAIL] Odoo: Not accessible at http://localhost:8069")
        return False

def main():
    print("="*60)
    print("GOLDEN TIER VERIFICATION")
    print("="*60)
    print()

    results = []

    # Check prerequisites
    print("[*] Prerequisites:")
    results.append(check_command('python', 'Python'))
    results.append(check_command('node', 'Node.js'))
    results.append(check_command('docker', 'Docker'))
    results.append(check_command('docker-compose', 'Docker Compose'))
    print()

    # Check Docker status
    print("[*] Docker Status:")
    results.append(check_docker())
    results.append(check_odoo())
    print()

    # Check vault structure
    print("[*] Vault Structure:")
    results.append(check_directory('AI_Employee_Vault', 'Vault'))
    results.append(check_directory('AI_Employee_Vault/Needs_Action', 'Needs_Action'))
    results.append(check_directory('AI_Employee_Vault/Pending_Approval', 'Pending_Approval'))
    results.append(check_directory('AI_Employee_Vault/Approved', 'Approved'))
    results.append(check_directory('AI_Employee_Vault/Done', 'Done'))
    results.append(check_directory('AI_Employee_Vault/Briefings', 'Briefings'))
    results.append(check_directory('AI_Employee_Vault/Logs', 'Logs'))
    results.append(check_file('AI_Employee_Vault/Business_Goals.md', 'Business_Goals.md'))
    results.append(check_file('AI_Employee_Vault/Company_Handbook.md', 'Company_Handbook.md'))
    print()

    # Check skills
    print("[*] Agent Skills:")
    skills = [
        'facebook-poster',
        'instagram-poster',
        'twitter-poster',
        'odoo-mcp-server',
        'ceo-briefing',
        'ralph-wiggum-loop',
        'linkedin-poster',
        'whatsapp-messenger',
        'email-sender',
    ]
    for skill in skills:
        results.append(check_directory(f'.claude/skills/{skill}', skill))
    print()

    # Check watchers
    print("[*] Watchers:")
    results.append(check_directory('watchers/facebook', 'Facebook watcher'))
    results.append(check_directory('watchers/instagram', 'Instagram watcher'))
    results.append(check_directory('watchers/twitter', 'Twitter watcher'))
    print()

    # Check documentation
    print("[*] Documentation:")
    results.append(check_file('GOLDEN_TIER_COMPLETE.md', 'GOLDEN_TIER_COMPLETE.md'))
    results.append(check_file('GOLDEN_TIER_SETUP.md', 'GOLDEN_TIER_SETUP.md'))
    results.append(check_file('ODOO_SETUP.md', 'ODOO_SETUP.md'))
    results.append(check_file('docker-compose.yml', 'docker-compose.yml'))
    print()

    # Check configuration files
    print("[*] Configuration:")
    results.append(check_file('.claude/skills/odoo-mcp-server/package.json', 'Odoo MCP package.json'))
    results.append(check_file('.claude/hooks/ralph_wiggum_stop.py', 'Ralph Wiggum hook'))
    print()

    # Summary
    print("="*60)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0

    print(f"RESULTS: {passed}/{total} checks passed ({percentage:.1f}%)")
    print("="*60)
    print()

    if percentage == 100:
        print("[SUCCESS] GOLDEN TIER COMPLETE!")
        print("All components verified and ready to use.")
        print()
        print("Next steps:")
        print("1. Start Odoo: docker-compose up -d")
        print("2. Setup social media sessions")
        print("3. Configure Business_Goals.md")
        print("4. Test each integration")
        sys.exit(0)
    elif percentage >= 80:
        print("[WARNING] MOSTLY COMPLETE")
        print("Most components are ready. Review missing items above.")
        sys.exit(0)
    else:
        print("[ERROR] INCOMPLETE")
        print("Several components are missing. Review setup guide.")
        sys.exit(1)

if __name__ == '__main__':
    main()
