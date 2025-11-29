/**
 * API клиент для взаимодействия с backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface FinancialData {
	company_name: string;
	assessment_date: string;
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
	full_name: string;
	assessment_date: string;
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
	individual_description: string;
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

export interface CompanyStatistics {
	total: number;
	assessments: Array<{
		id: number;
		company_name: string;
		assessment_date: string;
		altman_z_score: number;
		taffler_z_score: number;
		combined_risk_level: string;
		total_assets: number;
		liabilities: number;
		sales: number;
	}>;
}

export interface IndividualStatistics {
	total: number;
	assessments: Array<{
		id: number;
		full_name: string;
		assessment_date: string;
		credit_score: number;
		risk_level: string;
		monthly_income: number;
		credit_amount: number;
		age: number;
	}>;
}

export interface CompanyHistory {
	company_name: string;
	total_assessments: number;
	history: Array<{
		assessment_date: string;
		altman_z_score: number;
		taffler_z_score: number;
		combined_risk_level: string;
		total_assets: number;
		liabilities: number;
		sales: number;
	}>;
}

export interface IndividualHistory {
	full_name: string;
	total_assessments: number;
	history: Array<{
		assessment_date: string;
		credit_score: number;
		risk_level: string;
		monthly_income: number;
		credit_amount: number;
	}>;
}

/**
 * Получить статистику по компаниям
 */
export async function getCompanyStatistics(
	companyName?: string,
	startDate?: string,
	endDate?: string
): Promise<CompanyStatistics> {
	let url = `${API_BASE_URL}/api/statistics/companies?`;
	if (companyName) url += `company_name=${encodeURIComponent(companyName)}&`;
	if (startDate) url += `start_date=${startDate}&`;
	if (endDate) url += `end_date=${endDate}&`;

	const response = await fetch(url);
	if (!response.ok) {
		throw new Error('Не удалось получить статистику компаний');
	}
	return response.json();
}

/**
 * Получить статистику по физическим лицам
 */
export async function getIndividualStatistics(
	fullName?: string,
	startDate?: string,
	endDate?: string
): Promise<IndividualStatistics> {
	let url = `${API_BASE_URL}/api/statistics/individuals?`;
	if (fullName) url += `full_name=${encodeURIComponent(fullName)}&`;
	if (startDate) url += `start_date=${startDate}&`;
	if (endDate) url += `end_date=${endDate}&`;

	const response = await fetch(url);
	if (!response.ok) {
		throw new Error('Не удалось получить статистику физических лиц');
	}
	return response.json();
}

/**
 * Получить историю оценок компании
 */
export async function getCompanyHistory(companyName: string): Promise<CompanyHistory> {
	const response = await fetch(
		`${API_BASE_URL}/api/statistics/companies/${encodeURIComponent(companyName)}/history`
	);
	if (!response.ok) {
		throw new Error('Не удалось получить историю компании');
	}
	return response.json();
}

/**
 * Получить историю оценок физического лица
 */
export async function getIndividualHistory(fullName: string): Promise<IndividualHistory> {
	const response = await fetch(
		`${API_BASE_URL}/api/statistics/individuals/${encodeURIComponent(fullName)}/history`
	);
	if (!response.ok) {
		throw new Error('Не удалось получить историю физического лица');
	}
	return response.json();
}

/**
 * Удалить оценку компании по ID
 */
export async function deleteCompanyAssessment(assessmentId: number): Promise<void> {
	const response = await fetch(
		`${API_BASE_URL}/api/statistics/companies/${assessmentId}`,
		{
			method: 'DELETE'
		}
	);
	if (!response.ok) {
		const error = await response.json().catch(() => ({ detail: 'Не удалось удалить оценку компании' }));
		throw new Error(error.detail || 'Не удалось удалить оценку компании');
	}
}

/**
 * Удалить оценку физического лица по ID
 */
export async function deleteIndividualAssessment(assessmentId: number): Promise<void> {
	const response = await fetch(
		`${API_BASE_URL}/api/statistics/individuals/${assessmentId}`,
		{
			method: 'DELETE'
		}
	);
	if (!response.ok) {
		const error = await response.json().catch(() => ({ detail: 'Не удалось удалить оценку физического лица' }));
		throw new Error(error.detail || 'Не удалось удалить оценку физического лица');
	}
}
