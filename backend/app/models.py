"""
Pydantic модели для валидации данных финансовых моделей.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional


class FinancialDataRequest(BaseModel):
    """Модель запроса финансовых данных компании для оценки кредитных рисков."""
    
    # Данные для модели Альтмана
    current_assets: float = Field(..., description="Текущие активы")
    current_liabilities: float = Field(..., gt=0, description="Текущие обязательства")
    debt_capital: float = Field(..., description="Заемный капитал")
    liabilities: float = Field(..., gt=0, description="Пассивы")
    
    # Данные для модели Таффлера
    sales_profit: float = Field(..., description="Прибыль от продаж")
    short_term_liabilities: float = Field(..., gt=0, description="Краткосрочные обязательства")
    long_term_liabilities: float = Field(..., description="Долгосрочные обязательства")
    total_assets: float = Field(..., gt=0, description="Общая сумма активов")
    sales: float = Field(..., description="Выручка от продаж")
    
    @field_validator('current_liabilities', 'liabilities', 'short_term_liabilities', 'total_assets')
    @classmethod
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError('Значение должно быть положительным')
        return float(v)
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_assets": 700000,
                "current_liabilities": 200000,
                "debt_capital": 500000,
                "liabilities": 800000,
                "sales_profit": 300000,
                "short_term_liabilities": 200000,
                "long_term_liabilities": 300000,
                "total_assets": 2000000,
                "sales": 3000000
            }
        }


class PredictionResponse(BaseModel):
    """Модель ответа с результатами оценки кредитных рисков."""
    
    altman_z_score: float = Field(..., description="Z-score модели Альтмана")
    altman_risk_level: str = Field(..., description="Уровень риска по модели Альтмана (low/medium/high)")
    altman_recommendation: str = Field(..., description="Рекомендация по модели Альтмана")
    
    taffler_z_score: float = Field(..., description="T-score модели Таффлера")
    taffler_risk_level: str = Field(..., description="Уровень риска по модели Таффлера (low/medium/high)")
    taffler_recommendation: str = Field(..., description="Рекомендация по модели Таффлера")
    
    combined_risk_level: str = Field(..., description="Комбинированный уровень риска (low/medium/high)")
    combined_recommendation: str = Field(..., description="Общая рекомендация")


class HealthResponse(BaseModel):
    """Модель ответа для health check."""
    
    status: str
    message: str
    timestamp: str


class ModelInfoResponse(BaseModel):
    """Модель ответа с информацией о финансовых моделях."""
    
    models: list[str] = Field(..., description="Список доступных моделей")
    altman_description: str = Field(..., description="Описание модели Альтмана")
    taffler_description: str = Field(..., description="Описание модели Таффлера")
    required_fields: dict = Field(..., description="Требуемые поля для каждой модели")
