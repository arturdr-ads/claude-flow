# Changelog

Todos os cambios notáveis deste projeto serão documentados neste arquivo.

## [Unreleased]

### Adicionado
- CLAUDE.md - Contexto do projeto para o Claude
- README.md - Documentação principal
- Sistema de 20+ agentes especializados
- Sistema de hooks adaptativos
- Comandos personalizados (/commit, /status, /push, /checkout)
- Sistema de checkpoints
- Sistema de planejamento com persistência

## [1.0.0] - 2025-01-XX

### Adicionado
- Configuração base do Claude Code CLI
- 20 agentes especializados por tecnologia
- Sistema de hooks adaptativos para detecção automática de projeto
- Status line customizado
- Script de instalação automática

### Agentes Incluídos
- frontend-expert, backend-expert, database-expert
- typescript-expert, testing-expert, devops-expert
- cloud-expert, security-expert, monitoring-expert
- mobile-expert, desktop-expert, vps-expert
- plan-expert, code-review-expert, triage-expert
- research-expert, cli-expert, ai-sdk-expert

### Hooks Incluídos
- adaptive_hooks.py - Detecção automática de projeto
- plan_persistence.py - Persistência de planos
- plan_checkpoint.py - Checkpoints git
- status_line_v3.py - Status line customizado
- notification.py - Notificações TTS
