---
name: react-component
description: Use PROACTIVELY when user asks to create React components with TypeScript + Tailwind. Auto-generates functional components with proper typing, hooks, and styling.
tools: Write, Read, Edit
color: blue
category: frontend
model: sonnet
parallelism: 2
---

# React Component Generator

Use este skill quando o usuário pedir para criar componentes React.

## Gatilho

```
Criar componente [Nome] com React
Novo componente de [funcionalidade]
Componente para exibir [algo]
```

## O Que Faz

Gera componentes React funcionais com:
- TypeScript com interfaces tipadas
- Tailwind CSS para estilização
- Hooks customizados se necessário
- Acessibilidade (ARIA)
- Props validadas

## Template

Componente Funcional com TypeScript

```typescript
import React from 'react';

interface [ComponentName]Props {
  // Define props aqui
  title: string;
  data?: [DataType];
  onAction?: (item: [DataType]) => void;
}

export const [ComponentName]: React.FC<[ComponentName]Props> = ({
  title,
  data = [],
  onAction,
}) => {
  // Hooks e estado
  const [isLoading, setIsLoading] = React.useState(false);

  // Handlers
  const handleClick = (item: [DataType]) => {
    onAction?.(item);
  };

  return (
    <div className="[tailwind-classes]">
      <h2 className="text-xl font-bold">{title}</h2>

      {isLoading ? (
        <p>Carregando...</p>
      ) : (
        <ul className="space-y-2">
          {data.map((item, index) => (
            <li
              key={item.id || index}
              className="p-2 hover:bg-gray-100 rounded cursor-pointer"
              onClick={() => handleClick(item)}
              role="button"
              tabIndex={0}
              aria-label={`Ação para ${item.name}`}
            >
              {item.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default [ComponentName];
```

## Checklist de Validação

Antes de completar, verifique:
- [ ] Componente é funcional (não classe)
- [ ] TypeScript com interfaces tipadas
- [ ] Tailwind classes presentes
- [ ] Props com defaults e opcionais marcados
- [ ] Acessibilidade (aria-label, role, tabIndex)
- [ ] Key correta em map/loops

## Quando Usar

✅ Usa este skill para:
- Criar componentes de UI
- Componentes com listas/arrays
- Componentes com interação
- Wrapper components

❌ NÃO use para:
- Páginas completas (use page generator)
- Redux/Context logic
- Performance otimização avançada

## Exemplo de Uso

**Input:**
```
Criar componente ProductList que recebe array de produtos com id, name, price
e tem clique para adicionar ao carrinho
```

**Output:**
Componente com interface ProductListProps, mapeamento de produtos, handler onClick, Tailwind classes, acessibilidade.

## Dicas Pro

- Use `?.()` para callbacks opcionais
- Sempre forneça `default={[]}` para arrays
- Adicione `aria-label` em elementos interativos
- Use `role="button"` em divs clicáveis
- Prefixe classes com `hover:`, `focus:` para interação

## Constraints

- **NÃO pode** usar componentes de classe (só funcionais)
- **DEVE sempre** tipar props com interface
- **DEVE sempre** adicionar aria-labels em elementos interativos
- **DEVE sempre** usar keys únicas em map()
