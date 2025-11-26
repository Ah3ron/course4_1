/**
 * API клиент для взаимодействия с backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface FinancialData {
	// Данные для модели Альтмана
	working_capital: number;
	total_assets: number;
	retained_earnings: number;
	ebit: number;
	market_value_equity: number;
	total_liabilities: number;
	sales: number;
	
	// Данные для модели Таффлера
	profit_before_tax: number;
	current_liabilities: number;
	current_assets: number;
	operating_income: number;
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
 * Получить оценку риска банкротства
 */
export async function predictBankruptcyRisk(financialData: FinancialData): Promise<PredictionResponse> {
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
