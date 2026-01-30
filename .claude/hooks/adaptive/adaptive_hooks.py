#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Cache de detecção (60 segundos)
_cache = {"type": None, "timestamp": 0}

# OTIMIZAÇÃO: Debounce de validações (5 segundos)
_last_validation = {"timestamp": 0, "result": None}
DEBOUNCE_SECONDS = 5

PROJECT_DETECTORS = {
    "nodejs": ["package.json"],
    "python": ["requirements.txt", "pyproject.toml", "setup.py", "setup.cfg", "Pipfile"],
    "rust": ["Cargo.toml"],
    "go": ["go.mod"],
    "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
    "dotnet": ["*.csproj", "*.fsproj", "*.vbproj"],
    "ruby": ["Gemfile"],
}

# Comandos de validação por tipo de projeto
VALIDATIONS = {
    "nodejs": [
        ["npx", "eslint", "--cache", "."],
        ["npx", "prettier", "--check", "."],
        ["npx", "tsc", "--noEmit"],
    ],
    "python": [
        ["ruff", "check", "."],
        ["mypy", "."],
        ["pylint", "."],
    ],
    "rust": [
        ["cargo", "check"],
        ["cargo", "clippy", "--", "-D", "warnings"],
    ],
    "go": [
        ["go", "vet", "./..."],
        ["go", "fmt", "./..."],
    ],
    "java": [
        ["mvn", "test"],
    ],
    "dotnet": [
        ["dotnet", "build"],
    ],
}


def detect_project_type() -> str:
    """Detect project type from files in current directory."""
    now = os.times()[4]

    if _cache["type"] and (now - _cache["timestamp"]) < 60:
        return _cache["type"]

    cwd = Path.cwd()
    for proj_type, indicators in PROJECT_DETECTORS.items():
        for indicator in indicators:
            if "*" in indicator:
                # Glob pattern para .csproj, etc.
                if list(cwd.glob(indicator)):
                    _cache["type"] = proj_type
                    _cache["timestamp"] = now
                    return proj_type
            elif (cwd / indicator).exists():
                _cache["type"] = proj_type
                _cache["timestamp"] = now
                return proj_type

    _cache["type"] = "default"
    _cache["timestamp"] = now
    return "default"


def run_validations(project_type: str, timeout: int = 30) -> dict:
    """
    Executa as validações para o tipo de projeto detectado.
    OTIMIZADO: Debounce de 5 segundos para evitar validações excessivas.

    Args:
        project_type: Tipo de projeto detectado
        timeout: Timeout em segundos para cada validação

    Returns:
        Dict com resultados das validações executadas
    """
    global _last_validation

    # OTIMIZAÇÃO: Debounce - retorna cache se validou recentemente
    import time
    now = time.time()
    if _last_validation["result"] and (now - _last_validation["timestamp"]) < DEBOUNCE_SECONDS:
        return _last_validation["result"]

    results = []
    commands = VALIDATIONS.get(project_type, [])

    if not commands:
        return {
            "project_type": project_type,
            "validations": [],
            "message": f"No validations configured for project type: {project_type}"
        }

    for cmd in commands:
        cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=Path.cwd()
            )
            results.append({
                "command": cmd_str,
                "success": result.returncode == 0,
                "exit_code": result.returncode,
                "output": result.stdout[-1000:] if result.stdout else "",  # Últimos 1000 chars
                "error": result.stderr[-1000:] if result.stderr else "",
            })
        except subprocess.TimeoutExpired:
            results.append({
                "command": cmd_str,
                "success": False,
                "error": f"Timeout after {timeout}s",
            })
        except FileNotFoundError:
            results.append({
                "command": cmd_str,
                "success": False,
                "error": "Command not found (tool not installed)",
            })
        except Exception as e:
            results.append({
                "command": cmd_str,
                "success": False,
                "error": str(e),
            })

    # OTIMIZAÇÃO: Atualiza cache de debounce
    _last_validation["timestamp"] = now
    _last_validation["result"] = output

    return output


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--detect":
            print(detect_project_type())
            sys.exit(0)
        elif sys.argv[1] == "--validate":
            proj_type = detect_project_type()
            result = run_validations(proj_type)
            print(json.dumps(result, indent=2))
            sys.exit(0)

    # Modo hook: lê stdin e retorna tipo + validações
    input_data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    proj_type = detect_project_type()

    # Executa validações apenas se solicitado via input ou se detectado projeto
    should_validate = input_data.get("run_validations", False)

    if should_validate:
        output = run_validations(proj_type)
    else:
        output = {"project_type": proj_type}

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
