# Índice - Prompt Optimizer Plan

## Documentos Criados

| Arquivo | Linhas | Descrição |
|---------|--------|-----------|
| **PLAN_OPTIMIZER.md** | 1074 | Plano detalhado completo |
| **PLAN_OPTIMIZER_RESUMO.md** | 329 | Resumo executivo |
| **PLAN_OPTIMIZER_INDEX.md** | Este arquivo | Índice de navegação |

## Navegação Rápida

### 📋 Para Começar
Leia **PLAN_OPTIMIZER_RESUMO.md** primeiro (3 min)

### 📖 Para Implementar
Siga **PLAN_OPTIMIZER.md** sequencialmente:
1. Contexto Atual (linhas 1-100)
2. Arquitetura da Solução (linhas 101-200)
3. Plano de Implementação (linhas 201-900)
4. Checklist (linhas 901-950)
5. Success Criteria (linhas 951-1074)

### 🎯 Seções Principais do Plano Detalhado

#### Contexto
- ✅ Já existe (linhas 8-70)
- ❌ Problemas identificados (linhas 71-130)
- 🎯 Requisitos claros (linhas 131-180)

#### Arquitetura
- Hierarquia de 7 cores (linhas 190-280)
- Fluxo de otimização (linhas 281-350)

#### Implementação (7 Fases)
1. **FASE 1: Preparação** (linhas 360-450)
2. **FASE 2: Criar Hook** (linhas 451-650)
3. **FASE 3: Configuração** (linhas 651-720)
4. **FASE 4: Atualizar Agente** (linhas 721-810)
5. **FASE 5: Testes** (linhas 811-890)
6. **FASE 6: Documentação** (linhas 891-960)
7. **FASE 7: Cleanup** (linhas 961-1000)

#### Validação
- Checklist completo (linhas 1005-1050)
- Success criteria (linhas 1051-1074)

## Quick Start

### 1. Entender o Problema (5 min)
```bash
# Ler resumo executivo
cat PLAN_OPTIMIZER_RESUMO.md

# Ver problema atual (seção "❌ O que está quebrado")
grep -A 20 "O que está quebrado" PLAN_OPTIMIZER_RESUMO.md
```

### 2. Revisar Solução (10 min)
```bash
# Ver arquitetura proposta
grep -A 30 "Arquitetura da Solução" PLAN_OPTIMIZER_RESUMO.md

# Ver hierarquia de cores
grep -A 15 "Hierarquia de 7 Cores" PLAN_OPTIMIZER_RESUMO.md
```

### 3. Planejar Implementação (5 min)
```bash
# Ver cronograma
grep -A 30 "Cronograma de Implementação" PLAN_OPTIMIZER_RESUMO.md

# Ver checklist
grep -A 50 "checklist de Implementação" PLAN_OPTIMIZER.md
```

### 4. Começar Implementação (3h)
```bash
# Seguir fases do plano detalhado
# FASE 1: Preparação (linhas 360-450)
# FASE 2: Criar Hook (linhas 451-650)
# ...
```

## Comandos Úteis

### Buscar no Plano
```bash
# Buscar por palavra-chave
grep -n "optimize_hook" PLAN_OPTIMIZER.md

# Ver linhas específicas
sed -n '451,650p' PLAN_OPTIMIZER.md  # FASE 2

# Buscar seção
grep -A 50 "FASE 2:" PLAN_OPTIMIZER.md
```

### Extração de Código
```bash
# Extrair código do hook
sed -n '/^```python/,/^```/p' PLAN_OPTIMIZER.md > optimize_hook.py.example

# Extrair código de testes
sed -n '/^```python/,/^```/p' PLAN_OPTIMIZER.md | grep -A 100 "test_optimize" > test_example.py
```

### Validação
```bash
# Ver checklist não implementado
grep "\[ \]" PLAN_OPTIMIZER.md

# Contar tarefas
grep -c "\[ \]" PLAN_OPTIMIZER.md  # Total
grep -c "\[x\]" PLAN_OPTIMIZER.md  # Feitas
```

## Exemplo de Workflow

### Opção 1: Implementação Completa (Recomendado)
```bash
# 1. Ler resumo
cat PLAN_OPTIMIZER_RESUMO.md

# 2. Criar checkpoint
git add . && git commit -m "checkpoint: antes de implementar optimizer"

# 3. Seguir plano fase por fase
# FASE 1: Backup e preparação
# FASE 2: Criar optimize_hook.py
# FASE 3: Atualizar settings.json
# FASE 4: Atualizar prompt-optimizer.md
# FASE 5: Criar e rodar testes
# FASE 6: Documentação
# FASE 7: Cleanup

# 4. Marcar tarefas no plano (vim/nano)
# Substituir [ ] por [x] conforme completa

# 5. Commit final
git add . && git commit -m "feat: implementar Prompt Optimizer integrado"
```

### Opção 2: Implementação Parcial (Testes)
```bash
# 1. Implementar só FASE 2 (Hook)
sed -n '451,650p' PLAN_OPTIMIZER.md

# 2. Testar manualmente
echo '{"prompt": "<optimize> teste"}' | python3 .claude/hooks/optimize_hook.py

# 3. Validar antes de continuar
# Se OK → continuar FASE 3+
# Se NOK → ajustar e retestar
```

### Opção 3: Revisão Crítica
```bash
# 1. Revisar apenas código do hook
sed -n '/^#### 2.1 Criar/,/^#### 2.2/p' PLAN_OPTIMIZER.md

# 2. Revisar apenas testes
sed -n '/#### 5.1 Criar suite/,/^#### 5.2/p' PLAN_OPTIMIZER.md

# 3. Revisar apenas documentação
sed -n '/### 6.1 Atualizar/,/^### 6.3/p' PLAN_OPTIMIZER.md
```

## Status Tracking

### Progresso Atual
```
FASE 1: Preparação          [ ] 0/6 tarefas
FASE 2: Criar Hook          [ ] 0/6 tarefas
FASE 3: Configuração        [ ] 0/3 tarefas
FASE 4: Atualizar Agente    [ ] 0/4 tarefas
FASE 5: Testes              [ ] 0/6 tarefas
FASE 6: Documentação        [ ] 0/5 tarefas
FASE 7: Cleanup             [ ] 0/4 tarefas
```

### Atualizar Status
```bash
# Editar plano com editor
vim PLAN_OPTIMIZER.md

# Buscar primeira tarefa não completa
/^\[ \]

# Marcar como completa
# Substituir [ ] por [x]

# Salvar e commit
git add PLAN_OPTIMIZER.md && git commit -m "progress: FASE X completa"
```

## Referências Rápidas

### Comandos do Sistema
```bash
# Ver paralelismo atual
cat .claude/auto_config.json

# Ver agentes disponíveis
ls -1 .claude/agents/*.md

# Testar hook manual
echo '<optimize> teste' | uv run .claude/hooks/optimize_hook.py
```

### Links Relevantes
- `.claude/hooks/auto_parallelism.py` - Paralelismo dinâmico
- `.claude/agents/orchestrator-expert.md` - Swarm coordination
- `.claude/settings.json` - Configuração de hooks
- `.claude/COVERAGE_MATRIX.md` - Matriz de agentes

### Documentos Externos
- Anthropic Prompt Engineering Guide (quando disponível)
- Testes em `tests/test_optimize_hook.py` (após criação)
- Documentação em `.claude/PROMPT_OPTIMIZER.md` (após criação)

## Troubleshooting

### Problema: Não acho seção específica
```bash
# Buscar palavra-chave em todos os documentos
grep -r "optimize_hook" . --include="*.md"
```

### Problema: Código não funciona
```bash
# Ver exemplo completo no plano
sed -n '/^#### 2.1 Criar/,/^#### 2.2/p' PLAN_OPTIMIZER.md

# Comparar com implementação atual
diff <(sed -n '/^#### 2.1 Criar/,/^#### 2.2/p' PLAN_OPTIMIZER.md) .claude/hooks/optimize_hook.py
```

### Problema: Testes falham
```bash
# Ver seção de testes no plano
sed -n '/#### 5.1 Criar suite/,/^#### 5.2/p' PLAN_OPTIMIZER.md

# Rodar testes com verbose
python3 tests/test_optimize_hook.py -v
```

## Próximos Passos

1. ✅ **Planejamento completo** - DONE
2. 🟡 **Aprovação do plano** - PENDING
3. 🔵 **Implementação FASE 1-7** - TODO
4. 🟢 **Testes e validação** - TODO
5. 🟠 **Deploy e documentação** - TODO

---

**Última atualização:** 2026-01-29
**Status:** 🟡 PRONTO PARA IMPLEMENTAÇÃO
**Tempo estimado:** 3 horas
