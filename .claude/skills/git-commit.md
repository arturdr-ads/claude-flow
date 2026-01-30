---
name: git-commit
description: Use PROACTIVELY when user asks to make git commits. Auto-creates commit messages following project conventions (feat/fix/docs/refactor/test/chore).
tools: Bash
color: orange
category: git
model: haiku
parallelism: 1
---

# Git Commit Helper

Use este skill quando o usuário pedir para fazer commit de mudanças.

## Gatilho

```
Fazer commit das mudanças
Commitar alterações
Criar commit com [descrição]
Salvar mudanças no git
```

## O Que Faz

Cria commits seguindo Conventional Commits:
- Analisa `git status` e `git diff`
- Sugerem mensagem apropriada
- Confirma com usuário antes de commitar
- Usa formato: `type(scope): description`

## Template

Formato de Commit Message

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: Nova funcionalidade
- `fix`: Bug fix
- `docs`: Documentação
- `style`: Formatação, missing semicolons
- `refactor`: Refatoração
- `test`: Adicionar/alterar tests
- `chore`: Maintenance, dependencies

**Exemplos:**
```
feat(auth): add JWT authentication
fix(api): handle null response from user endpoint
docs(readme): update installation instructions
refactor(components): extract Button component
test(users): add integration tests for CRUD
```

## Checklist de Validação

Antes de commitar, verifique:
- [ ] Arquivos corretos estão staged (git status)
- [ ] Diff mostra apenas mudanças esperadas
- [ ] Mensagem segue formato type(scope): description
- [ ] Type é apropriado (feat/fix/docs/etc)
- [ ] Subject descreve mudança claramente

## Quando Usar

✅ Usa este skill para:
- Fazer commits após implementação
- Commitar múltiplos arquivos
- Criar commits com mensagem formatada

❌ NÃO use para:
- Push remoto (use git push)
- Branch creation (use git checkout -b)
- Merge/rebase (use comandos específicos)

## Exemplo de Uso

**Input:**
```
Fazer commit da nova funcionalidade de login
```

**Output:**
```bash
1. Ver git status
2. Ver git diff --staged
3. Sugerir mensagem: feat(auth): add login with email/password
4. Confirmar com usuário
5. Executar: git commit -m "feat(auth): add login with email/password"
```

## Workflow

```bash
# 1. Verificar status
git status

# 2. Ver diff (se necessário)
git diff
git diff --staged

# 3. Adicionar arquivos (se necessário)
git add <files>
# ou
git add .

# 4. Criar commit
git commit -m "type(scope): description"

# 5. Confirmar
git log -1 --stat
```

## Dicas Pro

- Use `git add -p` para stage por partes
- Use `git status -s` para view compacto
- Commits pequenos e frequentes são melhores
- Use imperativo ("add feature" não "added feature")
- Limite subject a 72 caracteres
- Use body para explicar "why" não "what"

## Padrões do Projeto

Verificar `.gitignore` e commits recentes:

```bash
# Ver estilo de commits do projeto
git log --oneline -10

# Verificar se tem Co-Authored-By
git log -1 --pretty=full
```

## Constraints

- **NÃO pode** fazer commit sem confirmar com usuário
- **DEVE sempre** verificar git status antes
- **DEVE sempre** usar formato type(scope): description
- **DEVE sempre** usar imperativo no subject
- **SE** mudanças forem grandes → sugerir múltiplos commits
