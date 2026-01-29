# Plan Mode - Melhorias

Sistema aprimorado de planejamento para Claude Code CLI.

## Arquivos Criados

| Arquivo | Propósito |
|---------|-----------|
| `.claude/hooks/plan_persistence.py` | Salva/carrega planos entre sessões |
| `.claude/hooks/plan_checkpoint.py` | Checkpoints git antes de implementar |
| `.claude/hooks/plan_to_tasks.py` | Converte planos em TaskCreate |
| `.claude/templates/prd_template.md` | Template de PRD |
| `.claude/templates/plan_template.md` | Template de plano |
| `.claude/agents/plan-expert.md` | Agente especializado em planos |

## Uso

### Modo /plan Básico

```
/plane
> Quero adicionar autenticação JWT na API
```

### Persistência de Planos

```bash
# Listar planos salvos
python3 .claude/hooks/plan_persistence.py list

# Carregar último plano (para o Claude ler)
python3 .claude/hooks/plan_persistence.py load

# Salvar plano manualmente
echo "meu plano" | python3 .claude/hooks/plan_persistence.py save --title="Feature X"
```

### Checkpoints

```bash
# Criar checkpoint antes de implementar
python3 .claude/hooks/plan_checkpoint.py create

# Ver checkpoint atual
python3 .claude/hooks/plan_checkpoint.py show

# Restaurar checkpoint (se algo der errado)
python3 .claude/hooks/plan_checkpoint.py restore
```

### Converter Plano em Tarefas

```bash
# Preview das tarefas extraídas
python3 .claude/hooks/plan_to_tasks.py --preview

# Gerar comandos TaskCreate
python3 .claude/hooks/plan_to_tasks.py
```

## Workflow Recomendado

```
1. /plan → Criar plano detalhado
2. python3 .claude/hooks/plan_checkpoint.py create → Salvar estado
3. Executar implementação
4. (opcional) python3 .claude/hooks/plan_persistence.py save → Salvar plano
```

## Integração com Hooks Existentes

O plan mode funciona junto com seus hooks atuais:
- **adaptive_hooks**: Valida código após implementação
- **checkpoint**: Cria checkpoints automáticos ao final
- **thinking-level**: Ajusta nível de detalhe

## Próximas Melhorias Possíveis

- [ ] Hook automático ao entrar/exit do plan mode
- [ ] Integração com TaskCreate nativo
- [ ] Dashboard de planos em HTML
- [ ] Sincronização com GitHub Issues
- [ ] Histórico de decisões tomadas
