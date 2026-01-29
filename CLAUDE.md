# Claude Code Config - Contexto do Projeto

> **Descrição**: Repositório de configuração personalizada do Claude Code CLI com agentes especializados, hooks adaptativos e automações.

## Visão Geral

Este é um **ecossistema de automação** para o Claude Code CLI que inclui:
- 20+ agentes especializados por tecnologia
- Sistema de hooks adaptativos para validação automática
- Comandos personalizados para workflows comuns
- Sistema de planejamento com persistência e checkpoints
- Status line customizado com informações úteis

## Estrutura do Projeto

```
.claude/
├── agents/              # Agentes especializados (Task tool)
├── commands/            # Comandos personalizados (/command)
├── hooks/               # Hooks de automação (eventos)
├── status_lines/        # Scripts de status line
├── templates/           # Templates de documentos
└── settings.json        # Configuração principal
```

## Instalação

```bash
./setup-claude.sh install
```

## Principais Funcionalidades

### 1. Agentes Especializados
Use o agente apropriado para cada tecnologia:

| Área | Agente | Quando Usar |
|------|--------|-------------|
| Frontend | `frontend-expert` | React, Vue, Svelte, CSS, acessibilidade |
| Backend | `backend-expert` | Node.js, Python, Go, APIs |
| Database | `database-expert` | PostgreSQL, MongoDB, queries |
| DevOps | `devops-expert` | Docker, CI/CD, GitHub Actions |
| Cloud | `cloud-expert` | AWS, GCP, Azure |
| Security | `security-expert` | OWASP, pentest, hardening |
| Mobile | `mobile-expert` | React Native, Flutter |
| Desktop | `desktop-expert` | Electron, Tauri |
| TypeScript | `typescript-expert` | Tipos, generics, build |
| Testing | `testing-expert` | Jest, Vitest, Playwright |

### 2. Comandos Personalizados

```bash
# Git
/commit          # Criar commit com estilo do projeto
/status          # Análise inteligente do git status
/push            # Push com safety checks
/checkout        # Branch creation com naming convencional

# Checkpoints
/checkpoint:create    # Criar checkpoint git
/checkpoint:list      # Listar checkpoints
/checkpoint:restore   # Restaurar checkpoint

# Código
/code-review     # Code review multi-aspect
/research        # Deep research com citações
/validate-and-fix # Quality checks + auto-fix
```

### 3. Hooks Adaptativos

O sistema detecta automaticamente o tipo de projeto e executa validações apropriadas:

- **Node.js**: eslint, prettier, tsc
- **Python**: ruff, mypy, pylint
- **Rust**: cargo-check, cargo-clippy
- **Go**: go-vet, go-fmt

### 4. Sistema de Planejamento

```bash
# Criar plano persistente
python3 .claude/hooks/plan_persistence.py save --title="Feature X"

# Listar planos
python3 .claude/hooks/plan_persistence.py list

# Criar checkpoint antes de implementar
python3 .claude/hooks/plan_checkpoint.py create
```

## Variáveis de Ambiente

```bash
# .env.local
ANTHROPIC_API_KEY=sk-ant-xxx
ELEVENLABS_API_KEY=xxx      # Opcional - TTS
OPENAI_API_KEY=xxx          # Opcional - TTS
ENGINEER_NAME=SeuNome       # Opcional - TTS
```

## Workflow Recomendado

```
1. /plan → Criar plano detalhado
2. checkpoint:create → Salvar estado atual
3. Implementar com agentes especializados
4. /validate-and-fix → Quality check
5. /commit → Commit com mensagem apropriada
```

## Manutenção

```bash
# Atualizar configuração
./setup-claude.sh update

# Verificar status
./setup-claude.sh status

# Ver agentes disponíveis
ls -1 .claude/agents/**/*.md
```

## Documentação Adicional

- `.claude/PLAN_MODE.md` - Sistema de planejamento
- `.claude/WORKFLOW_AUTOMATION.md` - Detalhes dos hooks
- `.claude/COVERAGE_MATRIX.md` - Matriz de cobertura de agentes

## Notas para o Claude

**Sempre que trabalhar neste repositório:**
1. Usar português para comunicações
2. Manter estrutura consistente
3. Documentar novas funcionalidades
4. Testar hooks após modificações
5. Atualizar COVERAGE_MATRIX.md ao adicionar agentes

**Hooks críticos:**
- `adaptive/adaptive_hooks.py` - Detecção automática de projeto
- `plan_persistence.py` - Persistência de planos
- `plan_checkpoint.py` - Checkpoints git
- `status_line_v3.py` - Status line customizado
