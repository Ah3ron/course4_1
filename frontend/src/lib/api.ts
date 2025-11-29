/**
 * API клиент для взаимодействия с backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface FinancialData {
	// Данные для модели Альтмана
	current_assets: number;
	current_liabilities: number;
	debt_capital: number;
	liabilities: number;

	// Данные для модели Таффлера
	sales_profit: number;
	short_term_liabilities: number;
	long_term_liabilities: number;
	total_assets: number;
	sales: number;
}

export interface IndividualData {
	monthly_income: number;
	monthly_expenses: number;
	credit_amount: number;
	credit_history_score: number;
	has_collateral: number;
	employment_years: number;
	age: number;
}

export interface PredictionResponse {
	altman_z_score: number;
	altman_risk_level: 'low' | 'medium' | 'high';
	altman_recommendation: string;
	taffler_z_score: number;
	taffler_risk_level: 'low' | 'medium' | 'high';
	taffler_recommendation: string;
	combined_risk_level: 'low' | 'medium' | 'high';
	combined_recommendation: string;
}

export interface IndividualPredictionResponse {
	credit_score: number;
	risk_level: 'low' | 'medium' | 'high';
	recommendation: string;
}

export interface ModelInfo {
	models: string[];
	altman_description: string;
	taffler_description: string;
	required_fields: {
		altman: string[];
		taffler: string[];
	};
}

export interface HealthStatus {
	status: string;
	message: string;
	timestamp: string;
}

/**
 * Проверка здоровья API
 */
export async function checkHealth(): Promise<HealthStatus> {
	const response = await fetch(`${API_BASE_URL}/api/health`);
	if (!response.ok) {
		throw new Error('API недоступен');
	}
	return response.json();
}

/**
 * Получить информацию о моделях
 */
export async function getModelInfo(): Promise<ModelInfo> {
	const response = await fetch(`${API_BASE_URL}/api/model-info`);
	if (!response.ok) {
		throw new Error('Не удалось получить информацию о моделях');
	}
	return response.json();
}

/**
 * Получить оценку кредитного риска
 */
export async function predictCreditRisk(
	financialData: FinancialData
): Promise<PredictionResponse> {
	const response = await fetch(`${API_BASE_URL}/api/predict`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(financialData)
	});

	if (!response.ok) {
		const error = await response.json().catch(() => ({ detail: 'Неизвестная ошибка' }));
		throw new Error(error.detail || 'Ошибка при получении оценки');
	}

	return response.json();
}

/**
 * Получить оценку кредитного риска для физического лица
 */
export async function predictIndividualCreditRisk(
	individualData: IndividualData
): Promise<IndividualPredictionResponse> {
	const response = await fetch(`${API_BASE_URL}/api/predict/individual`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(individualData)
	});

	if (!response.ok) {
		const error = await response.json().catch(() => ({ detail: 'Неизвестная ошибка' }));
		throw new Error(error.detail || 'Ошибка при получении оценки');
	}

	return response.json();
}
