#!/usr/bin/env python3
"""
Ralph Wiggum Stop Hook - Autonomous task completion loop
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# State file location
STATE_FILE = Path(__file__).parent / 'ralph_state.json'
LOG_FILE = Path(__file__).parent / 'ralph_loop.log'

def log(message):
    """Log to file"""
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

def load_state():
    """Load current loop state"""
    if not STATE_FILE.exists():
        return None

    try:
        return json.loads(STATE_FILE.read_text())
    except:
        return None

def save_state(state):
    """Save loop state"""
    STATE_FILE.write_text(json.dumps(state, indent=2))

def check_completion(state):
    """Check if task is complete"""

    check_type = state.get('completion_check', 'promise')

    if check_type == 'promise':
        # Check for promise in Claude's output
        # This would be passed via stdin or environment
        return False  # Simplified for now

    elif check_type == 'file_movement':
        # Check if target file moved to Done folder
        target_file = state.get('target_file', '')
        done_folder = Path(state.get('done_folder', 'AI_Employee_Vault/Done'))

        if target_file:
            # Check if file exists in Done folder
            target_name = Path(target_file).name
            done_file = done_folder / target_name

            if done_file.exists():
                log(f"✓ Task complete: {target_name} found in Done folder")
                return True

    elif check_type == 'folder_empty':
        # Check if target folder is empty
        target_folder = Path(state.get('target_folder', ''))

        if target_folder.exists():
            files = list(target_folder.glob('*.md'))
            if len(files) == 0:
                log(f"✓ Task complete: {target_folder} is empty")
                return True

    return False

def main():
    """Stop hook main logic"""

    # Load state
    state = load_state()

    if not state:
        # No active Ralph loop, allow exit
        sys.exit(0)

    # Check if loop is enabled
    if not state.get('enabled', False):
        log("Ralph loop disabled, allowing exit")
        sys.exit(0)

    # Check max iterations
    current_iteration = state.get('current_iteration', 0)
    max_iterations = state.get('max_iterations', 10)

    if current_iteration >= max_iterations:
        log(f"✓ Max iterations reached ({max_iterations}), allowing exit")
        STATE_FILE.unlink(missing_ok=True)
        sys.exit(0)

    # Check for manual stop signal
    stop_signal = Path(__file__).parent / 'STOP_RALPH_LOOP'
    if stop_signal.exists():
        log("✓ Manual stop signal detected, allowing exit")
        stop_signal.unlink()
        STATE_FILE.unlink(missing_ok=True)
        sys.exit(0)

    # Check if task is complete
    if check_completion(state):
        log("✓ Task complete, allowing exit")
        STATE_FILE.unlink(missing_ok=True)
        sys.exit(0)

    # Task not complete, continue loop
    current_iteration += 1
    state['current_iteration'] = current_iteration
    state['last_check'] = datetime.now().isoformat()
    save_state(state)

    log(f"⟳ Task not complete, continuing loop (iteration {current_iteration}/{max_iterations})")

    # Block exit (return non-zero to prevent Claude from stopping)
    # In practice, this would re-inject the prompt
    sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(f"❌ Error in Ralph hook: {e}")
        sys.exit(0)  # Allow exit on error
