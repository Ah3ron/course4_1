<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { isLoading, modelInfo, predictionHistory } from '$lib/stores';
	import { getModelInfo, predictCreditRisk, type FinancialData } from '$lib/api';
	import type { PredictionResponse } from '$lib/api';

	// Компоненты
	import FinancialForm from '$lib/components/FinancialForm.svelte';
	import PredictionResults from '$lib/components/PredictionResults.svelte';
	import ModelInfoCard from '$lib/components/ModelInfoCard.svelte';
	import PredictionHistory from '$lib/components/PredictionHistory.svelte';

	let formData: FinancialData = {
		// Данные для модели Альтмана
		current_assets: 700000,
		current_liabilities: 200000,
		debt_capital: 500000,
		liabilities: 800000,
		// Данные для модели Таффлера
		sales_profit: 300000,
		short_term_liabilities: 200000,
		long_term_liabilities: 300000,
		total_assets: 2000000,
		sales: 3000000
	};

	let prediction: PredictionResponse | null = null;
	let error: string | null = null;
	let formErrors: Record<string, string> = {};

	// Загрузка информации о моделях при монтировании
	onMount(async () => {
		try {
			isLoading.set(true);
			const info = await getModelInfo();
			modelInfo.set(info);
		} catch (e) {
			console.error('Ошибка при загрузке информации о моделях:', e);
		} finally {
			isLoading.set(false);
		}
	});

	function validateForm(): boolean {
		formErrors = {};

		// Валидация обязательных положительных полей
		if (!formData.total_assets || formData.total_assets <= 0) {
			formErrors.total_assets = 'Общие активы должны быть положительным числом';
		}

		if (!formData.liabilities || formData.liabilities <= 0) {
			formErrors.liabilities = 'Пассивы должны быть положительным числом';
		}

		if (!formData.current_liabilities || formData.current_liabilities <= 0) {
			formErrors.current_liabilities = 'Текущие обязательства должны быть положительным числом';
		}

		if (!formData.short_term_liabilities || formData.short_term_liabilities <= 0) {
			formErrors.short_term_liabilities = 'Краткосрочные обязательства должны быть положительным числом';
		}

		return Object.keys(formErrors).length === 0;
	}

	async function handleSubmit() {
		error = null;
		prediction = null;

		if (!validateForm()) {
			error = 'Пожалуйста, исправьте ошибки в форме';
			return;
		}

		try {
			isLoading.set(true);
			const result = await predictCreditRisk(formData);
			prediction = result;

			// Добавляем в историю
			predictionHistory.add({
				id: Date.now().toString(),
				timestamp: new Date().toISOString(),
				data: {
					total_assets: formData.total_assets,
					liabilities: formData.liabilities,
					sales: formData.sales
				},
				result
			});
		} catch (e) {
			error = e instanceof Error ? e.message : 'Произошла ошибка при оценке кредитного риска';
			console.error('Ошибка оценки:', e);
		} finally {
			isLoading.set(false);
		}
	}
</script>

<svelte:head>
	<title>Система оценки кредитных рисков</title>
</svelte:head>

<div class="min-h-screen bg-base-200">
	<div class="container mx-auto px-4 py-8 max-w-7xl">
		<!-- Заголовок -->
		<div class="text-center mb-8" transition:fade={{ duration: 400 }}>
			<h1 class="text-4xl font-bold mb-2 animate-fade-in-title">
				Система оценки кредитных рисков
			</h1>
			<p class="text-lg text-base-content/70 animate-fade-in-subtitle">
				Программный модуль на основе статистических моделей Альтмана и Таффлера
			</p>
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<!-- Основной контент -->
			<div class="lg:col-span-2 space-y-6">
				<!-- Форма ввода данных -->
				<FinancialForm
					bind:formData
					bind:formErrors
					isLoading={$isLoading}
					bind:error
					{handleSubmit}
				/>

				<!-- Результаты оценки -->
				{#if prediction}
					<PredictionResults {prediction} />
				{/if}
			</div>

			<!-- Боковая панель -->
			<aside class="lg:col-span-1 space-y-6">
				<!-- Информация о моделях -->
				{#if $modelInfo}
					<ModelInfoCard modelInfo={$modelInfo} />
				{/if}

				<!-- История оценок -->
				<PredictionHistory
					history={$predictionHistory}
					clearHistory={() => predictionHistory.clear()}
				/>
			</aside>
		</div>
	</div>
</div>
