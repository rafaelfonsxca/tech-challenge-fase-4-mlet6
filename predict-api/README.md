# Predict API

API FastAPI para realizar predições de preços de ações utilizando modelos LSTM treinados.

## 🚀 Instalação

Este projeto utiliza `uv` para gerenciamento de dependências.

### Pré-requisitos

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) instalado

### Instalar Dependências

```bash
uv sync
```

### 2. Instale as dependências

#### 2.1. Instalar UV
```bash
pip install uv
```
Outros formas de instalação: [Documentação UV](https://docs.astral.sh/uv/getting-started/installation/).

#### 2.2. Instalação das dependências utilizando comandos UV
Linux
```bash
uv venv
source .venv/bin/activate
uv pip sync pyproject.toml
```
Windows
```bash
uv venv
.\venv\Scripts\activate
uv pip sync pyproject.toml
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```
DATABASE_URL=sqlite:///./nome-banco.db
SECRET_KEY=sua-chave-secreta
```

### 4. Execute as migrações do banco de dados

```bash
alembic upgrade head
```

### 5. Inicie a API

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
├── api/              # Endpoints da API
│   └── ml.py        # Endpoints de machine learning
├── schemas/          # Schemas Pydantic para validação
│   └── prediction.py
├── main.py          # Aplicação principal FastAPI
└── pyproject.toml   # Configuração do projeto
```

## 🔧 Dependências

- FastAPI >= 0.128.0
- Uvicorn >= 0.40.0

## 📝 Notas

Certifique-se de que os modelos treinados estão disponíveis na pasta `model/models/` antes de fazer predições.

