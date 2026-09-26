# Notaflix

Sistema de avaliação de filmes inspirado no Letterboxd, desenvolvido como parte da **Atividade DEV** do Rocket Lab 2026.2 (Visagio). Permite cadastrar filmes, navegar por um catálogo paginado e filtrável, ver detalhes e avaliações de cada título, e adicionar novas notas e resenhas.

## Funcionalidades

- Cadastro, edição e remoção de filmes (título, diretor, ano, gênero, sinopse)
- Catálogo paginado com busca por título, diretor ou ano
- Filtros por gênero, ano e nota mínima, combináveis com a busca por texto
- Layout responsivo, adaptado para desktop e mobile
- Página de detalhes com elenco, direção, produtoras, sinopse e histórico de avaliações
- Adição de novas avaliações (nota de 0 a 10 + comentário)
- Cálculo automático da nota média de cada filme
- Testes automatizados no frontend (Vitest + Testing Library) e no backend (pytest)

## Stack

- **Frontend:** Vite + React + TypeScript
- **Backend:** FastAPI (Python)
- **Banco de dados:** SQLite, com SQLAlchemy (ORM) e Alembic (migrações)

## Estrutura do projeto

```
backend/
  app/            # código da API (routers, models, schemas)
  migrations/     # migrações do Alembic
  scripts/        # script de seed do banco (seed_db.py)
  seed_data/      # CSVs de população (bases_atv_dev1/, bases_atv_dev_2/)
  tests/          # testes automatizados da API (pytest)
frontend/
  src/
    pages/        # telas (catálogo, detalhes, formulário)
    components/   # componentes reutilizáveis (header, footer, avaliação)
    api.ts         # chamadas à API
    types.ts       # tipos TypeScript
    *.test.ts(x)   # testes automatizados (Vitest + Testing Library)
```

## Pré-requisitos

- Python 3.11 ou superior
- Node.js 18 ou superior (com npm)

## Como rodar

### 1. Backend

Em um terminal, na raiz do projeto:

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install -e ".[dev]"

# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env

alembic upgrade head
python scripts/seed_db.py
uvicorn app.main:app --reload
```

A API sobe em `http://127.0.0.1:8000`, com documentação interativa (Swagger) em `http://127.0.0.1:8000/docs`.

### 2. Frontend

Em **outro terminal**, na raiz do projeto:

```bash
cd frontend
npm install
npm run dev
```

O app abre em `http://localhost:5173` (ou na porta indicada no terminal).

> Os dois precisam estar rodando ao mesmo tempo, em terminais separados, para o app funcionar.

## Populando o banco de dados

O script `backend/scripts/seed_db.py` lê os arquivos CSV em `backend/seed_data/bases_atv_dev1/` e `backend/seed_data/bases_atv_dev_2/` e popula todas as tabelas do banco (filmes, gêneros, elenco, produtoras, avaliações, etc). Ele só precisa ser executado uma vez — se o banco já tiver filmes cadastrados, o script não duplica os dados.

## Testes automatizados

### Backend (pytest)

```bash
cd backend
pytest
```

Os testes rodam contra um banco SQLite em memória, isolado do banco real (`rocketlab.db`), cobrindo o catálogo (busca, filtros, paginação), CRUD de filmes e avaliações, validações de entrada e o health check da API.

### Frontend (Vitest + Testing Library)

```bash
cd frontend
npm run test
```

Cobre a lógica de limpeza de títulos/sinopses, o componente de estrelas de avaliação e o catálogo (carregamento, filtros e tratamento de erro da API).

## Sobre a escala de notas

As avaliações usam escala de **0 a 10**, conforme orientação oficial da equipe do Rocket Lab (e não de 1 a 5 estrelas, como constava inicialmente no enunciado da atividade), seguindo o campo `nota` definido nas models do banco de dados.

## Autoria

Desenvolvido por Laura Miranda como parte da Atividade DEV do Rocket Lab 2026.2 (Visagio).