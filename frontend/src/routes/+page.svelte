<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { isLoading, modelInfo, predictionHistory } from '$lib/stores';
	import { getModelInfo, predictBankruptcyRisk, type FinancialData } from '$lib/api';
	import type { PredictionResponse } from '$lib/api';

	// Компоненты
	import FinancialForm from '$lib/components/FinancialForm.svelte';
	import PredictionResults from '$lib/components/PredictionResults.svelte';
	import ModelInfoCard from '$lib/components/ModelInfoCard.svelte';
	import PredictionHistory from '$lib/components/PredictionHistory.svelte';

	let formData: FinancialData = {
		// Данные для модели Альтмана
		working_capital: 500000,
		total_assets: 2000000,
		retained_earnings: 300000,
		ebit: 400000,
		market_value_equity: 1500000,
		total_liabilities: 500000,
		sales: 3000000,
		// Данные для модели Таффлера
		profit_before_tax: 350000,
		current_liabilities: 200000,
		current_assets: 700000,
		operating_income: 380000
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

		if (!formData.total_liabilities || formData.total_liabilities <= 0) {
			formErrors.total_liabilities = 'Общие обязательства должны быть положительным числом';
		}

		if (!formData.current_liabilities || formData.current_liabilities <= 0) {
			formErrors.current_liabilities = 'Текущие обязательства должны быть положительным числом';
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
			const result = await predictBankruptcyRisk(formData);
			prediction = result;

			// Добавляем в историю
			predictionHistory.add({
				id: Date.now().toString(),
				timestamp: new Date().toISOString(),
				data: {
					total_assets: formData.total_assets,
					total_liabilities: formData.total_liabilities,
					sales: formData.sales
				},
				result
			});
		} catch (e) {
			error = e instanceof Error ? e.message : 'Произошла ошибка при получении оценки';
			console.error('Ошибка оценки:', e);
		} finally {
			isLoading.set(false);
		}
	}
</script>

<svelte:head>
	<title>Оценка риска банкротства</title>
</svelte:head>

<div class="min-h-screen bg-base-200">
	<div class="container mx-auto px-4 py-8 max-w-7xl">
		<!-- Заголовок -->
		<div class="text-center mb-8" transition:fade={{ duration: 400 }}>
			<h1 class="text-4xl font-bold mb-2 animate-fade-in-title">Система оценки риска банкротства</h1>
			<p class="text-lg text-base-content/70 animate-fade-in-subtitle">
				Модели Альтмана и Таффлера для анализа финансового состояния компании
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
					handleSubmit={handleSubmit}
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
				<PredictionHistory history={$predictionHistory} clearHistory={() => predictionHistory.clear()} />
			</aside>
		</div>
	</div>
</div>

<style>
	@keyframes fade-in-title {
		from {
			opacity: 0;
			transform: translateY(-20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.animate-fade-in-title {
		animation: fade-in-title 0.6s ease-out;
	}

	@keyframes fade-in-subtitle {
		from {
			opacity: 0;
			transform: translateY(-10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.animate-fade-in-subtitle {
		animation: fade-in-subtitle 0.6s ease-out 0.2s both;
	}
</style>
