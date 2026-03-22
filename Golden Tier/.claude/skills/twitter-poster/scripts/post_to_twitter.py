#!/usr/bin/env python3
"""
Twitter/X Poster - Post tweets and threads to Twitter
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time

def parse_approval_file(file_path):
    """Parse approval file and extract tweet content"""
    content = Path(file_path).read_text(encoding='utf-8')

    # Split frontmatter and content
    parts = content.split('---')
    if len(parts) < 3:
        raise ValueError("Invalid approval file format")

    # Parse frontmatter
    frontmatter = parts[1].strip()
    is_thread = False
    for line in frontmatter.split('\n'):
        if line.startswith('thread:'):
            is_thread = line.split(':', 1)[1].strip().lower() == 'true'

    # Extract tweet content
    tweet_content = '---'.join(parts[2:]).strip()

    # Remove markdown header if present
    if tweet_content.startswith('# Twitter'):
        lines = tweet_content.split('\n')
        tweet_content = '\n'.join(lines[1:]).strip()

    # If thread, split by ---
    if is_thread:
        tweets = [t.strip() for t in tweet_content.split('---') if t.strip()]
    else:
        tweets = [tweet_content]

    # Validate character count
    for i, tweet in enumerate(tweets):
        if len(tweet) > 280:
            raise ValueError(f"Tweet {i+1} exceeds 280 characters ({len(tweet)} chars)")

    return tweets

def post_to_twitter(session_path, tweets, vault_path):
    """Post tweet(s) to Twitter using Playwright"""

    print(f"[Twitter] Starting post process...")
    print(f"[Twitter] Session: {session_path}")
    print(f"[Twitter] Tweets to post: {len(tweets)}")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            print("[Twitter] Navigating to Twitter...")
            page.goto('https://twitter.com/home', wait_until='networkidle', timeout=30000)
            time.sleep(3)

            # Check if logged in
            if 'login' in page.url.lower():
                print("[Twitter] ❌ Not logged in. Please run setup_twitter_session.py first.")
                return False

            print("[Twitter] ✓ Logged in successfully")

            # Post each tweet
            for i, tweet in enumerate(tweets):
                print(f"[Twitter] Posting tweet {i+1}/{len(tweets)}...")

                # Find tweet compose box
                compose_selectors = [
                    'div[data-testid="tweetTextarea_0"]',
                    'div[role="textbox"][aria-label*="Tweet"]',
                    'div.public-DraftEditor-content',
                ]

                compose_box = None
                for selector in compose_selectors:
                    try:
                        compose_box = page.wait_for_selector(selector, timeout=5000)
                        if compose_box:
                            print(f"[Twitter] ✓ Found compose box")
                            break
                    except:
                        continue

                if not compose_box:
                    print("[Twitter] ❌ Could not find compose box")
                    screenshot_path = Path(vault_path) / 'Logs' / f'twitter_error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                    screenshot_path.parent.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(screenshot_path))
                    return False

                # Type tweet
                compose_box.click()
                time.sleep(1)
                page.keyboard.type(tweet, delay=50)
                time.sleep(2)

                print(f"[Twitter] ✓ Tweet {i+1} typed ({len(tweet)} chars)")

                # Take screenshot before posting
                screenshot_path = Path(vault_path) / 'Logs' / f'twitter_preview_{i+1}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                screenshot_path.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(screenshot_path))
                print(f"[Twitter] Preview screenshot: {screenshot_path}")

                # Find and click Post/Tweet button
                post_button_selectors = [
                    'div[data-testid="tweetButtonInline"]',
                    'div[data-testid="tweetButton"]',
                    'button[data-testid="tweetButton"]',
                ]

                posted = False
                for selector in post_button_selectors:
                    try:
                        page.click(selector, timeout=5000)
                        posted = True
                        print(f"[Twitter] ✓ Clicked Post button")
                        break
                    except:
                        continue

                if not posted:
                    print("[Twitter] ❌ Could not find Post button")
                    return False

                # Wait for post to complete
                print("[Twitter] Waiting for post to complete...")
                time.sleep(5)

                # If thread, wait before next tweet
                if i < len(tweets) - 1:
                    print(f"[Twitter] Waiting before next tweet in thread...")
                    time.sleep(3)

            # Take final screenshot
            screenshot_path = Path(vault_path) / 'Logs' / f'twitter_success_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            page.screenshot(path=str(screenshot_path))
            print(f"[Twitter] Success screenshot: {screenshot_path}")

            # Log the post
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'platform': 'twitter',
                'tweet_count': len(tweets),
                'is_thread': len(tweets) > 1,
                'total_chars': sum(len(t) for t in tweets),
                'status': 'success',
                'screenshot': str(screenshot_path)
            }

            log_file = Path(vault_path) / 'Logs' / f'{datetime.now().strftime("%Y-%m-%d")}_twitter_posts.json'
            log_file.parent.mkdir(parents=True, exist_ok=True)

            logs = []
            if log_file.exists():
                logs = json.loads(log_file.read_text())
            logs.append(log_entry)
            log_file.write_text(json.dumps(logs, indent=2))

            print("[Twitter] ✅ Post published successfully!")
            return True

        except Exception as e:
            print(f"[Twitter] ❌ Error: {str(e)}")
            screenshot_path = Path(vault_path) / 'Logs' / f'twitter_error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
            print(f"[Twitter] Error screenshot: {screenshot_path}")
            return False

        finally:
            browser.close()

def main():
    parser = argparse.ArgumentParser(description='Post to Twitter with approval workflow')
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
        tweets = parse_approval_file(approval_file)
    except Exception as e:
        print(f"Error parsing approval file: {e}")
        sys.exit(1)

    # Post to Twitter
    success = post_to_twitter(str(session_path), tweets, str(vault_path))

    if success:
        done_dir = vault_path / 'Done'
        done_dir.mkdir(exist_ok=True)
        done_file = done_dir / approval_file.name
        approval_file.rename(done_file)
        print(f"[Twitter] Moved approval file to: {done_file}")
        sys.exit(0)
    else:
        print("[Twitter] Post failed. Approval file remains in place.")
        sys.exit(1)

if __name__ == '__main__':
    main()
