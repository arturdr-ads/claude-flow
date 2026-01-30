# Batch Creation: 5 Priority Skills for Claude Code

## Objetivo
Criar 5 skills prioritários em `.claude/skills/` para acelerar desenvolvimento full-stack em 3-5x.

## Contexto
- Projeto: Claude Code CLI - Ecossistema de automação com 28 agentes especializados
- Stack: React, TypeScript, NestJS, Prisma, Docker, Git
- Skills existentes: 1 (optimize.md)
- Framework de skills: Frontmatter YAML + Gatilho + Template + Checklist
- Tamanho alvo: 40-80 linhas por skill

## Requisitos Funcionais
- [RF-001] Criar `react-component.md` - Gerar componentes React + TypeScript + Tailwind
- [RF-002] Criar `nestjs-controller.md` - Gerar controllers NestJS com DTOs e validação
- [RF-003] Criar `prisma-schema.md` - Gerar schemas Prisma com relações
- [RF-004] Criar `git-commit.md` - Fazer commits seguindo estilo do projeto
- [RF-005] Criar `dockerfile.md` - Gerar Dockerfiles otimizados multi-stage

## Constraints & Limitations
- **NÃO pode** criar skills > 100 linhas (manter foco em velocidade)
- **NÃO pode** usar ferramentas não listadas no frontmatter
- **DEVE sempre** incluir frontmatter YAML completo (name, description, tools, color, category, model, parallelism)
- **DEVE sempre** incluir seção de gatilho claro (quando usar o skill)
- **DEVE sempre** incluir template pronto com placeholders [assim]
- **DEVE sempre** incluir checklist de validação final
- **QUANDO** skill for invocado → seguir template estruturado
- **SE** prompt for ambíguo → perguntar antes de gerar código

## Formato Obrigatório de Skill

Cada skill DEVE seguir esta estrutura:

```markdown
---
name: <nome-kebab-case>
description: Use <quando> para <o que faz>. <gatilho claro>
tools: <lista separada por vírgula>
color: <red|blue|green|yellow|purple|orange|pink|cyan>
category: <frontend|backend|database|devops|git|testing|etc>
model: <haiku|sonnet|opus>
parallelism: <1|2>
---

# <Nome Legível do Skill>

Use este skill quando <gatilho claro e específico>.

## Gatilho

```
<exemplo de comando ou situação que dispara o skill>
```

## O Que Faz

<Descrição clara do que o skill gera/cria>

## Template

<Nome do Template>

```typescript
<exemplo de código com placeholders>
```

## Checklist de Validação

Antes de completar, verifique:
- [ ] <critério 1>
- [ ] <critério 2>
- [ ] <critério 3>

## Quando Usar

✅ Usa este skill para:
- <caso de uso 1>
- <caso de uso 2>

❌ NÃO use para:
- <caso que NÃO é este skill>

## Exemplo de Uso

**Input:**
```
<exemplo de pedido do usuário>
```

**Output:**
```
<exemplo do que o skill gera>
```

## Dicas Pro

- <dica 1>
- <dica 2>

## Constraints

- **NÃO pode** <limitação>
- **DEVE sempre** <regra>
```

## Test-Driven Development

1. **RED**: Definir requisitos de cada skill
   - react-component: Componente funcional com TypeScript + Tailwind
   - nestjs-controller: Controller com DTOs, validação class-validator
   - prisma-schema: Schema com models, relações, indexes
   - git-commit: Commit message following project style
   - dockerfile: Multi-stage build otimizado

2. **GREEN**: Criar skills funcionais
   - Frontmatter completo
   - Template com placeholders
   - Checklist de validação
   - Exemplos de uso

3. **REFACTOR**: Otimizar
   - Reduzir tamanho se > 80 linhas
   - Melhorar clareza de gatilhos
   - Adicionar mais exemplos se útil

## Detalhamento dos Skills

### 1. react-component.md
- **Tools**: Write, Read, Edit
- **Color**: blue
- **Category**: frontend
- **Model**: sonnet
- **Gatilho**: "criar componente React", "novo componente"
- **Template**: Componente funcional com TypeScript, interfaces, Tailwind classes, hooks
- **Validação**: Compila, tipos corretos, acessibilidade (ARIA)

### 2. nestjs-controller.md
- **Tools**: Write, Read, Edit, Grep
- **Color**: green
- **Category**: backend
- **Model**: sonnet
- **Gatilho**: "criar controller", "nova rota", "endpoint"
- **Template**: Controller class, DTOs, class-validator, decorators, Swagger docs
- **Validação**: Endpoints funcionam, DTOs validam, Swagger docs presentes

### 3. prisma-schema.md
- **Tools**: Write, Read, Edit
- **Color**: purple
- **Category**: database
- **Model**: sonnet
- **Gatilho**: "criar schema", "modelo Prisma", "migration"
- **Template**: Model com campos, relações (@relation), indexes (@@index)
- **Validação**: Schema válido, relações consistentes, indexes adequados

### 4. git-commit.md
- **Tools**: Bash
- **Color**: orange
- **Category**: git
- **Model**: haiku
- **Gatilho**: "fazer commit", "commitar mudanças"
- **Template**: Commit message com prefixo (feat/fix/docs/refactor), escopo, descrição
- **Validação**: Message segue estilo, git status confirmado, arquivos certos staged

### 5. dockerfile.md
- **Tools**: Write, Read
- **Color**: cyan
- **Category**: devops
- **Model**: sonnet
- **Gatilho**: "criar Dockerfile", "containerizar app"
- **Template**: Multi-stage build, FROM alpine/node, copia de arquivos, CMD/ENTRYPOINT
- **Validação**: Multi-stage, cache otimizado, usuário não-root, porta exposta

## Output Validation

Antes de completar, verifique:
- [ ] Todos 5 skills criados em `.claude/skills/`
- [ ] Cada skill tem frontmatter YAML completo
- [ ] Cada skill tem 40-80 linhas (foco em velocidade)
- [ ] Cada skill tem gatilho claro específico
- [ ] Cada skill tem template com placeholders [assim]
- [ ] Cada skill tem checklist de validação
- [ ] Nomes são kebab-case
- [ ] Tools são minimal e apropriadas
- [ ] Cores são distintas por categoria
- [ ] Model é apropriado (haiku para simples, sonnet para padrão)
- [ ] Parallelism definido (1 ou 2)

## Observações Adicionais

- Skills devem ser **rápidos de usar** (não enciclopédias)
- Skills devem ser **específicos** (não genéricos demais)
- Skills devem ter **exemplos práticos** (não só teoria)
- Skills devem usar **placeholders visíveis** [assim]
- Skills devem ter **checklists curtos** (3-5 itens máximo)
