"""
API endpoints для оценки кредитных рисков.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends

from app.models import (
    FinancialDataRequest,
    PredictionResponse,
    IndividualDataRequest,
    IndividualPredictionResponse,
    HealthResponse,
    ModelInfoResponse
)
from app.financial_models.model import calculate_bankruptcy_risk, calculate_individual_risk, get_model_info
from app.database import get_db
from app.db_models import CompanyAssessment, IndividualAssessment

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
    financial_data: FinancialDataRequest,
    db: Session = Depends(get_db)
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
        
        # Преобразуем данные в словарь (исключаем company_name и assessment_date)
        financial_dict = financial_data.model_dump(exclude={'company_name', 'assessment_date'})
        
        # Получаем результаты расчетов
        results = calculate_bankruptcy_risk(financial_dict)
        
        # Сохраняем в базу данных
        assessment_date = datetime.strptime(financial_data.assessment_date, "%Y-%m-%d")
        db_assessment = CompanyAssessment(
            company_name=financial_data.company_name,
            assessment_date=assessment_date,
            current_assets=financial_data.current_assets,
            current_liabilities=financial_data.current_liabilities,
            debt_capital=financial_data.debt_capital,
            liabilities=financial_data.liabilities,
            sales_profit=financial_data.sales_profit,
            short_term_liabilities=financial_data.short_term_liabilities,
            long_term_liabilities=financial_data.long_term_liabilities,
            total_assets=financial_data.total_assets,
            sales=financial_data.sales,
            altman_z_score=results['altman_z_score'],
            altman_risk_level=results['altman_risk_level'],
            altman_recommendation=results['altman_recommendation'],
            taffler_z_score=results['taffler_z_score'],
            taffler_risk_level=results['taffler_risk_level'],
            taffler_recommendation=results['taffler_recommendation'],
            combined_risk_level=results['combined_risk_level'],
            combined_recommendation=results['combined_recommendation']
        )
        
        try:
            db.add(db_assessment)
            db.commit()
            db.refresh(db_assessment)
            logger.info(f"Оценка сохранена в БД с ID: {db_assessment.id}")
        except Exception as e:
            db.rollback()
            logger.error(f"Ошибка при сохранении в БД: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при сохранении данных: {str(e)}"
            )
        
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


@router.post("/predict/individual", response_model=IndividualPredictionResponse)
async def predict_individual_credit_risk(
    individual_data: IndividualDataRequest,
    db: Session = Depends(get_db)
) -> IndividualPredictionResponse:
    """
    Оценка кредитного риска физического лица с использованием скоринговой модели.
    
    Args:
        individual_data: Данные физического лица
        
    Returns:
        IndividualPredictionResponse с результатами оценки
        
    Raises:
        HTTPException: При ошибке валидации или обработки данных
    """
    try:
        logger.info(
            f"Получен запрос на оценку кредитного риска для физ. лица: "
            f"monthly_income={individual_data.monthly_income}, "
            f"credit_amount={individual_data.credit_amount}, "
            f"age={individual_data.age}"
        )
        
        # Преобразуем данные в словарь (исключаем full_name и assessment_date)
        individual_dict = individual_data.model_dump(exclude={'full_name', 'assessment_date'})
        
        # Получаем результаты расчетов
        results = calculate_individual_risk(individual_dict)
        
        # Сохраняем в базу данных
        assessment_date = datetime.strptime(individual_data.assessment_date, "%Y-%m-%d")
        db_assessment = IndividualAssessment(
            full_name=individual_data.full_name,
            assessment_date=assessment_date,
            monthly_income=individual_data.monthly_income,
            monthly_expenses=individual_data.monthly_expenses,
            credit_amount=individual_data.credit_amount,
            credit_history_score=individual_data.credit_history_score,
            has_collateral=bool(individual_data.has_collateral),
            employment_years=individual_data.employment_years,
            age=individual_data.age,
            credit_score=results['credit_score'],
            risk_level=results['risk_level'],
            recommendation=results['recommendation']
        )
        
        try:
            db.add(db_assessment)
            db.commit()
            db.refresh(db_assessment)
            logger.info(f"Оценка физ. лица сохранена в БД с ID: {db_assessment.id}")
        except Exception as e:
            db.rollback()
            logger.error(f"Ошибка при сохранении в БД: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при сохранении данных: {str(e)}"
            )
        
        result = IndividualPredictionResponse(**results)
        
        logger.info(
            f"Оценка выполнена: Скоринг={results['credit_score']}, "
            f"Уровень риска={results['risk_level']}"
        )
        
        return result
        
    except ValueError as e:
        logger.warning(f"Ошибка валидации данных: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Ошибка при оценке кредитного риска для физ. лица: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при выполнении оценки: {str(e)}"
        )


@router.get("/statistics/companies")
async def get_company_statistics(
    company_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить статистику по компаниям."""
    try:
        query = db.query(CompanyAssessment)
        
        if company_name:
            query = query.filter(CompanyAssessment.company_name.ilike(f"%{company_name}%"))
        
        if start_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                query = query.filter(CompanyAssessment.assessment_date >= start)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Неверный формат даты начала: '{start_date}'. Ожидается формат YYYY-MM-DD."
                )
        
        if end_date:
            try:
                end = datetime.strptime(end_date, "%Y-%m-%d")
                # Используем следующий день в полночь, чтобы включить весь указанный день
                end = end + timedelta(days=1)
                query = query.filter(CompanyAssessment.assessment_date < end)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Неверный формат даты окончания: '{end_date}'. Ожидается формат YYYY-MM-DD."
                )
        
        assessments = query.order_by(CompanyAssessment.assessment_date.desc()).all()
        
        return {
            "total": len(assessments),
            "assessments": [
                {
                    "id": a.id,
                    "company_name": a.company_name,
                    "assessment_date": a.assessment_date.isoformat(),
                    "altman_z_score": a.altman_z_score,
                    "taffler_z_score": a.taffler_z_score,
                    "combined_risk_level": a.combined_risk_level,
                    "total_assets": a.total_assets,
                    "liabilities": a.liabilities,
                    "sales": a.sales
                }
                for a in assessments
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении статистики компаний: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении статистики: {str(e)}"
        )


@router.get("/statistics/individuals")
async def get_individual_statistics(
    full_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить статистику по физическим лицам."""
    try:
        query = db.query(IndividualAssessment)
        
        if full_name:
            query = query.filter(IndividualAssessment.full_name.ilike(f"%{full_name}%"))
        
        if start_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                query = query.filter(IndividualAssessment.assessment_date >= start)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Неверный формат даты начала: '{start_date}'. Ожидается формат YYYY-MM-DD."
                )
        
        if end_date:
            try:
                end = datetime.strptime(end_date, "%Y-%m-%d")
                # Используем следующий день в полночь, чтобы включить весь указанный день
                end = end + timedelta(days=1)
                query = query.filter(IndividualAssessment.assessment_date < end)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Неверный формат даты окончания: '{end_date}'. Ожидается формат YYYY-MM-DD."
                )
        
        assessments = query.order_by(IndividualAssessment.assessment_date.desc()).all()
        
        return {
            "total": len(assessments),
            "assessments": [
                {
                    "id": a.id,
                    "full_name": a.full_name,
                    "assessment_date": a.assessment_date.isoformat(),
                    "credit_score": a.credit_score,
                    "risk_level": a.risk_level,
                    "monthly_income": a.monthly_income,
                    "credit_amount": a.credit_amount,
                    "age": a.age
                }
                for a in assessments
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении статистики физ. лиц: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении статистики: {str(e)}"
        )


@router.get("/statistics/companies/{company_name}/history")
async def get_company_history(
    company_name: str,
    db: Session = Depends(get_db)
):
    """Получить историю оценок конкретной компании."""
    try:
        assessments = db.query(CompanyAssessment)\
            .filter(CompanyAssessment.company_name == company_name)\
            .order_by(CompanyAssessment.assessment_date.asc())\
            .all()
        
        if not assessments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Компания '{company_name}' не найдена"
            )
        
        return {
            "company_name": company_name,
            "total_assessments": len(assessments),
            "history": [
                {
                    "assessment_date": a.assessment_date.isoformat(),
                    "altman_z_score": a.altman_z_score,
                    "taffler_z_score": a.taffler_z_score,
                    "combined_risk_level": a.combined_risk_level,
                    "total_assets": a.total_assets,
                    "liabilities": a.liabilities,
                    "sales": a.sales
                }
                for a in assessments
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении истории компании: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении истории: {str(e)}"
        )


@router.get("/statistics/individuals/{full_name}/history")
async def get_individual_history(
    full_name: str,
    db: Session = Depends(get_db)
):
    """Получить историю оценок конкретного физического лица."""
    try:
        assessments = db.query(IndividualAssessment)\
            .filter(IndividualAssessment.full_name == full_name)\
            .order_by(IndividualAssessment.assessment_date.asc())\
            .all()
        
        if not assessments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Физическое лицо '{full_name}' не найдено"
            )
        
        return {
            "full_name": full_name,
            "total_assessments": len(assessments),
            "history": [
                {
                    "assessment_date": a.assessment_date.isoformat(),
                    "credit_score": a.credit_score,
                    "risk_level": a.risk_level,
                    "monthly_income": a.monthly_income,
                    "credit_amount": a.credit_amount
                }
                for a in assessments
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении истории физ. лица: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении истории: {str(e)}"
        )
