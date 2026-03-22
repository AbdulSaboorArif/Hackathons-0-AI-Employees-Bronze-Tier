#!/usr/bin/env python3
"""
WhatsApp Message Sender
Sends approved messages via WhatsApp Web using Playwright automation
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import argparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time

class WhatsAppSender:
    def __init__(self, vault_path: str, session_path: str):
        self.vault_path = Path(vault_path)
        self.session_path = Path(session_path)
        self.logs_dir = self.vault_path / 'Logs'
        self.done_dir = self.vault_path / 'Done'

        # Create directories
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.done_dir.mkdir(parents=True, exist_ok=True)

    def extract_message_details(self, approval_file: Path):
        """Extract message details from approval file"""
        content = approval_file.read_text(encoding='utf-8')

        details = {
            'recipient': None,
            'message': None
        }

        # Parse frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key == 'to' or key == 'recipient':
                            details['recipient'] = value

                body = parts[2]
        else:
            body = content

        # Extract message content
        if '## Message' in body or '## Reply' in body:
            for section_marker in ['## Message', '## Reply', '## Response']:
                if section_marker in body:
                    parts = body.split(section_marker, 1)
                    if len(parts) > 1:
                        msg_section = parts[1].split('##')[0].strip()
                        # Remove markdown code blocks if present
                        msg_section = msg_section.replace('```', '').strip()
                        details['message'] = msg_section
                        break

        return details

    def send_whatsapp_message(self, recipient: str, message: str):
        """Send message via WhatsApp Web using Playwright"""
        print(f"\n[*] Opening WhatsApp Web...")

        with sync_playwright() as p:
            # Launch browser with persistent context
            browser = p.chromium.launch_persistent_context(
                str(self.session_path),
                headless=False,
                args=['--no-sandbox'],
                viewport={'width': 1280, 'height': 720}
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            try:
                # Navigate to WhatsApp Web
                print("[*] Navigating to WhatsApp Web...")
                page.goto('https://web.whatsapp.com', wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(3000)

                # Take initial screenshot
                screenshot_path = self.logs_dir / f"whatsapp_01_initial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=str(screenshot_path))
                print(f"[DEBUG] Screenshot saved: {screenshot_path.name}")

                # Check if logged in
                print("[*] Checking login status...")
                logged_in = False

                try:
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=10000, state='visible')
                    logged_in = True
                    print("[OK] Logged in to WhatsApp Web")
                except:
                    print("[ERROR] Not logged in to WhatsApp Web")
                    print("[INFO] Please scan QR code in the browser window")
                    print("[*] Waiting up to 5 minutes for login...")

                    try:
                        page.wait_for_selector('[data-testid="chat-list"]', timeout=300000, state='visible')
                        logged_in = True
                        print("[OK] Login successful!")
                    except:
                        raise Exception("Login timeout - please try again")

                # Search for contact
                print(f"[*] Searching for contact: {recipient}")

                # Click search box
                search_selectors = [
                    '[data-testid="chat-list-search"]',
                    '[title="Search input textbox"]',
                    'div[contenteditable="true"][data-tab="3"]'
                ]

                search_clicked = False
                for selector in search_selectors:
                    try:
                        element = page.wait_for_selector(selector, timeout=3000, state='visible')
                        if element:
                            element.click()
                            search_clicked = True
                            print(f"[OK] Clicked search box using: {selector}")
                            break
                    except:
                        continue

                if not search_clicked:
                    raise Exception("Could not find search box")

                page.wait_for_timeout(1000)

                # Type recipient name
                page.keyboard.type(recipient, delay=100)
                page.wait_for_timeout(2000)

                # Take screenshot of search results
                screenshot_path = self.logs_dir / f"whatsapp_02_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=str(screenshot_path))

                # Click on first result
                print("[*] Selecting contact from search results...")
                result_selectors = [
                    f'span[title="{recipient}"]',
                    '[data-testid="cell-frame-container"]',
                    '.x1n2onr6'
                ]

                contact_clicked = False
                for selector in result_selectors:
                    try:
                        element = page.wait_for_selector(selector, timeout=3000, state='visible')
                        if element:
                            element.click()
                            contact_clicked = True
                            print(f"[OK] Clicked contact using: {selector}")
                            break
                    except:
                        continue

                if not contact_clicked:
                    # Try clicking first search result
                    try:
                        page.click('[data-testid="cell-frame-container"]', timeout=3000)
                        contact_clicked = True
                        print("[OK] Clicked first search result")
                    except:
                        pass

                if not contact_clicked:
                    raise Exception(f"Could not find contact: {recipient}")

                page.wait_for_timeout(2000)

                # Find message input box
                print("[*] Typing message...")

                message_box_selectors = [
                    '[data-testid="conversation-compose-box-input"]',
                    'div[contenteditable="true"][data-tab="10"]',
                    'div[contenteditable="true"][role="textbox"]'
                ]

                message_typed = False
                for selector in message_box_selectors:
                    try:
                        element = page.wait_for_selector(selector, timeout=3000, state='visible')
                        if element:
                            element.click()
                            page.wait_for_timeout(500)

                            # Type message line by line to handle newlines
                            for line in message.split('\n'):
                                page.keyboard.type(line, delay=50)
                                if line != message.split('\n')[-1]:  # Not last line
                                    page.keyboard.press('Shift+Enter')

                            message_typed = True
                            print(f"[OK] Message typed using: {selector}")
                            break
                    except:
                        continue

                if not message_typed:
                    raise Exception("Could not find message input box")

                page.wait_for_timeout(1000)

                # Take screenshot with message
                screenshot_path = self.logs_dir / f"whatsapp_03_message_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=str(screenshot_path))

                # Click send button
                print("[*] Sending message...")

                send_button_selectors = [
                    '[data-testid="send"]',
                    'button[aria-label="Send"]',
                    'span[data-icon="send"]'
                ]

                message_sent = False
                for selector in send_button_selectors:
                    try:
                        element = page.wait_for_selector(selector, timeout=3000, state='visible')
                        if element:
                            element.click()
                            message_sent = True
                            print(f"[OK] Clicked send button using: {selector}")
                            break
                    except:
                        continue

                if not message_sent:
                    # Try pressing Enter as fallback
                    try:
                        page.keyboard.press('Enter')
                        message_sent = True
                        print("[OK] Sent message using Enter key")
                    except:
                        pass

                if not message_sent:
                    raise Exception("Could not send message")

                # Wait for message to be sent
                page.wait_for_timeout(3000)

                # Take final screenshot
                screenshot_path = self.logs_dir / f"whatsapp_success_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=str(screenshot_path))

                print(f"[OK] Message sent successfully!")
                print(f"[INFO] Screenshot saved: {screenshot_path.name}")

                browser.close()

                return {
                    'success': True,
                    'timestamp': datetime.now().isoformat(),
                    'recipient': recipient,
                    'screenshot': str(screenshot_path)
                }

            except Exception as e:
                error_msg = str(e)
                try:
                    print(f"[ERROR] Error sending WhatsApp message: {error_msg}")
                except UnicodeEncodeError:
                    print("[ERROR] Error sending WhatsApp message (contains special characters)")

                # Take error screenshot
                try:
                    screenshot_path = self.logs_dir / f"whatsapp_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
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
        """Log sending action"""
        log_file = self.logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}_whatsapp_messages.json"

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

    def send_approved_message(self, approval_file: Path):
        """Main workflow: Send approved message"""
        print("=" * 60)
        print("WhatsApp Message Sender")
        print("=" * 60)
        print(f"\n[*] Processing: {approval_file.name}")

        # Extract details
        details = self.extract_message_details(approval_file)

        if not details['recipient']:
            print("[ERROR] Could not extract recipient from approval file")
            return {'success': False, 'error': 'Recipient extraction failed'}

        if not details['message']:
            print("[ERROR] Could not extract message from approval file")
            return {'success': False, 'error': 'Message extraction failed'}

        print(f"\n[INFO] Recipient: {details['recipient']}")
        print(f"[INFO] Message length: {len(details['message'])} characters")
        print("-" * 60)
        try:
            print(details['message'][:200] + "..." if len(details['message']) > 200 else details['message'])
        except UnicodeEncodeError:
            print("[Message contains special characters - preview skipped]")
        print("-" * 60)

        # Send message
        result = self.send_whatsapp_message(details['recipient'], details['message'])

        # Log action
        self.log_action(approval_file, result)

        if result['success']:
            # Move to Done
            done_file = self.move_to_done(approval_file)
            print(f"\n[*] Moved to: {done_file}")

            print(f"\n{'=' * 60}")
            print("[OK] WhatsApp Message Sent Successfully")
            print(f"{'=' * 60}")
        else:
            print(f"\n{'=' * 60}")
            print("[ERROR] WhatsApp Message Failed")
            print(f"{'=' * 60}")
            print(f"Error: {result.get('error', 'Unknown error')}")

        return result

def main():
    parser = argparse.ArgumentParser(description='Send approved WhatsApp message')
    parser.add_argument('--vault', required=True, help='Path to Obsidian vault')
    parser.add_argument('--session', required=True, help='Path to browser session directory')
    parser.add_argument('--approval-file', required=True, help='Path to approval file')

    args = parser.parse_args()

    approval_file = Path(args.approval_file)
    if not approval_file.exists():
        print(f"[ERROR] Approval file not found: {approval_file}")
        sys.exit(1)

    sender = WhatsAppSender(args.vault, args.session)
    result = sender.send_approved_message(approval_file)

    # Output JSON for programmatic use
    print(f"\n{json.dumps(result, indent=2)}")

    sys.exit(0 if result['success'] else 1)

if __name__ == '__main__':
    main()
