#!/usr/bin/env python3
"""
Script para exportar métricas da API para Netdata via logs estruturados.
Este script pode ser usado para enviar métricas customizadas para o Netdata.
"""
import json
import sys
import time
from datetime import datetime


def export_metric(chart_name: str, dimension: str, value: float, chart_type: str = "line"):
    """
    Exporta uma métrica no formato esperado pelo Netdata.
    
    Args:
        chart_name: Nome do gráfico (ex: "api.response_time")
        dimension: Nome da dimensão (ex: "avg", "p95")
        value: Valor da métrica
        chart_type: Tipo de gráfico (line, area, stacked)
    """
    metric = {
        "timestamp": int(time.time()),
        "chart": chart_name,
        "dimension": dimension,
        "value": value,
        "type": chart_type
    }
    
    # Netdata pode ler métricas via logs estruturados
    print(json.dumps(metric), file=sys.stderr)


def export_api_metrics(response_time: float, status_code: int, endpoint: str):
    """
    Exporta métricas de API para Netdata.
    
    Args:
        response_time: Tempo de resposta em segundos
        status_code: Código de status HTTP
        endpoint: Endpoint chamado
    """
    # Métricas de tempo de resposta
    export_metric("api.response_time", "avg", response_time)
    export_metric("api.response_time", "max", response_time)
    
    # Métricas de status codes
    status_family = f"{status_code // 100}xx"
    export_metric(f"api.status_codes.{status_family}", "count", 1, "stacked")
    
    # Métricas por endpoint
    export_metric(f"api.endpoints.{endpoint.replace('/', '_')}", "requests", 1, "stacked")


if __name__ == "__main__":
    # Exemplo de uso
    export_api_metrics(0.123, 200, "/api/v1/predict")
    export_api_metrics(0.456, 500, "/api/v1/predict")
