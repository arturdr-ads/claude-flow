#!/usr/bin/env python3
"""
Plan Persistence Hook
Salva e recupera planos do modo /plan do Claude Code
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

PLAN_DIR = Path.home() / ".cache" / "claude-plans"
CURRENT_PLAN_FILE = PLAN_DIR / "current_plan.md"
PLAN_INDEX = PLAN_DIR / "index.json"


def ensure_plan_dir():
    """Garante que o diretório de planos existe"""
    PLAN_DIR.mkdir(parents=True, exist_ok=True)
    if not PLAN_INDEX.exists():
        PLAN_INDEX.write_text(json.dumps({"plans": []}))


def save_plan(plan_content: str, metadata: dict = None):
    """Salva o plano atual"""
    ensure_plan_dir()

    timestamp = datetime.now().isoformat()
    plan_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Salvar plano individual
    plan_file = PLAN_DIR / f"plan_{plan_id}.md"
    plan_file.write_text(plan_content)

    # Atualizar índice
    index = json.loads(PLAN_INDEX.read_text())
    index["plans"].insert(0, {
        "id": plan_id,
        "file": str(plan_file),
        "created_at": timestamp,
        "metadata": metadata or {}
    })
    # Manter apenas últimos 20 planos
    index["plans"] = index["plans"][:20]
    PLAN_INDEX.write_text(json.dumps(index, indent=2))

    # Atualizar plano atual
    CURRENT_PLAN_FILE.write_text(plan_content)

    print(f"✅ Plano salvo: {plan_file}")
    return plan_id


def load_latest_plan():
    """Carrega o plano mais recente"""
    ensure_plan_dir()

    if CURRENT_PLAN_FILE.exists():
        content = CURRENT_PLAN_FILE.read_text()
        print(f"📋 Plano carregado de {CURRENT_PLAN_FILE}")
        return content

    index = json.loads(PLAN_INDEX.read_text())
    if index["plans"]:
        latest = index["plans"][0]
        content = Path(latest["file"]).read_text()
        print(f"📋 Plano carregado: {latest['file']}")
        return content

    return None


def list_plans():
    """Lista todos os planos salvos"""
    ensure_plan_dir()

    index = json.loads(PLAN_INDEX.read_text())
    if not index["plans"]:
        print("📭 Nenhum plano salvo")
        return

    print(f"\n📋 Planos salvos ({len(index['plans'])}):\n")
    for i, plan in enumerate(index["plans"], 1):
        created = plan["created_at"][:19].replace("T", " ")
        metadata = plan.get("metadata", {})
        title = metadata.get("title", f"Plano #{plan['id']}")
        print(f"  {i}. {title}")
        print(f"     Criado: {created}")
        print(f"     ID: {plan['id']}")
        print()


def main():
    args = sys.argv[1:]

    if not args or args[0] == "--help":
        print("""
Plan Persistence Hook - Uso:

  plan_persistence.py save [--title="<título>"] [--project="<projeto>"]
      Salva o plano atual do stdin

  plan_persistence.py load
      Carrega o plano mais recente

  plan_persistence.py list
      Lista todos os planos salvos

  plan_persistence.py clear
      Limpa o plano atual
        """)
        return

    command = args[0]

    if command == "save":
        content = sys.stdin.read()
        metadata = {}
        for i, arg in enumerate(args[1:], 1):
            if arg.startswith("--title="):
                metadata["title"] = arg.split("=", 1)[1].strip('"')
            elif arg.startswith("--project="):
                metadata["project"] = arg.split("=", 1)[1].strip('"')
        save_plan(content, metadata)

    elif command == "load":
        plan = load_latest_plan()
        if plan:
            print(plan)

    elif command == "list":
        list_plans()

    elif command == "clear":
        if CURRENT_PLAN_FILE.exists():
            CURRENT_PLAN_FILE.unlink()
            print("🗑️  Plano atual limpo")


if __name__ == "__main__":
    main()
