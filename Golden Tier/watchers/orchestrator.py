"""
Master Orchestrator - Runs all watchers in parallel
Manages Gmail, WhatsApp, and LinkedIn watchers simultaneously
"""
import sys
import threading
import signal
from pathlib import Path
from datetime import datetime

# Add watchers to path
sys.path.append(str(Path(__file__).parent))

from gmail.gmail_watcher import GmailWatcher
from whatsapp.whatsapp_watcher import WhatsAppWatcher
from linkedin.linkedin_watcher import LinkedInWatcher

class WatcherOrchestrator:
    """Orchestrates multiple watchers running in parallel"""

    def __init__(self, config: dict):
        self.config = config
        self.watchers = []
        self.threads = []
        self.running = True

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def shutdown(self, signum, frame):
        """Graceful shutdown handler"""
        print('\n\n>> Shutting down watchers...')
        self.running = False
        sys.exit(0)

    def start_gmail_watcher(self):
        """Start Gmail watcher in thread"""
        if not self.config.get('gmail', {}).get('enabled', False):
            print('[SKIP] Gmail watcher disabled')
            return

        try:
            watcher = GmailWatcher(
                vault_path=self.config['vault_path'],
                credentials_path=self.config['gmail']['credentials_path'],
                check_interval=self.config['gmail'].get('interval', 120)
            )
            self.watchers.append(watcher)

            thread = threading.Thread(target=watcher.run, daemon=True)
            thread.start()
            self.threads.append(thread)

            print('[OK] Gmail watcher started')
        except Exception as e:
            print(f'[ERROR] Gmail watcher failed: {e}')

    def start_whatsapp_watcher(self):
        """Start WhatsApp watcher in thread"""
        if not self.config.get('whatsapp', {}).get('enabled', False):
            print('[SKIP] WhatsApp watcher disabled')
            return

        try:
            watcher = WhatsAppWatcher(
                vault_path=self.config['vault_path'],
                session_path=self.config['whatsapp']['session_path'],
                check_interval=self.config['whatsapp'].get('interval', 60)
            )
            self.watchers.append(watcher)

            thread = threading.Thread(target=watcher.run, daemon=True)
            thread.start()
            self.threads.append(thread)

            print('[OK] WhatsApp watcher started')
        except Exception as e:
            print(f'[ERROR] WhatsApp watcher failed: {e}')

    def start_linkedin_watcher(self):
        """Start LinkedIn watcher in thread"""
        if not self.config.get('linkedin', {}).get('enabled', False):
            print('[SKIP] LinkedIn watcher disabled')
            return

        try:
            watcher = LinkedInWatcher(
                vault_path=self.config['vault_path'],
                session_path=self.config['linkedin']['session_path'],
                check_interval=self.config['linkedin'].get('interval', 300)
            )
            self.watchers.append(watcher)

            thread = threading.Thread(target=watcher.run, daemon=True)
            thread.start()
            self.threads.append(thread)

            print('[OK] LinkedIn watcher started')
        except Exception as e:
            print(f'[ERROR] LinkedIn watcher failed: {e}')

    def run(self):
        """Start all enabled watchers"""
        print('=' * 60)
        print('>> SILVER TIER WATCHER ORCHESTRATOR')
        print('=' * 60)
        print(f'Vault: {self.config["vault_path"]}')
        print(f'Started: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print('=' * 60)
        print()

        # Start all watchers (LinkedIn first, then WhatsApp)
        self.start_linkedin_watcher()
        self.start_whatsapp_watcher()
        self.start_gmail_watcher()

        print()
        print('=' * 60)
        print(f'>> {len(self.watchers)} watcher(s) running')
        print('>> Press Ctrl+C to stop all watchers')
        print('=' * 60)
        print()

        # Keep main thread alive
        try:
            while self.running:
                for thread in self.threads:
                    thread.join(timeout=1.0)
        except KeyboardInterrupt:
            self.shutdown(None, None)

if __name__ == '__main__':
    import json
    import argparse

    parser = argparse.ArgumentParser(description='Silver Tier Watcher Orchestrator')
    parser.add_argument('--config', required=True, help='Path to config.json')
    args = parser.parse_args()

    # Load configuration
    with open(args.config, 'r') as f:
        config = json.load(f)

    # Start orchestrator
    orchestrator = WatcherOrchestrator(config)
    orchestrator.run()
