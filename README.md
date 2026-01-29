# Claude Code Config

Configuração personalizada e ecossistema de automação para [Claude Code CLI](https://claude.ai/code).

## Visão Geral

Este repositório contém uma configuração completa para o Claude Code CLI, incluindo:

- 20+ agentes especializados por tecnologia
- Sistema de hooks adaptativos para validação automática
- Comandos personalizados para workflows comuns
- Sistema de planejamento com persistência e checkpoints
- Status line customizado com informações úteis

## Instalação Rápida

```bash
# Clonar e instalar
git clone <repo-url> ~/Claude
cd ~/Claude
./setup-claude.sh install
```

## Estrutura

```
.claude/
├── agents/              # Agentes especializados
├── commands/            # Comandos personalizados (/comando)
├── hooks/               # Hooks de automação
├── status_lines/        # Scripts de status line
├── templates/           # Templates (plan, PRD)
├── PLAN_MODE.md         # Doc do sistema de planejamento
├── WORKFLOW_AUTOMATION.md  # Doc dos hooks
└── COVERAGE_MATRIX.md   # Matriz de agentes
```

## Comandos Disponíveis

### Git
- `/commit` - Criar commit seguindo estilo do projeto
- `/status` - Análise inteligente do git status
- `/push` - Push com validações de segurança
- `/checkout` - Criação de branches com naming convencional

### Checkpoints
- `/checkpoint:create` - Criar checkpoint git
- `/checkpoint:list` - Listar checkpoints salvos
- `/checkpoint:restore` - Restaurar checkpoint anterior

### Código
- `/code-review` - Code review multi-aspect paralelo
- `/research` - Deep research com citações automáticas
- `/validate-and-fix` - Quality checks + auto-fix

### GitHub
- `/gh:repo-init` - Criar novo repositório com setup completo

### Dev
- `/dev:cleanup` - Limpar arquivos de debug e testes

## Hooks Adaptativos

O sistema detecta automaticamente o tipo de projeto e executa validações:

| Tipo | Detecção | Validações |
|------|----------|------------|
| Node.js | `package.json` | eslint, prettier, tsc |
| Python | `requirements.txt`, `pyproject.toml` | ruff, mypy, pylint |
| Rust | `Cargo.toml` | cargo-check, cargo-clippy |
| Go | `go.mod` | go-vet, go-fmt |
| Java | `pom.xml`, `build.gradle` | mvn/gradle test |

## Agentes Especializados

| Área | Agente |
|------|--------|
| Frontend | `frontend-expert`, `react-expert` |
| Backend | `backend-expert`, `nestjs-expert` |
| Database | `database-expert`, `postgres-expert`, `mongodb-expert` |
| DevOps | `devops-expert`, `cloud-expert` |
| Security | `security-expert` |
| Mobile | `mobile-expert` |
| Desktop | `desktop-expert` |
| TypeScript | `typescript-expert` |
| Testing | `testing-expert`, `jest-testing-expert`, `vitest-testing-expert` |
| VPS | `vps-expert` |
| Monitoring | `monitoring-expert` |

## Sistema de Planejamento

```bash
# Salvar plano
python3 .claude/hooks/plan_persistence.py save --title="Feature X"

# Listar planos
python3 .claude/hooks/plan_persistence.py list

# Criar checkpoint
python3 .claude/hooks/plan_checkpoint.py create

# Restaurar checkpoint
python3 .claude/hooks/plan_checkpoint.py restore
```

## Variáveis de Ambiente

```bash
# .env.local
ANTHROPIC_API_KEY=sk-ant-xxx
ELEVENLABS_API_KEY=xxx      # Opcional - TTS
OPENAI_API_KEY=xxx          # Opcional - TTS
```

## Manutenção

```bash
# Atualizar configuração
./setup-claude.sh update

# Verificar status
./setup-claude.sh status
```

## Documentação

- [PLAN_MODE.md](.claude/PLAN_MODE.md) - Sistema de planejamento
- [WORKFLOW_AUTOMATION.md](.claude/WORKFLOW_AUTOMATION.md) - Detalhes dos hooks
- [COVERAGE_MATRIX.md](.claude/COVERAGE_MATRIX.md) - Matriz de cobertura

## Licença

MIT
