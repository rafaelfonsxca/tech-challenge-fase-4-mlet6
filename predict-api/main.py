from fastapi import FastAPI
from src.api import auth, predict, user
from src.core.monitoring import init_sentry, PerformanceMonitoringMiddleware

# Inicializa Sentry antes de criar a aplicação
init_sentry()

app = FastAPI(
    title="Stock Price Prediction API",
    description="API for predicting stock prices using LSTM model.",
    version="1.0.0"
)

# Adiciona middleware de monitoramento de performance
app.add_middleware(PerformanceMonitoringMiddleware)

app.include_router(
    auth.router, 
    prefix="/api/v1",
    tags=["Auth"])

app.include_router(
    user.router, 
    prefix="/api/v1",
    tags=["Users"])

app.include_router(
    predict.router,
    prefix="/api/v1",
    tags=["Prediction"])


@app.get("/health")
def health_check():
    """
    Endpoint de health check para monitoramento.
    """
    return {
        "status": "healthy",
        "service": "predict-api",
        "version": "1.0.0"
    }