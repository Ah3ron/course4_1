"""
Модуль для расчета кредитного риска физических лиц.
Реализует скоринговую модель на основе финансовых показателей.
"""

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# Пороговые значения для скоринговой модели
INDIVIDUAL_LOW_RISK_THRESHOLD = 700
INDIVIDUAL_MEDIUM_RISK_THRESHOLD = 500


def calculate_individual_credit_score(financial_data: Dict[str, float]) -> Tuple[float, str, str]:
    """
    Рассчитывает кредитный скоринг для физического лица.
    
    Скоринговая модель:
    Score = 300 + (Доход/Расход * 200) + (Кредитная история * 150) + 
            (Залог * 100) + (Стаж * 50) - (Возраст/10 * 20) - (Сумма кредита/Доход * 100)
    
    Где:
    - Доход/Расход: коэффициент платежеспособности (макс 3.0)
    - Кредитная история: от 0 до 1 (1 - отличная, 0 - плохая)
    - Залог: 1 если есть, 0 если нет
    - Стаж: в годах (макс 20)
    - Возраст: в годах
    - Сумма кредита/Доход: коэффициент долговой нагрузки
    
    Интерпретация:
    - Score > 700: Низкий кредитный риск
    - 500 < Score < 700: Средний кредитный риск
    - Score < 500: Высокий кредитный риск
    
    Args:
        financial_data: Словарь с финансовыми показателями:
            - monthly_income: Месячный доход
            - monthly_expenses: Месячные расходы
            - credit_amount: Сумма кредита
            - credit_history_score: Оценка кредитной истории (0-1)
            - has_collateral: Наличие залога (0 или 1)
            - employment_years: Трудовой стаж в годах
            - age: Возраст в годах
    
    Returns:
        Tuple (credit_score, risk_level, recommendation)
    """
    try:
        # Извлекаем данные
        monthly_income = financial_data.get('monthly_income', 0)
        monthly_expenses = financial_data.get('monthly_expenses', 1)  # Избегаем деления на 0
        credit_amount = financial_data.get('credit_amount', 0)
        credit_history_score = financial_data.get('credit_history_score', 0)
        has_collateral = financial_data.get('has_collateral', 0)
        employment_years = financial_data.get('employment_years', 0)
        age = financial_data.get('age', 30)
        
        # Проверка на валидность данных
        if monthly_income <= 0:
            raise ValueError("Месячный доход должен быть положительным")
        if monthly_expenses <= 0:
            raise ValueError("Месячные расходы должны быть положительными")
        if credit_history_score < 0 or credit_history_score > 1:
            raise ValueError("Оценка кредитной истории должна быть от 0 до 1")
        if age < 18 or age > 100:
            raise ValueError("Возраст должен быть от 18 до 100 лет")
        
        # Расчет коэффициента платежеспособности (макс 3.0)
        income_to_expense_ratio = min(monthly_income / monthly_expenses, 3.0)
        
        # Расчет коэффициента долговой нагрузки
        debt_to_income_ratio = min(credit_amount / monthly_income if monthly_income > 0 else 10, 10.0)
        
        # Ограничиваем стаж (макс 20 лет)
        employment_years = min(employment_years, 20)
        
        # Расчет кредитного скоринга
        base_score = 300
        income_score = income_to_expense_ratio * 200
        history_score = credit_history_score * 150
        collateral_score = has_collateral * 100
        employment_score = employment_years * 50 / 20  # Нормализуем до 50 баллов
        age_penalty = (age / 10) * 20
        debt_penalty = debt_to_income_ratio * 100
        
        credit_score = (
            base_score + 
            income_score + 
            history_score + 
            collateral_score + 
            employment_score - 
            age_penalty - 
            debt_penalty
        )
        
        # Ограничиваем скоринг в диапазоне 300-850 (стандартный диапазон FICO)
        credit_score = max(300, min(850, credit_score))
        
        # Определение уровня риска
        if credit_score > INDIVIDUAL_LOW_RISK_THRESHOLD:
            risk_level = "low"
            recommendation = (
                "Низкий кредитный риск. Заемщик имеет хорошую платежеспособность и кредитную историю. "
                "Кредит может быть одобрен на выгодных условиях."
            )
        elif credit_score > INDIVIDUAL_MEDIUM_RISK_THRESHOLD:
            risk_level = "medium"
            recommendation = (
                "Средний кредитный риск. Заемщик имеет приемлемую платежеспособность. "
                "Рекомендуется дополнительная проверка и возможно повышение процентной ставки или требование залога."
            )
        else:
            risk_level = "high"
            recommendation = (
                "Высокий кредитный риск. Заемщик имеет низкую платежеспособность или плохую кредитную историю. "
                "Рекомендуется отказ в кредите или требование значительного залога и повышенной процентной ставки."
            )
        
        return credit_score, risk_level, recommendation
        
    except Exception as e:
        logger.error(f"Ошибка при расчете кредитного скоринга для физ. лица: {e}")
        raise ValueError(f"Ошибка расчета модели: {str(e)}")

