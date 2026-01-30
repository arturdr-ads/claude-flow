# Skills Quick Start Guide

**Data**: 2026-01-29
**Sprint**: 1 - Otimização de Velocidade

---

## 🚀 O QUE SÃO SKILLS?

Skills são **templates especializados** para tarefas comuns. Em vez de explicar o que você quer toda vez, você pode invocar um skill específico que já sabe exatamente como fazer aquela tarefa.

**Benefícios**:
- ⚡ **5-10x mais rápido** - Não precisa explicar contexto
- 🎯 **Resultado consistente** - Templates testados
- 📝 **Best practices** - Cada skill segue padrões da indústria

---

## 📚 SKILLS DISPONÍVEIS

### 1. react-component
**Quando usar**: Criar componentes React com TypeScript + Tailwind

**Exemplo**:
```
Criar componente ProductCard com props para nome, preço, imagem e callback para adicionar ao carrinho
```

**O que você ganha**:
- Componente funcional com TypeScript
- Props tipadas com interface
- Tailwind classes
- Acessibilidade (ARIA)
- Callbacks opcionais

---

### 2. nestjs-controller
**Quando usar**: Criar controllers NestJS com DTOs e validação

**Exemplo**:
```
Criar controller UsersController com endpoints CRUD, validação de email único, senha min 8 chars
```

**O que você ganha**:
- Controller completo (GET/POST/PUT/DELETE)
- DTOs com class-validator
- Swagger/OpenAPI docs
- Status codes corretos
- Error handling

---

### 3. prisma-schema
**Quando usar**: Criar schemas Prisma com relações

**Exemplo**:
```
Criar schema User com email único, Post com título/conteúdo, User tem muitos Posts
```

**O que você ganha**:
- Models com campos tipados
- Relações (@relation)
- Indexes (@@index)
- Constraints (@@unique)
- Enums se necessário

---

### 4. git-commit
**Quando usar**: Fazer commits seguindo estilo do projeto

**Exemplo**:
```
Fazer commit da nova feature de login
```

**O que você ganha**:
- Mensagem formatada (Conventional Commits)
- Análise de git status
- Confirmação antes de commitar
- Type apropriado (feat/fix/docs/etc)

---

### 5. dockerfile
**Quando usar**: Criar Dockerfiles otimizados

**Exemplo**:
```
Criar Dockerfile para app Node.js na porta 3000
```

**O que você ganha**:
- Multi-stage build
- Imagem Alpine leve
- Cache de dependencies
- Usuário não-root
- Healthcheck

---

## 💡 COMO USAR SKILLS

### Método 1: Invoke Explícito
```
<skill-name> <seu pedido>
```

**Exemplos**:
```
react-component Criar Button com variant primary/secondary
nestjs-controller Criar AuthController com login/register
prisma-schema Criar models Product e Category
git-commit Commitar mudanças de refatoração
dockerfile Dockerfile para API FastAPI
```

### Método 2: Delegação Automática
Às vezes, Claude detecta que você precisa de um skill e invoca automaticamente baseado no seu pedido.

**Exemplos**:
```
"Criar componente React para lista de produtos"
→ Claude invoca react-component automaticamente

"Criar controller de usuários em NestJS"
→ Claude invoca nestjs-controller automaticamente
```

---

## 🎯 FLUXO DE TRABALHO RECOMENDADO

### Desenvolvimento Full-Stack

```
1. prisma-schema
   ↓ (criar models do banco)

2. nestjs-controller
   ↓ (criar API endpoints)

3. react-component
   ↓ (criar UI para consumir API)

4. git-commit
   ↓ (salvar progresso)

5. dockerfile
   ↓ (containerizar para deploy)
```

### Bug Fix

```
1. Corrigir código manualmente
2. git-commit "fix: corrigir validação de email"
3. React/Update components se necessário
```

### Novo Feature

```
1. prisma-schema (novos models)
2. nestjs-controller (novos endpoints)
3. react-component (nova UI)
4. git-commit (salvar cada etapa)
```

---

## 📊 COMPARAÇÃO: COM VS SEM SKILLS

### Tarefa: Criar componente de produto

**SEM Skill** (3-5 min):
```
Você: "Preciso de um componente React para mostrar produtos"
Claude: "Qual framework? TypeScript? Tailwind? Props? Callbacks?"
Você: "React com TypeScript, Tailwind, props id/nome/preço"
Claude: [gera código genérico]
Você: "Precisa de acessibilidade, callback no clique"
Claude: [ajusta código]
→ 5 interações, 3-5 minutos
```

**COM Skill** (30 seg):
```
Você: "react-component Criar ProductCard com id, nome, preço, callback onAddToCart"
Claude: [gera código completo com TypeScript, Tailwind, ARIA]
→ 1 interação, 30 segundos
```

**Ganho**: **6-10x mais rápido!** ⚡

---

## 🔧 CUSTOMIZAÇÃO

Cada skill tem **placeholders** que você pode substituir:

```
[ComponentName]    → Nome do seu componente
[DataType]         → Tipo dos seus dados
[tailwind-classes] → Suas classes Tailwind
[serviceVariable]  → Nome do seu service
```

---

## 🚨 ERROS COMUNS

### ERRO: Invocar skill errado
```
❌ "react-component Criar API de produtos"
✅ "nestjs-controller Criar ProductsController"
```

### ERRO: Não fornecer detalhes suficientes
```
❌ "react-component Criar componente"
✅ "react-component Criar UserCard com avatar, nome, email"
```

### ERRO: Misturar línguas
```
❌ "react-component Create component for products"
✅ "react-component Criar componente para produtos"
```

---

## 📈 PRÓXIMOS SKILLS (Sprint 2)

Planejamos adicionar:

- **test-unit** - Testes unitários (Jest/Vitest)
- **test-e2e** - Testes E2E (Playwright/Cypress)
- **github-actions** - CI/CD pipelines
- **k8s-deployment** - Kubernetes manifests
- **redis-cache** - Cache com Redis
- **postgres-query** - Queries otimizadas
- **graphql-schema** - Schemas GraphQL
- **nextjs-page** - Páginas Next.js
- **vue-component** - Componentes Vue 3
- **svelte-component** - Componentes Svelte

---

## 💬 FEEDBACK

Se um skill não funcionar bem, documente:
1. Qual skill você usou
2. Qual foi seu pedido
3. Qual foi o problema
4. O que você esperava

Isso ajuda a melhorar os skills no próximo sprint!

---

**Divirta-se codando 3-5x mais rápido!** 🚀
