#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import os
import sys
from pathlib import Path

# Cache de detecção (60 segundos)
_cache = {"type": None, "timestamp": 0}

PROJECT_DETECTORS = {
    "nodejs": ["package.json"],
    "python": ["requirements.txt", "pyproject.toml", "setup.py", "setup.cfg", "Pipfile"],
    "rust": ["Cargo.toml"],
    "go": ["go.mod"],
    "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
    "dotnet": ["*.csproj", "*.fsproj", "*.vbproj"],
    "ruby": ["Gemfile"],
}

HOOKS_BY_TYPE = {
    "nodejs": ["eslint", "prettier", "tsc"],
    "python": ["ruff", "mypy", "pylint"],
    "rust": ["cargo-check", "cargo-clippy"],
    "go": ["go-vet", "go-fmt"],
    "java": ["mvn-test", "gradle-test"],
    "dotnet": ["dotnet-build"],
    "default": ["basic-check"],
}


def detect_project_type():
    """Detect project type from files in current directory."""
    now = os.times()[4]

    if _cache["type"] and (now - _cache["timestamp"]) < 60:
        return _cache["type"]

    cwd = Path.cwd()
    for proj_type, indicators in PROJECT_DETECTORS.items():
        for indicator in indicators:
            if (cwd / indicator).exists():
                _cache["type"] = proj_type
                _cache["timestamp"] = now
                return proj_type

    _cache["type"] = "default"
    _cache["timestamp"] = now
    return "default"


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--detect":
        print(detect_project_type())
    else:
        input_data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
        proj_type = detect_project_type()
        print(json.dumps({"project_type": proj_type}))

    sys.exit(0)


if __name__ == "__main__":
    main()
