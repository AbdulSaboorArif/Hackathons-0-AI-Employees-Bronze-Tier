#!/usr/bin/env python3
"""
Instagram Watcher - Monitor Instagram for DMs, comments, and engagement opportunities
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

class InstagramWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str, check_interval: int = 300):
        super().__init__(vault_path, check_interval)
        self.session_path = Path(session_path)
        self.keywords = ['urgent', 'help', 'question', 'inquiry', 'interested', 'price', 'buy']
        self.processed_ids = set()

    def check_for_updates(self) -> list:
        """Check Instagram for new DMs and notifications"""
        updates = []

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    viewport={'width': 1280, 'height': 720}
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                # Navigate to Instagram
                page.goto('https://www.instagram.com/', timeout=30000)
                time.sleep(3)

                # Check if logged in
                if 'login' in page.url.lower():
                    self.logger.warning("Not logged in to Instagram")
                    browser.close()
                    return []

                # Check direct messages
                try:
                    # Navigate to DMs
                    dm_selectors = [
                        'a[href="/direct/inbox/"]',
                        'svg[aria-label="Direct"]',
                        'a[href*="/direct/"]',
                    ]

                    for selector in dm_selectors:
                        try:
                            page.click(selector, timeout=5000)
                            break
                        except:
                            continue

                    time.sleep(3)

                    # Get unread message threads
                    unread_selectors = [
                        'div[role="button"]:has-text("unread")',
                        'div[class*="unread"]',
                    ]

                    # Get all message threads
                    threads = page.query_selector_all('div[role="button"]')

                    for thread in threads[:5]:  # Check top 5 threads
                        try:
                            text = thread.inner_text().lower()

                            # Check for keywords or indicators of new messages
                            if any(kw in text for kw in self.keywords) or 'new' in text:
                                message_id = f"ig_dm_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                                if message_id not in self.processed_ids:
                                    updates.append({
                                        'type': 'direct_message',
                                        'id': message_id,
                                        'text': text[:500],
                                        'timestamp': datetime.now().isoformat()
                                    })
                                    self.processed_ids.add(message_id)
                        except Exception as e:
                            self.logger.error(f"Error processing DM: {e}")
                            continue

                except Exception as e:
                    self.logger.error(f"Error checking DMs: {e}")

                # Check notifications
                try:
                    # Go back to home
                    page.goto('https://www.instagram.com/', timeout=30000)
                    time.sleep(2)

                    # Click notifications
                    notification_selectors = [
                        'svg[aria-label="Notifications"]',
                        'a[href*="/notifications/"]',
                    ]

                    for selector in notification_selectors:
                        try:
                            page.click(selector, timeout=5000)
                            break
                        except:
                            continue

                    time.sleep(2)

                    # Get notification items
                    notifications = page.query_selector_all('div[role="button"]')

                    for notif in notifications[:5]:  # Check top 5
                        try:
                            text = notif.inner_text().lower()

                            # Check for engagement opportunities
                            if any(kw in text for kw in ['comment', 'mentioned', 'tagged', 'liked']):
                                notif_id = f"ig_notif_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                                if notif_id not in self.processed_ids:
                                    updates.append({
                                        'type': 'notification',
                                        'id': notif_id,
                                        'text': text[:500],
                                        'timestamp': datetime.now().isoformat()
                                    })
                                    self.processed_ids.add(notif_id)
                        except Exception as e:
                            self.logger.error(f"Error processing notification: {e}")
                            continue

                except Exception as e:
                    self.logger.error(f"Error checking notifications: {e}")

                browser.close()

        except Exception as e:
            self.logger.error(f"Error in Instagram watcher: {e}")

        return updates

    def create_action_file(self, item) -> Path:
        """Create action file for Instagram update"""
        item_type = item.get('type', 'notification')
        item_id = item.get('id', 'unknown')
        text = item.get('text', '')
        timestamp = item.get('timestamp', datetime.now().isoformat())

        content = f"""---
type: instagram_{item_type}
source: instagram
item_id: {item_id}
detected: {timestamp}
priority: high
status: pending
---

# Instagram {item_type.replace('_', ' ').title()}

## Content
{text}

## Suggested Actions
- [ ] Review the {item_type.replace('_', ' ')}
- [ ] Draft appropriate response
- [ ] Respond via Instagram
- [ ] Mark as processed

## Notes
- Detected by Instagram Watcher
- Potential engagement opportunity
- Requires timely response
"""

        filename = f'INSTAGRAM_{item_type.upper()}_{item_id}.md'
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')

        self.logger.info(f"Created action file: {filename}")
        return filepath

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Instagram Watcher')
    parser.add_argument('--vault', required=True, help='Path to AI Employee Vault')
    parser.add_argument('--session', required=True, help='Path to browser session')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds')

    args = parser.parse_args()

    watcher = InstagramWatcher(
        vault_path=args.vault,
        session_path=args.session,
        check_interval=args.interval
    )

    print(f"[Instagram Watcher] Starting...")
    print(f"[Instagram Watcher] Vault: {args.vault}")
    print(f"[Instagram Watcher] Session: {args.session}")
    print(f"[Instagram Watcher] Interval: {args.interval}s")
    print(f"[Instagram Watcher] Press Ctrl+C to stop")

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\n[Instagram Watcher] Stopped by user")
        sys.exit(0)

if __name__ == '__main__':
    main()
