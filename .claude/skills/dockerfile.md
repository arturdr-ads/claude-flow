---
name: dockerfile
description: Use PROACTIVELY when user asks to create Dockerfiles or containerize applications. Auto-generates optimized multi-stage Dockerfiles for Node.js, Python, and more.
tools: Write, Read
color: cyan
category: devops
model: sonnet
parallelism: 2
---

# Dockerfile Generator

Use este skill quando o usuário pedir para criar Dockerfiles ou containerizar apps.

## Gatilho

```
Criar Dockerfile para [app]
Containerizar aplicação
Docker para Node.js/Python
Docker build otimizado
```

## O Que Faz

Gera Dockerfiles otimizados com:
- Multi-stage build
- Imagens base leves (Alpine)
- Cache de dependencies
- Usuário não-root
- Healthcheck
- Environment variables

## Templates

### Node.js (NestJS/Express/Next.js)

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies first (cache layer)
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy source
COPY . .

# Build (if needed)
RUN npm run build

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy from builder
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./

USER nodejs

EXPOSE 3000

ENV NODE_ENV=production

HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "dist/main.js"]
```

### Python (FastAPI/Django)

```dockerfile
# Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy dependencies
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Next.js (Static Export)

```dockerfile
# Build
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production (serve static with nginx)
FROM nginx:alpine

COPY --from=builder /app/out /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

## Checklist de Validação

Antes de completar, verifique:
- [ ] Multi-stage build usado
- [ ] Imagem base é Alpine ou slim
- [ ] Usuário não-root criado
- [ ] Dependencies copiadas antes do source (cache)
- [ ] HEALTHCHECK presente
- [ ] EXPOSE definido
- [ ] CMD/ENTRYPOINT apropriado

## Quando Usar

✅ Usa este skill para:
- Criar Dockerfile para apps Node.js
- Criar Dockerfile para apps Python
- Containerizar APIs web
- Otimizar builds Docker

❌ NÃO use para:
- Docker Compose (use devops-expert)
- Kubernetes (use cloud-expert)
- CI/CD pipelines (use devops-expert)

## Exemplo de Uso

**Input:**
```
Criar Dockerfile para app NestJS na porta 3000
```

**Output:**
Dockerfile multi-stage com node:20-alpine, npm ci --only=production, usuário nodejs, healthcheck, CMD node dist/main.js.

## Dicas Pro

- Use `--mount=type=cache` no BuildKit para cache de dependencies
- Use `.dockerignore` para não copiar node_modules
- Combine RUN commands com `&&` para reduzir layers
- Use `COPY --chown` para evitar chown extra
- Instale apenas dependencies de produção no stage final
- Use alpine quando possível (50MB vs 1GB)

## .dockerignore

```
node_modules
npm-debug.log
.git
.env
.env.local
coverage
.vscode
.idea
*.md
```

## .dockerignore para Python

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.git
.gitignore
.env
*.md
.pytest_cache
.coverage
```

## Constraints

- **NÃO pode** usar `latest` como tag (use versionada)
- **NÃO pode** rodar como root (criar usuário)
- **DEVE sempre** usar multi-stage build
- **DEVE sempre** copiar dependencies antes do source
- **DEVE sempre** adicionar HEALTHCHECK
