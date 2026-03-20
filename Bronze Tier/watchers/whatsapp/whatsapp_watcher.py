"""
WhatsApp Watcher - Monitors WhatsApp Web for urgent messages
Uses Playwright to automate WhatsApp Web and detect important messages
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from base_watcher import BaseWatcher
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import json

class WhatsAppWatcher(BaseWatcher):
    """Watches WhatsApp Web for urgent messages"""

    def __init__(self, vault_path: str, session_path: str, check_interval: int = 60):
        """
        Initialize WhatsApp watcher

        Args:
            vault_path: Path to Obsidian vault
            session_path: Path to store browser session data
            check_interval: Seconds between checks (default: 60)
        """
        super().__init__(vault_path, check_interval)
        self.session_path = Path(session_path)
        self.session_path.mkdir(parents=True, exist_ok=True)

        # Urgent keywords to detect
        self.urgent_keywords = [
            'urgent', 'asap', 'emergency', 'help',
            'invoice', 'payment', 'due', 'deadline',
            'problem', 'issue', 'error', 'broken',
            'meeting', 'call', 'now', 'immediately'
        ]

        self.processed_messages = set()
        self.logger.info('WhatsApp Watcher initialized')

    def check_for_updates(self) -> list:
        """Check WhatsApp Web for new urgent messages"""
        messages = []

        try:
            with sync_playwright() as p:
                # Launch browser with persistent context (keeps login session)
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,  # Set to True for background operation
                    args=['--no-sandbox']
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                # Navigate to WhatsApp Web
                page.goto('https://web.whatsapp.com', wait_until='domcontentloaded')

                # Wait for either QR code or chat list
                try:
                    # Check if already logged in
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=10000)
                    self.logger.info('WhatsApp Web loaded successfully')

                    # Get unread chats
                    unread_chats = page.query_selector_all('[data-testid="cell-frame-container"]')

                    for chat in unread_chats[:10]:  # Check first 10 chats
                        try:
                            # Check if chat has unread badge
                            unread_badge = chat.query_selector('[data-testid="icon-unread-count"]')
                            if not unread_badge:
                                continue

                            # Get chat name
                            name_elem = chat.query_selector('[data-testid="cell-frame-title"]')
                            name = name_elem.inner_text() if name_elem else 'Unknown'

                            # Get last message
                            msg_elem = chat.query_selector('[data-testid="last-msg"]')
                            message_text = msg_elem.inner_text() if msg_elem else ''

                            # Get timestamp
                            time_elem = chat.query_selector('[data-testid="cell-frame-secondary"]')
                            timestamp = time_elem.inner_text() if time_elem else ''

                            # Check if message contains urgent keywords
                            message_lower = message_text.lower()
                            is_urgent = any(kw in message_lower for kw in self.urgent_keywords)

                            # Create unique ID for this message
                            msg_id = f"{name}_{message_text[:20]}"

                            if is_urgent and msg_id not in self.processed_messages:
                                messages.append({
                                    'name': name,
                                    'message': message_text,
                                    'timestamp': timestamp,
                                    'id': msg_id
                                })
                                self.processed_messages.add(msg_id)

                        except Exception as e:
                            self.logger.debug(f'Error processing chat: {e}')
                            continue

                except PlaywrightTimeout:
                    self.logger.warning('WhatsApp Web not logged in - please scan QR code')
                    print('\n[LOGIN] WhatsApp Web requires login!')
                    print('[QR] Please scan the QR code in the browser window')
                    print('[INFO] Waiting up to 5 minutes for login...\n')

                    # Wait up to 5 minutes for login
                    try:
                        page.wait_for_selector('[data-testid="chat-list"]', timeout=300000)
                        print('[OK] Login successful! Checking for messages...\n')

                        # Now check for messages since we're logged in
                        unread_chats = page.query_selector_all('[data-testid="cell-frame-container"]')

                        for chat in unread_chats[:10]:
                            try:
                                unread_badge = chat.query_selector('[data-testid="icon-unread-count"]')
                                if not unread_badge:
                                    continue

                                name_elem = chat.query_selector('[data-testid="cell-frame-title"]')
                                name = name_elem.inner_text() if name_elem else 'Unknown'

                                msg_elem = chat.query_selector('[data-testid="last-msg"]')
                                message_text = msg_elem.inner_text() if msg_elem else ''

                                time_elem = chat.query_selector('[data-testid="cell-frame-secondary"]')
                                timestamp = time_elem.inner_text() if time_elem else ''

                                message_lower = message_text.lower()
                                is_urgent = any(kw in message_lower for kw in self.urgent_keywords)

                                msg_id = f"{name}_{message_text[:20]}"

                                if is_urgent and msg_id not in self.processed_messages:
                                    messages.append({
                                        'name': name,
                                        'message': message_text,
                                        'timestamp': timestamp,
                                        'id': msg_id
                                    })
                                    self.processed_messages.add(msg_id)

                            except Exception as e:
                                self.logger.debug(f'Error processing chat: {e}')
                                continue

                    except PlaywrightTimeout:
                        print('[TIMEOUT] Login not completed within 5 minutes')
                        print('[INFO] Will retry on next check\n')

                browser.close()

        except Exception as e:
            self.logger.error(f'Error checking WhatsApp: {e}')

        return messages

    def create_action_file(self, item) -> Path:
        """Create action file for WhatsApp message"""
        name = item['name']
        message = item['message']
        timestamp = item['timestamp']

        # Determine priority
        priority = 'high'  # All urgent keyword messages are high priority

        content = f"""---
type: whatsapp_message
from: {name}
received: {datetime.now().isoformat()}
whatsapp_timestamp: {timestamp}
priority: {priority}
status: pending
---

## Message Content

{message}

## Context
- Contact: {name}
- Detected as urgent based on keywords
- Requires prompt response

## Suggested Actions
- [ ] Draft reply
- [ ] Request approval for response
- [ ] Send response via WhatsApp
- [ ] Mark as done

## Response Guidelines
- Keep professional tone
- Address the urgent matter directly
- Provide clear next steps or timeline
"""

        # Create filename
        file_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = ''.join(c for c in name[:20] if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f'WHATSAPP_{file_timestamp}_{safe_name}.md'

        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')

        return filepath

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='WhatsApp Watcher')
    parser.add_argument('--vault', required=True, help='Path to Obsidian vault')
    parser.add_argument('--session', required=True, help='Path to browser session directory')
    parser.add_argument('--interval', type=int, default=60, help='Check interval in seconds')

    args = parser.parse_args()

    watcher = WhatsAppWatcher(
        vault_path=args.vault,
        session_path=args.session,
        check_interval=args.interval
    )

    print(f'[START] WhatsApp Watcher started')
    print(f'[VAULT] Vault: {args.vault}')
    print(f'[SESSION] Session: {args.session}')
    print(f'[INTERVAL] Checking every {args.interval} seconds')
    print(f'Press Ctrl+C to stop\n')

    watcher.run()
