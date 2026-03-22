#!/usr/bin/env python3
"""
Setup Instagram session - One-time login to save session
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

def setup_instagram_session(session_path):
    """Setup Instagram session with manual login"""

    print("[Instagram Setup] Starting session setup...")
    print("[Instagram Setup] You will need to log in manually.")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,
            viewport={'width': 1280, 'height': 720}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            print("[Instagram Setup] Opening Instagram...")
            page.goto('https://www.instagram.com/', wait_until='networkidle')

            print("\n" + "="*60)
            print("PLEASE LOG IN TO INSTAGRAM IN THE BROWSER WINDOW")
            print("="*60)
            print("\nInstructions:")
            print("1. Enter your username and password")
            print("2. Complete any 2FA if required")
            print("3. Click 'Not Now' on save login info prompt")
            print("4. Click 'Not Now' on notifications prompt")
            print("5. Wait until you see your Instagram feed")
            print("6. Press ENTER in this terminal when done")
            print("="*60 + "\n")

            input("Press ENTER after you've logged in...")

            time.sleep(2)
            if 'login' in page.url.lower():
                print("[Instagram Setup] ❌ Still on login page. Please try again.")
                return False

            print("[Instagram Setup] ✅ Login successful!")
            print(f"[Instagram Setup] Session saved to: {session_path}")
            print("[Instagram Setup] You can now use post_to_instagram.py")

            return True

        except Exception as e:
            print(f"[Instagram Setup] ❌ Error: {str(e)}")
            return False

        finally:
            browser.close()

def main():
    session_path = Path(__file__).parent.parent.parent.parent / 'watchers' / 'instagram' / '.browser-session'
    session_path.mkdir(parents=True, exist_ok=True)

    print(f"Session will be saved to: {session_path}")

    success = setup_instagram_session(str(session_path))

    if success:
        print("\n✅ Setup complete! You can now post to Instagram.")
        sys.exit(0)
    else:
        print("\n❌ Setup failed. Please try again.")
        sys.exit(1)

if __name__ == '__main__':
    main()
