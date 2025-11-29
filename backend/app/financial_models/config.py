"""
Конфигурация для финансовых моделей оценки кредитных рисков.
"""

# Пороговые значения для моделей
ALTMAN_THRESHOLDS = {
    'safe_zone': -0.5,      # Z < -0.5 - безопасная зона (низкий риск, хорошее положение)
    'gray_zone': 0.0,       # -0.5 <= Z < 0.0 - серая зона (средний риск)
    'danger_zone': 0.0      # Z >= 0.0 - зона опасности (высокий риск, критичная ситуация)
}

TAFFLER_THRESHOLDS = {
    'low_risk': 0.3,        # T > 0.3 - низкий риск дефолта
    'medium_risk': 0.2,     # 0.2 < T <= 0.3 - средний риск
    'high_risk': 0.2        # T <= 0.2 - значительный риск потери платежеспособности
}

# Описание финансовых показателей для моделей
FINANCIAL_INDICATORS = {
    'altman': {
        'current_assets': {
            'name': 'Текущие активы',
            'description': 'Активы, обращаемые в деньги в течение года',
            'required': True
        },
        'current_liabilities': {
            'name': 'Текущие обязательства',
            'description': 'Краткосрочные обязательства компании',
            'required': True
        },
        'debt_capital': {
            'name': 'Заемный капитал',
            'description': 'Сумма заемных средств компании',
            'required': True
        },
        'liabilities': {
            'name': 'Пассивы',
            'description': 'Общая сумма пассивов компании',
            'required': True
        }
    },
    'taffler': {
        'sales_profit': {
            'name': 'Прибыль от продаж',
            'description': 'Прибыль от реализации продукции',
            'required': True
        },
        'short_term_liabilities': {
            'name': 'Краткосрочные обязательства',
            'description': 'Обязательства со сроком погашения до года',
            'required': True
        },
        'current_assets': {
            'name': 'Текущие активы',
            'description': 'Активы, обращаемые в деньги в течение года',
            'required': True
        },
        'liabilities': {
            'name': 'Обязательства',
            'description': 'Общая сумма обязательств компании',
            'required': True
        },
        'long_term_liabilities': {
            'name': 'Долгосрочные обязательства',
            'description': 'Обязательства со сроком погашения более года',
            'required': True
        },
        'total_assets': {
            'name': 'Общая сумма активов',
            'description': 'Сумма всех активов компании',
            'required': True
        },
        'sales': {
            'name': 'Выручка от продаж',
            'description': 'Объем продаж компании',
            'required': True
        }
    }
}

