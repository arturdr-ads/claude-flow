# Workflow e Automação - Claude Code CLI Modificado

## 📋 CICLO DE VIDA COMPLETO DO CLAUDE CODE CLI

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SESSÃO CLAUDE CODE                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. SESSION START                                                   │
│     ├─ Carrega settings.json                                       │
│     ├─ Carrega agentes (.claude/agents/)                           │
│     ├─ Carrega comandos (.claude/commands/)                        │
│     ├─ Executa hooks SessionStart                                  │
│     └─ Inicializa MCP servers                                      │
│                                                                     │
│  2. USER PROMPT SUBMIT                                              │
│     ├─ Usuário envia prompt                                        │
│     ├─ Executa hooks UserPromptSubmit                              │
│     │  └─ thinking-level (injeção de megathink)                   │
│     └─ Analisa intenção + escolhe agentes                          │
│                                                                     │
│  3. TOOL USE (Loop)                                                 │
│     ├─ PRE TOOL USE                                                │
│     │  └─ file-guard (valida arquivos sensíveis)                   │
│     │                                                               │
│     ├─ EXECUÇÃO DA FERRAMENTA                                      │
│     │  └─ Read, Edit, Write, Bash, etc.                           │
│     │                                                               │
│     └─ POST TOOL USE                                               │
│        ├─ adaptive_hooks (detecta tipo de projeto)                 │
│        ├─ lint-changed                                             │
│        ├─ typecheck-changed                                        │
│        ├─ check-comment-replacement (Edit apenas)                  │
│        └─ check-unused-parameters (Edit apenas)                    │
│                                                                     │
│  4. STOP                                                            │
│     ├─ Executa hooks Stop                                          │
│     │  ├─ create-checkpoint (git auto-checkpoint)                 │
│     │  └─ check-todos                                              │
│     ├─ Salva transcrição                                           │
│     └─ Encerra sessão                                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 HOOKS DISPONÍVEIS E ORDEM DE EXECUÇÃO

| Hook | Quando Executa | Uso Típico |
|------|----------------|------------|
| **SessionStart** | Início da sessão | Carregar contexto, setup |
| **UserPromptSubmit** | Antes de enviar prompt | thinking-level, codebase-map |
| **PreToolUse** | Antes de qualquer ferramenta | Validação, segurança |
| **PostToolUse** | Depois de Write/Edit | Lint, typecheck, testes |
| **SubagentStart** | Início de subagente | Setup específico |
| **SubagentStop** | Fim de subagente | Cleanup |
| **Stop** | Fim da sessão | Checkpoint, validações |
| **PreCompact** | Antes de compactar | Backup |
| **Notification** | Notificações | TTS, alerts |

---

## 🤖 SISTEMA DE AGENTES

### Agentes por Categoria (42 totais)

```
FRONTEND (4)
├── react-expert
├── react-performance-expert
├── css-styling-expert
└── accessibility-expert

FRAMEWORK (1)
└── nextjs-expert

BACKEND (2)
├── nodejs-expert
└── nestjs-expert

DATABASE (3)
├── postgres-expert
├── mongodb-expert
└── database-expert

DEVOPS/INFRA (3)
├── docker-expert
├── github-actions-expert
└── devops-expert

VPS/SERVIDOR (1) 🆕
└── vps-expert

SECURITY (1) 🆕
└── security-expert

MONITORING (1) 🆕
└── monitoring-expert

CLOUD (1) 🆕
└── cloud-expert

MOBILE (1) 🆕
└── mobile-expert

DESKTOP (1) 🆕
└── desktop-expert

BUILD TOOLS (2)
├── vite-expert
└── webpack-expert

TESTING (4)
├── testing-expert
├── jest-testing-expert
├── vitest-testing-expert
└── playwright-expert

TYPESCRIPT (3)
├── typescript-expert
├── typescript-build-expert
└── typescript-type-expert

OUTROS (14)
├── git-expert
├── refactoring-expert
├── cli-expert
├── ai-sdk-expert
├── research-expert
├── kafka-expert
├── loopback-expert
├── code-review-expert
├── triage-expert
├── documentation-expert
├── code-search
├── linting-expert
└── meta-agent
```

---

## 🔄 HOOKS ADAPTATIVOS

### Sistema de Detecção Automática

```bash
.claude/hooks/adaptive/adaptive_hooks.py
```

**Detecta automaticamente:**
- `package.json` → Node.js (eslint, prettier, tsc)
- `requirements.txt`/`pyproject.toml` → Python (ruff, mypy, pylint)
- `Cargo.toml` → Rust (cargo-check, cargo-clippy)
- `go.mod` → Go (go-vet, go-fmt)
- `pom.xml`/`build.gradle` → Java (mvn/gradle test)
- `*.csproj` → .NET (dotnet-build)

**Cache inteligente:** 60 segundos para evitar re-deteção.

---

## 📦 AUTOMATIZAÇÃO - SCRIPT DE SETUP

### Script de Instalação Automática

```bash
#!/bin/bash
# setup-claude.sh - Instalação automática do sistema Claude Code CLI

set -e

CLAUDE_DIR="$HOME/.claude"
CONFIG_REPO="https://github.com/seu-usuario/claude-config.git"
CONFIG_DIR="$HOME/claude-config"

echo "🚀 Configurando Claude Code CLI..."

# 1. Clona repositório de configuração
if [ ! -d "$CONFIG_DIR" ]; then
    git clone "$CONFIG_REPO" "$CONFIG_DIR"
else
    cd "$CONFIG_DIR" && git pull
fi

# 2. Cria diretórios
mkdir -p "$CLAUDE_DIR/agents"
mkdir -p "$CLAUDE_DIR/hooks"
mkdir -p "$CLAUDE_DIR/commands"

# 3. Copia configurações
cp "$CONFIG_DIR/.claude/settings.json" "$CLAUDE_DIR/settings.json"
cp -r "$CONFIG_DIR/.claude/agents/"* "$CLAUDE_DIR/agents/"
cp -r "$CONFIG_DIR/.claude/hooks/"* "$CLAUDE_DIR/hooks/"
cp -r "$CONFIG_DIR/.claude/commands/"* "$CLAUDE_DIR/commands/"

# 4. Instala dependências
if command -v uv &> /dev/null; then
    echo "✅ uv já instalado"
else
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# 5. Instala claudekit-hooks
if command -v claudekit-hooks &> /dev/null; then
    echo "✅ claudekit-hooks já instalado"
else
    npm install -g claudekit-hooks
fi

# 6. Configura ambiente local
cat > "$CLAUDE_DIR/settings.local.json" << EOF
{
  "outputStyle": "default",
  "tts": {
    "enabled": false
  }
}
EOF

echo "✅ Claude Code CLI configurado com sucesso!"
echo "📁 Configuração em: $CLAUDE_DIR"
echo "🔄 Para atualizar: cd $CONFIG_DIR && git pull"
```

---

## 🎯 DISTRIBUIÇÃO VIA NPM PACKAGE

### package.json para distribuição

```json
{
  "name": "@seu-usuario/claude-config",
  "version": "1.0.0",
  "description": "Configuração completa do Claude Code CLI",
  "files": [
    ".claude/**/*"
  ],
  "scripts": {
    "install": "node scripts/install.js",
    "postinstall": "bash scripts/postinstall.sh"
  }
}
```

### Script de instalação (scripts/install.js)

```javascript
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const claudeDir = path.join(process.env.HOME, '.claude');
const pkgDir = __dirname;

// Copia agentes
fs.cpSync(
  path.join(pkgDir, '.claude', 'agents'),
  path.join(claudeDir, 'agents'),
  { recursive: true }
);

// Copia hooks
fs.cpSync(
  path.join(pkgDir, '.claude', 'hooks'),
  path.join(claudeDir, 'hooks'),
  { recursive: true }
);

// Copia settings
fs.copyFileSync(
  path.join(pkgDir, '.claude', 'settings.json'),
  path.join(claudeDir, 'settings.json')
);

console.log('✅ Claude Code CLI configurado!');
```

---

## 🔑 VARIÁVEIS DE AMBIENTE

### .env.example

```bash
# Claude API
ANTHROPIC_API_KEY=sk-ant-xxx
ANTHROPIC_BASE_URL=https://api.anthropic.com

# TTS (opcional)
ELEVENLABS_API_KEY=xxx
OPENAI_API_KEY=xxx
ENGINEER_NAME=SeuNome

# Hooks
CLAUDE_HOOKS_TIMEOUT=30000
CLAUDE_HOOKS_DEBUG=false
```

---

## 📊 ESTRUTURA FINAL DO PROJETO

```
claude-config/
├── .claude/
│   ├── settings.json              # Configuração principal
│   ├── settings.local.json        # Override local (gitignore)
│   ├── agents/                    # 42 agentes especializados
│   │   ├── vps-expert.md         🆕
│   │   ├── security-expert.md    🆕
│   │   ├── monitoring-expert.md  🆕
│   │   ├── cloud-expert.md       🆕
│   │   ├── mobile-expert.md      🆕
│   │   └── desktop-expert.md     🆕
│   ├── commands/                  # Comandos personalizados
│   ├── hooks/
│   │   └── adaptive/
│   │       └── adaptive_hooks.py # Detecção automática
│   └── status_lines/
│       └── status_line_v3.py     # Status line com cache
├── setup-claude.sh                # Script de instalação
├── package.json                  # Distribuição NPM
├── .env.example                  # Variáveis de ambiente
└── README.md                     # Documentação
```

---

## 🚀 COMANDOS ÚTEIS

```bash
# Instalar/Atualizar
./setup-claude.sh

# Ver tipo de projeto detectado
uv run .claude/hooks/adaptive/adaptive_hooks.py --detect

# Listar hooks disponíveis
claudekit-hooks list

# Ver agentes disponíveis
ls -1 .claude/agents/**/*.md

# Testar configuração
cat .claude/settings.json | jq .
```

---

## 📝 MELHORES PRÁTICAS

1. **Versionar tudo** no Git (exceto settings.local.json)
2. **Usar settings.local.json** para configurações sensíveis
3. **Manter agentes focados** - um especialista por área
4. **Hooks com timeout** para evitar bloqueios
5. **Cache em hooks** para performance
6. **Documentar cada agente** com metadata YAML

---

**Sistema 100% funcional e automatizável!** 🎉
