"""
Модуль для работы с финансовыми моделями оценки банкротства.
"""

import logging
from typing import Dict, Tuple, Optional

from app.financial_models.financial_models import (
    calculate_altman_z_score,
    calculate_taffler_score,
    calculate_combined_risk
)

logger = logging.getLogger(__name__)

# Обязательные поля для моделей
REQUIRED_FIELDS_ALTMAN = [
    'working_capital', 'total_assets', 'retained_earnings',
    'ebit', 'market_value_equity', 'total_liabilities', 'sales'
]

REQUIRED_FIELDS_TAFFLER = [
    'profit_before_tax', 'current_liabilities', 'current_assets',
    'total_liabilities', 'total_assets', 'operating_income'
]

POSITIVE_FIELDS = ['total_assets', 'total_liabilities', 'current_liabilities']


def validate_financial_data(financial_data: Dict) -> Tuple[bool, Optional[str]]:
    """
    Валидация финансовых данных.
    
    Args:
        financial_data: Словарь с финансовыми показателями
        
    Returns:
        Tuple (is_valid, error_message)
    """
    all_required = set(REQUIRED_FIELDS_ALTMAN + REQUIRED_FIELDS_TAFFLER)
    
    # Проверяем наличие всех полей
    missing_fields = all_required - set(financial_data.keys())
    if missing_fields:
        return False, f"Отсутствуют обязательные поля: {', '.join(sorted(missing_fields))}"
    
    # Проверяем, что обязательные положительные значения действительно положительны
    for field in POSITIVE_FIELDS:
        if field in financial_data and financial_data[field] <= 0:
            return False, f"Поле {field} должно быть положительным числом"
    
    return True, None


def calculate_bankruptcy_risk(financial_data: Dict) -> Dict:
    """
    Рассчитывает риск банкротства используя модели Альтмана и Таффлера.
    
    Args:
        financial_data: Словарь с финансовыми показателями
        
    Returns:
        Словарь с результатами расчетов:
        {
            'altman_z_score': float,
            'altman_risk_level': str,
            'altman_recommendation': str,
            'taffler_z_score': float,
            'taffler_risk_level': str,
            'taffler_recommendation': str,
            'combined_risk_level': str,
            'combined_recommendation': str
        }
        
    Raises:
        ValueError: При ошибке валидации или расчета
    """
    # Валидация данных
    is_valid, error_message = validate_financial_data(financial_data)
    if not is_valid:
        raise ValueError(error_message)
    
    try:
        # Расчет по модели Альтмана
        altman_data = {
            key: financial_data[key] for key in REQUIRED_FIELDS_ALTMAN
        }
        altman_score, altman_risk, altman_rec = calculate_altman_z_score(altman_data)
        
        # Расчет по модели Таффлера
        taffler_data = {
            key: financial_data[key] for key in REQUIRED_FIELDS_TAFFLER
        }
        taffler_score, taffler_risk, taffler_rec = calculate_taffler_score(taffler_data)
        
        # Комбинированная оценка
        combined_risk, combined_rec = calculate_combined_risk(altman_score, taffler_score)
        
        return {
            'altman_z_score': round(altman_score, 4),
            'altman_risk_level': altman_risk,
            'altman_recommendation': altman_rec,
            'taffler_z_score': round(taffler_score, 4),
            'taffler_risk_level': taffler_risk,
            'taffler_recommendation': taffler_rec,
            'combined_risk_level': combined_risk,
            'combined_recommendation': combined_rec
        }
        
    except Exception as e:
        logger.error(f"Ошибка при расчете риска банкротства: {e}", exc_info=True)
        raise ValueError(f"Ошибка при выполнении расчета: {str(e)}")


def get_model_info() -> Dict:
    """
    Возвращает информацию о доступных финансовых моделях.
    
    Returns:
        Словарь с информацией о моделях
    """
    return {
        'models': ['altman', 'taffler'],
        'altman_description': (
            'Модель Альтмана (Z-score) - классическая модель для прогнозирования банкротства, '
            'разработанная Эдвардом Альтманом в 1968 году. Использует 5 финансовых коэффициентов '
            'для оценки вероятности банкротства компании в течение 2 лет.'
        ),
        'taffler_description': (
            'Модель Таффлера - модель прогнозирования банкротства, разработанная Ричардом Таффлером. '
            'Использует 4 финансовых коэффициента и показывает эффективность в различных отраслях.'
        ),
        'required_fields': {
            'altman': REQUIRED_FIELDS_ALTMAN,
            'taffler': REQUIRED_FIELDS_TAFFLER
        }
    }
