/**
 * Svelte stores для управления состоянием приложения.
 */

import { writable } from 'svelte/store';
import type { PredictionResponse, IndividualPredictionResponse, ModelInfo } from './api';

// История предсказаний для компаний
export interface CompanyHistoryItem {
	id: string;
	timestamp: string;
	type: 'company';
	data: {
		total_assets: number;
		liabilities: number;
		sales: number;
	};
	result: PredictionResponse;
}

// История предсказаний для физических лиц
export interface IndividualHistoryItem {
	id: string;
	timestamp: string;
	type: 'individual';
	data: {
		monthly_income: number;
		credit_amount: number;
		credit_score: number;
	};
	result: IndividualPredictionResponse;
}

// Объединенный тип для истории
export type PredictionHistoryItem = CompanyHistoryItem | IndividualHistoryItem;

function createPredictionHistory() {
	const { subscribe, set, update } = writable<PredictionHistoryItem[]>([]);

	// Загрузка из localStorage
	if (typeof window !== 'undefined') {
		try {
			const stored = localStorage.getItem('predictionHistory');
			if (stored) {
				try {
					const parsed = JSON.parse(stored);
					// Фильтруем только валидные записи с новым форматом
					const validHistory = Array.isArray(parsed)
						? parsed.filter((item: any) => {
								// Проверяем тип записи
								if (item?.type === 'company') {
									return (
										item?.result?.altman_z_score !== undefined &&
										item?.result?.taffler_z_score !== undefined &&
										item?.result?.combined_risk_level !== undefined
									);
								} else if (item?.type === 'individual') {
									return (
										item?.result?.credit_score !== undefined &&
										item?.result?.risk_level !== undefined &&
										item?.result?.recommendation !== undefined
									);
								}
								return false;
							})
						: [];
					set(validHistory);
					// Сохраняем очищенную историю обратно
					if (validHistory.length !== parsed.length) {
						try {
							localStorage.setItem('predictionHistory', JSON.stringify(validHistory));
						} catch (e) {
							console.warn('Не удалось сохранить очищенную историю:', e);
						}
					}
				} catch (e) {
					console.error('Ошибка при загрузке истории:', e);
					// Очищаем поврежденные данные
					try {
						localStorage.removeItem('predictionHistory');
					} catch (removeError) {
						console.warn('Не удалось очистить поврежденную историю:', removeError);
					}
				}
			}
		} catch (e) {
			console.warn('Не удалось получить доступ к localStorage для истории:', e);
		}
	}

	return {
		subscribe,
		add: (item: PredictionHistoryItem) => {
			update((history) => {
				const newHistory = [item, ...history].slice(0, 50); // Храним последние 50
				if (typeof window !== 'undefined') {
					try {
						localStorage.setItem('predictionHistory', JSON.stringify(newHistory));
					} catch (e) {
						console.warn('Не удалось сохранить историю в localStorage:', e);
					}
				}
				return newHistory;
			});
		},
		clear: () => {
			set([]);
			if (typeof window !== 'undefined') {
				try {
					localStorage.removeItem('predictionHistory');
				} catch (e) {
					console.warn('Не удалось очистить историю из localStorage:', e);
				}
			}
		}
	};
}

export const predictionHistory = createPredictionHistory();

// Информация о модели
export const modelInfo = writable<ModelInfo | null>(null);

// Состояние загрузки
export const isLoading = writable<boolean>(false);

// Тема (светлая/темная)
const LIGHT_THEME = 'lofi';
const DARK_THEME = 'business';

type ThemeName = typeof LIGHT_THEME | typeof DARK_THEME;

function createTheme() {
	const { subscribe, set, update } = writable<ThemeName>(LIGHT_THEME);

	// Определяем, является ли тема светлой
	const isLightTheme = (theme: string): boolean => {
		return theme === LIGHT_THEME;
	};

	// Получаем противоположную тему
	const getOppositeTheme = (currentTheme: ThemeName): ThemeName => {
		return isLightTheme(currentTheme) ? DARK_THEME : LIGHT_THEME;
	};

	if (typeof window !== 'undefined') {
		try {
			const stored = localStorage.getItem('theme') as ThemeName | null;
			if (stored && (stored === LIGHT_THEME || stored === DARK_THEME)) {
				set(stored);
				document.documentElement.setAttribute('data-theme', stored);
			} else {
				// Если сохранена старая тема (light/dark), конвертируем
				const oldStored = localStorage.getItem('theme');
				if (oldStored === 'light') {
					set(LIGHT_THEME);
					document.documentElement.setAttribute('data-theme', LIGHT_THEME);
					localStorage.setItem('theme', LIGHT_THEME);
				} else if (oldStored === 'dark') {
					set(DARK_THEME);
					document.documentElement.setAttribute('data-theme', DARK_THEME);
					localStorage.setItem('theme', DARK_THEME);
				}
			}
		} catch (e) {
			// Игнорируем ошибки localStorage
			console.warn('Не удалось загрузить тему из localStorage:', e);
		}
	}

	return {
		subscribe,
		set: (value: ThemeName) => {
			set(value);
			if (typeof window !== 'undefined') {
				try {
					localStorage.setItem('theme', value);
					document.documentElement.setAttribute('data-theme', value);
				} catch (e) {
					console.warn('Не удалось сохранить тему в localStorage:', e);
					// Все равно устанавливаем тему в DOM, даже если не удалось сохранить
					document.documentElement.setAttribute('data-theme', value);
				}
			}
		},
		toggle: () => {
			update((current) => {
				const newTheme = getOppositeTheme(current);
				if (typeof window !== 'undefined') {
					try {
						localStorage.setItem('theme', newTheme);
						document.documentElement.setAttribute('data-theme', newTheme);
					} catch (e) {
						console.warn('Не удалось сохранить тему в localStorage:', e);
						// Все равно устанавливаем тему в DOM
						document.documentElement.setAttribute('data-theme', newTheme);
					}
				}
				return newTheme;
			});
		},
		isLight: () => {
			let current: ThemeName = LIGHT_THEME;
			subscribe((value) => {
				current = value;
			})();
			return isLightTheme(current);
		}
	};
}

export const theme = createTheme();
