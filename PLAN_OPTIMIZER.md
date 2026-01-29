# Plano de Implementação - Prompt Optimizer Integrado

## Status: 🟡 PLANEJAMENTO

**Objetivo:** Implementar Prompt Optimizer que respeita nossa hierarquia de cores, paralelismo dinâmico e integra com swarms.

---

## Contexto Atual

### ✅ Já Existe
1. **`.claude/agents/prompt-optimizer.md`** - Agente especialista (cor cyan)
2. **`.claude/commands/optimize.md`** - Command `/optimize`
3. **`.claude/commands/optimize-prompt.md`** - Command para otimizar prompts de agentes
4. **`.claude/hooks/prompt_optimizer.py`** - Hook automático (UserPromptSubmit)
5. **`.claude/hooks/auto_parallelism.py`** - Detecção de RAM para paralelismo

### ❌ Problemas Identificados
1. **Hook automático vs Manual**: `prompt_optimizer.py` roda em TODOS os prompts automaticamente
2. **Tag `<optimize>` não implementada**: Command existe mas hook não respeita a tag
3. **Sem integração com hierarquia de cores**: Não recomenda agentes baseados nas 7 camadas
4. **Sem integração com swarms**: Não usa Task tool para sugerir agentes
5. **Código duplicado**: `optimize.md` e `optimize-prompt.md` têm propósitos similares

### 🎯 Requisitos Claros
- **Tag MANUAL**: Só ativa com `<optimize>` (não automático)
- **Hierarquia de 7 cores**: Recomenda agentes baseados nas camadas
- **Paralelismo dinâmico**: Respeita limites do auto_parallelism.py
- **Integração swarms**: Usa Task tool para recomendar agentes
- **Output em português**: Segue padrão do sistema
- **Patterns TDD + Constraints + Output Validation**: Mantém estrutura

---

## Arquitetura da Solução

### Hierarquia de Cores (7 camadas)

```
🟣 Purple (4 agents) - Orquestração & Estratégia
├─ orchestrator-expert
├─ architect-expert
├─ product-expert
└─ ux-expert

🔵 Blue (6 agents) - Implementação Core
├─ frontend-expert
├─ backend-expert
├─ database-expert
├─ server-expert
├─ mobile-expert
└─ desktop-expert

🟢 Green (3 agents) - Qualidade
├─ testing-expert
├─ security-expert
└─ code-review-expert

🟠 Orange (4 agents) - Infraestrutura & Deploy
├─ devops-expert
├─ cloud-expert
├─ build-tools-expert
└─ monitoring-expert

🟡 Yellow (4 agents) - Tooling & Linguagens
├─ cli-expert
├─ typescript-expert
├─ ai-sdk-expert
└─ refactoring-expert

🩷 Pink (3 agents) - Conhecimento & Documentação
├─ documentation-expert
├─ research-expert
└─ llm-ai-agents-and-eng-research

🔴 Cyan (4 agents) - Meta & Sistema
├─ meta-agent
├─ oracle
├─ code-search
└─ triage-expert
```

### Fluxo de Otimização

```
┌─────────────────────────────────────────────────────────────┐
│  1. USUÁRIO insere <optimize> no prompt                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  2. HOOK detecta tag <optimize>                             │
│     - Verifica se tag está presente                         │
│     - Se NÃO: passa prompt sem modificação                  │
│     - Se SIM: inicia otimização                             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  3. PROMPT OPTIMIZER analisa o prompt                       │
│     - Identifica domínio/tipo de tarefa                     │
│     - Mapeia para hierarquia de cores                       │
│     - Recomenda agentes apropriados                         │
│     - Adiciona estrutura TDD + Constraints                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  4. OUTPUT otimizado com recomendações                      │
│     - Prompt estruturado                                     │
│     - Lista de agentes recomendados (com cores)             │
│     - Sugestão de uso Task tool se multi-agente             │
└─────────────────────────────────────────────────────────────┘
```

---

## Plano de Implementação

### FASE 1: Preparação & Limpeza (30 min)

#### 1.1 Backup do código atual
```bash
# Criar backup do hook automático antigo
cp .claude/hooks/prompt_optimizer.py .claude/hooks/prompt_optimizer.py.backup

# Documentar o que vai mudar
echo "# Migrando de automático para manual (<optimize>)" >> .claude/MIGRATION.md
```

#### 1.2 Consolidar comandos
```bash
# Analisar diferenças entre:
# - optimize.md (para otimizar prompts de usuário)
# - optimize-prompt.md (para otimizar prompts de agentes)

# Decisão: Manter ambos com propósitos distintos
# - /optimize: Para prompts de usuário (com tag <optimize>)
# - /optimize-prompt: Para melhorar prompts de agentes existentes
```

#### 1.3 Remover código duplicado/obsoleto
```bash
# Identificar arquivos que serão removidos após migração
# - prompt_optimizer.py (será substituído por optimize_hook.py)
# - Salvar apenas como .backup
```

---

### FASE 2: Criar Novo Hook Manual (45 min)

#### 2.1 Criar `.claude/hooks/optimize_hook.py`

**Especificações:**

```python
#!/usr/bin/env python3
"""
Manual Prompt Optimizer Hook

Ativa SOMENTE quando detecta tag <optimize> no prompt.
Respeita hierarquia de 7 cores e paralelismo dinâmico.
Matcher: UserPromptSubmit
"""

import sys
import os
import json
import re
from pathlib import Path

# Hierarquia de cores (7 camadas)
COLOR_HIERARCHY = {
    'purple': {  # Orquestração & Estratégia
        'agents': ['orchestrator-expert', 'architect-expert', 'product-expert', 'ux-expert'],
        'keywords': ['projeto', 'planejamento', 'arquitetura', 'produto', 'ux', 'design', 'coordenar']
    },
    'blue': {  # Implementação Core
        'agents': ['frontend-expert', 'backend-expert', 'database-expert', 'server-expert', 'mobile-expert', 'desktop-expert'],
        'keywords': ['api', 'componente', 'banco de dados', 'server', 'mobile', 'app', 'frontend', 'backend']
    },
    'green': {  # Qualidade
        'agents': ['testing-expert', 'security-expert', 'code-review-expert'],
        'keywords': ['teste', 'segurança', 'review', 'qualidade', 'vulnerabilidade']
    },
    'orange': {  # Infraestrutura & Deploy
        'agents': ['devops-expert', 'cloud-expert', 'build-tools-expert', 'monitoring-expert'],
        'keywords': ['deploy', 'docker', 'kubernetes', 'aws', 'cloud', 'ci/cd', 'monitoramento', 'infra']
    },
    'yellow': {  # Tooling & Linguagens
        'agents': ['cli-expert', 'typescript-expert', 'ai-sdk-expert', 'refactoring-expert'],
        'keywords': ['cli', 'typescript', 'refatoração', 'refactoring', 'tipos']
    },
    'pink': {  # Conhecimento & Documentação
        'agents': ['documentation-expert', 'research-expert', 'llm-ai-agents-and-eng-research'],
        'keywords': ['documentação', 'docs', 'pesquisa', 'research', 'ai', 'llm']
    },
    'cyan': {  # Meta & Sistema
        'agents': ['meta-agent', 'oracle', 'code-search', 'triage-expert'],
        'keywords': ['meta', 'oracle', 'buscar código', 'code search', 'triage']
    }
}

def has_optimize_tag(prompt: str) -> bool:
    """Verifica se prompt contém tag <optimize>"""
    return '<optimize>' in prompt.lower()

def detect_domain(prompt: str) -> list:
    """
    Detecta domínio da tarefa baseado em keywords
    Retorna lista de cores relevantes (em ordem de prioridade)
    """
    prompt_lower = prompt.lower()
    detected_colors = []

    for color, data in COLOR_HIERARCHY.items():
        if any(keyword in prompt_lower for keyword in data['keywords']):
            detected_colors.append(color)

    return detected_colors

def recommend_agents(prompt: str, detected_colors: list) -> list:
    """
    Recomenda agentes baseados no domínio detectado
    Retorna lista de tuplas: (agent_name, color, reason)
    """
    recommendations = []

    for color in detected_colors:
        for agent in COLOR_HIERARCHY[color]['agents']:
            # Adiciona lógica específica por agente
            if agent == 'orchestrator-expert':
                if any(kw in prompt.lower() for kw in ['projeto completo', 'sistema', 'do zero', 'coordenar']):
                    recommendations.append((agent, color, 'Multi-agente complexo'))
            elif agent == 'frontend-expert':
                if any(kw in prompt.lower() for kw in ['componente', 'ui', 'frontend', 'react', 'vue']):
                    recommendations.append((agent, color, 'Implementação frontend'))
            # ... adicionar lógica para outros agentes

    return recommendations

def read_parallelism_config() -> dict:
    """Lê configuração de paralelismo do auto_parallelism.py"""
    config_file = Path.cwd() / '.claude' / 'auto_config.json'
    if config_file.exists():
        return json.loads(config_file.read_text())
    return {'parallelism': 2, 'orchestrator_parallelism': 1}

def optimize_prompt(prompt: str) -> str:
    """
    Otimiza prompt com estrutura TDD + Constraints + recomendações de agentes
    """
    # Remove tag <optimize>
    clean_prompt = prompt.replace('<optimize>', '').strip()

    # Detecta domínio
    detected_colors = detect_domain(clean_prompt)
    recommendations = recommend_agents(clean_prompt, detected_colors)

    # Lê paralelismo
    parallelism_config = read_parallelism_config()

    # Constrói prompt otimizado
    optimized = f"""## 🎯 Prompt Otimizado

Seu request foi estruturado com melhores práticas Anthropic + TDD + nossa hierarquia de agentes.

---

## Prompt Original
{clean_prompt}

---

## 🎯 Objetivo Clarificado
[Objetivo principal detectado]

---

## 📋 Requisitos Específicos
- [RF-001] [Requisito funcional 1]
- [RF-002] [Requisito funcional 2]

---

## ⚠️ Constraints & Limitations
- **NÃO pode** [limitação clara]
- **DEVE sempre** [regra obrigatória]
- **SE** [condição] → delegar para [agente especialista]

---

## 🧪 Test-Driven Development
1. **RED**: [O que testar primeiro]
2. **GREEN**: [Como fazer funcionar]
3. **REFACTOR**: [Como melhorar]

---

## ✅ Output Validation
Antes de completar:
- [ ] Todos requisitos atendidos
- [ ] Código compila/roda sem erros
- [ ] Testes passam (se aplicável)
- [ ] Best practices seguidas

---

## 👥 Agentes Recomendados (Hierarquia de Cores)
"""

    # Adiciona recomendações de agentes
    if recommendations:
        for agent, color, reason in recommendations[:5]:  # Max 5 recomendações
            emoji = {
                'purple': '🟣', 'blue': '🔵', 'green': '🟢',
                'orange': '🟠', 'yellow': '🟡', 'pink': '🩷', 'cyan': '🔴'
            }.get(color, '⚪')
            optimized += f"\n{emoji} **{agent}**: {reason}\n"

        # Adiciona sugestão de Task tool se multi-agente
        if len(recommendations) > 1:
            optimized += f"""
## 🔄 Multi-Agente? Use Task Tool

Se precisar coordenar múltiplos agentes:

```
Task(description="Coordenar projeto", prompt="orchestrator-expert: {clean_prompt[:100]}...")
```

**Paralelismo Disponível:** {parallelism_config['parallelism']} agentes simultâneos
"""

    return optimized

def main():
    """Main hook function"""
    try:
        # Read JSON input
        input_data = json.loads(sys.stdin.read())

        # Extract prompt
        prompt = None
        for field in ['prompt', 'content', 'userPrompt', 'request']:
            if field in input_data:
                prompt = input_data[field]
                break

        if not prompt:
            # No prompt, pass through
            print(json.dumps(input_data))
            sys.exit(0)

        # Check for <optimize> tag
        if not has_optimize_tag(prompt):
            # No tag, pass through unchanged
            print(json.dumps(input_data))
            sys.exit(0)

        # Tag found, optimize prompt
        optimized = optimize_prompt(prompt)

        # Update prompt field
        for field in ['prompt', 'content', 'userPrompt', 'request']:
            if field in input_data:
                input_data[field] = optimized
                break

        # Add hook output
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PromptOptimized",
                "originalLength": len(prompt),
                "optimizedLength": len(optimized),
                "optimizationApplied": True,
                "tagDetected": "<optimize>"
            }
        }

        input_data.update(output)

        # Output optimized data
        print(json.dumps(input_data))
        sys.exit(0)

    except json.JSONDecodeError:
        # Not JSON, plain text
        stdin_text = sys.stdin.read()
        if has_optimize_tag(stdin_text):
            optimized = optimize_prompt(stdin_text)
            print(optimized)
        else:
            print(stdin_text)
        sys.exit(0)
    except Exception as e:
        # Fail silently
        import logging
        logging.basicConfig(filename='logs/optimize_hook_errors.log', level=logging.ERROR)
        logging.error(f"Error in optimize_hook: {type(e).__name__}: {e}")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

#### 2.2 Testar hook manualmente
```bash
# Testar com tag <optimize>
echo '{"prompt": "<optimize> cria uma api de usuarios"}' | python3 .claude/hooks/optimize_hook.py

# Testar sem tag (deve passar sem modificação)
echo '{"prompt": "cria uma api de usuarios"}' | python3 .claude/hooks/optimize_hook.py
```

---

### FASE 3: Atualizar settings.json (15 min)

#### 3.1 Modificar `.claude/settings.json`

**Antes:**
```json
"UserPromptSubmit": [
  {
    "matcher": "*",
    "hooks": [
      {"type": "command", "command": "python3 .claude/hooks/prompt_optimizer.py"}
    ]
  }
]
```

**Depois:**
```json
"UserPromptSubmit": [
  {
    "matcher": "*",
    "hooks": [
      {"type": "command", "command": "uv run .claude/hooks/optimize_hook.py"}
    ]
  }
]
```

#### 3.2 Validar mudança
```bash
# Verificar que settings.json é válido
cat .claude/settings.json | jq .

# Testar reload do Claude Code
# (reiniciar sessão)
```

---

### FASE 4: Atualizar Agente prompt-optimizer.md (30 min)

#### 4.1 Revisar `.claude/agents/prompt-optimizer.md`

**Mudanças necessárias:**

1. **Adicionar seção sobre hierarquia de cores**
2. **Documentar integração com Task tool**
3. **Atualizar exemplos com novos agentes**
4. **Adicionar lógica de recomendação de agentes**

**Conteúdo a adicionar:**

```markdown
## Hierarquia de Cores - Sistema de 7 Camadas

Quando otimizar prompts, recomende agentes baseados na cor apropriada:

### 🟣 Purple - Orquestração & Estratégia
Use para: Projetos complexos, decisões de arquitetura, planejamento
- **orchestrator-expert**: Coordenar múltiplos agentes
- **architect-expert**: Decisões de stack e padrões
- **product-expert**: Requisitos e priorização
- **ux-expert**: Jornadas e wireframes

### 🔵 Blue - Implementação Core
Use para: Desenvolvimento de código
- **frontend-expert**: React, Vue, Angular, UI
- **backend-expert**: APIs, Node.js, Python, Go
- **database-expert**: PostgreSQL, MongoDB, queries
- **server-expert**: Linux, systemd, nginx
- **mobile-expert**: React Native, Flutter
- **desktop-expert**: Electron, Tauri

### 🟢 Green - Qualidade
Use para: Testes, segurança, review
- **testing-expert**: Jest, Vitest, Playwright
- **security-expert**: OWASP, pentest, hardening
- **code-review-expert**: Review multi-aspect

### 🟠 Orange - Infraestrutura & Deploy
Use para: Deploy, containers, cloud
- **devops-expert**: Docker, CI/CD, K8s
- **cloud-expert**: AWS, GCP, Azure
- **build-tools-expert**: Vite, Webpack, esbuild
- **monitoring-expert**: Prometheus, Grafana

### 🟡 Yellow - Tooling & Linguagens
Use para: Ferramentas de desenvolvimento
- **cli-expert**: CLI tools, scripts
- **typescript-expert**: Types, generics
- **ai-sdk-expert**: Anthropic SDK, AI tools
- **refactoring-expert**: Refatoração de código

### 🩷 Pink - Conhecimento & Documentação
Use para: Docs, pesquisa, learning
- **documentation-expert**: README, API docs
- **research-expert**: Deep research
- **llm-ai-agents-and-eng-research**: AI/LLM research

### 🔴 Cyan - Meta & Sistema
Use para: Meta-tarefas, busca, diagnóstico
- **meta-agent**: Meta-cognitive tasks
- **oracle**: Knowledge retrieval
- **code-search**: Busca de código
- **triage-expert**: Diagnóstico de problemas

## Integração com Task Tool

Quando múltiplos agentes forem recomendados, sugira uso do Task tool:

```
Task(description="Implementar feature completa", prompt="""
orchestrator-expert: Coordenar projeto de X

Frontend: frontend-expert
Backend: backend-expert
Database: database-expert
Quality: testing-expert
""")
```

**Paralelismo dinâmico:**
- Sistema detecta RAM automaticamente (auto_parallelism.py)
- 16GB RAM → 2 agentes simultâneos
- Respeite limites do sistema
```

---

### FASE 5: Testes & Validação (45 min)

#### 5.1 Criar suite de testes

**Arquivo:** `tests/test_optimize_hook.py`

```python
#!/usr/bin/env python3
"""
Testes para optimize_hook.py
"""

import json
import sys
from pathlib import Path

# Add .claude/hooks to path
sys.path.insert(0, str(Path(__file__).parent.parent / '.claude' / 'hooks'))

import optimize_hook

def test_has_optimize_tag():
    """Testa detecção da tag <optimize>"""
    assert optimize_hook.has_optimize_tag("<optimize> cria api") == True
    assert optimize_hook.has_optimize_tag("cria api") == False
    assert optimize_hook.has_optimize_tag("<OPTIMIZE> cria api") == True  # Case insensitive

def test_detect_domain():
    """Testa detecção de domínio"""
    # Frontend
    colors = optimize_hook.detect_domain("criar componente react")
    assert 'blue' in colors

    # Infrastructure
    colors = optimize_hook.detect_domain("configurar docker kubernetes")
    assert 'orange' in colors

    # Multiple domains
    colors = optimize_hook.detect_domain("api com testes e deploy")
    assert 'blue' in colors
    assert 'green' in colors
    assert 'orange' in colors

def test_recommend_agents():
    """Testa recomendação de agentes"""
    recommendations = optimize_hook.recommend_agents(
        "criar sistema completo com frontend e backend",
        ['purple', 'blue']
    )

    agent_names = [agent for agent, _, _ in recommendations]
    assert 'orchestrator-expert' in agent_names
    assert 'frontend-expert' in agent_names
    assert 'backend-expert' in agent_names

def test_full_optimization():
    """Testa otimização completa"""
    original = "<optimize> cria uma api de usuarios"
    optimized = optimize_hook.optimize_prompt(original)

    # Verifica estrutura
    assert "## Objetivo Clarificado" in optimized
    assert "## Requisitos Específicos" in optimized
    assert "## Constraints & Limitations" in optimized
    assert "## Test-Driven Development" in optimized
    assert "## Output Validation" in optimized
    assert "## Agentes Recomendados" in optimized

    # Verifica que tag foi removida
    assert "<optimize>" not in optimized

def test_pass_through_without_tag():
    """Testa que prompts sem tag passam sem modificação"""
    import io
    import contextlib

    # Simula stdin JSON
    input_data = {"prompt": "cria uma api"}
    stdin = io.StringIO(json.dumps(input_data))

    # Captura stdout
    stdout = io.StringIO()

    with contextlib.redirect_stdin(stdin):
        with contextlib.redirect_stdout(stdout):
            optimize_hook.main()

    output = json.loads(stdout.getvalue())
    assert output["prompt"] == "cria uma api"  # Sem modificação

if __name__ == "__main__":
    test_has_optimize_tag()
    test_detect_domain()
    test_recommend_agents()
    test_full_optimization()
    test_pass_through_without_tag()
    print("✅ Todos os testes passaram!")
```

#### 5.2 Executar testes
```bash
# Criar diretório de tests
mkdir -p tests

# Executar testes
python3 tests/test_optimize_hook.py

# Deveria ver: "✅ Todos os testes passaram!"
```

#### 5.3 Testes manuais (cenários reais)

**Cenário 1: Prompt simples com tag**
```
<optimize> criar api de usuarios
```

**Esperado:**
- Prompt otimizado com estrutura completa
- Recomenda: backend-expert 🔵, database-expert 🔵
- Sugere TDD approach

**Cenário 2: Prompt sem tag**
```
criar api de usuarios
```

**Esperado:**
- Passa sem modificação
- Nenhuma otimização aplicada

**Cenário 3: Projeto complexo**
```
<optimize> criar sistema SaaS completo do zero
```

**Esperado:**
- Prompt otimizado
- Recomenda: orchestrator-expert 🟣, architect-expert 🟣, product-expert 🟣
- Sugere uso de Task tool
- Respeita paralelismo dinâmico

**Cenário 4: Multi-domínio**
```
<optimize> criar app mobile com backend e deploy
```

**Esperado:**
- Recomenda: mobile-expert 🔵, backend-expert 🔵, devops-expert 🟠
- Sugere Task tool para orquestração

---

### FASE 6: Documentação (30 min)

#### 6.1 Atualizar `.claude/CLAUDE.md`

**Adicionar seção:**

```markdown
### 6. Prompt Optimizer (NOVO)

**Tag MANUAL:** `<optimize>`

Otimiza prompts com estrutura TDD + Constraints + recomendações de agentes.

```bash
# Usar otimizador
<optimize> criar api de usuarios

# Projeto complexo
<optimize> criar sistema SaaS completo
```

**O que faz:**
- Estrutura prompt com Requisitos, Constraints, TDD, Output Validation
- Recomenda agentes baseados na hierarquia de 7 cores
- Sugere uso de Task tool para multi-agente
- Respeita paralelismo dinâmico do sistema

**Hierarquia de Cores:**
- 🟣 Purple: Orquestração (orchestrator, architect, product, ux)
- 🔵 Blue: Implementação (frontend, backend, database, server, mobile, desktop)
- 🟢 Green: Qualidade (testing, security, code-review)
- 🟠 Orange: Infra (devops, cloud, build-tools, monitoring)
- 🟡 Yellow: Tooling (cli, typescript, ai-sdk, refactoring)
- 🩷 Pink: Conhecimento (documentation, research, ai-research)
- 🔴 Cyan: Meta (meta-agent, oracle, code-search, triage)

**Paralelismo:**
- Auto-detectado via auto_parallelism.py
- 16GB RAM → 2 agentes simultâneos
- Respeite limites ao usar Task tool
```

#### 6.2 Criar `.claude/PROMPT_OPTIMIZER.md`

**Documentação completa:**

```markdown
# Prompt Optimizer - Sistema Manual

## Visão Geral

Otimizador de prompts que respeita nossa arquitetura de 28 agentes, hierarquia de 7 cores e paralelismo dinâmico.

## Como Usar

### Tag Manual

Adicione `<optimize>` ao início do seu prompt:

```
<optimize> criar api de usuarios
```

### O que Acontece

1. **Hook detecta tag** → `optimize_hook.py`
2. **Analisa domínio** → Detecta cores relevantes
3. **Recomenda agentes** → Baseado em keywords
4. **Estrutura prompt** → TDD + Constraints + Output Validation
5. **Sugere Task tool** → Se multi-agente

## Exemplos

### Exemplo 1: Backend API

**Input:**
```
<optimize> criar API de autenticação com JWT
```

**Output:**
- Objetivo clarificado
- Requisitos específicos (endpoints, validação)
- Constraints (não armazenar senha em texto)
- TDD approach (testes primeiro)
- Agentes recomendados: backend-expert 🔵, security-expert 🟢

### Exemplo 2: Projeto Completo

**Input:**
```
<optimize> criar sistema SaaS de gestão de projetos
```

**Output:**
- Objetivo clarificado
- Requisitos por camada (produto, UX, tech)
- Constraints (escalabilidade, segurança)
- Agentes recomendados: orchestrator-expert 🟣, architect-expert 🟣, product-expert 🟣
- Sugestão explícita de usar Task tool
- Paralelismo disponível: 2 agentes

### Exemplo 3: Frontend Component

**Input:**
```
<optimize> criar formulário de login com validação
```

**Output:**
- Objetivo clarificado
- Requisitos de UI e validação
- Acessibilidade (WCAG)
- Agentes recomendados: frontend-expert 🔵
- TDD para componentes React

## Hierarquia de Cores

Detalhes completos em `.claude/COVERAGE_MATRIX.md`

## Integração com Task Tool

Quando múltiplos agentes são recomendados:

```
Task(description="Sistema de gestão", prompt="""
orchestrator-expert: Coordenar projeto completo

Fases:
1. product-expert: Entender problema
2. ux-expert: Mapear jornadas
3. architect-expert: Definir stack
4. frontend-expert: Implementar UI
5. backend-expert: Implementar APIs
6. testing-expert: Testes E2E
""")
```

## Paralelismo Dinâmico

Configurado via `auto_parallelism.py`:
- Detecta RAM total do sistema
- 16GB → 2 agentes simultâneos
- Orchestrator usa parallelism-1

## Troubleshooting

### Tag não funciona
- Verifique se `<optimize>` está no prompt
- Confirme que `optimize_hook.py` está em settings.json
- Reinicie sessão do Claude Code

### Recomendações incorretas
- Keywords podem não cobrir seu caso
- Use agente específico manualmente
- Feedback via `/optimize-prompt [agente]`

### Paralelismo errado
- Verifique `.claude/auto_config.json`
- Ajuste manualmente se necessário
- Re-run `auto_parallelism.py`
```

#### 6.3 Atualizar `.claude/COVERAGE_MATRIX.md`

**Adicionar seção sobre Prompt Optimizer:**

```markdown
## Sistema de Otimização de Prompts

| Componente | Arquivo | Descrição |
|-----------|---------|-----------|
| **Hook Manual** | `optimize_hook.py` | Ativa com tag `<optimize>` |
| **Agente** | `prompt-optimizer.md` | Especialista em otimização |
| **Command** | `/optimize` | Documentação de uso |
| **Integration** | settings.json | UserPromptSubmit hook |

**Fluxo:**
1. Usuário insere `<optimize>`
2. Hook detecta e otimiza
3. Recomenda agentes por cor
4. Sugere Task tool se multi-agente
5. Respeita paralelismo dinâmico
```

---

### FASE 7: Cleanup & Remoção (15 min)

#### 7.1 Remover código antigo

```bash
# Mover para backup (não deletar ainda)
mv .claude/hooks/prompt_optimizer.py .claude/hooks/prompt_optimizer.py.old

# Criar nota de migração
cat > .claude/MIGRATION_OPTIMIZER.md << 'EOF'
# Migração Prompt Optimizer

## De: Automático → Para: Manual (<optimize>)

### Mudanças
- **Antes**: `prompt_optimizer.py` rodava em TODOS os prompts
- **Depois**: `optimize_hook.py` só roda com tag `<optimize>`

### Motivo
- Usuário quer controle manual
- Evita otimizações indesejadas
- Respeita intenções do usuário

### Backup
- Código antigo: `.claude/hooks/prompt_optimizer.py.old`
- Pode ser removido após 1 semana se tudo OK
EOF
```

#### 7.2 Validar não há quebras

```bash
# Testar que hook antigo não é mais referenciado
grep -r "prompt_optimizer.py" .claude/settings.json
# Deve retornar vazio ou apontar para optimize_hook.py

# Testar que novo hook funciona
echo '<optimize> teste' | uv run .claude/hooks/optimize_hook.py
# Deve retornar prompt otimizado
```

---

## Checklist de Implementação

### ✅ FASE 1: Preparação
- [ ] Backup de `prompt_optimizer.py`
- [ ] Análise de `optimize.md` vs `optimize-prompt.md`
- [ ] Documentar mudanças em `MIGRATION.md`

### ✅ FASE 2: Novo Hook
- [ ] Criar `optimize_hook.py` com lógica completa
- [ ] Implementar detecção de tag `<optimize>`
- [ ] Implementar mapeamento de 7 cores
- [ ] Implementar recomendação de agentes
- [ ] Implementar integração com auto_parallelism
- [ ] Testar hook manualmente

### ✅ FASE 3: Configuração
- [ ] Atualizar `settings.json` (UserPromptSubmit)
- [ ] Validar JSON válido
- [ ] Testar reload do Claude Code

### ✅ FASE 4: Agente Atualizado
- [ ] Adicionar seção de hierarquia de cores
- [ ] Documentar integração com Task tool
- [ ] Atualizar exemplos com novos agentes
- [ ] Adicionar lógica de recomendação

### ✅ FASE 5: Testes
- [ ] Criar `tests/test_optimize_hook.py`
- [ ] Testar detecção de tag
- [ ] Testar detecção de domínio
- [ ] Testar recomendação de agentes
- [ ] Testar otimização completa
- [ ] Testar pass-through sem tag
- [ ] Testar cenários manuais

### ✅ FASE 6: Documentação
- [ ] Atualizar `CLAUDE.md` com seção Prompt Optimizer
- [ ] Criar `PROMPT_OPTIMIZER.md` completo
- [ ] Atualizar `COVERAGE_MATRIX.md`
- [ ] Documentar hierarquia de 7 cores
- [ ] Documentar integração swarms

### ✅ FASE 7: Cleanup
- [ ] Mover `prompt_optimizer.py` para `.old`
- [ ] Criar nota de migração
- [ ] Validar não há referências ao código antigo
- [ ] Testar que novo hook funciona

---

## Estimativa de Tempo

| Fase | Tempo | Responsabilidade |
|------|-------|------------------|
| FASE 1 | 30 min | Preparação |
| FASE 2 | 45 min | Implementação principal |
| FASE 3 | 15 min | Configuração |
| FASE 4 | 30 min | Agente |
| FASE 5 | 45 min | Qualidade |
| FASE 6 | 30 min | Documentação |
| FASE 7 | 15 min | Cleanup |
| **TOTAL** | **3h** | **End-to-end** |

---

## Riscos & Mitigações

### Risco 1: Hook não detecta tag
**Mitigação:**
- Testar com case variations (`<OPTIMIZE>`, `< Optimize >`)
- Adicionar logging para debug
- Fallback silencioso (pass-through)

### Risco 2: Recomendações incorretas
**Mitigação:**
- Keywords bem definidas por cor
- Validação manual de exemplos
- Feedback loop com usuário

### Risco 3: Quebra de sistema
**Mitigação:**
- Backup completo antes de mudanças
- Testes exaustivos antes de deploy
- Rollback rápido (restaurar .backup)

### Risco 4: Performance
**Mitigação:**
- Hook roda só com tag (não em todos os prompts)
- Operações leves (string matching)
- Cache de config de paralelismo

---

## Success Criteria

### Funcional
- ✅ Tag `<optimize>` ativa otimização
- ✅ Sem tag = pass-through sem modificação
- ✅ Recomenda agentes baseados em cores
- ✅ Respeita paralelismo dinâmico
- ✅ Output em português

### Técnico
- ✅ Hook integrado em settings.json
- ✅ Testes passando (100%)
- ✅ Código legível e documentado
- ✅ Performance OK (<100ms por otimização)

### UX
- ✅ Fácil de usar (só adicionar tag)
- ✅ Recomendações úteis
- ✅ Não intrusivo (só quando pedido)
- ✅ Feedback claro (agents + cores)

---

## Próximos Passos

### Imediato (Após Implementação)
1. Executar checklist completo
2. Testar em ambiente real
3. Coletar feedback
4. Ajustar keywords se necessário

### Curto Prazo (1 semana)
1. Analisar logs de uso
2. Refinar recomendações
3. Adicionar mais keywords
4. Melhorar precisão de detecção

### Médio Prazo (1 mês)
1. Métricas de efetividade
2. Aprendizado com exemplos reais
3. Possível ML para recomendações
4. Integração com outros comandos

---

## Contato & Suporte

**Issues:** Reportar problemas em `/question`
**Melhorias:** Usar `/optimize-prompt prompt-optimizer`
**Documentação:** `.claude/PROMPT_OPTIMIZER.md`

---

**Status do Plano:** 🟡 PLANEJAMENTO → 🟢 PRONTO PARA IMPLEMENTAÇÃO
