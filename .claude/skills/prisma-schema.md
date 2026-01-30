---
name: prisma-schema
description: Use PROACTIVELY when user asks to create Prisma schemas, models, or migrations. Auto-generates schemas with fields, relations, and indexes.
tools: Write, Read, Edit
color: purple
category: database
model: sonnet
parallelism: 2
---

# Prisma Schema Generator

Use este skill quando o usuário pedir para criar schemas ou modelos Prisma.

## Gatilho

```
Criar schema Prisma para [domain]
Model de [entidade]
Migration para [funcionalidade]
Adicionar modelo [Model]
```

## O Que Faz

Gera schemas Prisma com:
- Models com campos tipados
- Relações (@relation)
- Indexes (@@index)
- Constraints (@@unique)
- Enums se necessário
- Default values

## Template

Model com Relações

```prisma
// Enum se necessário
enum [ModelName]Status {
  ACTIVE
  INACTIVE
  PENDING
}

model [ModelName] {
  id        String   @id @default(cuid())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Campos
  name        String          @db.VarChar(255)
  email       String?         @db.VarChar(255)
  status      [ModelName]Status @default(ACTIVE)
  description String?         @db.Text

  // Relações (1:N)
  [RelatedModel]s [RelatedModel][]

  // Relações (N:1)
  [ParentModel]Id [ParentModel]Id?
  [ParentModel]   [ParentModel]?  @relation(fields: [[ParentModel]Id], references: [id])

  // Relações (N:N)
  [OtherModel]s [OtherModel][] @relation("[TableName]")
}

model [RelatedModel] {
  id          String    @id @default(cuid())
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  // Campos
  name     String

  // Relação inversa
  [ModelName]Id String
  [ModelName]   [ModelName] @relation(fields: [[ModelName]Id], references: [id])

  // Index
  @@index([createdAt])
  @@index([[ModelName]Id])
}

model [OtherModel] {
  id        String   @id @default(cuid())
  createdAt DateTime @default(now())

  name String

  // N:N relation
  [ModelName]s [ModelName][] @relation("[TableName]")
}
```

## Checklist de Validação

Antes de completar, verifique:
- [ ] Model tem @id com @default(cuid()) ou uuid()
- [ ] Relações têm @relation com fields/references
- [ ] Indexes adicionados em campos frequentemente queryados
- [ ] Tipos apropriados (@db.VarChar, @db.Text, etc.)
- [ ] Defaults definidos (status, enums)
- [ ] Campos nullable marcados com `?`

## Quando Usar

✅ Usa este skill para:
- Criar novos modelos Prisma
- Adicionar relações entre modelos
- Adicionar indexes para performance
- Criar enums

❌ NÃO use para:
- Queries complexas (use database-expert)
- Migrations manuais (use prisma migrate)
- Performance tuning avançado

## Exemplo de Uso

**Input:**
```
Criar schema para User e Post
User tem nome, email (único)
Post tem título, conteúdo, author
User pode ter muitos posts
```

**Output:**
```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  posts     Post[]
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
}
```

## Dicas Pro

- Use `@default(cuid())` para IDs (mais seguro que uuid())
- Use `@db.VarChar(255)` para strings com limite
- Use `@db.Text` para campos longos (description, content)
- Adicione `@@index()` em campos frequentemente filtrados
- Use `@unique` para emails, slugs, usernames
- Adicione `@@map("[table_name]")` se nome da tabela for diferente

## Relações Comuns

```prisma
// 1:N (Um usuário tem muitos posts)
model User {
  posts Post[]
}
model Post {
  userId String
  user   User   @relation(fields: [userId], references: [id])
}

// N:N (Posts têm muitas tags)
model Post {
  tags Tag[] @relation("PostTags")
}
model Tag {
  posts Post[] @relation("PostTags")
}
```

## Constraints

- **NÃO pode** criar model sem @id
- **DEVE sempre** definir @relation em ambos lados
- **DEVE sempre** adicionar fields/references em @relation
- **DEVE sempre** usar tipos apropriados do Prisma
