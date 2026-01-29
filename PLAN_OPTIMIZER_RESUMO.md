# Prompt Optimizer - Resumo Executivo

## Status: 🟡 PRONTO PARA IMPLEMENTAÇÃO

**Tempo estimado:** 3 horas end-to-end
**Arquivo detalhado:** `PLAN_OPTIMIZER.md` (1074 linhas)

---

## O Que Vamos Criar

Sistema de **otimização MANUAL de prompts** que:
1. ✅ Só ativa com tag `<optimize>` (não automático)
2. ✅ Respeita nossa **hierarquia de 7 cores** (28 agentes)
3. ✅ Integra com **paralelismo dinâmico** (auto_parallelism.py)
4. ✅ Recomenda agentes baseados em **domínio detectado**
5. ✅ Sugere uso do **Task tool** para multi-agente
6. ✅ Output em **português** com estrutura TDD

---

## Problema Atual

### ❌ O que está quebrado:
- `prompt_optimizer.py` roda **automaticamente** em TODOS os prompts
- Usuário perde controle (otimizações indesejadas)
- Não respeita nossa hierarquia de cores
- Não integra com swarms/orchestrator
- Não usa paralelismo dinâmico

### ✅ Solução proposta:
- Hook **manual** com tag `<optimize>`
- Sistema de **7 cores** para recomendações inteligentes
- Integração completa com **Task tool**
- Respeita limites do **auto_parallelism.py**

---

## Arquitetura da Solução

### Fluxo de Otimização

```
┌─────────────────────────────────────────────────────────────┐
│  1. USUÁRIO: "<optimize> criar API de usuários"            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  2. HOOK: Detecta tag <optimize>                           │
│     optimize_hook.py (UserPromptSubmit)                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  3. DETECÇÃO: Analisa domínio → Mapeia cores               │
│     "API" → Blue (backend, database)                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  4. RECOMENDA: Agentes específicos                         │
│     🔵 backend-expert: Implementação de APIs               │
│     🔵 database-expert: Schema e queries                   │
│     🟢 testing-expert: Testes automatizados                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  5. ESTRUTURA: TDD + Constraints + Output Validation       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  6. OUTPUT: Prompt otimizado + recomendações               │
└─────────────────────────────────────────────────────────────┘
```

### Hierarquia de 7 Cores

```
🟣 Purple (4)  → Orquestração: orchestrator, architect, product, ux
🔵 Blue (6)    → Implementação: frontend, backend, database, server, mobile, desktop
🟢 Green (3)   → Qualidade: testing, security, code-review
🟠 Orange (4)  → Infra: devops, cloud, build-tools, monitoring
🟡 Yellow (4)  → Tooling: cli, typescript, ai-sdk, refactoring
🩷 Pink (3)    → Conhecimento: documentation, research, ai-research
🔴 Cyan (4)    → Meta: meta-agent, oracle, code-search, triage
```

---

## Arquivos a Criar/Atualizar

### Novos Arquivos

1. **`.claude/hooks/optimize_hook.py`** (300 linhas)
   - Hook principal que detecta tag `<optimize>`
   - Mapeamento de 7 cores
   - Recomendação de agentes
   - Integração com auto_parallelism

2. **`tests/test_optimize_hook.py`** (150 linhas)
   - Suite de testes completa
   - Teste de detecção de tag
   - Teste de detecção de domínio
   - Teste de recomendações
   - Teste de pass-through

3. **`.claude/PROMPT_OPTIMIZER.md`** (250 linhas)
   - Documentação completa
   - Exemplos de uso
   - Hierarquia de cores
   - Troubleshooting

4. **`.claude/MIGRATION_OPTIMIZER.md`** (50 linhas)
   - Nota de migração
   - Antes vs Depois
   - Rollback se necessário

### Arquivos a Atualizar

5. **`.claude/settings.json`**
   - Trocar `prompt_optimizer.py` → `optimize_hook.py`
   - Manter em UserPromptSubmit

6. **`.claude/agents/prompt-optimizer.md`**
   - Adicionar seção de 7 cores
   - Documentar integração com Task tool
   - Atualizar exemplos

7. **`.claude/COVERAGE_MATRIX.md`**
   - Adicionar seção Prompt Optimizer
   - Documentar fluxo de otimização

8. **`.claude/CLAUDE.md`**
   - Adicionar seção "6. Prompt Optimizer"
   - Como usar tag `<optimize>`

### Arquivos a Remover (Backup)

9. **`.claude/hooks/prompt_optimizer.py`** → `.old`
   - Mover para backup (não deletar ainda)

---

## Exemplo de Uso

### Cenário 1: Backend API

**Input:**
```
<optimize> criar API de autenticação com JWT
```

**Output:**
```markdown
## Objetivo Clarificado
Criar API REST de autenticação usando JWT com refresh tokens...

## Requisitos Específicos
- [RF-001] POST /api/auth/login (email + password)
- [RF-002] POST /api/auth/refresh (refresh token)
- [RF-003] GET /api/auth/me (dados do usuário)

## Constraints & Limitations
- NÃO pode armazenar senhas em texto plano
- DEVE usar bcrypt para hash
- SE email inválido → retornar 401 sem revelar existência

## Test-Driven Development
1. RED: Testar login com credenciais válidas/inválidas
2. GREEN: Implementar AuthService com JWT
3. REFACTOR: Extrair lógica de validação

## Agentes Recomendados
🔵 backend-expert: Implementação de APIs
🔵 database-expert: Schema de users + sessions
🟢 security-expert: Validação JWT + OWASP
🟢 testing-expert: Testes automatizados
```

### Cenário 2: Projeto Completo

**Input:**
```
<optimize> criar sistema SaaS de gestão de projetos do zero
```

**Output:**
```markdown
## Objetivo Clarificado
Criar sistema SaaS completo para gestão de projetos com múltiplos usuários...

## Agentes Recomendados
🟣 orchestrator-expert: Coordenar projeto multi-fase
🟣 architect-expert: Definir stack e padrões
🟣 product-expert: Requisitos e priorização
🟣 ux-expert: Jornadas e wireframes

## Multi-Agente? Use Task Tool
Task(description="SaaS gestão de projetos", prompt="""
orchestrator-expert: Coordenar do PRD ao deploy

Fases:
1. product-expert: Entender problema e usuários
2. ux-expert: Mapear jornadas e criar wireframes
3. architect-expert: Decidir stack (React+NestJS+PostgreSQL)
4. frontend-expert: Implementar UI components
5. backend-expert: Implementar APIs e lógica
6. database-expert: Schema e migrations
7. testing-expert: Testes E2E
8. devops-expert: Docker + CI/CD
9. cloud-expert: Deploy em AWS
""")

**Paralelismo Disponível:** 2 agentes simultâneos
```

---

## Cronograma de Implementação

### FASE 1: Preparação (30 min)
- [ ] Backup de `prompt_optimizer.py`
- [ ] Análise de comandos existentes
- [ ] Documentar mudanças

### FASE 2: Criar Hook (45 min)
- [ ] Implementar `optimize_hook.py`
- [ ] Detecção de tag `<optimize>`
- [ ] Mapeamento de 7 cores
- [ ] Recomendação de agentes
- [ ] Integração com auto_parallelism
- [ ] Teste manual

### FASE 3: Configuração (15 min)
- [ ] Atualizar `settings.json`
- [ ] Validar JSON válido
- [ ] Testar reload

### FASE 4: Atualizar Agente (30 min)
- [ ] Revisar `prompt-optimizer.md`
- [ ] Adicionar seção 7 cores
- [ ] Documentar Task tool

### FASE 5: Testes (45 min)
- [ ] Criar suite de testes
- [ ] Testar todos os cenários
- [ ] Testar edge cases

### FASE 6: Documentação (30 min)
- [ ] Criar `PROMPT_OPTIMIZER.md`
- [ ] Atualizar `CLAUDE.md`
- [ ] Atualizar `COVERAGE_MATRIX.md`

### FASE 7: Cleanup (15 min)
- [ ] Mover código antigo para `.old`
- [ ] Criar nota de migração
- [ ] Validar não há quebras

**Total: 3 horas**

---

## Success Criteria

### Funcional
- ✅ Tag `<optimize>` ativa otimização
- ✅ Sem tag = pass-through sem modificação
- ✅ Recomenda agentes por cor
- ✅ Respeita paralelismo dinâmico
- ✅ Output em português

### Técnico
- ✅ Hook integrado em settings.json
- ✅ 100% dos testes passando
- ✅ Performance <100ms por otimização
- ✅ Código documentado

### UX
- ✅ Fácil de usar (só adicionar tag)
- ✅ Recomendações úteis
- ✅ Não intrusivo
- ✅ Feedback claro (agents + cores)

---

## Riscos & Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Hook não detecta tag | Baixa | Alto | Case-insensitive + logging |
| Recomendações incorretas | Média | Médio | Keywords refinadas + feedback |
| Quebra de sistema | Baixa | Alto | Backup + rollback rápido |
| Performance lenta | Baixa | Médio | Só roda com tag + cache |

---

## Próximos Passos

1. **Revisar plano completo**: `PLAN_OPTIMIZER.md` (1074 linhas)
2. **Aprovar implementação**: Confirmar que está OK
3. **Executar FASE 1**: Preparação e backup
4. **Implementar FASE 2**: Hook principal
5. **Testar FASE 5**: Validar tudo funciona
6. **Deploy**: Atualizar settings.json
7. **Documentar**: Criar docs finais

---

## Comandos Úteis

```bash
# Ver plano detalhado
cat PLAN_OPTIMIZER.md

# Ver este resumo
cat PLAN_OPTIMIZER_RESUMO.md

# Criar checkpoint antes
git add . && git commit -m "checkpoint: antes de implementar prompt optimizer"

# Implementar (após aprovação)
# Seguir FASES 1-7 do plano detalhado
```

---

**Status do Plano:** 🟡 PRONTO PARA IMPLEMENTAÇÃO

**Arquivo Detalhado:** `/home/arturdr/Claude/PLAN_OPTIMIZER.md`

**Tempo Estimado:** 3 horas end-to-end
