---
name: nestjs-controller
description: Use PROACTIVELY when user asks to create NestJS controllers, routes, or endpoints. Auto-generates controllers with DTOs, validation, and Swagger documentation.
tools: Write, Read, Edit, Grep
color: green
category: backend
model: sonnet
parallelism: 2
---

# NestJS Controller Generator

Use este skill quando o usuário pedir para criar controllers ou endpoints NestJS.

## Gatilho

```
Criar controller [Resource] em NestJS
Nova rota POST/GET/PUT/DELETE
Endpoint para [funcionalidade]
API de [recurso]
```

## O Que Faz

Gera controllers NestJS completos com:
- DTOs com class-validator
- Swagger/OpenAPI documentation
- CRUD padrão (Create, Read, Update, Delete)
- Status codes apropriados
- Error handling

## Template

Controller com DTOs e Validação

```typescript
import { Controller, Get, Post, Put, Delete, Body, Param, HttpCode, HttpStatus } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { [ServiceName]Service } from './[service-name].service';
import { Create[Resource]Dto, Update[Resource]Dto } from './dto';

@ApiTags('[resources]')
@Controller('[resources]')
export class [Resource]Controller {
  constructor(private readonly [serviceVariable]: [ServiceName]Service) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Create new [resource]' })
  @ApiResponse({ status: 201, description: '[Resource] created successfully' })
  @ApiResponse({ status: 400, description: 'Bad Request' })
  async create(@Body() createDto: Create[Resource]Dto) {
    return this.[serviceVariable].create(createDto);
  }

  @Get()
  @ApiOperation({ summary: 'Get all [resources]' })
  @ApiResponse({ status: 200, description: 'List of [resources]' })
  async findAll() {
    return this.[serviceVariable].findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get [resource] by ID' })
  @ApiResponse({ status: 200, description: '[Resource] found' })
  @ApiResponse({ status: 404, description: '[Resource] not found' })
  async findOne(@Param('id') id: string) {
    return this.[serviceVariable].findOne(id);
  }

  @Put(':id')
  @ApiOperation({ summary: 'Update [resource]' })
  @ApiResponse({ status: 200, description: '[Resource] updated' })
  @ApiResponse({ status: 404, description: '[Resource] not found' })
  async update(
    @Param('id') id: string,
    @Body() updateDto: Update[Resource]Dto,
  ) {
    return this.[serviceVariable].update(id, updateDto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  @ApiOperation({ summary: 'Delete [resource]' })
  @ApiResponse({ status: 204, description: '[Resource] deleted' })
  @ApiResponse({ status: 404, description: '[Resource] not found' })
  async remove(@Param('id') id: string) {
    return this.[serviceVariable].remove(id);
  }
}
```

DTOs (Salvar em `dto.ts`)

```typescript
import { IsString, IsNotEmpty, IsOptional, MinLength } from 'class-validator';

export class Create[Resource]Dto {
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  name: string;

  @IsString()
  @IsOptional()
  description?: string;
}

export class Update[Resource]Dto {
  @IsString()
  @IsOptional()
  name?: string;

  @IsString()
  @IsOptional()
  description?: string;
}
```

## Checklist de Validação

Antes de completar, verifique:
- [ ] Controller tem decorator @Controller com rota
- [ ] Todos métodos HTTP têm @ApiOperation
- [ ] DTOs usam class-validator decorators
- [ ] Status codes corretos (201, 200, 204, 404)
- [ ] Service injetado no constructor
- [ ] Parâmetros tipados corretamente

## Quando Usar

✅ Usa este skill para:
- Criar novos controllers CRUD
- Adicionar endpoints a controllers existentes
- Criar DTOs com validação

❌ NÃO use para:
- Guards/Interceptors (use security-expert)
- Database logic (use database-expert)
- Complex business logic

## Exemplo de Uso

**Input:**
```
Criar controller Products com endpoints CRUD completo
com validação de nome (obrigatório, min 3 chars)
```

**Output:**
ProductsController com CreateProductDto/UpdateProductDto, validação class-validator, Swagger docs em todos endpoints.

## Dicas Pro

- Use `@IsOptional()` para campos nullable
- Use `HttpCode(HttpStatus.NO_CONTENT)` para DELETE
- Nomeie DTOs como `Create{Resource}Dto` e `Update{Resource}Dto`
- Extraia DTOs para arquivo `dto.ts` separado
- Use `@ApiTags()` para agrupar no Swagger UI

## Constraints

- **NÃO pode** criar sem DTOs (mesmo que vazios)
- **DEVE sempre** adicionar @ApiOperation em cada endpoint
- **DEVE sempre** usar class-validator nos DTOs
- **DEVE sempre** tipar parâmetros com @Param, @Body, @Query
