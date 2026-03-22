"""
File System Watcher
Monitors the Inbox folder for new files and creates action items
"""

import shutil
from pathlib import Path
from datetime import datetime
from base_watcher import BaseWatcher

class FileSystemWatcher(BaseWatcher):
    """Watches the Inbox folder for new files"""

    def __init__(self, vault_path: str, check_interval: int = 30):
        """
        Initialize the file system watcher

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 30)
        """
        super().__init__(vault_path, check_interval)
        self.inbox = self.vault_path / 'Inbox'
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.processed_files = set()

        self.logger.info(f'Watching inbox: {self.inbox}')

    def check_for_updates(self) -> list:
        """
        Check for new files in the Inbox folder

        Returns:
            List of new files found
        """
        new_files = []

        # Get all files in inbox (excluding hidden files and .md files)
        for file_path in self.inbox.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                # Skip if already processed
                if file_path.name not in self.processed_files:
                    new_files.append(file_path)
                    self.processed_files.add(file_path.name)

        return new_files

    def create_action_file(self, file_path: Path) -> Path:
        """
        Create an action file for the new file

        Args:
            file_path: Path to the new file

        Returns:
            Path to the created action file
        """
        timestamp = datetime.now().isoformat()
        file_size = file_path.stat().st_size
        file_ext = file_path.suffix

        # Create metadata file
        action_filename = f'FILE_{file_path.stem}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        action_path = self.needs_action / action_filename

        # Determine file type and suggested actions
        file_type = self._determine_file_type(file_ext)
        suggested_actions = self._get_suggested_actions(file_type)

        content = f"""---
type: file_drop
original_name: {file_path.name}
file_type: {file_type}
size_bytes: {file_size}
size_readable: {self._format_size(file_size)}
location: {file_path}
detected: {timestamp}
status: pending
priority: medium
---

# New File Detected: {file_path.name}

## File Information
- **Name**: {file_path.name}
- **Type**: {file_type}
- **Size**: {self._format_size(file_size)}
- **Location**: `{file_path}`
- **Detected**: {timestamp}

## Suggested Actions
{suggested_actions}

## Processing Notes
*Add your notes here after reviewing the file*

---
*Created by File System Watcher*
"""

        action_path.write_text(content, encoding='utf-8')
        return action_path

    def _determine_file_type(self, extension: str) -> str:
        """Determine file type from extension"""
        ext_map = {
            '.pdf': 'PDF Document',
            '.doc': 'Word Document',
            '.docx': 'Word Document',
            '.xls': 'Excel Spreadsheet',
            '.xlsx': 'Excel Spreadsheet',
            '.csv': 'CSV Data',
            '.txt': 'Text File',
            '.md': 'Markdown Document',
            '.jpg': 'Image (JPEG)',
            '.jpeg': 'Image (JPEG)',
            '.png': 'Image (PNG)',
            '.gif': 'Image (GIF)',
            '.zip': 'Archive (ZIP)',
            '.rar': 'Archive (RAR)',
            '.py': 'Python Script',
            '.js': 'JavaScript File',
            '.json': 'JSON Data',
            '.xml': 'XML Data',
        }
        return ext_map.get(extension.lower(), 'Unknown File Type')

    def _get_suggested_actions(self, file_type: str) -> str:
        """Get suggested actions based on file type"""
        if 'Document' in file_type:
            return """- [ ] Review document content
- [ ] Extract key information
- [ ] File in appropriate folder
- [ ] Update relevant records"""
        elif 'Spreadsheet' in file_type or 'CSV' in file_type:
            return """- [ ] Review data
- [ ] Import to accounting system
- [ ] Generate summary report
- [ ] Archive processed data"""
        elif 'Image' in file_type:
            return """- [ ] Review image
- [ ] Add to relevant project
- [ ] Archive or delete if not needed"""
        elif 'PDF' in file_type:
            return """- [ ] Review PDF content
- [ ] Extract important information
- [ ] File appropriately
- [ ] Update Dashboard if relevant"""
        else:
            return """- [ ] Review file
- [ ] Determine appropriate action
- [ ] Process or archive"""

    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"


if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = '../AI_Employee_Vault'

    # Create and run the watcher
    watcher = FileSystemWatcher(vault_path, check_interval=30)

    print(f"\n{'='*60}")
    print("File System Watcher - Bronze Tier")
    print(f"{'='*60}")
    print(f"Vault: {watcher.vault_path}")
    print(f"Inbox: {watcher.inbox}")
    print(f"Check interval: {watcher.check_interval} seconds")
    print(f"{'='*60}\n")
    print("Watching for new files... (Press Ctrl+C to stop)\n")

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\n\nWatcher stopped. Goodbye!")
