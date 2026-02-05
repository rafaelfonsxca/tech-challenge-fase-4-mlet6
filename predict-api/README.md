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

Crie um arquivo `.env` na raiz do projeto:

```env
# Database
DATABASE_URL=sqlite:///./predict_stocks.db

# Security
SECRET_KEY=sua-chave-secreta-aqui

# Sentry Configuration (opcional)
# Obtenha seu DSN em https://sentry.io
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
SENTRY_TRACES_SAMPLE_RATE=1.0
SENTRY_PROFILES_SAMPLE_RATE=0.0

# Environment
ENVIRONMENT=development
RELEASE_VERSION=1.0.0
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

## 📊 Monitoramento

A API está configurada com **Sentry** e **Netdata** para monitoramento completo de erros, performance e recursos.

### Sentry - Monitoramento de Erros e Performance

O Sentry está integrado para:
- **Rastreamento de erros**: Captura automática de exceções e erros
- **Performance monitoring**: Rastreamento de tempo de resposta de requisições
- **Transações**: Monitoramento de endpoints e operações do banco de dados
- **Métricas customizadas**: Tempo de predição do modelo ML

#### Configuração do Sentry

1. Crie uma conta em [https://sentry.io](https://sentry.io)
2. Crie um novo projeto (selecione Python/FastAPI)
3. Copie o DSN fornecido
4. Adicione o DSN no arquivo `.env`:

```env
SENTRY_DSN=https://seu-dsn@sentry.io/project-id
SENTRY_TRACES_SAMPLE_RATE=1.0  # 1.0 = 100% das transações são rastreadas
ENVIRONMENT=production
RELEASE_VERSION=1.0.0
```

#### O que é monitorado

- ✅ Erros e exceções em todos os endpoints
- ✅ Tempo de resposta de cada requisição
- ✅ Performance de predições do modelo ML
- ✅ Operações do banco de dados (SQLAlchemy)
- ✅ Logs de erro estruturados

### Netdata - Monitoramento de Recursos

O Netdata monitora recursos do sistema e performance da aplicação.

#### Instalação do Netdata

**Opção 1: Docker (Recomendado)**

```bash
docker-compose -f docker-compose.netdata.yml up -d
```

O Netdata estará disponível em [http://localhost:19999](http://localhost:19999)

**Opção 2: Instalação nativa**

```bash
# Instalação automática
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

#### Métricas monitoradas pelo Netdata

- **CPU**: Uso de processador por core
- **Memória**: RAM utilizada e disponível
- **Disco**: I/O e espaço em disco
- **Rede**: Tráfego de entrada e saída
- **Processos Python**: Recursos utilizados pela aplicação
- **Docker**: Se executado em container

#### Integração com a API

A API envia métricas customizadas via:
- **Headers HTTP**: `X-Process-Time` em todas as respostas
- **Logs estruturados**: Métricas de performance registradas nos logs
- **Health check**: Endpoint `/health` para verificação de status

#### Exportação de métricas customizadas

Use o script `scripts/export_metrics.py` para exportar métricas customizadas:

```python
from scripts.export_metrics import export_api_metrics

# Exemplo de uso
export_api_metrics(response_time=0.123, status_code=200, endpoint="/api/v1/predict")
```

### Endpoints de Monitoramento

- `GET /health` - Health check da API
  - Retorna status da aplicação
  - Útil para load balancers e sistemas de monitoramento

### Visualização de Métricas

#### Sentry Dashboard
- Acesse [https://sentry.io](https://sentry.io)
- Visualize erros, performance e transações
- Configure alertas para erros críticos

#### Netdata Dashboard
- Acesse `http://localhost:19999` (se instalado localmente)
- Visualize métricas em tempo real
- Configure alertas para recursos do sistema

## 📝 Notas

- Certifique-se de que os modelos treinados estão disponíveis na pasta `../model/models/` (relativo à API) antes de fazer predições.
- O modelo espera 30 dias de dados com 5 features cada (Open, High, Low, Close, Volume).
- O Sentry é opcional - a API funciona sem ele, mas sem monitoramento de erros.
- O Netdata pode ser executado separadamente da API para monitorar o sistema host.

