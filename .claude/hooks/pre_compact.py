#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import argparse
import json
import shutil
import sys
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def log_pre_compact(input_data):
    """Log pre-compact event to logs directory."""
    log_file = Path("logs/pre_compact.json")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Read existing log data or initialize empty list
    try:
        if log_file.exists():
            with open(log_file, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = []
    except (json.JSONDecodeError, ValueError):
        log_data = []

    # Append and write back
    log_data.append(input_data)
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)


def backup_transcript(transcript_path, trigger):
    """Create a backup of the transcript before compaction."""
    try:
        transcript_path = Path(transcript_path)
        if not transcript_path.exists():
            return None

        # Create backup directory and generate backup filename
        backup_dir = Path("logs/transcript_backups")
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{transcript_path.stem}_pre_compact_{trigger}_{timestamp}.jsonl"

        # Copy transcript to backup
        shutil.copy2(transcript_path, backup_path)
        return str(backup_path)
    except Exception:
        return None


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--backup', action='store_true',
                          help='Create backup of transcript before compaction')
        parser.add_argument('--verbose', action='store_true',
                          help='Print verbose output')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Extract fields
        session_id = input_data.get('session_id', 'unknown')
        transcript_path = input_data.get('transcript_path', '')
        trigger = input_data.get('trigger', 'unknown')  # "manual" or "auto"
        custom_instructions = input_data.get('custom_instructions', '')
        
        # Log the pre-compact event
        log_pre_compact(input_data)
        
        # Create backup if requested
        backup_path = None
        if args.backup and transcript_path:
            backup_path = backup_transcript(transcript_path, trigger)
        
        # Provide feedback based on trigger type
        if args.verbose:
            if trigger == "manual":
                message = f"Preparing for manual compaction (session: {session_id[:8]}...)"
                if custom_instructions:
                    message += f"\nCustom instructions: {custom_instructions[:100]}..."
            else:  # auto
                message = f"Auto-compaction triggered due to full context window (session: {session_id[:8]}...)"
            
            if backup_path:
                message += f"\nTranscript backed up to: {backup_path}"
            
            print(message)
        
        # Success - compaction will proceed
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)


if __name__ == '__main__':
    main()