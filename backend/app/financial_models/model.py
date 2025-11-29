"""
Модуль для работы с финансовыми моделями оценки кредитных рисков.
"""

import logging
from typing import Dict, Tuple, Optional

from app.financial_models.financial_models import (
    calculate_altman_z_score,
    calculate_taffler_score,
    calculate_combined_risk
)
from app.financial_models.individual_models import (
    calculate_individual_credit_score
)

logger = logging.getLogger(__name__)

# Обязательные поля для моделей
REQUIRED_FIELDS_ALTMAN = [
    'current_assets', 'current_liabilities', 'debt_capital', 'liabilities'
]

REQUIRED_FIELDS_TAFFLER = [
    'sales_profit', 'short_term_liabilities', 'current_assets',
    'liabilities', 'long_term_liabilities', 'total_assets', 'sales'
]

POSITIVE_FIELDS = ['current_liabilities', 'liabilities', 'short_term_liabilities', 'total_assets']


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
    Рассчитывает кредитный риск используя статистические модели Альтмана и Таффлера.
    
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
        logger.error(f"Ошибка при расчете кредитного риска: {e}", exc_info=True)
        raise ValueError(f"Ошибка при выполнении расчета: {str(e)}")


def calculate_individual_risk(individual_data: Dict) -> Dict:
    """
    Рассчитывает кредитный риск для физического лица.
    
    Args:
        individual_data: Словарь с данными физического лица
        
    Returns:
        Словарь с результатами расчетов:
        {
            'credit_score': float,
            'risk_level': str,
            'recommendation': str
        }
        
    Raises:
        ValueError: При ошибке валидации или расчета
    """
    try:
        credit_score, risk_level, recommendation = calculate_individual_credit_score(individual_data)
        
        return {
            'credit_score': round(credit_score, 2),
            'risk_level': risk_level,
            'recommendation': recommendation
        }
        
    except Exception as e:
        logger.error(f"Ошибка при расчете кредитного риска для физ. лица: {e}", exc_info=True)
        raise ValueError(f"Ошибка при выполнении расчета: {str(e)}")


def get_model_info() -> Dict:
    """
    Возвращает информацию о доступных финансовых моделях.
    
    Returns:
        Словарь с информацией о моделях
    """
    return {
        'models': ['altman', 'taffler', 'individual'],
        'altman_description': (
            'Модель Альтмана (Z-score) - статистическая модель для оценки кредитных рисков компаний. '
            'Использует коэффициент текущей ликвидности и отношение заемного капитала к пассивам '
            'для оценки кредитоспособности. При значении Z < -0.5 - низкий риск (хорошее положение), '
            'при -0.5 ≤ Z < 0.0 - средний риск, при Z ≥ 0.0 - высокий риск (критичная ситуация).'
        ),
        'taffler_description': (
            'Модель Таффлера - статистическая модель оценки кредитных рисков компаний, разработанная Ричардом Таффлером в 1977 году. '
            'Использует 4 финансовых коэффициента: отношение прибыли от продаж к краткосрочным обязательствам, '
            'отношение оборотных активов к обязательствам, отношение долгосрочных обязательств к активам, '
            'и отношение выручки к активам для комплексной оценки кредитоспособности. '
            'При значении T > 0.3 - низкий риск дефолта, при 0.2 < T ≤ 0.3 - средний риск, '
            'при T ≤ 0.2 - значительный риск потери платежеспособности.'
        ),
        'individual_description': (
            'Скоринговая модель для оценки кредитных рисков физических лиц. '
            'Использует комплексный анализ финансовых показателей: соотношение дохода и расходов, '
            'кредитную историю, наличие залога, трудовой стаж, возраст и долговую нагрузку. '
            'Скоринг рассчитывается по шкале от 300 до 850 баллов. '
            'При значении Score > 700 - низкий кредитный риск, при 500 < Score ≤ 700 - средний риск, '
            'при Score ≤ 500 - высокий кредитный риск.'
        ),
        'required_fields': {
            'altman': REQUIRED_FIELDS_ALTMAN,
            'taffler': REQUIRED_FIELDS_TAFFLER
        }
    }
