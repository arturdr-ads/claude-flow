#!/bin/bash
# Plan Mode - Aliases Convenientes

# Cache directory
PLAN_CACHE="$HOME/.cache/claude-plans"
mkdir -p "$PLAN_CACHE"

case "$1" in
  ls|list)
    python3 .claude/hooks/plan_persistence.py list
    ;;
  load)
    python3 .claude/hooks/plan_persistence.py load
    ;;
  save)
    shift
    python3 .claude/hooks/plan_persistence.py save "$@"
    ;;
  checkpoint|cp)
    python3 .claude/hooks/plan_checkpoint.py create
    ;;
  restore)
    python3 .claude/hooks/plan_checkpoint.py restore
    ;;
  tasks)
    python3 .claude/hooks/plan_to_tasks.py "$@"
    ;;
  clean)
    rm -f "$PLAN_CACHE/current_plan.md"
    echo "🗑️  Plano atual limpo"
    ;;
  *)
    echo "Plan Mode - Comandos disponíveis:"
    echo ""
    echo "  plan ls          Listar planos salvos"
    echo "  plan load       Carregar último plano"
    echo "  plan save       Salvar plano atual"
    echo "  plan cp         Criar checkpoint git"
    echo "  plan restore    Restaurar checkpoint"
    echo "  plan tasks      Converter plano em tarefas"
    echo "  plan clean      Limpar plano atual"
    echo ""
    echo "Exemplos:"
    echo "  plan save --title='Feature Auth'"
    echo "  plan tasks --preview"
    ;;
esac
