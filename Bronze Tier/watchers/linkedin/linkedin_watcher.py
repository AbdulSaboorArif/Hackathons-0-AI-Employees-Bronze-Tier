"""
LinkedIn Watcher - Monitors LinkedIn for notifications and messages
Uses Playwright to automate LinkedIn and detect engagement opportunities
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from base_watcher import BaseWatcher
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

class LinkedInWatcher(BaseWatcher):
    """Watches LinkedIn for notifications and engagement opportunities"""

    def __init__(self, vault_path: str, session_path: str, check_interval: int = 300):
        """
        Initialize LinkedIn watcher

        Args:
            vault_path: Path to Obsidian vault
            session_path: Path to store browser session data
            check_interval: Seconds between checks (default: 300 = 5 minutes)
        """
        super().__init__(vault_path, check_interval)
        self.session_path = Path(session_path)
        self.session_path.mkdir(parents=True, exist_ok=True)

        self.processed_notifications = set()
        self.logger.info('LinkedIn Watcher initialized')

    def check_for_updates(self) -> list:
        """Check LinkedIn for new notifications and messages"""
        items = []

        try:
            with sync_playwright() as p:
                # Launch browser with persistent context
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,  # Set to True for background operation
                    args=['--no-sandbox']
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                # Navigate to LinkedIn
                page.goto('https://www.linkedin.com', wait_until='domcontentloaded')

                try:
                    # Wait for feed to load (indicates logged in)
                    page.wait_for_selector('[data-test-id="feed-container"]', timeout=10000)
                    self.logger.info('LinkedIn loaded successfully')

                    # Check notifications
                    notifications_button = page.query_selector('[id="global-nav-icon-notifications-badge"]')
                    if notifications_button:
                        # Check if there are unread notifications
                        badge = page.query_selector('.notification-badge')
                        if badge:
                            notifications_button.click()
                            page.wait_for_timeout(2000)

                            # Get notification items
                            notification_items = page.query_selector_all('.notification-card')

                            for notif in notification_items[:5]:  # Check first 5
                                try:
                                    text = notif.inner_text()

                                    # Create unique ID
                                    notif_id = text[:50]

                                    if notif_id not in self.processed_notifications:
                                        # Determine notification type
                                        notif_type = 'engagement'
                                        if 'commented' in text.lower():
                                            notif_type = 'comment'
                                        elif 'liked' in text.lower() or 'reacted' in text.lower():
                                            notif_type = 'reaction'
                                        elif 'shared' in text.lower():
                                            notif_type = 'share'
                                        elif 'message' in text.lower():
                                            notif_type = 'message'
                                        elif 'connection' in text.lower():
                                            notif_type = 'connection_request'

                                        items.append({
                                            'type': notif_type,
                                            'text': text,
                                            'id': notif_id,
                                            'timestamp': datetime.now().isoformat()
                                        })

                                        self.processed_notifications.add(notif_id)

                                except Exception as e:
                                    self.logger.debug(f'Error processing notification: {e}')
                                    continue

                    # Check for post engagement opportunities
                    # Look for posts with high engagement that we haven't commented on
                    feed_posts = page.query_selector_all('[data-test-id="feed-post"]')

                    for post in feed_posts[:3]:  # Check first 3 posts
                        try:
                            # Get engagement count
                            reactions = post.query_selector('.social-details-social-counts__reactions-count')
                            if reactions:
                                reaction_text = reactions.inner_text()
                                # If post has significant engagement (e.g., 50+ reactions)
                                if any(char.isdigit() for char in reaction_text):
                                    post_text = post.query_selector('.feed-shared-text')
                                    if post_text:
                                        text = post_text.inner_text()[:200]
                                        post_id = f"post_{text[:30]}"

                                        if post_id not in self.processed_notifications:
                                            items.append({
                                                'type': 'engagement_opportunity',
                                                'text': text,
                                                'reactions': reaction_text,
                                                'id': post_id,
                                                'timestamp': datetime.now().isoformat()
                                            })
                                            self.processed_notifications.add(post_id)
                        except Exception as e:
                            self.logger.debug(f'Error processing post: {e}')
                            continue

                except PlaywrightTimeout:
                    self.logger.warning('LinkedIn not logged in - please login')
                    print('\n[LOGIN] LinkedIn requires login!')
                    print('[AUTH] Please login in the browser window')
                    print('[INFO] Waiting up to 5 minutes for login...\n')

                    # Wait up to 5 minutes for login
                    try:
                        page.wait_for_selector('[data-test-id="feed-container"]', timeout=300000)
                        print('[OK] Login successful! Checking for notifications...\n')

                        # Now check for notifications since we're logged in
                        notifications_button = page.query_selector('[id="global-nav-icon-notifications-badge"]')
                        if notifications_button:
                            badge = page.query_selector('.notification-badge')
                            if badge:
                                notifications_button.click()
                                page.wait_for_timeout(2000)

                                notification_items = page.query_selector_all('.notification-card')

                                for notif in notification_items[:5]:
                                    try:
                                        text = notif.inner_text()
                                        notif_id = text[:50]

                                        if notif_id not in self.processed_notifications:
                                            notif_type = 'engagement'
                                            if 'commented' in text.lower():
                                                notif_type = 'comment'
                                            elif 'liked' in text.lower() or 'reacted' in text.lower():
                                                notif_type = 'reaction'
                                            elif 'shared' in text.lower():
                                                notif_type = 'share'
                                            elif 'message' in text.lower():
                                                notif_type = 'message'
                                            elif 'connection' in text.lower():
                                                notif_type = 'connection_request'

                                            items.append({
                                                'type': notif_type,
                                                'text': text,
                                                'id': notif_id,
                                                'timestamp': datetime.now().isoformat()
                                            })

                                            self.processed_notifications.add(notif_id)

                                    except Exception as e:
                                        self.logger.debug(f'Error processing notification: {e}')
                                        continue

                        # Check feed posts
                        feed_posts = page.query_selector_all('[data-test-id="feed-post"]')

                        for post in feed_posts[:3]:
                            try:
                                reactions = post.query_selector('.social-details-social-counts__reactions-count')
                                if reactions:
                                    reaction_text = reactions.inner_text()
                                    if any(char.isdigit() for char in reaction_text):
                                        post_text = post.query_selector('.feed-shared-text')
                                        if post_text:
                                            text = post_text.inner_text()[:200]
                                            post_id = f"post_{text[:30]}"

                                            if post_id not in self.processed_notifications:
                                                items.append({
                                                    'type': 'engagement_opportunity',
                                                    'text': text,
                                                    'reactions': reaction_text,
                                                    'id': post_id,
                                                    'timestamp': datetime.now().isoformat()
                                                })
                                                self.processed_notifications.add(post_id)
                            except Exception as e:
                                self.logger.debug(f'Error processing post: {e}')
                                continue

                    except PlaywrightTimeout:
                        print('[TIMEOUT] Login not completed within 5 minutes')
                        print('[INFO] Will retry on next check\n')

                browser.close()

        except Exception as e:
            self.logger.error(f'Error checking LinkedIn: {e}')

        return items

    def create_action_file(self, item) -> Path:
        """Create action file for LinkedIn notification"""
        item_type = item['type']
        text = item['text']
        timestamp = item.get('timestamp', datetime.now().isoformat())

        # Determine priority based on type
        priority_map = {
            'message': 'high',
            'connection_request': 'high',
            'comment': 'normal',
            'engagement_opportunity': 'normal',
            'reaction': 'low',
            'share': 'normal'
        }
        priority = priority_map.get(item_type, 'normal')

        content = f"""---
type: linkedin_{item_type}
received: {timestamp}
priority: {priority}
status: pending
---

## LinkedIn Activity

**Type:** {item_type.replace('_', ' ').title()}

{text}

## Suggested Actions
"""

        if item_type == 'comment':
            content += """- [ ] Review comment
- [ ] Draft thoughtful reply
- [ ] Engage with commenter's profile
- [ ] Mark as done
"""
        elif item_type == 'connection_request':
            content += """- [ ] Review profile
- [ ] Accept or decline with message
- [ ] Add to CRM if relevant
- [ ] Mark as done
"""
        elif item_type == 'engagement_opportunity':
            content += f"""- [ ] Read full post
- [ ] Draft insightful comment
- [ ] Request approval for comment
- [ ] Post comment
- [ ] Mark as done

**Engagement:** {item.get('reactions', 'N/A')}
"""
        else:
            content += """- [ ] Review notification
- [ ] Take appropriate action
- [ ] Mark as done
"""

        content += """
## Context
This LinkedIn activity may present a business opportunity or require engagement to maintain professional presence.
"""

        # Create filename
        file_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_type = item_type.replace('_', '-')
        filename = f'LINKEDIN_{file_timestamp}_{safe_type}.md'

        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')

        return filepath

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='LinkedIn Watcher')
    parser.add_argument('--vault', required=True, help='Path to Obsidian vault')
    parser.add_argument('--session', required=True, help='Path to browser session directory')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds')

    args = parser.parse_args()

    watcher = LinkedInWatcher(
        vault_path=args.vault,
        session_path=args.session,
        check_interval=args.interval
    )

    print(f'[START] LinkedIn Watcher started')
    print(f'[VAULT] Vault: {args.vault}')
    print(f'[SESSION] Session: {args.session}')
    print(f'[INTERVAL] Checking every {args.interval} seconds')
    print(f'Press Ctrl+C to stop\n')

    watcher.run()
