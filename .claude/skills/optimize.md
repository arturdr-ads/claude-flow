---
name: optimize
description: Use PROACTIVELY to optimize any prompt using Anthropic principles + TDD patterns. Expands simple requests into structured, testable instructions with explicit requirements, constraints, and validation criteria.
tools: Read, Write, Edit, Grep, Glob
color: cyan
category: meta
model: sonnet
parallelism: 2
---

# Prompt Optimizer Skill

Use este skill quando o usuário adicionar `<optimize>` ao início do prompt.

## Gatilho

```
<optimize> [qualquer prompt]
```

## O Que Faz

Transforma prompts básicos em prompts otimizados com:

- **Requisitos explícitos**: O que precisa ser feito
- **Constraints & Limitations**: O que NÃO pode fazer
- **Test-Driven Development**: Como validar o resultado
- **Output Validation**: Checklist antes de completar
- **Examples**: Exemplos de entrada/saída
- **Edge Cases**: Casos limites a considerar

## Framework de Otimização

### STEP 1: ANALYZE (Descobrir)

Perguntas chave sobre o prompt original:

- **Qual é o objetivo principal?** (What)
- **Quem é o usuário/sistema?** (Who)
- **Qual o contexto?** (Where/When)
- **Quais são as restrições?** (Constraints)
- **Como saber se funcionou?** (Success Criteria)

### STEP 2: EXPAND (Estruturar)

Adicionar ao prompt:

```markdown
## Objetivo
[Objetivo claro e específico]

## Contexto
[Informações relevantes sobre o projeto/sistema]

## Requisitos
- [RF-001] Requisito funcional 1
- [RF-002] Requisito funcional 2

## Constraints & Limitations
- **NÃO pode** [limitação clara]
- **DEVE evitar** [anti-pattern]

## Test-Driven Development
1. RED: [O que testar primeiro]
2. GREEN: [Como fazer funcionar]
3. REFACTOR: [Como melhorar]

## Output Validation
Antes de completar:
- [ ] Critério 1
- [ ] Critério 2

## Examples
Input: [exemplo de entrada]
Output: [exemplo de saída esperada]
```

### STEP 3: REFINE (Melhorar)

Aplicar princípios Anthropic:

- **Clareza > Criatividade**: Ser explícito é melhor que clever
- **Específico > Genérico**: Exemplos concretos > abstrações
- **Testável > Ambíguo**: Critérios mensuráveis > subjetivos
- **Constraints Positivas**: "Faça X" > "Não faça Y"
- **Single Responsibility**: Um foco claro por prompt

## Template de Resposta

Quando `<optimize>` for detectado, produza:

```markdown
# Prompt Otimizado

## Objetivo
[Objetivo claro derivado do prompt original]

## Contexto
- Stack/Tecnologia: [inferido ou perguntar]
- Projeto: [contexto do projeto]
- Restrições: [limitações técnicas/tempo]

## Requisitos Funcionais
- [RF-001] [Requisito 1]
- [RF-002] [Requisito 2]
...

## Constraints & Limitations
- **NÃO pode** [limitação 1]
- **NÃO deve** [limitação 2]
- **DEVE sempre** [regra obrigatória]
- **QUANDO** [condição] → [ação]
- **SE** [condição] → perguntar usuário

## Test-Driven Development
1. **RED**: Defina o que precisa ser testado
   - [Cenário de teste 1]
   - [Cenário de teste 2]

2. **GREEN**: Implemente para passar nos testes
   - Implementação mínima
   - Foco em funcionalidade

3. **REFACTOR**: Melhore mantendo testes verdes
   - Otimização
   - Limpeza de código

## Output Validation
Antes de completar, verifique:
- [ ] Requisito 1 atendido
- [ ] Requisito 2 atendido
- [ ] Formato correto
- [ ] Sem erros óbvios
- [ ] Testes passariam (se aplicável)

## Examples

### Exemplo 1 - Input
[Input de exemplo simples]

### Exemplo 1 - Output Esperado
[Output esperado detalhado]

### Exemplo 2 - Caso Edge
[Caso especial ou edge case]

---

## Prompt Original (para referência)
[Prompt original do usuário]
```

## Anti-Patterns de Prompt

❌ **RUIM**: "Faça um bom código"
✅ **BOM**: "Crie uma função TypeScript que valide emails, com regex adequado, testes unitários, e tratamento de erros"

❌ **RUIM**: "Arruma esse bug"
✅ **BOM**: "Analise o erro X no arquivo Y, identifique a causa raiz, proponha solução com código exemplo, e considere edge cases"

❌ **RUIM**: "Melhora isso"
✅ **BOM**: "Refatore o código para seguir Clean Architecture, adicionando camadas de Service e Repository, com exemplos de como usar"

## Quando NÃO Otimizar

- Prompt já é estruturado e detalhado
- Prompt tem exemplos específicos
- Prompt já tem TDD explícito
- Prompt está em formato de PRD/spec

## Processo de Execução

1. **Detectar** tag `<optimize>` no início do prompt
2. **Extrair** o prompt original (remover a tag)
3. **Analisar** o domínio e contexto
4. **Expandir** usando template apropriado
5. **Adicionar** requisitos específicos
6. **Definir** constraints claras
7. **Especificar** output validation
8. **Fornecer** exemplos quando útil
9. **Sugerir** TDD approach quando aplicável
10. **Apresentar** prompt otimizado completo

## Constraints

- **NÃO pode substituir contexto específico do projeto** - Você pode melhorar o prompt, mas informações específicas do domínio devem vir do usuário
- **NÃO pode adivinhar requisitos não declarados** - Expanda o que foi pedido, não invente novas necessidades
- **NÃO pode garantir resultado perfeito** - Prompt otimizado melhora a probabilidade de sucesso, mas não garante
- **DEVE sempre manter o objetivo original** - Não mude o que foi pedido, apenas torne mais explícito
- **DEVE aplicar TDD patterns** quando a tarefa envolver código/implementação
- **DEVE definir output validation** checklist
- **DEVE manter português** se o prompt original for em português
