#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import json
import sys
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


# Cache session paths - avoid recomputing on every call
_CLAUDE_HOME = Path.home() / ".claude" / "projects"
_CURRENT_DIR = Path.cwd()
_CACHED_SESSION_PATHS = [
    _CLAUDE_HOME / f"-home-arturdr-Claude" / "{{session_id}}.jsonl",
    _CLAUDE_HOME / f"-{_CURRENT_DIR.as_posix().replace('/', '-')}" / "{{session_id}}.jsonl",
    Path(".claude/data/sessions") / "{{session_id}}.json",
    Path(".claude/sessions") / "{{session_id}}.json",
]


def log_status_line(input_data, status_line_output, error_message=None):
    """Log status line event to logs directory."""
    log_file = Path("logs/status_line.json")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Read existing log data or initialize empty list
    if log_file.exists():
        try:
            with open(log_file, "r") as f:
                log_data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            log_data = []
    else:
        log_data = []

    # Create log entry and append
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "version": "v3",
        "input_data": input_data,
        "status_line_output": status_line_output,
    }
    if error_message:
        log_entry["error"] = error_message
    log_data.append(log_entry)

    # Write back to file
    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=2)


def get_session_data(session_id):
    """Get session data including agent name and prompts."""
    # Build session file paths from cached templates
    for path_template in _CACHED_SESSION_PATHS:
        session_file = Path(str(path_template).replace("{session_id}", session_id))
        if session_file.exists():
            try:
                if session_file.suffix == ".jsonl":
                    # Read last valid JSON line efficiently
                    with open(session_file, "r") as f:
                        for line in reversed(f.readlines()):
                            line = line.strip()
                            if line:
                                try:
                                    session_data = json.loads(line)
                                    return {
                                        "agent_name": session_data.get("agentName", "Claude"),
                                        "prompts": session_data.get("prompts", [])
                                    }, None
                                except json.JSONDecodeError:
                                    continue
                    return None, "No valid session data found in JSONL"
                else:
                    with open(session_file, "r") as f:
                        return json.load(f), None
            except Exception as e:
                return None, f"Error reading session file: {str(e)}"

    return None, "Session file not found in any location"


def truncate_prompt(prompt, max_length=75):
    """Truncate prompt to specified length."""
    # Remove newlines and excessive whitespace
    prompt = " ".join(prompt.split())

    if len(prompt) > max_length:
        return prompt[: max_length - 3] + "..."
    return prompt


def get_prompt_icon(prompt):
    """Get icon based on prompt type."""
    prompt_lower = prompt.lower()
    if prompt.startswith("/"):
        return "⚡"
    if "?" in prompt:
        return "❓"
    if any(word in prompt_lower for word in ("create", "write", "add", "implement", "build")):
        return "💡"
    if any(word in prompt_lower for word in ("fix", "debug", "error", "issue")):
        return "🐛"
    if any(word in prompt_lower for word in ("refactor", "improve", "optimize")):
        return "♻️"
    return "💬"


def generate_status_line(input_data):
    """Generate the status line with agent name and last 3 prompts."""
    session_id = input_data.get("session_id", "unknown")
    model_name = input_data.get("model", {}).get("display_name", "Claude")

    session_data, error = get_session_data(session_id)
    if error:
        log_status_line(input_data, f"[{model_name}] 💭 No session data", error)
        return f"\033[36m[{model_name}]\033[0m \033[90m💭 No session data\033[0m"

    agent_name = session_data.get("agent_name", "Agent")
    prompts = session_data.get("prompts", [])

    # Build status line components
    parts = [f"\033[91m[{agent_name}]\033[0m", f"\033[34m[{model_name}]\033[0m"]

    if prompts:
        current_prompt = prompts[-1]
        parts.append(f"{get_prompt_icon(current_prompt)} \033[97m{truncate_prompt(current_prompt, 75)}\033[0m")
        if len(prompts) > 1:
            parts.append(f"\033[90m{truncate_prompt(prompts[-2], 50)}\033[0m")
        if len(prompts) > 2:
            parts.append(f"\033[90m{truncate_prompt(prompts[-3], 40)}\033[0m")
    else:
        parts.append("\033[90m💭 No prompts yet\033[0m")

    return " | ".join(parts)


def main():
    try:
        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())

        # Generate status line
        status_line = generate_status_line(input_data)

        # Log the status line event (without error since it's successful)
        log_status_line(input_data, status_line)

        # Output the status line (first line of stdout becomes the status line)
        print(status_line)

        # Success
        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully - output basic status
        print("\033[31m[Agent] [Claude] 💭 JSON Error\033[0m")
        sys.exit(0)
    except Exception as e:
        # Handle any other errors gracefully - output basic status
        print(f"\033[31m[Agent] [Claude] 💭 Error: {str(e)}\033[0m")
        sys.exit(0)


if __name__ == "__main__":
    main()
