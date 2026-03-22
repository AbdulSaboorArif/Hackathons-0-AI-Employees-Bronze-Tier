#!/usr/bin/env python3
"""
LinkedIn Post Publisher - Debug Version
Posts approved content to LinkedIn using Playwright automation
Includes extensive debugging and screenshot capture
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import argparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time

class LinkedInPublisher:
    def __init__(self, vault_path: str, session_path: str):
        self.vault_path = Path(vault_path)
        self.session_path = Path(session_path)
        self.logs_dir = self.vault_path / 'Logs'
        self.done_dir = self.vault_path / 'Done'

        # Create directories
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.done_dir.mkdir(parents=True, exist_ok=True)

    def extract_post_content(self, approval_file: Path):
        """Extract post content from approval file"""
        content = approval_file.read_text(encoding='utf-8')

        # Find the post content section
        if '## Post Content' in content:
            parts = content.split('## Post Content')
            if len(parts) > 1:
                # Get content until next section
                post_section = parts[1].split('##')[0].strip()
                return post_section

        return None

    def post_to_linkedin(self, content: str):
        """Post content to LinkedIn using Playwright with extensive debugging"""
        print(f"\n[*] Opening LinkedIn...")

        with sync_playwright() as p:
            # Launch browser with persistent context (visible for debugging)
            browser = p.chromium.launch_persistent_context(
                str(self.session_path),
                headless=False,  # Keep visible for debugging
                args=['--no-sandbox'],
                viewport={'width': 1280, 'height': 720}
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            try:
                # Navigate to LinkedIn
                print("[*] Navigating to LinkedIn...")
                page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(3000)

                # Take screenshot of initial page
                screenshot_path = self.logs_dir / f"debug_01_initial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=str(screenshot_path))
                print(f"[DEBUG] Screenshot saved: {screenshot_path.name}")

                # Check if logged in
                print("[*] Checking login status...")
                logged_in = False

                # Wait for page to fully load (increased timeout)
                try:
                    page.wait_for_load_state('networkidle', timeout=30000)
                except:
                    print("[WARNING] Network idle timeout, continuing anyway...")

                # Check for feed presence (indicates logged in)
                try:
                    page.wait_for_selector('main', timeout=15000, state='visible')
                    logged_in = True
                    print("[OK] Logged in to LinkedIn")
                except:
                    # Try alternative selectors
                    try:
                        page.wait_for_selector('.scaffold-layout__main', timeout=10000, state='visible')
                        logged_in = True
                        print("[OK] Logged in to LinkedIn (alternative selector)")
                    except:
                        print("[ERROR] Not logged in to LinkedIn")
                        screenshot_path = self.logs_dir / f"debug_02_not_logged_in_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        page.screenshot(path=str(screenshot_path))
                        raise Exception("Please login manually in the browser window")

                # Find and click "Start a post" button
                print("[*] Looking for 'Start a post' button...")
                page.wait_for_timeout(2000)

                # Take screenshot before clicking
                screenshot_path = self.logs_dir / f"debug_03_before_click_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=str(screenshot_path))

                # Try multiple selectors for the "Start a post" button
                start_post_selectors = [
                    'button.share-box-feed-entry__trigger',
                    'button[aria-label*="Start a post"]',
                    '.share-box-feed-entry__trigger',
                    'button:has-text("Start a post")',
                    '[data-control-name="share_box_trigger"]',
                    '.artdeco-button.share-box-feed-entry__trigger'
                ]

                clicked = False
                for selector in start_post_selectors:
                    try:
                        print(f"[DEBUG] Trying selector: {selector}")
                        element = page.wait_for_selector(selector, timeout=3000, state='visible')
                        if element:
                            element.click()
                            clicked = True
                            print(f"[OK] Clicked using selector: {selector}")
                            break
                    except Exception as e:
                        print(f"[DEBUG] Selector failed: {selector} - {str(e)}")
                        continue

                if not clicked:
                    # Try clicking by text
                    try:
                        page.click('text="Start a post"', timeout=3000)
                        clicked = True
                        print("[OK] Clicked using text selector")
                    except:
                        pass

                if not clicked:
                    raise Exception("Could not find 'Start a post' button")

                # Wait for modal to appear
                print("[*] Waiting for post editor modal...")
                page.wait_for_timeout(2000)

                # Take screenshot of modal
                screenshot_path = self.logs_dir / f"debug_04_modal_opened_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=str(screenshot_path))

                # Find the post editor
                print("[*] Looking for post editor...")

                editor_selectors = [
                    '.ql-editor[contenteditable="true"]',
                    'div[contenteditable="true"][role="textbox"]',
                    '.share-creation-state__text-editor',
                    'div[data-placeholder*="share"]',
                    'div.ql-editor.ql-blank'
                ]

                editor_found = False
                for selector in editor_selectors:
                    try:
                        print(f"[DEBUG] Trying editor selector: {selector}")
                        element = page.wait_for_selector(selector, timeout=3000, state='visible')
                        if element:
                            # Click to focus
                            element.click()
                            page.wait_for_timeout(500)

                            # Type content (handle emojis properly)
                            try:
                                element.type(content, delay=50)
                            except Exception as type_error:
                                # Fallback: use keyboard.type which handles Unicode better
                                page.keyboard.type(content, delay=50)

                            editor_found = True
                            print(f"[OK] Content typed using selector: {selector}")
                            break
                    except Exception as e:
                        # Avoid printing exception details that might contain emojis
                        print(f"[DEBUG] Editor selector failed: {selector}")
                        continue

                if not editor_found:
                    # Try alternative: focus and type
                    try:
                        page.keyboard.type(content, delay=50)
                        editor_found = True
                        print("[OK] Content typed using keyboard")
                    except:
                        pass

                if not editor_found:
                    screenshot_path = self.logs_dir / f"debug_05_editor_not_found_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    page.screenshot(path=str(screenshot_path))
                    raise Exception("Could not find post editor")

                page.wait_for_timeout(1000)

                # Take screenshot with content
                screenshot_path = self.logs_dir / f"debug_06_content_entered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=str(screenshot_path))

                # Click the Post button
                print("[*] Looking for Post button...")

                post_button_selectors = [
                    'button.share-actions__primary-action',
                    'button[aria-label*="Post"]',
                    'button:has-text("Post")',
                    '.share-actions__primary-action',
                    'button[data-test-share-button="true"]'
                ]

                posted = False
                for selector in post_button_selectors:
                    try:
                        print(f"[DEBUG] Trying post button selector: {selector}")
                        element = page.wait_for_selector(selector, timeout=3000, state='visible')
                        if element and not element.is_disabled():
                            element.click()
                            posted = True
                            print(f"[OK] Clicked Post button using selector: {selector}")
                            break
                    except Exception as e:
                        print(f"[DEBUG] Post button selector failed: {selector} - {str(e)}")
                        continue

                if not posted:
                    screenshot_path = self.logs_dir / f"debug_07_post_button_not_found_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    page.screenshot(path=str(screenshot_path))
                    raise Exception("Could not find Post button")

                # Wait for post to be published
                print("[*] Waiting for post to publish...")
                page.wait_for_timeout(5000)

                # Take final screenshot
                screenshot_path = self.logs_dir / f"linkedin_post_success_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=str(screenshot_path))

                print(f"[OK] Post published successfully!")
                print(f"[INFO] Screenshot saved: {screenshot_path.name}")

                browser.close()

                return {
                    'success': True,
                    'timestamp': datetime.now().isoformat(),
                    'screenshot': str(screenshot_path)
                }

            except Exception as e:
                # Avoid printing exception details that might contain emojis
                error_msg = str(e)
                try:
                    print(f"[ERROR] Error posting to LinkedIn: {error_msg}")
                except UnicodeEncodeError:
                    print("[ERROR] Error posting to LinkedIn (contains special characters)")

                # Take error screenshot
                try:
                    screenshot_path = self.logs_dir / f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    page.screenshot(path=str(screenshot_path))
                    print(f"[ERROR] Error screenshot saved: {screenshot_path.name}")
                except:
                    pass

                browser.close()
                return {
                    'success': False,
                    'error': error_msg,
                    'timestamp': datetime.now().isoformat()
                }

    def log_action(self, approval_file: Path, result: dict):
        """Log posting action"""
        log_file = self.logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}_linkedin_posts.json"

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'approval_file': approval_file.name,
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

    def move_to_done(self, approval_file: Path):
        """Move approval file to Done folder"""
        dest = self.done_dir / approval_file.name
        approval_file.rename(dest)
        return dest

    def publish_approved_post(self, approval_file: Path):
        """Main workflow: Publish approved post"""
        print("=" * 60)
        print("LinkedIn Post Publisher (Debug Mode)")
        print("=" * 60)
        print(f"\n[*] Processing: {approval_file.name}")

        # Extract content
        content = self.extract_post_content(approval_file)
        if not content:
            print("[ERROR] Could not extract post content from approval file")
            return {'success': False, 'error': 'Content extraction failed'}

        print(f"\n[INFO] Post content ({len(content)} characters)")
        print("-" * 60)
        # Avoid printing emojis due to Windows console encoding issues
        try:
            print(content[:200] + "..." if len(content) > 200 else content)
        except UnicodeEncodeError:
            print("[Content contains emojis - preview skipped]")
        print("-" * 60)

        # Post to LinkedIn
        result = self.post_to_linkedin(content)

        # Log action
        self.log_action(approval_file, result)

        if result['success']:
            # Move to Done
            done_file = self.move_to_done(approval_file)
            print(f"\n[*] Moved to: {done_file}")

            print(f"\n{'=' * 60}")
            print("[OK] LinkedIn Post Published Successfully")
            print(f"{'=' * 60}")
        else:
            print(f"\n{'=' * 60}")
            print("[ERROR] LinkedIn Post Failed")
            print(f"{'=' * 60}")
            print(f"Error: {result.get('error', 'Unknown error')}")

        return result

def main():
    parser = argparse.ArgumentParser(description='Publish approved LinkedIn post')
    parser.add_argument('--vault', required=True, help='Path to Obsidian vault')
    parser.add_argument('--session', required=True, help='Path to browser session directory')
    parser.add_argument('--approval-file', required=True, help='Path to approval file')

    args = parser.parse_args()

    approval_file = Path(args.approval_file)
    if not approval_file.exists():
        print(f"[ERROR] Approval file not found: {approval_file}")
        sys.exit(1)

    publisher = LinkedInPublisher(args.vault, args.session)
    result = publisher.publish_approved_post(approval_file)

    # Output JSON for programmatic use
    print(f"\n{json.dumps(result, indent=2)}")

    sys.exit(0 if result['success'] else 1)

if __name__ == '__main__':
    main()
