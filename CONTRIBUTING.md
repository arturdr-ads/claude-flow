# Contribuindo com o Claude Code Config

Obrigado por interessar-se em contribuir! Este documento orienta como contribuir com este projeto.

## Estrutura do Projeto

```
.claude/
├── agents/              # Agentes especializados (Task tool)
├── commands/            # Comandos personalizados (/command)
├── hooks/               # Hooks de automação (eventos)
├── status_lines/        # Scripts de status line
├── templates/           # Templates de documentos
└── settings.json        # Configuração principal
```

## Tipos de Contribuições

### 1. Adicionando um Novo Agente

Crie um arquivo em `.claude/agents/` seguindo o template:

```markdown
---
description: Agente especialista em [TECNOLOGIA]
type: [frontend|backend|database|devops|testing|etc]
---

# [Nome] Expert

Agente especialista em [TECNOLOGIA] para Claude Code CLI.

## Quando Usar

Use este agente quando precisar de ajuda com:
- [Cenário 1]
- [Cenário 2]
- [Cenário 3]

## Especialidades

- [Especialidade 1]
- [Especialidade 2]

## Ferramentas Disponíveis

- [Lista de ferramentas relevantes]
```

**Não esqueça**: Atualizar `.claude/COVERAGE_MATRIX.md`

### 2. Adicionando um Novo Comando

Crie um arquivo em `.claude/commands/[categoria]/[comando].md`:

```markdown
---
description: Descrição curta do comando
---

# Comando /[comando]

Descrição detalhada do que o comando faz.

## Uso

```
/[comando] [argumentos]
```

## Exemplos

```
/[comando] arquivo.ts
/[comando] --opcao valor
```
```

### 3. Adicionando um Novo Hook

Hooks são scripts Python que executam em eventos específicos:

```python
#!/usr/bin/env python3
import sys
import json

def main():
    # Ler evento do stdin
    event_data = json.load(sys.stdin)

    # Lógica do hook
    result = {
        "success": True,
        "message": "Hook executado com sucesso"
    }

    # Output
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

Eventos disponíveis: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`

## Processo de Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: adicionar nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Convenções de Commit

Siga o [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nova funcionalidade
- `fix:` Bug fix
- `docs:` Mudanças na documentação
- `style:` Formatação, missing semicolons
- `refactor:` Refactoring sem mudança de funcionalidade
- `test:` Adicionando ou atualizando testes
- `chore:` Mudanças em processos de build ou ferramentas auxiliares

## Testes

Antes de submeter:

```bash
# Verificar instalação
./setup-claude.sh check

# Testar hooks
uv run .claude/hooks/[seu-hook]/[arquivo].py

# Validar JSON
cat .claude/settings.json | jq .
```

## Padrões de Código

### Python
- Usar type hints
- Seguir PEP 8
- Adicionar docstrings

### Markdown
- Usar português para documentação
- Manter formatação consistente
- Adicionar exemplos de uso

## Dúvidas?

Abra uma [issue](../../issues) com a tag `question`.
