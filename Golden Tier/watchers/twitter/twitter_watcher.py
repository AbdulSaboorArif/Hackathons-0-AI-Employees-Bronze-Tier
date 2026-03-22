#!/usr/bin/env python3
"""
Twitter Watcher - Monitor Twitter for mentions, DMs, and engagement opportunities
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

class TwitterWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str, check_interval: int = 300):
        super().__init__(vault_path, check_interval)
        self.session_path = Path(session_path)
        self.keywords = ['urgent', 'help', 'question', 'inquiry', 'interested', '@']
        self.processed_ids = set()

    def check_for_updates(self) -> list:
        """Check Twitter for new mentions, DMs, and notifications"""
        updates = []

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    viewport={'width': 1280, 'height': 720}
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                # Navigate to Twitter
                page.goto('https://twitter.com/home', timeout=30000)
                time.sleep(3)

                # Check if logged in
                if 'login' in page.url.lower():
                    self.logger.warning("Not logged in to Twitter")
                    browser.close()
                    return []

                # Check notifications
                try:
                    # Navigate to notifications
                    page.goto('https://twitter.com/notifications', timeout=30000)
                    time.sleep(3)

                    # Get notification items
                    notification_selectors = [
                        'article[data-testid="tweet"]',
                        'div[data-testid="cellInnerDiv"]',
                    ]

                    notifications = []
                    for selector in notification_selectors:
                        try:
                            notifications = page.query_selector_all(selector)
                            if notifications:
                                break
                        except:
                            continue

                    for notif in notifications[:5]:  # Check top 5
                        try:
                            text = notif.inner_text().lower()

                            # Check for mentions or keywords
                            if any(kw in text for kw in self.keywords):
                                notif_id = f"tw_notif_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

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

                # Check mentions
                try:
                    # Navigate to mentions
                    page.goto('https://twitter.com/notifications/mentions', timeout=30000)
                    time.sleep(3)

                    # Get mention tweets
                    mentions = page.query_selector_all('article[data-testid="tweet"]')

                    for mention in mentions[:5]:  # Check top 5
                        try:
                            text = mention.inner_text().lower()

                            # Check for urgent keywords
                            if any(kw in text for kw in ['urgent', 'help', 'question', 'inquiry']):
                                mention_id = f"tw_mention_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                                if mention_id not in self.processed_ids:
                                    updates.append({
                                        'type': 'mention',
                                        'id': mention_id,
                                        'text': text[:500],
                                        'timestamp': datetime.now().isoformat()
                                    })
                                    self.processed_ids.add(mention_id)
                        except Exception as e:
                            self.logger.error(f"Error processing mention: {e}")
                            continue

                except Exception as e:
                    self.logger.error(f"Error checking mentions: {e}")

                # Check direct messages
                try:
                    # Navigate to messages
                    page.goto('https://twitter.com/messages', timeout=30000)
                    time.sleep(3)

                    # Get unread message indicators
                    unread_selectors = [
                        'div[data-testid*="unread"]',
                        'div[aria-label*="unread"]',
                    ]

                    # Get all conversations
                    conversations = page.query_selector_all('div[data-testid="conversation"]')

                    for conv in conversations[:3]:  # Check top 3
                        try:
                            text = conv.inner_text().lower()

                            if any(kw in text for kw in self.keywords):
                                dm_id = f"tw_dm_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                                if dm_id not in self.processed_ids:
                                    updates.append({
                                        'type': 'direct_message',
                                        'id': dm_id,
                                        'text': text[:500],
                                        'timestamp': datetime.now().isoformat()
                                    })
                                    self.processed_ids.add(dm_id)
                        except Exception as e:
                            self.logger.error(f"Error processing DM: {e}")
                            continue

                except Exception as e:
                    self.logger.error(f"Error checking DMs: {e}")

                browser.close()

        except Exception as e:
            self.logger.error(f"Error in Twitter watcher: {e}")

        return updates

    def create_action_file(self, item) -> Path:
        """Create action file for Twitter update"""
        item_type = item.get('type', 'notification')
        item_id = item.get('id', 'unknown')
        text = item.get('text', '')
        timestamp = item.get('timestamp', datetime.now().isoformat())

        content = f"""---
type: twitter_{item_type}
source: twitter
item_id: {item_id}
detected: {timestamp}
priority: high
status: pending
---

# Twitter {item_type.replace('_', ' ').title()}

## Content
{text}

## Suggested Actions
- [ ] Review the {item_type.replace('_', ' ')}
- [ ] Draft appropriate response (max 280 chars)
- [ ] Respond via Twitter
- [ ] Mark as processed

## Notes
- Detected by Twitter Watcher
- Requires timely response
- Keep response under 280 characters
"""

        filename = f'TWITTER_{item_type.upper()}_{item_id}.md'
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')

        self.logger.info(f"Created action file: {filename}")
        return filepath

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Twitter Watcher')
    parser.add_argument('--vault', required=True, help='Path to AI Employee Vault')
    parser.add_argument('--session', required=True, help='Path to browser session')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds')

    args = parser.parse_args()

    watcher = TwitterWatcher(
        vault_path=args.vault,
        session_path=args.session,
        check_interval=args.interval
    )

    print(f"[Twitter Watcher] Starting...")
    print(f"[Twitter Watcher] Vault: {args.vault}")
    print(f"[Twitter Watcher] Session: {args.session}")
    print(f"[Twitter Watcher] Interval: {args.interval}s")
    print(f"[Twitter Watcher] Press Ctrl+C to stop")

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\n[Twitter Watcher] Stopped by user")
        sys.exit(0)

if __name__ == '__main__':
    main()
