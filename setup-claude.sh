#!/bin/bash
# setup-claude.sh - Instalação/Atualização automática do Claude Code CLI Modificado
# Uso: ./setup-claude.sh [install|update|check|status]

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretórios
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
PROJECT_DIR="$SCRIPT_DIR/.claude"

# Funções de log
log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✅${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }

# Verificar dependências
check_dependencies() {
    log_info "Verificando dependências..."

    if command -v claude &> /dev/null; then
        log_success "Claude Code CLI instalado: $(claude --version 2>/dev/null | head -1)"
    else
        log_error "Claude Code CLI não encontrado!"
        log_info "Instale em: https://claude.ai/code"
        return 1
    fi

    if command -v uv &> /dev/null; then
        log_success "uv instalado: $(uv --version | head -1)"
    else
        log_warning "uv não encontrado, instalando..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi

    if command -v npm &> /dev/null; then
        log_success "npm instalado: $(npm --version)"
    else
        log_warning "npm não encontrado"
    fi

    if command -v claudekit-hooks &> /dev/null; then
        log_success "claudekit-hooks instalado: $(claudekit-hooks --version 2>/dev/null || echo 'unknown')"
    else
        log_warning "claudekit-hooks não encontrado, instalando..."
        npm install -g claudekit-hooks
    fi
}

# Copiar configurações
copy_configs() {
    log_info "Copiando configurações..."

    # Criar diretórios
    mkdir -p "$CLAUDE_DIR/agents"
    mkdir -p "$CLAUDE_DIR/hooks"
    mkdir -p "$CLAUDE_DIR/commands"
    mkdir -p "$CLAUDE_DIR/status_lines"

    # Copiar agentes
    if [ -d "$PROJECT_DIR/agents" ]; then
        cp -rn "$PROJECT_DIR/agents/"* "$CLAUDE_DIR/agents/" 2>/dev/null || true
        log_success "Agentes copiados: $(find "$CLAUDE_DIR/agents" -name "*.md" | wc -l) arquivos"
    fi

    # Copiar hooks
    if [ -d "$PROJECT_DIR/hooks" ]; then
        cp -rn "$PROJECT_DIR/hooks/"* "$CLAUDE_DIR/hooks/" 2>/dev/null || true
        log_success "Hooks copiados"
    fi

    # Copiar comandos
    if [ -d "$PROJECT_DIR/commands" ]; then
        cp -rn "$PROJECT_DIR/commands/"* "$CLAUDE_DIR/commands/" 2>/dev/null || true
        log_success "Comandos copiados: $(find "$CLAUDE_DIR/commands" -name "*.md" | wc -l) arquivos"
    fi

    # Copiar status line
    if [ -d "$PROJECT_DIR/status_lines" ]; then
        cp -rn "$PROJECT_DIR/status_lines/"* "$CLAUDE_DIR/status_lines/" 2>/dev/null || true
        log_success "Status line copiado"
    fi

    # Copiar settings.json (não sobrescrever se existe)
    if [ -f "$PROJECT_DIR/settings.json" ]; then
        if [ ! -f "$CLAUDE_DIR/settings.json" ]; then
            cp "$PROJECT_DIR/settings.json" "$CLAUDE_DIR/settings.json"
            log_success "settings.json criado"
        else
            log_info "settings.json já existe (preservado)"
        fi
    fi
}

# Criar settings.local.json
create_local_config() {
    if [ ! -f "$CLAUDE_DIR/settings.local.json" ]; then
        cat > "$CLAUDE_DIR/settings.local.json" << EOF
{
  "outputStyle": "default",
  "tts": {
    "enabled": false,
    "provider": "pyttsx3"
  }
}
EOF
        log_success "settings.local.json criado"
    fi
}

# Verificar instalação
check_installation() {
    log_info "Verificando instalação..."

    echo ""
    echo "📊 Estatísticas:"
    echo "   Agentes: $(find "$CLAUDE_DIR/agents" -name "*.md" 2>/dev/null | wc -l)"
    echo "   Comandos: $(find "$CLAUDE_DIR/commands" -name "*.md" 2>/dev/null | wc -l)"
    echo "   Hooks: $(find "$CLAUDE_DIR/hooks" -type f 2>/dev/null | wc -l)"
    echo ""

    # Testar detecção de projeto
    if [ -f "$PROJECT_DIR/hooks/adaptive/adaptive_hooks.py" ]; then
        PROJECT_TYPE=$(echo '{}' | uv run "$PROJECT_DIR/hooks/adaptive/adaptive_hooks.py" 2>/dev/null | jq -r '.project_type // "unknown"')
        log_success "Detecção de projeto: $PROJECT_TYPE"
    fi
}

# Comandos
case "${1:-install}" in
    install)
        echo -e "${BLUE}🚀 Instalando Claude Code CLI Modificado...${NC}"
        echo ""
        check_dependencies
        copy_configs
        create_local_config
        check_installation
        echo ""
        log_success "Instalação concluída!"
        ;;
    update)
        echo -e "${BLUE}🔄 Atualizando Claude Code CLI Modificado...${NC}"
        echo ""
        copy_configs
        check_installation
        echo ""
        log_success "Atualização concluída!"
        ;;
    check)
        check_installation
        ;;
    status)
        echo "📂 Diretório do projeto: $PROJECT_DIR"
        echo "📂 Diretório Claude: $CLAUDE_DIR"
        echo ""
        check_dependencies
        check_installation
        ;;
    *)
        echo "Uso: $0 [install|update|check|status]"
        exit 1
        ;;
esac
