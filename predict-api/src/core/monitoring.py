"""
Módulo de monitoramento com Sentry e métricas de performance.
"""
import os
import time
import logging
from typing import Callable
from functools import wraps
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


def init_sentry():
    """
    Inicializa o Sentry SDK para monitoramento de erros e performance.
    """
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    
    sentry_dsn = os.getenv("SENTRY_DSN")
    
    if not sentry_dsn:
        logger.warning("SENTRY_DSN não configurado. Monitoramento Sentry desabilitado.")
        return
    
    # Configuração do Sentry
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
            SqlalchemyIntegration(),
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR
            ),
        ],
        # Performance monitoring
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
        # Profiling (opcional, requer plano pago)
        profiles_sample_rate=float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.0")),
        # Environment
        environment=os.getenv("ENVIRONMENT", "development"),
        # Release version
        release=os.getenv("RELEASE_VERSION", "1.0.0"),
    )
    logger.info("Sentry inicializado com sucesso.")


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """
    Middleware para monitoramento de performance das requisições.
    Registra tempo de resposta, status codes e métricas básicas.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Processa a requisição
        response = await call_next(request)
        
        # Calcula tempo de processamento
        process_time = time.time() - start_time
        
        # Adiciona headers de performance
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request.headers.get("X-Request-ID", "unknown")
        
        # Log de métricas (pode ser integrado com Netdata via logs)
        logger.info(
            f"Request: {request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time:.4f}s"
        )
        
        # Envia métricas para Sentry (se configurado)
        try:
            import sentry_sdk
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag("http.status_code", response.status_code)
                scope.set_tag("http.method", request.method)
                scope.set_tag("http.path", request.url.path)
                scope.set_measurement("request.duration", process_time)
        except ImportError:
            pass
        
        return response


def track_model_performance(func: Callable) -> Callable:
    """
    Decorator para rastrear performance de funções de modelo ML.
    Suporta funções síncronas e assíncronas.
    """
    import asyncio
    import inspect
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            # Verifica se a função é assíncrona
            if inspect.iscoroutinefunction(func):
                async def async_wrapper():
                    result = await func(*args, **kwargs)
                    process_time = time.time() - start_time
                    
                    # Log de performance do modelo
                    logger.info(
                        f"Model prediction completed | "
                        f"Function: {func.__name__} | "
                        f"Time: {process_time:.4f}s"
                    )
                    
                    # Envia métricas para Sentry
                    try:
                        import sentry_sdk
                        with sentry_sdk.configure_scope() as scope:
                            scope.set_measurement("model.prediction.duration", process_time)
                            scope.set_tag("model.function", func.__name__)
                    except ImportError:
                        pass
                    
                    return result
                return async_wrapper()
            else:
                # Função síncrona
                result = func(*args, **kwargs)
                process_time = time.time() - start_time
                
                # Log de performance do modelo
                logger.info(
                    f"Model prediction completed | "
                    f"Function: {func.__name__} | "
                    f"Time: {process_time:.4f}s"
                )
                
                # Envia métricas para Sentry
                try:
                    import sentry_sdk
                    with sentry_sdk.configure_scope() as scope:
                        scope.set_measurement("model.prediction.duration", process_time)
                        scope.set_tag("model.function", func.__name__)
                except ImportError:
                    pass
                
                return result
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Model prediction failed | "
                f"Function: {func.__name__} | "
                f"Time: {process_time:.4f}s | "
                f"Error: {str(e)}"
            )
            raise
    
    return wrapper
