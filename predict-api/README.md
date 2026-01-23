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

## 🏃 Executando a API

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

## 📚 Documentação

Após iniciar a API, acesse:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

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

