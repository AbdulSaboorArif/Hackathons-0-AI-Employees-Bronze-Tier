#!/usr/bin/env python3
"""
Setup Twitter session - One-time login to save session
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

def setup_twitter_session(session_path):
    """Setup Twitter session with manual login"""

    print("[Twitter Setup] Starting session setup...")
    print("[Twitter Setup] You will need to log in manually.")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,
            viewport={'width': 1280, 'height': 720}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            print("[Twitter Setup] Opening Twitter...")
            page.goto('https://twitter.com/', wait_until='networkidle')

            print("\n" + "="*60)
            print("PLEASE LOG IN TO TWITTER IN THE BROWSER WINDOW")
            print("="*60)
            print("\nInstructions:")
            print("1. Enter your username/email/phone and password")
            print("2. Complete any 2FA if required")
            print("3. Wait until you see your Twitter home feed")
            print("4. Press ENTER in this terminal when done")
            print("="*60 + "\n")

            input("Press ENTER after you've logged in...")

            time.sleep(2)
            if 'login' in page.url.lower():
                print("[Twitter Setup] ❌ Still on login page. Please try again.")
                return False

            print("[Twitter Setup] ✅ Login successful!")
            print(f"[Twitter Setup] Session saved to: {session_path}")
            print("[Twitter Setup] You can now use post_to_twitter.py")

            return True

        except Exception as e:
            print(f"[Twitter Setup] ❌ Error: {str(e)}")
            return False

        finally:
            browser.close()

def main():
    session_path = Path(__file__).parent.parent.parent.parent / 'watchers' / 'twitter' / '.browser-session'
    session_path.mkdir(parents=True, exist_ok=True)

    print(f"Session will be saved to: {session_path}")

    success = setup_twitter_session(str(session_path))

    if success:
        print("\n✅ Setup complete! You can now post to Twitter.")
        sys.exit(0)
    else:
        print("\n❌ Setup failed. Please try again.")
        sys.exit(1)

if __name__ == '__main__':
    main()
