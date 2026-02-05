# Guia de Monitoramento - Predict API

Este documento detalha como configurar e usar o sistema de monitoramento da API.

## 📋 Visão Geral

A API utiliza duas ferramentas principais para monitoramento:

1. **Sentry**: Monitoramento de erros, performance e transações
2. **Netdata**: Monitoramento de recursos do sistema (CPU, memória, disco, rede)

## 🔧 Configuração do Sentry

### Passo 1: Criar conta e projeto

1. Acesse [https://sentry.io](https://sentry.io)
2. Crie uma conta (há plano gratuito disponível)
3. Crie um novo projeto:
   - Selecione **Python** como plataforma
   - Escolha **FastAPI** como framework
4. Copie o **DSN** fornecido

### Passo 2: Configurar variáveis de ambiente

Adicione as seguintes variáveis no seu arquivo `.env`:

```env
SENTRY_DSN=https://seu-dsn@sentry.io/project-id
SENTRY_TRACES_SAMPLE_RATE=1.0
ENVIRONMENT=production
RELEASE_VERSION=1.0.0
```

**Parâmetros:**
- `SENTRY_DSN`: DSN do seu projeto Sentry (obrigatório)
- `SENTRY_TRACES_SAMPLE_RATE`: Taxa de amostragem de transações (0.0 a 1.0)
  - `1.0` = 100% das transações são rastreadas (recomendado para desenvolvimento)
  - `0.1` = 10% das transações (recomendado para produção com alto tráfego)
- `ENVIRONMENT`: Ambiente da aplicação (development, staging, production)
- `RELEASE_VERSION`: Versão da aplicação (útil para rastrear releases)

### Passo 3: Verificar funcionamento

1. Inicie a API:
   ```bash
   uv run uvicorn main:app --reload
   ```

2. Faça uma requisição que cause erro (ex: endpoint inválido)

3. Verifique no dashboard do Sentry se o erro foi capturado

### O que é monitorado pelo Sentry

✅ **Erros e Exceções**
- Todas as exceções não tratadas
- HTTPExceptions do FastAPI
- Erros de banco de dados
- Erros de predição do modelo ML

✅ **Performance**
- Tempo de resposta de cada endpoint
- Tempo de predição do modelo ML
- Operações de banco de dados (queries SQL)
- Transações completas (request → response)

✅ **Contexto**
- Headers HTTP relevantes
- Parâmetros de requisição
- Informações do usuário autenticado
- Stack traces completos

## 📊 Configuração do Netdata

### Opção 1: Docker (Recomendado)

1. Inicie o Netdata:
   ```bash
   docker-compose -f docker-compose.netdata.yml up -d
   ```

2. Acesse o dashboard:
   - URL: [http://localhost:19999](http://localhost:19999)

3. Para parar:
   ```bash
   docker-compose -f docker-compose.netdata.yml down
   ```

### Opção 2: Instalação Nativa

```bash
# Instalação automática
bash <(curl -Ss https://my-netdata.io/kickstart.sh)

# Ou via package manager (Ubuntu/Debian)
sudo apt-get install netdata

# Iniciar serviço
sudo systemctl start netdata
sudo systemctl enable netdata
```

### Métricas disponíveis no Netdata

O Netdata monitora automaticamente:

- **CPU**: Uso por core, load average, frequência
- **Memória**: RAM total, usada, livre, cache, swap
- **Disco**: I/O, espaço usado, latência
- **Rede**: Tráfego de entrada/saída, conexões, erros
- **Processos**: Recursos por processo (incluindo Python)
- **Sistema**: Uptime, temperatura (se disponível)

### Integração com a API

A API envia métricas customizadas através de:

1. **Headers HTTP**: Todas as respostas incluem `X-Process-Time`
2. **Logs estruturados**: Métricas são registradas nos logs
3. **Health check**: Endpoint `/health` para verificação de status

### Exportação de Métricas Customizadas

Para exportar métricas customizadas para o Netdata:

```python
from scripts.export_metrics import export_api_metrics

# Em um endpoint ou middleware
export_api_metrics(
    response_time=0.123,
    status_code=200,
    endpoint="/api/v1/predict"
)
```

## 📈 Métricas de Performance

### Tempo de Resposta

O middleware `PerformanceMonitoringMiddleware` registra:
- Tempo total de processamento de cada requisição
- Status code HTTP
- Método HTTP (GET, POST, etc.)
- Path do endpoint

**Exemplo de log:**
```
Request: POST /api/v1/predict | Status: 200 | Time: 0.1234s
```

### Performance do Modelo ML

O decorator `@track_model_performance` registra:
- Tempo de execução da predição
- Sucesso/falha da predição
- Erros específicos do modelo

**Exemplo de log:**
```
Model prediction completed | Function: predict_stock_price | Time: 0.4567s
```

## 🚨 Alertas

### Configurar Alertas no Sentry

1. Acesse o dashboard do Sentry
2. Vá em **Alerts** → **Create Alert Rule**
3. Configure condições (ex: erro rate > 5%)
4. Configure notificações (email, Slack, etc.)

### Configurar Alertas no Netdata

1. Acesse o dashboard do Netdata
2. Vá em **Alerts** → **All Alerts**
3. Configure thresholds para:
   - CPU usage > 80%
   - Memory usage > 90%
   - Disk space < 10%
   - Response time > 1s

## 🔍 Troubleshooting

### Sentry não está capturando erros

1. Verifique se `SENTRY_DSN` está configurado no `.env`
2. Verifique os logs da aplicação para mensagens do Sentry
3. Teste com um erro intencional para verificar a conexão

### Netdata não está acessível

1. Verifique se a porta 19999 está disponível
2. Verifique se o container está rodando: `docker ps`
3. Verifique os logs: `docker logs predict-api-netdata`

### Métricas não aparecem

1. Verifique se o middleware está ativo no `main.py`
2. Verifique os logs da aplicação
3. Faça algumas requisições para gerar métricas

## 📚 Recursos Adicionais

- [Documentação do Sentry](https://docs.sentry.io/platforms/python/)
- [Documentação do Netdata](https://learn.netdata.cloud/)
- [FastAPI Monitoring Best Practices](https://fastapi.tiangolo.com/advanced/middleware/)
