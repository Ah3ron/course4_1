"""
Pydantic модели для валидации данных финансовых моделей.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional


class FinancialDataRequest(BaseModel):
    """Модель запроса финансовых данных компании для оценки банкротства."""
    
    # Данные для модели Альтмана
    working_capital: float = Field(..., description="Оборотный капитал (текущие активы - текущие обязательства)")
    total_assets: float = Field(..., gt=0, description="Общие активы")
    retained_earnings: float = Field(..., description="Нераспределенная прибыль")
    ebit: float = Field(..., description="Прибыль до уплаты процентов и налогов (EBIT)")
    market_value_equity: float = Field(..., description="Рыночная стоимость собственного капитала")
    total_liabilities: float = Field(..., gt=0, description="Общие обязательства")
    sales: float = Field(..., description="Выручка")
    
    # Данные для модели Таффлера
    profit_before_tax: float = Field(..., description="Прибыль до налогообложения")
    current_liabilities: float = Field(..., gt=0, description="Текущие обязательства")
    current_assets: float = Field(..., description="Текущие активы")
    operating_income: float = Field(..., description="Операционная прибыль")
    
    @field_validator('total_assets', 'total_liabilities', 'current_liabilities')
    @classmethod
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError('Значение должно быть положительным')
        return float(v)
    
    class Config:
        json_schema_extra = {
            "example": {
                "working_capital": 500000,
                "total_assets": 2000000,
                "retained_earnings": 300000,
                "ebit": 400000,
                "market_value_equity": 1500000,
                "total_liabilities": 500000,
                "sales": 3000000,
                "profit_before_tax": 350000,
                "current_liabilities": 200000,
                "current_assets": 700000,
                "operating_income": 380000
            }
        }


class PredictionResponse(BaseModel):
    """Модель ответа с результатами оценки банкротства."""
    
    altman_z_score: float = Field(..., description="Z-score модели Альтмана")
    altman_risk_level: str = Field(..., description="Уровень риска по модели Альтмана (low/medium/high)")
    altman_recommendation: str = Field(..., description="Рекомендация по модели Альтмана")
    
    taffler_z_score: float = Field(..., description="Z-score модели Таффлера")
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
