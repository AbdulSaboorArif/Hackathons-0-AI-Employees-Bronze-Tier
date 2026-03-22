#!/usr/bin/env python3
"""
Facebook Watcher - Monitor Facebook for notifications, messages, and engagement opportunities
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Add parent directory to path for base_watcher import
sys.path.insert(0, str(Path(__file__).parent.parent))
from base_watcher import BaseWatcher

class FacebookWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str, check_interval: int = 300):
        super().__init__(vault_path, check_interval)
        self.session_path = Path(session_path)
        self.keywords = ['urgent', 'asap', 'help', 'question', 'inquiry', 'interested']
        self.processed_ids = set()

    def check_for_updates(self) -> list:
        """Check Facebook for new notifications and messages"""
        updates = []

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    viewport={'width': 1280, 'height': 720}
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                # Navigate to Facebook
                page.goto('https://www.facebook.com/', timeout=30000)
                time.sleep(3)

                # Check if logged in
                if 'login' in page.url.lower():
                    self.logger.warning("Not logged in to Facebook")
                    browser.close()
                    return []

                # Check notifications
                try:
                    # Click notifications icon
                    notifications_selectors = [
                        'div[aria-label="Notifications"]',
                        'a[href*="/notifications"]',
                    ]

                    for selector in notifications_selectors:
                        try:
                            page.click(selector, timeout=5000)
                            break
                        except:
                            continue

                    time.sleep(2)

                    # Get notification items
                    notification_items = page.query_selector_all('div[role="article"]')

                    for item in notification_items[:5]:  # Check top 5 notifications
                        try:
                            text = item.inner_text().lower()

                            # Check for keywords or unread status
                            if any(kw in text for kw in self.keywords) or 'new' in text:
                                notification_id = f"fb_notif_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                                if notification_id not in self.processed_ids:
                                    updates.append({
                                        'type': 'notification',
                                        'id': notification_id,
                                        'text': text[:500],  # Limit text length
                                        'timestamp': datetime.now().isoformat()
                                    })
                                    self.processed_ids.add(notification_id)
                        except Exception as e:
                            self.logger.error(f"Error processing notification: {e}")
                            continue

                except Exception as e:
                    self.logger.error(f"Error checking notifications: {e}")

                # Check messages
                try:
                    # Navigate to messages
                    page.goto('https://www.facebook.com/messages', timeout=30000)
                    time.sleep(3)

                    # Get unread message threads
                    unread_selectors = [
                        'div[aria-label*="unread"]',
                        'div[data-testid*="unread"]',
                    ]

                    unread_threads = []
                    for selector in unread_selectors:
                        try:
                            unread_threads = page.query_selector_all(selector)
                            if unread_threads:
                                break
                        except:
                            continue

                    for thread in unread_threads[:3]:  # Check top 3 unread
                        try:
                            text = thread.inner_text().lower()

                            if any(kw in text for kw in self.keywords):
                                message_id = f"fb_msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                                if message_id not in self.processed_ids:
                                    updates.append({
                                        'type': 'message',
                                        'id': message_id,
                                        'text': text[:500],
                                        'timestamp': datetime.now().isoformat()
                                    })
                                    self.processed_ids.add(message_id)
                        except Exception as e:
                            self.logger.error(f"Error processing message: {e}")
                            continue

                except Exception as e:
                    self.logger.error(f"Error checking messages: {e}")

                browser.close()

        except Exception as e:
            self.logger.error(f"Error in Facebook watcher: {e}")

        return updates

    def create_action_file(self, item) -> Path:
        """Create action file for Facebook update"""
        item_type = item.get('type', 'notification')
        item_id = item.get('id', 'unknown')
        text = item.get('text', '')
        timestamp = item.get('timestamp', datetime.now().isoformat())

        content = f"""---
type: facebook_{item_type}
source: facebook
item_id: {item_id}
detected: {timestamp}
priority: high
status: pending
---

# Facebook {item_type.title()}

## Content
{text}

## Suggested Actions
- [ ] Review the {item_type}
- [ ] Draft appropriate response
- [ ] Respond via Facebook
- [ ] Mark as processed

## Notes
- Detected by Facebook Watcher
- Contains urgent keywords
- Requires timely response
"""

        filename = f'FACEBOOK_{item_type.upper()}_{item_id}.md'
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')

        self.logger.info(f"Created action file: {filename}")
        return filepath

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Facebook Watcher')
    parser.add_argument('--vault', required=True, help='Path to AI Employee Vault')
    parser.add_argument('--session', required=True, help='Path to browser session')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds')

    args = parser.parse_args()

    watcher = FacebookWatcher(
        vault_path=args.vault,
        session_path=args.session,
        check_interval=args.interval
    )

    print(f"[Facebook Watcher] Starting...")
    print(f"[Facebook Watcher] Vault: {args.vault}")
    print(f"[Facebook Watcher] Session: {args.session}")
    print(f"[Facebook Watcher] Interval: {args.interval}s")
    print(f"[Facebook Watcher] Press Ctrl+C to stop")

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\n[Facebook Watcher] Stopped by user")
        sys.exit(0)

if __name__ == '__main__':
    main()
