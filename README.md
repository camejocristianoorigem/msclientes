# Microserviço de Gestão de Clientes

API RESTful assíncrona para cadastro e manutenção de clientes desenvolvida com FastAPI, SQLAlchemy 2.0 (AsyncIO), PostgreSQL e Redis.

## 🚀 Tecnologias e Ferramentas

- Linguagem: Python 3.14 (AsyncIO)
- Framework Web: FastAPI
- ORM & Banco de Dados: SQLAlchemy 2.0 (asyncpg), PostgreSQL 16
- Migrações: Alembic (Fluxo assíncrono)
- Cache: Redis 7 (Invalidação automática em mutações)
- Conteinerização: Docker Compose
- Testes: Pytest (pytest-asyncio, httpx)

---

## 🛠️ Como Executar o Projeto

### Pré-requisitos
- Docker e Docker Compose instalados.

### 1. Subir a aplicação via Docker
O comando constrói a imagem, sobe os containers do PostgreSQL e Redis, e executa as migrações do Alembic automaticamente na inicialização:

  docker compose up -d --build

A aplicação estará disponível em http://localhost:8000.

---

## 🧪 Executando os Testes Automatizados

Com os containers ativos, execute a suíte de testes unitários e de integração:

  docker compose exec app pytest -v

---

## 📌 Principais Endpoints

- GET /health - Healthcheck da aplicação
- POST /clientes - Cadastra um novo cliente
- GET /clientes/{id} - Busca cliente por ID (com cache no Redis)
- PATCH /clientes/{id} - Atualiza dados e invalida cache
- DELETE /clientes/{id} - Exclui cliente e limpa cache

Documentação interativa disponível em: http://localhost:8000/docs.

---

## 📦 Gerenciamento de Banco de Dados (Alembic)

Para gerar uma nova migração após alterar as models em app/domain/models.py:

  venv/bin/alembic revision --autogenerate -m "descricao_da_mudanca"
  docker compose up -d --build
