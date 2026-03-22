#!/usr/bin/env python3
"""
Instagram Poster - Post photos with captions to Instagram
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time

def parse_approval_file(file_path):
    """Parse approval file and extract post content and image path"""
    content = Path(file_path).read_text(encoding='utf-8')

    # Split frontmatter and content
    parts = content.split('---')
    if len(parts) < 3:
        raise ValueError("Invalid approval file format")

    # Parse frontmatter
    frontmatter = parts[1].strip()
    image_path = None
    for line in frontmatter.split('\n'):
        if line.startswith('image_path:'):
            image_path = line.split(':', 1)[1].strip()

    if not image_path:
        raise ValueError("No image_path found in frontmatter")

    # Extract caption (everything after second ---)
    caption = '---'.join(parts[2:]).strip()

    # Remove markdown header if present
    if caption.startswith('# Instagram Post'):
        lines = caption.split('\n')
        caption = '\n'.join(lines[1:]).strip()

    return caption, image_path

def post_to_instagram(session_path, caption, image_path, vault_path):
    """Post photo with caption to Instagram using Playwright"""

    print(f"[Instagram] Starting post process...")
    print(f"[Instagram] Session: {session_path}")
    print(f"[Instagram] Image: {image_path}")
    print(f"[Instagram] Caption length: {len(caption)} characters")

    # Validate image
    img_file = Path(image_path)
    if not img_file.exists():
        print(f"[Instagram] ❌ Image not found: {image_path}")
        return False

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            print("[Instagram] Navigating to Instagram...")
            page.goto('https://www.instagram.com/', wait_until='networkidle', timeout=30000)
            time.sleep(3)

            # Check if logged in
            if 'login' in page.url.lower():
                print("[Instagram] ❌ Not logged in. Please run setup_instagram_session.py first.")
                return False

            print("[Instagram] ✓ Logged in successfully")

            # Click Create button
            print("[Instagram] Looking for Create button...")

            create_selectors = [
                'svg[aria-label="New post"]',
                'a[href="#"]:has(svg[aria-label="New post"])',
                'svg[aria-label="Create"]',
            ]

            clicked = False
            for selector in create_selectors:
                try:
                    page.click(selector, timeout=5000)
                    clicked = True
                    print(f"[Instagram] ✓ Clicked Create button")
                    break
                except:
                    continue

            if not clicked:
                print("[Instagram] ❌ Could not find Create button")
                return False

            time.sleep(2)

            # Upload image
            print("[Instagram] Uploading image...")

            file_input = page.wait_for_selector('input[type="file"]', timeout=10000)
            file_input.set_input_files(str(img_file.absolute()))

            print("[Instagram] ✓ Image uploaded")
            time.sleep(3)

            # Click Next button (may need to click multiple times)
            print("[Instagram] Clicking Next...")

            for i in range(3):
                try:
                    next_button = page.wait_for_selector('button:has-text("Next")', timeout=5000)
                    next_button.click()
                    print(f"[Instagram] ✓ Clicked Next ({i+1})")
                    time.sleep(2)
                except:
                    break

            # Add caption
            print("[Instagram] Adding caption...")

            caption_selectors = [
                'textarea[aria-label="Write a caption..."]',
                'textarea[placeholder="Write a caption..."]',
                'div[contenteditable="true"][aria-label*="caption"]',
            ]

            caption_box = None
            for selector in caption_selectors:
                try:
                    caption_box = page.wait_for_selector(selector, timeout=5000)
                    if caption_box:
                        print(f"[Instagram] ✓ Found caption box")
                        break
                except:
                    continue

            if caption_box:
                caption_box.click()
                time.sleep(1)
                page.keyboard.type(caption, delay=50)
                print("[Instagram] ✓ Caption added")
            else:
                print("[Instagram] ⚠️ Could not find caption box, posting without caption")

            time.sleep(2)

            # Take screenshot before posting
            screenshot_path = Path(vault_path) / 'Logs' / f'instagram_preview_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
            print(f"[Instagram] Preview screenshot: {screenshot_path}")

            # Click Share button
            print("[Instagram] Looking for Share button...")

            share_button = page.wait_for_selector('button:has-text("Share")', timeout=10000)
            share_button.click()
            print("[Instagram] ✓ Clicked Share button")

            # Wait for post to complete
            print("[Instagram] Waiting for post to complete...")
            time.sleep(8)

            # Take final screenshot
            screenshot_path = Path(vault_path) / 'Logs' / f'instagram_success_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            page.screenshot(path=str(screenshot_path))
            print(f"[Instagram] Success screenshot: {screenshot_path}")

            # Log the post
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'platform': 'instagram',
                'image': str(image_path),
                'caption_length': len(caption),
                'status': 'success',
                'screenshot': str(screenshot_path)
            }

            log_file = Path(vault_path) / 'Logs' / f'{datetime.now().strftime("%Y-%m-%d")}_instagram_posts.json'
            log_file.parent.mkdir(parents=True, exist_ok=True)

            logs = []
            if log_file.exists():
                logs = json.loads(log_file.read_text())
            logs.append(log_entry)
            log_file.write_text(json.dumps(logs, indent=2))

            print("[Instagram] ✅ Post published successfully!")
            return True

        except Exception as e:
            print(f"[Instagram] ❌ Error: {str(e)}")
            screenshot_path = Path(vault_path) / 'Logs' / f'instagram_error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
            print(f"[Instagram] Error screenshot: {screenshot_path}")
            return False

        finally:
            browser.close()

def main():
    parser = argparse.ArgumentParser(description='Post to Instagram with approval workflow')
    parser.add_argument('--vault', required=True, help='Path to AI Employee Vault')
    parser.add_argument('--session', required=True, help='Path to browser session directory')
    parser.add_argument('--approval-file', required=True, help='Path to approval file')

    args = parser.parse_args()

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
        caption, image_path = parse_approval_file(approval_file)
    except Exception as e:
        print(f"Error parsing approval file: {e}")
        sys.exit(1)

    # Post to Instagram
    success = post_to_instagram(str(session_path), caption, image_path, str(vault_path))

    if success:
        done_dir = vault_path / 'Done'
        done_dir.mkdir(exist_ok=True)
        done_file = done_dir / approval_file.name
        approval_file.rename(done_file)
        print(f"[Instagram] Moved approval file to: {done_file}")
        sys.exit(0)
    else:
        print("[Instagram] Post failed. Approval file remains in place.")
        sys.exit(1)

if __name__ == '__main__':
    main()
