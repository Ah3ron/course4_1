"""
Схемы данных для API (переиспользуем модели из models.py).
"""

from app.models import (
    FinancialDataRequest,
    PredictionResponse,
    HealthResponse,
    ModelInfoResponse
)

__all__ = [
    'FinancialDataRequest',
    'PredictionResponse',
    'HealthResponse',
    'ModelInfoResponse'
]
