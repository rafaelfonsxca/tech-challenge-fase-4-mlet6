# Predict API

API FastAPI para realizar predições de preços de ações utilizando modelos LSTM treinados.

## 🚀 Instalação

Este projeto utiliza `uv` para gerenciamento de dependências e ambientes virtuais.

### Pré-requisitos

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) instalado

### 1. Instalar Dependências

Sincronize as dependências e crie o ambiente virtual automaticamente:

```bash
uv sync
```

Isso instala todas as dependências listadas em `pyproject.toml` e configura o ambiente virtual.

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (exemplo):

```
DATABASE_URL=sqlite:///./predict_stocks.db
SECRET_KEY=sua-chave-secreta-aqui
```

### 3. Execute as migrações do banco de dados

```bash
uv run alembic upgrade head
```

### 4. Inicie a API

```bash
uv run uvicorn main:app --reload
```

A API estará disponível em [http://localhost:8000](http://localhost:8000).

## Documentação da API

Documentação disponível em:

- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)

## 📁 Estrutura

```
predict-api/
├── src/
│   ├── api/
│   │   └── predict.py    # Endpoints de predição
│   ├── core/             # Configurações core (DB, auth, etc.)
│   ├── crud/             # Operações CRUD
│   ├── models/           # Modelos SQLAlchemy
│   └── schemas/          # Schemas Pydantic
│       └── prediction.py
├── main.py               # Aplicação principal FastAPI
├── pyproject.toml        # Configuração do projeto e dependências
├── alembic.ini           # Configuração do Alembic para migrações
└── migrations/           # Migrações do banco de dados
```

## 📝 Notas

- Certifique-se de que os modelos treinados estão disponíveis na pasta `../model/models/` (relativo à API) antes de fazer predições.
- O modelo espera 30 dias de dados com 5 features cada (Open, High, Low, Close, Volume).

