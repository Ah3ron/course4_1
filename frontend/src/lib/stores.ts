/**
 * Svelte stores для управления состоянием приложения.
 */

import { writable } from 'svelte/store';
import type { PredictionResponse, ModelInfo } from './api';

// История предсказаний
export interface PredictionHistoryItem {
	id: string;
	timestamp: string;
	data: {
		total_assets: number;
		total_liabilities: number;
		sales: number;
	};
	result: PredictionResponse;
}

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
						? parsed.filter((item: any) => 
							item?.result?.altman_z_score !== undefined && 
							item?.result?.taffler_z_score !== undefined &&
							item?.result?.combined_risk_level !== undefined
						)
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

// Тема (light/dark)
function createTheme() {
	const { subscribe, set, update } = writable<'light' | 'dark'>('light');

	if (typeof window !== 'undefined') {
		try {
			const stored = localStorage.getItem('theme') as 'light' | 'dark' | null;
			if (stored && (stored === 'light' || stored === 'dark')) {
				set(stored);
				document.documentElement.setAttribute('data-theme', stored);
			}
		} catch (e) {
			// Игнорируем ошибки localStorage
			console.warn('Не удалось загрузить тему из localStorage:', e);
		}
	}

	return {
		subscribe,
		set: (value: 'light' | 'dark') => {
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
				const newTheme = current === 'light' ? 'dark' : 'light';
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
		}
	};
}

export const theme = createTheme();
