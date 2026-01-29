#!/usr/bin/env python3
"""
Plan Checkpoint Hook
Cria checkpoints antes de executar planos
"""
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

CACHE_DIR = Path.home() / ".cache" / "claude-plans"
CHECKPOINT_FILE = CACHE_DIR / "checkpoint.json"


def create_checkpoint():
    """Cria um checkpoint git antes de executar"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Verificar se estamos em um repo git
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("⚠️  Não está em um repositório git")
            return None
    except FileNotFoundError:
        print("⚠️  Git não encontrado")
        return None

    # Obter estado atual
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    ).stdout

    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True
    ).stdout.strip()

    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True
    ).stdout.strip()

    has_changes = bool(status.strip())

    checkpoint = {
        "timestamp": datetime.now().isoformat(),
        "branch": branch,
        "commit": commit,
        "has_changes": has_changes,
        "status": status
    }

    CHECKPOINT_FILE.write_text(json.dumps(checkpoint, indent=2))

    if has_changes:
        print(f"📌 Checkpoint criado:")
        print(f"   Branch: {branch}")
        print(f"   Commit: {commit[:8]}")
        print(f"   ⚠️  Há mudanças não commitadas")
    else:
        print(f"📌 Checkpoint criado:")
        print(f"   Branch: {branch}")
        print(f"   Commit: {commit[:8]}")
        print(f"   ✅ Estado limpo")

    return checkpoint


def restore_checkpoint():
    """Restaura para o checkpoint"""
    if not CHECKPOINT_FILE.exists():
        print("❌ Nenhum checkpoint encontrado")
        return

    checkpoint = json.loads(CHECKPOINT_FILE.read_text())

    print(f"📌 Restaurando checkpoint:")
    print(f"   Branch: {checkpoint['branch']}")
    print(f"   Commit: {checkpoint['commit'][:8]}")

    # Reset para o commit
    subprocess.run(
        ["git", "reset", "--hard", checkpoint["commit"]],
        capture_output=True
    )

    print(f"   ✅ Restaurado")


def show_checkpoint():
    """Mostra informações do checkpoint"""
    if not CHECKPOINT_FILE.exists():
        print("📭 Nenhum checkpoint salvo")
        return

    checkpoint = json.loads(CHECKPOINT_FILE.read_text())
    timestamp = checkpoint["timestamp"][:19].replace("T", " ")

    print(f"\n📌 Checkpoint atual:")
    print(f"   Criado: {timestamp}")
    print(f"   Branch: {checkpoint['branch']}")
    print(f"   Commit: {checkpoint['commit'][:8]}")
    print(f"   Mudanças: {'Sim' if checkpoint['has_changes'] else 'Não'}")


def main():
    args = sys.argv[1:]

    if not args or args[0] == "--help":
        print("""
Plan Checkpoint Hook - Uso:

  plan_checkpoint.py create
      Cria um checkpoint do estado atual

  plan_checkpoint.py restore
      Restaura para o checkpoint salvo

  plan_checkpoint.py show
      Mostra informações do checkpoint
        """)
        return

    command = args[0]

    if command == "create":
        create_checkpoint()
    elif command == "restore":
        restore_checkpoint()
    elif command == "show":
        show_checkpoint()


if __name__ == "__main__":
    main()
