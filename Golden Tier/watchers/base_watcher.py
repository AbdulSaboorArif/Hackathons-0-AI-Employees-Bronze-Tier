"""
Base Watcher Class - Template for all watchers
Provides common functionality for monitoring and creating action files
"""
import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
import json

class BaseWatcher(ABC):
    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logs = self.vault_path / 'Logs'
        self.check_interval = check_interval

        # Create directories if they don't exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.FileHandler(self.logs / f'{self.__class__.__name__}.log')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder"""
        pass

    def log_action(self, action_type: str, details: dict):
        """Log watcher actions"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'watcher': self.__class__.__name__,
            'action': action_type,
            'details': details
        }
        self.logger.info(json.dumps(log_entry))

    def run(self):
        """Main watcher loop"""
        self.logger.info(f'Starting {self.__class__.__name__}')
        print(f'[START] {self.__class__.__name__} started - checking every {self.check_interval}s')

        while True:
            try:
                items = self.check_for_updates()
                if items:
                    print(f'[FOUND] Found {len(items)} new items')
                    for item in items:
                        filepath = self.create_action_file(item)
                        print(f'[OK] Created: {filepath.name}')
                        self.log_action('item_created', {'file': str(filepath)})
            except Exception as e:
                self.logger.error(f'Error in watcher loop: {e}', exc_info=True)
                print(f'[ERROR] Error: {e}')

            time.sleep(self.check_interval)
