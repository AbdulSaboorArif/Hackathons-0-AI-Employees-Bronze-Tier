#!/usr/bin/env python3
"""
Start Ralph Wiggum autonomous loop
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
import subprocess

def start_ralph_loop(vault_path, task_prompt, max_iterations=10, completion_check='file_movement'):
    """Start autonomous task loop"""

    print(f"[Ralph Loop] Starting autonomous task...")
    print(f"[Ralph Loop] Task: {task_prompt}")
    print(f"[Ralph Loop] Max iterations: {max_iterations}")
    print(f"[Ralph Loop] Completion check: {completion_check}")

    # Create state file
    state = {
        'task_id': f"ralph_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'prompt': task_prompt,
        'created': datetime.now().isoformat(),
        'max_iterations': max_iterations,
        'current_iteration': 0,
        'completion_check': completion_check,
        'enabled': True,
        'vault_path': str(vault_path)
    }

    if completion_check == 'file_movement':
        state['target_file'] = 'AI_Employee_Vault/Needs_Action/*.md'
        state['done_folder'] = str(Path(vault_path) / 'Done')
    elif completion_check == 'folder_empty':
        state['target_folder'] = str(Path(vault_path) / 'Needs_Action')

    # Save state
    hooks_dir = Path(__file__).parent.parent.parent / '.claude' / 'hooks'
    hooks_dir.mkdir(parents=True, exist_ok=True)

    state_file = hooks_dir / 'ralph_state.json'
    state_file.write_text(json.dumps(state, indent=2))

    print(f"[Ralph Loop] State saved to: {state_file}")
    print(f"[Ralph Loop] To stop manually: touch {hooks_dir}/STOP_RALPH_LOOP")
    print()
    print("="*60)
    print("RALPH LOOP ACTIVE - Claude will work autonomously")
    print("="*60)
    print()

    # Note: In production, this would launch Claude with the prompt
    # For now, we just create the state file
    print("[Ralph Loop] State file created. Start Claude to begin loop.")
    print(f"[Ralph Loop] Prompt: {task_prompt}")

    return state

def main():
    parser = argparse.ArgumentParser(description='Start Ralph Wiggum autonomous loop')
    parser.add_argument('--vault', required=True, help='Path to AI Employee Vault')
    parser.add_argument('--task', required=True, help='Task prompt for Claude')
    parser.add_argument('--max-iterations', type=int, default=10, help='Max loop iterations')
    parser.add_argument('--completion-check',
                       choices=['promise', 'file_movement', 'folder_empty'],
                       default='file_movement',
                       help='How to check for completion')

    args = parser.parse_args()

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"Error: Vault not found: {vault_path}")
        sys.exit(1)

    state = start_ralph_loop(
        vault_path=vault_path,
        task_prompt=args.task,
        max_iterations=args.max_iterations,
        completion_check=args.completion_check
    )

    print("\n✅ Ralph loop initialized!")
    sys.exit(0)

if __name__ == '__main__':
    main()
