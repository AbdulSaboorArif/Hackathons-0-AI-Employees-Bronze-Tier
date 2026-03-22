#!/usr/bin/env python3
"""
Facebook Poster - Post content to Facebook with approval workflow
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time

def parse_approval_file(file_path):
    """Parse approval file and extract post content"""
    content = Path(file_path).read_text(encoding='utf-8')

    # Split frontmatter and content
    parts = content.split('---')
    if len(parts) < 3:
        raise ValueError("Invalid approval file format")

    # Extract post content (everything after second ---)
    post_content = '---'.join(parts[2:]).strip()

    # Remove markdown header if present
    if post_content.startswith('# Facebook Post'):
        lines = post_content.split('\n')
        post_content = '\n'.join(lines[1:]).strip()

    return post_content

def post_to_facebook(session_path, post_content, vault_path):
    """Post content to Facebook using Playwright"""

    print(f"[Facebook] Starting post process...")
    print(f"[Facebook] Session: {session_path}")
    print(f"[Facebook] Content length: {len(post_content)} characters")

    with sync_playwright() as p:
        # Launch browser with persistent context
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,  # Set to True for production
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # Navigate to Facebook
            print("[Facebook] Navigating to Facebook...")
            page.goto('https://www.facebook.com/', wait_until='networkidle', timeout=30000)
            time.sleep(3)

            # Check if logged in
            if 'login' in page.url.lower():
                print("[Facebook] ❌ Not logged in. Please run setup_facebook_session.py first.")
                return False

            print("[Facebook] ✓ Logged in successfully")

            # Find and click the post creation area
            print("[Facebook] Looking for post creation area...")

            # Try multiple selectors (Facebook UI varies)
            post_selectors = [
                'div[role="button"][aria-label*="What\'s on your mind"]',
                'div[role="button"][aria-label*="Create a post"]',
                'div[role="button"][aria-label*="Write something"]',
                'span:has-text("What\'s on your mind")',
            ]

            clicked = False
            for selector in post_selectors:
                try:
                    page.click(selector, timeout=5000)
                    clicked = True
                    print(f"[Facebook] ✓ Clicked post area using: {selector}")
                    break
                except:
                    continue

            if not clicked:
                print("[Facebook] ❌ Could not find post creation area")
                screenshot_path = Path(vault_path) / 'Logs' / f'facebook_error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                screenshot_path.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(screenshot_path))
                print(f"[Facebook] Screenshot saved: {screenshot_path}")
                return False

            time.sleep(2)

            # Find the text input area in the modal
            print("[Facebook] Looking for text input...")

            text_selectors = [
                'div[role="textbox"][contenteditable="true"]',
                'div[aria-label*="What\'s on your mind"]',
                'div.notranslate[contenteditable="true"]',
            ]

            text_box = None
            for selector in text_selectors:
                try:
                    text_box = page.wait_for_selector(selector, timeout=5000)
                    if text_box:
                        print(f"[Facebook] ✓ Found text input using: {selector}")
                        break
                except:
                    continue

            if not text_box:
                print("[Facebook] ❌ Could not find text input")
                return False

            # Type the post content
            print("[Facebook] Typing post content...")
            text_box.click()
            time.sleep(1)

            # Type content with proper handling of special characters
            page.keyboard.type(post_content, delay=50)
            time.sleep(2)

            print("[Facebook] ✓ Content typed successfully")

            # Take screenshot before posting
            screenshot_path = Path(vault_path) / 'Logs' / f'facebook_preview_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
            print(f"[Facebook] Preview screenshot: {screenshot_path}")

            # Find and click Post button
            print("[Facebook] Looking for Post button...")

            post_button_selectors = [
                'div[role="button"][aria-label="Post"]',
                'div[role="button"]:has-text("Post")',
                'span:has-text("Post")',
            ]

            posted = False
            for selector in post_button_selectors:
                try:
                    page.click(selector, timeout=5000)
                    posted = True
                    print(f"[Facebook] ✓ Clicked Post button using: {selector}")
                    break
                except:
                    continue

            if not posted:
                print("[Facebook] ❌ Could not find Post button")
                return False

            # Wait for post to complete
            print("[Facebook] Waiting for post to complete...")
            time.sleep(5)

            # Take final screenshot
            screenshot_path = Path(vault_path) / 'Logs' / f'facebook_success_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            page.screenshot(path=str(screenshot_path))
            print(f"[Facebook] Success screenshot: {screenshot_path}")

            # Log the post
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'platform': 'facebook',
                'content_length': len(post_content),
                'status': 'success',
                'screenshot': str(screenshot_path)
            }

            log_file = Path(vault_path) / 'Logs' / f'{datetime.now().strftime("%Y-%m-%d")}_facebook_posts.json'
            log_file.parent.mkdir(parents=True, exist_ok=True)

            logs = []
            if log_file.exists():
                logs = json.loads(log_file.read_text())
            logs.append(log_entry)
            log_file.write_text(json.dumps(logs, indent=2))

            print("[Facebook] ✅ Post published successfully!")
            return True

        except Exception as e:
            print(f"[Facebook] ❌ Error: {str(e)}")
            screenshot_path = Path(vault_path) / 'Logs' / f'facebook_error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
            print(f"[Facebook] Error screenshot: {screenshot_path}")
            return False

        finally:
            browser.close()

def main():
    parser = argparse.ArgumentParser(description='Post to Facebook with approval workflow')
    parser.add_argument('--vault', required=True, help='Path to AI Employee Vault')
    parser.add_argument('--session', required=True, help='Path to browser session directory')
    parser.add_argument('--approval-file', required=True, help='Path to approval file')

    args = parser.parse_args()

    # Validate paths
    vault_path = Path(args.vault)
    session_path = Path(args.session)
    approval_file = Path(args.approval_file)

    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)

    if not approval_file.exists():
        print(f"Error: Approval file does not exist: {approval_file}")
        sys.exit(1)

    # Parse approval file
    try:
        post_content = parse_approval_file(approval_file)
    except Exception as e:
        print(f"Error parsing approval file: {e}")
        sys.exit(1)

    # Post to Facebook
    success = post_to_facebook(str(session_path), post_content, str(vault_path))

    if success:
        # Move approval file to Done
        done_dir = vault_path / 'Done'
        done_dir.mkdir(exist_ok=True)
        done_file = done_dir / approval_file.name
        approval_file.rename(done_file)
        print(f"[Facebook] Moved approval file to: {done_file}")
        sys.exit(0)
    else:
        print("[Facebook] Post failed. Approval file remains in place.")
        sys.exit(1)

if __name__ == '__main__':
    main()
