# Adaptive Hooks System

Sistema de hooks adaptativo e inteligente para Claude Code CLI.

## Como Funciona

O sistema detecta automaticamente o tipo de projeto e executa os hooks apropriados:

1. **Deteccao**: Analisa arquivos de configuracao do projeto
2. **Cache**: Armazena o resultado em `~/.cache/claude-hooks/` para execucao rapida
3. **Execucao**: Roda apenas os hooks relevantes para o projeto detectado

## Tipos de Projeto Suportados

### Node.js
**Detectado por**: `package.json`

**Framework especificos detectados**:
- Next.js, Nuxt.js, React, Vue, Svelte, Angular
- NestJS, Express, Fastify, Koa
- Remix, Astro

**Hooks ativados**:
| Hook | Descricao | Quando |
|------|-----------|--------|
| syntax-check-js | Verificacao de sintaxe JavaScript/TypeScript | Sempre |
| eslint | Lint com ESLint | Se .eslintrc* ou eslint.config.* existe |
| tsc | Type checking | Se tsconfig.json existe |
| prettier-check | Verificacao de formato | Se .prettierrc* existe |

### Python
**Detectado por**: `requirements.txt`, `pyproject.toml`, `setup.py`

**Framework especificos detectados**:
- Django, FastAPI, Flask, Tornado, AIOHTTP

**Hooks ativados**:
| Hook | Descricao | Quando |
|------|-----------|--------|
| syntax-check-py | Verificacao de sintaxe Python | Sempre |
| ruff-check | Lint com Ruff | Se ruff disponivel |
| mypy | Type checking | Se configurado no pyproject.toml |
| pytest-quick | Testes rapidos | Se pytest.ini ou pyproject.toml existe |

### Rust
**Detectado por**: `Cargo.toml`

**Hooks ativados**:
| Hook | Descricao |
|------|-----------|
| cargo-check | Verificacao de compilacao |
| cargo-clippy | Linter Clippy |
| cargo-test | Testes |
| cargo-fmt-check | Verificacao de formato |

### Go
**Detectado por**: `go.mod`

**Hooks ativados**:
| Hook | Descricao |
|------|-----------|
| golangci-lint | Linter (se disponivel) |
| go-vet | Analise estatica |
| go-test | Testes |
| gofmt-check | Verificacao de formato |

### Java
**Detectado por**: `pom.xml` (Maven), `build.gradle*` (Gradle)

**Hooks ativados**:
| Hook | Descricao |
|------|-----------|
| mvn-test | Testes Maven |
| gradle-test | Testes Gradle |

### C#/.NET
**Detectado por**: `*.csproj`

**Hooks ativados**:
| Hook | Descricao |
|------|-----------|
| dotnet-build | Build/validacao |

### Docker
**Detectado por**: `Dockerfile`, `docker-compose.yml`

**Hooks ativados**:
| Hook | Descricao |
|------|-----------|
| hadolint | Lint Dockerfile (se hadolint disponivel) |
| docker-compose-validate | Validar configuracao |

## Uso

### Comandos diretos
```bash
# Listar projetos detectados
uv run .claude/hooks/adaptive/adaptive_hooks.py --list-profiles

# Listar hooks disponiveis
uv run .claude/hooks/adaptive/adaptive_hooks.py --list-hooks

# Listar com comandos completos
uv run .claude/hooks/adaptive/adaptive_hooks.py --list-hooks --verbose

# Apenas detectar tipo de projeto
uv run .claude/hooks/adaptive/adaptive_hooks.py --detect-only

# Forcar刷新 do cache
uv run .claude/hooks/adaptive/adaptive_hooks.py --force-refresh
```

### Integracao com settings.json
Ja configurado em `/home/arturdr/Claude/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/adaptive/adaptive_hooks.py --event PostToolUse"
          }
        ]
      }
    ]
  }
}
```

## Configuracao Customizada

Crie `.claude/hooks/adaptive/adaptive_hooks_config.json` para customizar hooks:

```json
{
  "hooks": {
    "nodejs": {
      "post_tool_hooks": [
        {
          "name": "my-custom-hook",
          "command": "echo 'Running custom hook'",
          "description": "My custom hook",
          "timeout_seconds": 30,
          "enabled": true
        }
      ]
    }
  }
}
```

Veja `adaptive_hooks_config.example.json` para exemplos completos.

## Variaveis de Template

Os comandos suportam variaveis:
- `{changed_files}` - Arquivos modificados (com aspas)
- `{changed_files_list}` - Arquivos modificados (sem aspas)
- `{root}` - Diretorio raiz do projeto

## Projetos Poliglotas

O sistema suporta multiplos tipos de projeto simultaneamente. Por exemplo, um projeto com frontend Next.js e backend Python tera hooks de ambos.

## Cache

O cache fica em `~/.cache/claude-hooks/project_profile.json` e e invalidado automaticamente quando arquivos de configuracao sao modificados.
