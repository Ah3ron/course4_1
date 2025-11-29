"""
Модуль для расчета финансовых моделей оценки кредитных рисков.
Реализует статистические модели Альтмана (Z-score) и Таффлера.
"""

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# Пороговые значения для моделей
# Для модели Альтмана: чем выше Z, тем ниже риск (но формула может давать отрицательные значения)
ALTMAN_SAFE_THRESHOLD = 0.0
ALTMAN_GRAY_THRESHOLD = -0.5
# Для модели Таффлера: значения от 0 до 1, чем выше, тем лучше
TAFFLER_LOW_RISK_THRESHOLD = 0.5
TAFFLER_MEDIUM_RISK_THRESHOLD = 0.3


def calculate_altman_z_score(financial_data: Dict[str, float]) -> Tuple[float, str, str]:
    """
    Рассчитывает Z-score по модели Альтмана.
    
    Модель Альтмана:
    Z = -0.3877 - 1.0736 * Кт.л. + 0.0579 * (ЗК / П)
    
    Где:
    Кт.л. = коэффициент текущей ликвидности (текущие активы / текущие обязательства)
    ЗК = заемный капитал
    П = пассивы
    
    Интерпретация:
    - Z > 0.0: Безопасная зона (низкий кредитный риск)
    - -0.5 < Z < 0.0: Серая зона (средний кредитный риск)
    - Z < -0.5: Зона опасности (высокий кредитный риск)
    
    Args:
        financial_data: Словарь с финансовыми показателями:
            - current_assets: Текущие активы
            - current_liabilities: Текущие обязательства
            - debt_capital: Заемный капитал
            - liabilities: Пассивы
    
    Returns:
        Tuple (z_score, risk_level, recommendation)
    """
    try:
        # Извлекаем данные
        current_assets = financial_data.get('current_assets', 0)
        current_liabilities = financial_data.get('current_liabilities', 1)  # Избегаем деления на 0
        debt_capital = financial_data.get('debt_capital', 0)
        liabilities = financial_data.get('liabilities', 1)  # Избегаем деления на 0
        
        # Проверка на валидность данных
        if current_liabilities <= 0:
            raise ValueError("Текущие обязательства должны быть положительными")
        if liabilities <= 0:
            raise ValueError("Пассивы должны быть положительными")
        
        # Расчет коэффициента текущей ликвидности
        current_liquidity_ratio = current_assets / current_liabilities
        
        # Расчет отношения заемного капитала к пассивам
        debt_to_liabilities = debt_capital / liabilities
        
        # Расчет Z-score по модели Альтмана
        z_score = -0.3877 - 1.0736 * current_liquidity_ratio + 0.0579 * debt_to_liabilities
        
        # Определение уровня риска
        if z_score > ALTMAN_SAFE_THRESHOLD:
            risk_level = "low"
            recommendation = "Низкий кредитный риск. Компания находится в безопасной зоне."
        elif z_score > ALTMAN_GRAY_THRESHOLD:
            risk_level = "medium"
            recommendation = (
                "Средний кредитный риск. Компания находится в серой зоне. "
                "Требуется дополнительный мониторинг."
            )
        else:
            risk_level = "high"
            recommendation = (
                "Высокий кредитный риск. Компания находится в зоне опасности. "
                "Требуются срочные меры."
            )
        
        return z_score, risk_level, recommendation
        
    except Exception as e:
        logger.error(f"Ошибка при расчете Z-score Альтмана: {e}")
        raise ValueError(f"Ошибка расчета модели Альтмана: {str(e)}")


def calculate_taffler_score(financial_data: Dict[str, float]) -> Tuple[float, str, str]:
    """
    Рассчитывает T-score по модели Таффлера.
    
    Модель Таффлера:
    Т = 0.53*Х1 + 0.13*Х2 + 0.18*Х3 + 0.16*Х4
    
    Где:
    Х1 = отношение прибыли от продаж к краткосрочным обязательствам
    Х2 = отношение оборотных активов к обязательствам
    Х3 = отношение долгосрочных обязательств к общей сумме активов
    Х4 = отношение выручки от продаж к суммарным активам
    
    Интерпретация:
    - Т > 0.5: Низкий кредитный риск
    - 0.3 < Т < 0.5: Средний кредитный риск
    - Т < 0.3: Высокий кредитный риск
    
    Args:
        financial_data: Словарь с финансовыми показателями:
            - sales_profit: Прибыль от продаж
            - short_term_liabilities: Краткосрочные обязательства
            - current_assets: Оборотные активы
            - liabilities: Обязательства
            - long_term_liabilities: Долгосрочные обязательства
            - total_assets: Общая сумма активов
            - sales: Выручка от продаж
    
    Returns:
        Tuple (t_score, risk_level, recommendation)
    """
    try:
        # Извлекаем данные
        sales_profit = financial_data.get('sales_profit', 0)
        short_term_liabilities = financial_data.get('short_term_liabilities', 1)  # Избегаем деления на 0
        current_assets = financial_data.get('current_assets', 0)
        liabilities = financial_data.get('liabilities', 1)  # Избегаем деления на 0
        long_term_liabilities = financial_data.get('long_term_liabilities', 0)
        total_assets = financial_data.get('total_assets', 1)  # Избегаем деления на 0
        sales = financial_data.get('sales', 0)
        
        # Проверка на валидность данных
        if total_assets <= 0:
            raise ValueError("Общие активы должны быть положительными")
        if short_term_liabilities <= 0:
            raise ValueError("Краткосрочные обязательства должны быть положительными")
        if liabilities <= 0:
            raise ValueError("Обязательства должны быть положительными")
        
        # Расчет коэффициентов
        x1 = sales_profit / short_term_liabilities
        x2 = current_assets / liabilities
        x3 = long_term_liabilities / total_assets
        x4 = sales / total_assets
        
        # Расчет T-score по модели Таффлера
        t_score = 0.53 * x1 + 0.13 * x2 + 0.18 * x3 + 0.16 * x4
        
        # Определение уровня риска
        if t_score > TAFFLER_LOW_RISK_THRESHOLD:
            risk_level = "low"
            recommendation = "Низкий кредитный риск. Финансовое положение компании стабильное."
        elif t_score > TAFFLER_MEDIUM_RISK_THRESHOLD:
            risk_level = "medium"
            recommendation = (
                "Средний кредитный риск. Требуется внимательный мониторинг "
                "финансовых показателей."
            )
        else:
            risk_level = "high"
            recommendation = (
                "Высокий кредитный риск. Финансовое положение компании критическое."
            )
        
        return t_score, risk_level, recommendation
        
    except Exception as e:
        logger.error(f"Ошибка при расчете T-score Таффлера: {e}")
        raise ValueError(f"Ошибка расчета модели Таффлера: {str(e)}")


def calculate_combined_risk(altman_score: float, taffler_score: float) -> Tuple[str, str]:
    """
    Комбинирует результаты моделей Альтмана и Таффлера для общей оценки риска.
    
    Args:
        altman_score: Z-score модели Альтмана
        taffler_score: T-score модели Таффлера
    
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
            "Обе модели показывают низкий кредитный риск. "
            "Компания находится в стабильном финансовом положении."
        )
    elif combined_risk_level == "medium":
        recommendation = (
            "Модели показывают средний уровень кредитного риска. "
            "Рекомендуется регулярный мониторинг финансовых показателей и принятие мер по улучшению финансового состояния."
        )
    else:
        recommendation = (
            "Обе модели указывают на высокий кредитный риск. "
            "Требуются срочные меры по стабилизации финансового положения компании."
        )
    
    return combined_risk_level, recommendation

