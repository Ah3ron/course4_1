"""
Конфигурация для финансовых моделей оценки банкротства.
"""

# Пороговые значения для моделей
ALTMAN_THRESHOLDS = {
    'safe_zone': 2.99,      # Z > 2.99 - безопасная зона
    'gray_zone': 1.81,      # 1.81 < Z < 2.99 - серая зона
    'danger_zone': 1.81     # Z < 1.81 - зона опасности
}

TAFFLER_THRESHOLDS = {
    'low_risk': 0.2,        # Z > 0.2 - низкий риск
    'medium_risk': 0.0,     # 0.0 < Z < 0.2 - средний риск
    'high_risk': 0.0        # Z < 0.0 - высокий риск
}

# Описание финансовых показателей для моделей
FINANCIAL_INDICATORS = {
    'altman': {
        'working_capital': {
            'name': 'Оборотный капитал',
            'description': 'Текущие активы минус текущие обязательства',
            'required': True
        },
        'total_assets': {
            'name': 'Общие активы',
            'description': 'Сумма всех активов компании',
            'required': True
        },
        'retained_earnings': {
            'name': 'Нераспределенная прибыль',
            'description': 'Накопленная прибыль компании',
            'required': True
        },
        'ebit': {
            'name': 'EBIT',
            'description': 'Прибыль до уплаты процентов и налогов',
            'required': True
        },
        'market_value_equity': {
            'name': 'Рыночная стоимость собственного капитала',
            'description': 'Рыночная капитализация компании',
            'required': True
        },
        'total_liabilities': {
            'name': 'Общие обязательства',
            'description': 'Сумма всех обязательств компании',
            'required': True
        },
        'sales': {
            'name': 'Выручка',
            'description': 'Объем продаж компании',
            'required': True
        }
    },
    'taffler': {
        'profit_before_tax': {
            'name': 'Прибыль до налогообложения',
            'description': 'Прибыль до уплаты налогов',
            'required': True
        },
        'current_liabilities': {
            'name': 'Текущие обязательства',
            'description': 'Краткосрочные обязательства компании',
            'required': True
        },
        'current_assets': {
            'name': 'Текущие активы',
            'description': 'Активы, которые могут быть обращены в деньги в течение года',
            'required': True
        },
        'total_liabilities': {
            'name': 'Общие обязательства',
            'description': 'Сумма всех обязательств компании',
            'required': True
        },
        'total_assets': {
            'name': 'Общие активы',
            'description': 'Сумма всех активов компании',
            'required': True
        },
        'operating_income': {
            'name': 'Операционная прибыль',
            'description': 'Прибыль от основной деятельности',
            'required': True
        }
    }
}

