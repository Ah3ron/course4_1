"""
API endpoints для оценки кредитных рисков.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.models import (
    FinancialDataRequest,
    PredictionResponse,
    HealthResponse,
    ModelInfoResponse
)
from app.financial_models.model import calculate_bankruptcy_risk, get_model_info

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["credit-risk"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Проверка здоровья сервера.
    
    Returns:
        HealthResponse с информацией о статусе сервера
    """
    return HealthResponse(
        status="healthy",
        message="Credit Risk Assessment API is running",
        timestamp=datetime.now().isoformat()
    )


@router.get("/model-info", response_model=ModelInfoResponse)
async def get_model_info_endpoint() -> ModelInfoResponse:
    """
    Получить информацию о доступных финансовых моделях.
    
    Returns:
        ModelInfoResponse с информацией о моделях
        
    Raises:
        HTTPException: При ошибке получения информации
    """
    try:
        info = get_model_info()
        return ModelInfoResponse(**info)
    except Exception as e:
        logger.error(f"Ошибка при получении информации о моделях: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении информации о моделях: {str(e)}"
        )


@router.post("/predict", response_model=PredictionResponse)
async def predict_bankruptcy_risk(
    financial_data: FinancialDataRequest
) -> PredictionResponse:
    """
    Оценка кредитного риска компании с использованием статистических моделей Альтмана и Таффлера.
    
    Args:
        financial_data: Финансовые данные компании
        
    Returns:
        PredictionResponse с результатами оценки
        
    Raises:
        HTTPException: При ошибке валидации или обработки данных
    """
    try:
        logger.info(
            f"Получен запрос на оценку кредитного риска: "
            f"total_assets={financial_data.total_assets}, "
            f"liabilities={financial_data.liabilities}"
        )
        
        # Преобразуем данные в словарь
        financial_dict = financial_data.model_dump()
        
        # Получаем результаты расчетов
        results = calculate_bankruptcy_risk(financial_dict)
        
        result = PredictionResponse(**results)
        
        logger.info(
            f"Оценка выполнена: Альтман Z={results['altman_z_score']}, "
            f"Таффлер T={results['taffler_z_score']}, "
            f"Комбинированный риск={results['combined_risk_level']}"
        )
        
        return result
        
    except ValueError as e:
        logger.warning(f"Ошибка валидации данных: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Ошибка при оценке кредитного риска: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при выполнении оценки: {str(e)}"
        )
