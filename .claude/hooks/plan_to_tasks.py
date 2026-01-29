#!/usr/bin/env python3
"""
Plan to Tasks Hook
Converte planos do /plan em tarefas nativas do Claude Code
"""
import sys
import re
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "claude-plans"
CURRENT_PLAN = CACHE_DIR / "current_plan.md"


def extract_tasks_from_plan(plan_content: str) -> list:
    """Extrai tarefas de um plano formatado"""
    tasks = []
    current_section = None
    task_id = 1

    lines = plan_content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Identificar seção principal
        if line.startswith("###") and not line.startswith("####"):
            current_section = line.strip("# ").strip()
            i += 1
            continue

        # Identificar item de checkbox
        if line.strip().startswith("- [ ]"):
            task_text = line.replace("- [ ]", "").strip()
            indent = len(line) - len(line.lstrip())

            # Extrair descrição de subtarefas (próximas linhas com maior indent)
            description = ""
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                if next_line.strip().startswith("- [") or next_line.startswith("###"):
                    break
                if next_line.strip():
                    description += next_line.strip() + "\n"
                j += 1

            # Verificar se há referência de arquivo
            file_ref = ""
            if "`" in task_text:
                refs = re.findall(r'`([^`]+)`', task_text)
                if refs:
                    file_ref = f" (arquivo: {refs[0]})"

            tasks.append({
                "id": task_id,
                "section": current_section or "Geral",
                "text": task_text + file_ref,
                "description": description.strip() or None,
                "indent": indent
            })
            task_id += 1

        i += 1

    return tasks


def generate_task_create_commands(tasks: list) -> str:
    """Gera comandos TaskCreate Claude Code"""
    if not tasks:
        return "# Nenhuma tarefa encontrada no plano\n"

    output = ["# Tarefas Extraídas do Plano\n"]
    output.append(f"# Total: {len(tasks)} tarefas\n")
    output.append("# Copie os comandos abaixo para criar as tarefas:\n\n")

    for task in tasks:
        section = task["section"]
        text = task["text"]
        desc = task["description"] or ""

        # Formatar para TaskCreate
        active_form = text[:50].replace("...", "").strip()
        if len(text) > 50:
            active_form = active_form[:47] + "..."

        output.append(f"# [{section}]")
        output.append(f"# {text}")
        output.append(f'TaskCreate "{{"subject": "{text}", "description": "{desc}", "activeForm": "{active_form}}}"')
        output.append("")

    return "\n".join(output)


def main():
    args = sys.argv[1:]

    if not args or args[0] == "--help":
        print("""
Plan to Tasks Hook - Uso:

  plan_to_tasks.py
      Extrai tarefas do plano atual e gera comandos TaskCreate

  plan_to_tasks.py --preview
      Apenas mostra as tarefas sem gerar comandos
        """)
        return

    if not CURRENT_PLAN.exists():
        print("❌ Nenhum plano encontrado. Use /plan primeiro.")
        return

    plan_content = CURRENT_PLAN.read_text()
    tasks = extract_tasks_from_plan(plan_content)

    if "--preview" in args:
        print(f"\n📋 {len(tasks)} tarefas encontradas:\n")
        for task in tasks:
            indent = "  " * (task["indent"] // 2)
            print(f"{indent}- [{task['id']}] {task['text']}")
            if task["description"]:
                for line in task["description"].split("\n"):
                    if line.strip():
                        print(f"{indent}    {line}")
        print()
    else:
        print(generate_task_create_commands(tasks))


if __name__ == "__main__":
    main()
