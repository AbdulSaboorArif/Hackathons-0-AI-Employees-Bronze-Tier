"""
One-time setup script to authenticate WhatsApp and LinkedIn
Run this once to save your login sessions, then the watchers can run headless
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

def setup_whatsapp(session_path: str):
    """Setup WhatsApp Web session"""
    print('\n' + '='*60)
    print('WHATSAPP WEB SETUP')
    print('='*60)

    session_dir = Path(session_path)
    session_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print('[INFO] Opening WhatsApp Web...')
        browser = p.chromium.launch_persistent_context(
            str(session_dir),
            headless=False,
            args=['--no-sandbox']
        )

        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto('https://web.whatsapp.com', wait_until='domcontentloaded')

        print('[ACTION] Please scan the QR code with your phone')
        print('[INFO] Waiting for login (up to 10 minutes)...\n')

        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=600000)
            print('[SUCCESS] WhatsApp Web logged in successfully!')
            print('[INFO] Session saved. You can now run watchers in headless mode.\n')

            # Wait a bit to ensure session is fully saved
            page.wait_for_timeout(3000)

        except PlaywrightTimeout:
            print('[FAILED] Login timeout. Please try again.\n')

        browser.close()

def setup_linkedin(session_path: str):
    """Setup LinkedIn session"""
    print('\n' + '='*60)
    print('LINKEDIN SETUP')
    print('='*60)

    session_dir = Path(session_path)
    session_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print('[INFO] Opening LinkedIn...')
        browser = p.chromium.launch_persistent_context(
            str(session_dir),
            headless=False,
            args=['--no-sandbox']
        )

        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto('https://www.linkedin.com', wait_until='domcontentloaded')

        print('[ACTION] Please login with your LinkedIn credentials')
        print('[INFO] Waiting for login (up to 10 minutes)...\n')

        try:
            page.wait_for_selector('[data-test-id="feed-container"]', timeout=600000)
            print('[SUCCESS] LinkedIn logged in successfully!')
            print('[INFO] Session saved. You can now run watchers in headless mode.\n')

            # Wait a bit to ensure session is fully saved
            page.wait_for_timeout(3000)

        except PlaywrightTimeout:
            print('[FAILED] Login timeout. Please try again.\n')

        browser.close()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Setup browser sessions for watchers')
    parser.add_argument('--config', required=True, help='Path to config.json')
    parser.add_argument('--service', choices=['whatsapp', 'linkedin', 'both'], default='both',
                       help='Which service to setup')

    args = parser.parse_args()

    # Load config
    with open(args.config, 'r') as f:
        config = json.load(f)

    print('\n' + '='*60)
    print('WATCHER SESSION SETUP')
    print('='*60)
    print('This script will help you login to WhatsApp and LinkedIn')
    print('Your sessions will be saved for automated monitoring')
    print('='*60)

    if args.service in ['whatsapp', 'both']:
        if config.get('whatsapp', {}).get('enabled', False):
            setup_whatsapp(config['whatsapp']['session_path'])
        else:
            print('[SKIP] WhatsApp is disabled in config')

    if args.service in ['linkedin', 'both']:
        if config.get('linkedin', {}).get('enabled', False):
            setup_linkedin(config['linkedin']['session_path'])
        else:
            print('[SKIP] LinkedIn is disabled in config')

    print('\n' + '='*60)
    print('SETUP COMPLETE')
    print('='*60)
    print('You can now run: python orchestrator.py --config config.json')
    print('The watchers will use your saved sessions')
    print('='*60 + '\n')
