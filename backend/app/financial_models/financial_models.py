"""
Модуль для расчета финансовых моделей оценки банкротства.
Реализует модель Альтмана (Z-score) и модель Таффлера.
"""

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# Пороговые значения для моделей
ALTMAN_SAFE_THRESHOLD = 2.99
ALTMAN_GRAY_THRESHOLD = 1.81
TAFFLER_LOW_RISK_THRESHOLD = 0.2
TAFFLER_MEDIUM_RISK_THRESHOLD = 0.0


def calculate_altman_z_score(financial_data: Dict[str, float]) -> Tuple[float, str, str]:
    """
    Рассчитывает Z-score по модели Альтмана.
    
    Модель Альтмана для производственных компаний:
    Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
    
    Где:
    X1 = Working Capital / Total Assets
    X2 = Retained Earnings / Total Assets
    X3 = EBIT / Total Assets
    X4 = Market Value of Equity / Total Liabilities
    X5 = Sales / Total Assets
    
    Интерпретация:
    - Z > 2.99: Безопасная зона (низкий риск банкротства)
    - 1.81 < Z < 2.99: Серая зона (средний риск)
    - Z < 1.81: Зона опасности (высокий риск банкротства)
    
    Args:
        financial_data: Словарь с финансовыми показателями:
            - working_capital: Оборотный капитал
            - total_assets: Общие активы
            - retained_earnings: Нераспределенная прибыль
            - ebit: Прибыль до уплаты процентов и налогов
            - market_value_equity: Рыночная стоимость собственного капитала
            - total_liabilities: Общие обязательства
            - sales: Выручка
    
    Returns:
        Tuple (z_score, risk_level, recommendation)
    """
    try:
        # Извлекаем данные
        working_capital = financial_data.get('working_capital', 0)
        total_assets = financial_data.get('total_assets', 1)  # Избегаем деления на 0
        retained_earnings = financial_data.get('retained_earnings', 0)
        ebit = financial_data.get('ebit', 0)
        market_value_equity = financial_data.get('market_value_equity', 0)
        total_liabilities = financial_data.get('total_liabilities', 1)  # Избегаем деления на 0
        sales = financial_data.get('sales', 0)
        
        # Проверка на валидность данных
        if total_assets <= 0:
            raise ValueError("Общие активы должны быть положительными")
        if total_liabilities <= 0:
            raise ValueError("Общие обязательства должны быть положительными")
        
        # Расчет коэффициентов
        x1 = working_capital / total_assets
        x2 = retained_earnings / total_assets
        x3 = ebit / total_assets
        x4 = market_value_equity / total_liabilities
        x5 = sales / total_assets
        
        # Расчет Z-score
        z_score = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5
        
        # Определение уровня риска
        if z_score > ALTMAN_SAFE_THRESHOLD:
            risk_level = "low"
            recommendation = "Низкий риск банкротства. Компания находится в безопасной зоне."
        elif z_score > ALTMAN_GRAY_THRESHOLD:
            risk_level = "medium"
            recommendation = (
                "Средний риск банкротства. Компания находится в серой зоне. "
                "Требуется дополнительный мониторинг."
            )
        else:
            risk_level = "high"
            recommendation = (
                "Высокий риск банкротства. Компания находится в зоне опасности. "
                "Требуются срочные меры."
            )
        
        return z_score, risk_level, recommendation
        
    except Exception as e:
        logger.error(f"Ошибка при расчете Z-score Альтмана: {e}")
        raise ValueError(f"Ошибка расчета модели Альтмана: {str(e)}")


def calculate_taffler_score(financial_data: Dict[str, float]) -> Tuple[float, str, str]:
    """
    Рассчитывает Z-score по модели Таффлера.
    
    Модель Таффлера:
    Z = 3.2 + 12.18*X1 + 2.50*X2 - 10.68*X3 + 0.029*X4
    
    Где:
    X1 = Profit before Tax / Current Liabilities
    X2 = Current Assets / Total Liabilities
    X3 = Current Liabilities / Total Assets
    X4 = No Credit Interval (Operating Income / Total Assets) * 100
    
    Интерпретация:
    - Z > 0.2: Низкий риск банкротства
    - 0.0 < Z < 0.2: Средний риск
    - Z < 0.0: Высокий риск банкротства
    
    Args:
        financial_data: Словарь с финансовыми показателями:
            - profit_before_tax: Прибыль до налогообложения
            - current_liabilities: Текущие обязательства
            - current_assets: Текущие активы
            - total_liabilities: Общие обязательства
            - total_assets: Общие активы
            - operating_income: Операционная прибыль
    
    Returns:
        Tuple (z_score, risk_level, recommendation)
    """
    try:
        # Извлекаем данные
        profit_before_tax = financial_data.get('profit_before_tax', 0)
        current_liabilities = financial_data.get('current_liabilities', 1)  # Избегаем деления на 0
        current_assets = financial_data.get('current_assets', 0)
        total_liabilities = financial_data.get('total_liabilities', 1)  # Избегаем деления на 0
        total_assets = financial_data.get('total_assets', 1)  # Избегаем деления на 0
        operating_income = financial_data.get('operating_income', 0)
        
        # Проверка на валидность данных
        if total_assets <= 0:
            raise ValueError("Общие активы должны быть положительными")
        if current_liabilities <= 0:
            raise ValueError("Текущие обязательства должны быть положительными")
        if total_liabilities <= 0:
            raise ValueError("Общие обязательства должны быть положительными")
        
        # Расчет коэффициентов
        x1 = profit_before_tax / current_liabilities
        x2 = current_assets / total_liabilities
        x3 = current_liabilities / total_assets
        x4 = (operating_income / total_assets) * 100  # No Credit Interval в процентах
        
        # Расчет Z-score по модели Таффлера
        z_score = 3.2 + 12.18 * x1 + 2.50 * x2 - 10.68 * x3 + 0.029 * x4
        
        # Определение уровня риска
        if z_score > TAFFLER_LOW_RISK_THRESHOLD:
            risk_level = "low"
            recommendation = "Низкий риск банкротства. Финансовое положение компании стабильное."
        elif z_score > TAFFLER_MEDIUM_RISK_THRESHOLD:
            risk_level = "medium"
            recommendation = (
                "Средний риск банкротства. Требуется внимательный мониторинг "
                "финансовых показателей."
            )
        else:
            risk_level = "high"
            recommendation = (
                "Высокий риск банкротства. Финансовое положение компании критическое."
            )
        
        return z_score, risk_level, recommendation
        
    except Exception as e:
        logger.error(f"Ошибка при расчете Z-score Таффлера: {e}")
        raise ValueError(f"Ошибка расчета модели Таффлера: {str(e)}")


def calculate_combined_risk(altman_score: float, taffler_score: float) -> Tuple[str, str]:
    """
    Комбинирует результаты моделей Альтмана и Таффлера для общей оценки риска.
    
    Args:
        altman_score: Z-score модели Альтмана
        taffler_score: Z-score модели Таффлера
    
    Returns:
        Tuple (combined_risk_level, combined_recommendation)
    """
    # Определяем уровни риска для каждой модели
    altman_risk = (
        "low" if altman_score > ALTMAN_SAFE_THRESHOLD
        else ("medium" if altman_score > ALTMAN_GRAY_THRESHOLD else "high")
    )
    taffler_risk = (
        "low" if taffler_score > TAFFLER_LOW_RISK_THRESHOLD
        else ("medium" if taffler_score > TAFFLER_MEDIUM_RISK_THRESHOLD else "high")
    )
    
    # Маппинг уровней риска в числовые значения для сравнения
    risk_values = {"low": 1, "medium": 2, "high": 3}
    altman_value = risk_values[altman_risk]
    taffler_value = risk_values[taffler_risk]
    
    # Берем худший (наибольший) уровень риска
    combined_value = max(altman_value, taffler_value)
    combined_risk_level = {1: "low", 2: "medium", 3: "high"}[combined_value]
    
    # Формируем рекомендацию
    if combined_risk_level == "low":
        recommendation = (
            "Обе модели показывают низкий риск банкротства. "
            "Компания находится в стабильном финансовом положении."
        )
    elif combined_risk_level == "medium":
        recommendation = (
            "Модели показывают средний уровень риска. "
            "Рекомендуется регулярный мониторинг финансовых показателей и принятие мер по улучшению финансового состояния."
        )
    else:
        recommendation = (
            "Обе модели указывают на высокий риск банкротства. "
            "Требуются срочные меры по стабилизации финансового положения компании."
        )
    
    return combined_risk_level, recommendation

