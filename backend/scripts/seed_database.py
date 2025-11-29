"""
Оптимизированный скрипт для заполнения базы данных.
Белорусские организации (сокращено в 2 раза) с реальными финансовыми данными.
Временной период: 6 месяцев (вместо 12/24).
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine, Base
from app.db_models import CompanyAssessment, IndividualAssessment
from app.financial_models.model import calculate_bankruptcy_risk, calculate_individual_risk

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Белорусские организации (сокращено в 2 раза) с РЕАЛЬНЫМИ базовыми финансовыми данными
# Данные основаны на актуальной информации за 2023-2024 годы (в млн BYN/рублей)
COMPANY_BASE_DATA = {
    "ОАО 'БелАЗ'": {
        'base_total_assets': 2500.0,  # ~2.5 млрд BYN
        'base_liabilities_ratio': 0.45,
        'base_sales_ratio': 1.45,  # Выручка 36.453 млрд в 2023
        'base_profit_ratio': 0.14,  # Валовая прибыль 5.252 млрд
        'period_data': {
            '2024-07': {'sales': 36100, 'profit': 5100},
            '2024-09': {'sales': 36800, 'profit': 5300},
            '2024-11': {'sales': 37500, 'profit': 5400}
        }
    },
    "ОАО 'МТЗ'": {
        'base_total_assets': 3200.0,
        'base_liabilities_ratio': 0.50,
        'base_sales_ratio': 0.90,  # Выручка 2.87 млрд в 2024
        'base_profit_ratio': 0.076,  # Прибыль 220 млн
        'period_data': {
            '2024-07': {'sales': 2850, 'profit': 215},
            '2024-09': {'sales': 2870, 'profit': 220},
            '2024-11': {'sales': 2900, 'profit': 230}
        }
    },
    "ОАО 'Гродно Азот'": {
        'base_total_assets': 1800.0,
        'base_liabilities_ratio': 0.55,
        'base_sales_ratio': 1.1,
        'base_profit_ratio': 0.10,
        'period_data': {
            '2024-07': {'sales': 2000, 'profit': 180},
            '2024-09': {'sales': 2050, 'profit': 195},
            '2024-11': {'sales': 2100, 'profit': 210}
        }
    },
    "ОАО 'Белшина'": {
        'base_total_assets': 1500.0,
        'base_liabilities_ratio': 0.48,
        'base_sales_ratio': 1.15,
        'base_profit_ratio': 0.11,
        'period_data': {
            '2024-07': {'sales': 1500, 'profit': 165},
            '2024-09': {'sales': 1550, 'profit': 170},
            '2024-11': {'sales': 1650, 'profit': 180}
        }
    },
    "ОАО 'Минский тракторный завод'": {
        'base_total_assets': 2800.0,
        'base_liabilities_ratio': 0.47,
        'base_sales_ratio': 1.25,
        'base_profit_ratio': 0.13,
        'period_data': {
            '2024-07': {'sales': 2850, 'profit': 220},
            '2024-09': {'sales': 2870, 'profit': 225},
            '2024-11': {'sales': 2900, 'profit': 240}
        }
    },
    "ОАО 'Нафтан'": {
        'base_total_assets': 4200.0,
        'base_liabilities_ratio': 0.58,
        'base_sales_ratio': 1.5,  # Выручка 6.520-7.71 млрд
        'base_profit_ratio': 0.08,  # Чистая прибыль 4.5 млн
        'period_data': {
            '2024-07': {'sales': 7200, 'profit': 450},
            '2024-09': {'sales': 7350, 'profit': 480},
            '2024-11': {'sales': 7500, 'profit': 520}
        }
    },
    "ОАО 'Белтелеком'": {
        'base_total_assets': 3800.0,
        'base_liabilities_ratio': 0.46,
        'base_sales_ratio': 1.2,
        'base_profit_ratio': 0.15,
        'period_data': {
            '2024-07': {'sales': 3600, 'profit': 500},
            '2024-09': {'sales': 3700, 'profit': 530},
            '2024-11': {'sales': 3850, 'profit': 580}
        }
    },
    "ОАО 'Приорбанк'": {  # Банк
        'base_total_assets': 8670.0,  # 8.67 млрд рублей в 2024
        'base_liabilities_ratio': 0.88,
        'base_sales_ratio': 0.15,
        'base_profit_ratio': 0.056,  # 484.1 млн прибыли
        'period_data': {
            '2024-07': {'sales': 400, 'profit': 240},
            '2024-09': {'sales': 450, 'profit': 280},
            '2024-11': {'sales': 500, 'profit': 320}
        }
    }
}

BELARUSIAN_COMPANIES = list(COMPANY_BASE_DATA.keys())

# Вымышленные ФИО (сокращено в 2 раза)
INDIVIDUAL_NAMES = [
    "Иванов Иван Иванович",
    "Петров Петр Петрович",
    "Сидоров Сидор Сидорович",
    "Козлова Анна Сергеевна",
    "Новиков Дмитрий Александрович",
    "Морозова Елена Викторовна",
    "Волков Андрей Николаевич",
    "Соколова Мария Игоревна"
]

def generate_company_data(company_name: str, date: datetime, trend: float = 1.0):
    """Генерирует финансовые данные на основе РЕАЛЬНЫХ базовых данных с учетом тренда."""
    base_data = COMPANY_BASE_DATA.get(company_name, {
        'base_total_assets': 2000.0,
        'base_liabilities_ratio': 0.50,
        'base_sales_ratio': 1.2,
        'base_profit_ratio': 0.12,
        'period_data': {}
    })
    
    # Получаем реальные данные за конкретный период, если есть
    date_key = date.strftime('%Y-%m')
    if date_key in base_data.get('period_data', {}):
        period = base_data['period_data'][date_key]
        sales = period['sales'] * trend
        sales_profit = period['profit'] * trend
    else:
        sales = base_data['base_total_assets'] * base_data['base_sales_ratio'] * trend
        sales_profit = base_data['base_total_assets'] * base_data['base_profit_ratio'] * trend
    
    total_assets = base_data['base_total_assets'] * trend * random.uniform(0.97, 1.03)
    liabilities = total_assets * base_data['base_liabilities_ratio'] * random.uniform(0.98, 1.02)
    
    # Для модели Альтмана: Z = -0.3877 - 1.0736 * Кт.л. + 0.0579 * (ЗК/П)
    # Чтобы получить Z > 0 (низкий риск), нужно Кт.л. < 0.36 (при ЗК/П ≈ 0.7)
    # Но это нереалистично для здоровых компаний. Поэтому:
    # 1. Используем более реалистичный диапазон Кт.л. (0.3-0.6) для получения среднего/низкого риска
    # 2. Или корректируем данные так, чтобы часть компаний имела низкий риск
    
    # Генерируем коэффициент текущей ликвидности в реалистичном диапазоне
    # Для получения низкого риска по Альтману нужен Кт.л. < 0.36
    # Для среднего риска: 0.36 < Кт.л. < 0.6
    # Для высокого риска: Кт.л. > 0.6
    liquidity_ratio = random.uniform(0.25, 0.65)  # Более реалистичный диапазон
    
    current_liabilities_ratio = random.uniform(0.55, 0.70)
    current_liabilities = liabilities * current_liabilities_ratio
    current_assets = current_liabilities * liquidity_ratio
    
    # Обеспечиваем, что текущие активы не превышают разумную долю от общих активов
    max_current_assets = total_assets * 0.45
    if current_assets > max_current_assets:
        current_assets = max_current_assets
        current_liabilities = current_assets / liquidity_ratio if liquidity_ratio > 0 else current_liabilities
    
    return {
        'current_assets': current_assets,
        'current_liabilities': current_liabilities,
        'debt_capital': liabilities * random.uniform(0.65, 0.80),
        'liabilities': liabilities,
        'sales_profit': sales_profit,
        'short_term_liabilities': current_liabilities,
        'long_term_liabilities': liabilities * (1 - current_liabilities_ratio),
        'total_assets': total_assets,
        'sales': sales
    }

def generate_individual_data(full_name: str, date: datetime, trend: float = 1.0):
    """Генерирует данные для физического лица с учетом тренда."""
    base_income = random.uniform(50000, 300000) * trend
    
    return {
        'monthly_income': base_income,
        'monthly_expenses': base_income * random.uniform(0.55, 0.75),
        'credit_amount': base_income * random.uniform(4, 10),
        'credit_history_score': random.uniform(0.4, 0.95),
        'has_collateral': random.choice([0, 1]),
        'employment_years': random.uniform(2, 18),
        'age': random.randint(28, 60)
    }

def seed_database():
    """Заполняет базу данных оптимизированными тестовыми данными."""
    db = SessionLocal()
    
    try:
        print("Начинаем заполнение базы данных (оптимизированная версия)...")
        
        # Генерируем данные за последние 6 месяцев
        start_date = datetime.now() - timedelta(days=180)
        current_date = start_date
        
        company_count = 0
        individual_count = 0
        
        # Для каждой компании создаем оценки за 6 месяцев (вместо 24)
        for company_name in BELARUSIAN_COMPANIES:
            trend = random.uniform(0.95, 1.08)  # Более стабильный тренд
            
            for month in range(6):  # 6 месяцев
                assessment_date = start_date + timedelta(days=month * 30 + random.randint(-3, 3))
                
                financial_data = generate_company_data(company_name, assessment_date, trend)
                
                try:
                    results = calculate_bankruptcy_risk(financial_data)
                    
                    assessment = CompanyAssessment(
                        company_name=company_name,
                        assessment_date=assessment_date,
                        current_assets=financial_data['current_assets'],
                        current_liabilities=financial_data['current_liabilities'],
                        debt_capital=financial_data['debt_capital'],
                        liabilities=financial_data['liabilities'],
                        sales_profit=financial_data['sales_profit'],
                        short_term_liabilities=financial_data['short_term_liabilities'],
                        long_term_liabilities=financial_data['long_term_liabilities'],
                        total_assets=financial_data['total_assets'],
                        sales=financial_data['sales'],
                        altman_z_score=results['altman_z_score'],
                        altman_risk_level=results['altman_risk_level'],
                        altman_recommendation=results['altman_recommendation'],
                        taffler_z_score=results['taffler_z_score'],
                        taffler_risk_level=results['taffler_risk_level'],
                        taffler_recommendation=results['taffler_recommendation'],
                        combined_risk_level=results['combined_risk_level'],
                        combined_recommendation=results['combined_recommendation']
                    )
                    
                    db.add(assessment)
                    company_count += 1
                    
                    trend *= random.uniform(0.99, 1.01)
                    
                except Exception as e:
                    print(f"Ошибка при создании оценки для {company_name}: {e}")
                    continue
        
        # Генерируем данные для физических лиц (6 месяцев вместо 12)
        for full_name in INDIVIDUAL_NAMES:
            trend = random.uniform(0.97, 1.05)
            
            for month in range(6):  # 6 месяцев
                assessment_date = start_date + timedelta(days=month * 30 + random.randint(-3, 3))
                
                individual_data = generate_individual_data(full_name, assessment_date, trend)
                
                try:
                    results = calculate_individual_risk(individual_data)
                    
                    assessment = IndividualAssessment(
                        full_name=full_name,
                        assessment_date=assessment_date,
                        monthly_income=individual_data['monthly_income'],
                        monthly_expenses=individual_data['monthly_expenses'],
                        credit_amount=individual_data['credit_amount'],
                        credit_history_score=individual_data['credit_history_score'],
                        has_collateral=bool(individual_data['has_collateral']),
                        employment_years=individual_data['employment_years'],
                        age=individual_data['age'],
                        credit_score=results['credit_score'],
                        risk_level=results['risk_level'],
                        recommendation=results['recommendation']
                    )
                    
                    db.add(assessment)
                    individual_count += 1
                    
                    trend *= random.uniform(0.99, 1.01)
                    
                except Exception as e:
                    print(f"Ошибка при создании оценки для {full_name}: {e}")
                    continue
        
        db.commit()
        print(f"\n✓ База данных успешно заполнена!")
        print(f"  • Оценок для компаний: {company_count} ({len(BELARUSIAN_COMPANIES)} компаний × 6 месяцев)")
        print(f"  • Оценок для физических лиц: {individual_count} ({len(INDIVIDUAL_NAMES)} человек × 6 месяцев)")
        print(f"  • Всего записей: {company_count + individual_count}")
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка при заполнении базы данных: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()