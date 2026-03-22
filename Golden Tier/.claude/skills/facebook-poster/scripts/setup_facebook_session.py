#!/usr/bin/env python3
"""
Setup Facebook session - One-time login to save session
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

def setup_facebook_session(session_path):
    """Setup Facebook session with manual login"""

    print("[Facebook Setup] Starting session setup...")
    print("[Facebook Setup] You will need to log in manually.")
    print("[Facebook Setup] The session will be saved for future use.")

    with sync_playwright() as p:
        # Launch browser with persistent context
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,
            viewport={'width': 1280, 'height': 720}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # Navigate to Facebook
            print("[Facebook Setup] Opening Facebook...")
            page.goto('https://www.facebook.com/', wait_until='networkidle')

            print("\n" + "="*60)
            print("PLEASE LOG IN TO FACEBOOK IN THE BROWSER WINDOW")
            print("="*60)
            print("\nInstructions:")
            print("1. Enter your email/phone and password")
            print("2. Complete any 2FA if required")
            print("3. Wait until you see your Facebook feed")
            print("4. Press ENTER in this terminal when done")
            print("="*60 + "\n")

            input("Press ENTER after you've logged in...")

            # Verify login
            time.sleep(2)
            if 'login' in page.url.lower():
                print("[Facebook Setup] ❌ Still on login page. Please try again.")
                return False

            print("[Facebook Setup] ✅ Login successful!")
            print(f"[Facebook Setup] Session saved to: {session_path}")
            print("[Facebook Setup] You can now use post_to_facebook.py")

            return True

        except Exception as e:
            print(f"[Facebook Setup] ❌ Error: {str(e)}")
            return False

        finally:
            browser.close()

def main():
    # Default session path
    session_path = Path(__file__).parent.parent.parent.parent / 'watchers' / 'facebook' / '.browser-session'
    session_path.mkdir(parents=True, exist_ok=True)

    print(f"Session will be saved to: {session_path}")

    success = setup_facebook_session(str(session_path))

    if success:
        print("\n✅ Setup complete! You can now post to Facebook.")
        sys.exit(0)
    else:
        print("\n❌ Setup failed. Please try again.")
        sys.exit(1)

if __name__ == '__main__':
    main()
