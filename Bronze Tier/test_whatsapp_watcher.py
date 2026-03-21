#!/usr/bin/env python3
"""
Test WhatsApp Watcher - Single check for urgent messages
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from watchers.whatsapp.whatsapp_watcher import WhatsAppWatcher

def main():
    vault_path = "AI_Employee_Vault"
    session_path = "watchers/whatsapp/.browser-session"

    print("=" * 60)
    print("WhatsApp Watcher - Single Check Test")
    print("=" * 60)
    print(f"\nVault: {vault_path}")
    print(f"Session: {session_path}\n")

    watcher = WhatsAppWatcher(
        vault_path=vault_path,
        session_path=session_path,
        check_interval=60
    )

    print("[*] Checking WhatsApp for urgent messages...")
    print("[INFO] This will open a browser window")
    print("[INFO] If not logged in, scan the QR code with your phone\n")

    # Single check
    messages = watcher.check_for_updates()

    if messages:
        print(f"\n[OK] Found {len(messages)} urgent message(s)!")
        print("\nCreating action files...")

        for msg in messages:
            filepath = watcher.create_action_file(msg)
            print(f"[CREATED] {filepath.name}")
            print(f"  From: {msg['name']}")
            print(f"  Preview: {msg['message'][:50]}...")
            print()
    else:
        print("\n[INFO] No urgent messages found")
        print("[INFO] Urgent keywords: urgent, asap, invoice, payment, help, etc.")

    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

if __name__ == '__main__':
    main()
