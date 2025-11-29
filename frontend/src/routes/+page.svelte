<script lang="ts">
	import { onMount } from 'svelte';
	import { isLoading, modelInfo, predictionHistory } from '$lib/stores';
	import {
		getModelInfo,
		predictCreditRisk,
		predictIndividualCreditRisk,
		type FinancialData,
		type IndividualData
	} from '$lib/api';
	import type { PredictionResponse, IndividualPredictionResponse } from '$lib/api';

	// Компоненты
	import FinancialForm from '$lib/components/FinancialForm.svelte';
	import IndividualForm from '$lib/components/IndividualForm.svelte';
	import PredictionResults from '$lib/components/PredictionResults.svelte';
	import IndividualResult from '$lib/components/IndividualResult.svelte';
	import ModelInfoCard from '$lib/components/ModelInfoCard.svelte';
	import PredictionHistory from '$lib/components/PredictionHistory.svelte';

	type BorrowerType = 'company' | 'individual';

	let borrowerType: BorrowerType = 'company';

	let formData: FinancialData = {
		company_name: '',
		assessment_date: new Date().toISOString().split('T')[0],
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

	let individualData: IndividualData = {
		full_name: '',
		assessment_date: new Date().toISOString().split('T')[0],
		monthly_income: 100000,
		monthly_expenses: 60000,
		credit_amount: 500000,
		credit_history_score: 0.8,
		has_collateral: 1,
		employment_years: 5,
		age: 35
	};

	let prediction: PredictionResponse | null = null;
	let individualPrediction: IndividualPredictionResponse | null = null;
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

		if (borrowerType === 'company') {
			// Валидация для юридических лиц
			if (!formData.company_name || formData.company_name.trim() === '') {
				formErrors.company_name = 'Название организации обязательно';
			}
			if (!formData.assessment_date) {
				formErrors.assessment_date = 'Дата оценки обязательна';
			}
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
		} else {
			// Валидация для физических лиц
			if (!individualData.full_name || individualData.full_name.trim() === '') {
				formErrors.full_name = 'ФИО обязательно';
			}
			if (!individualData.assessment_date) {
				formErrors.assessment_date = 'Дата оценки обязательна';
			}
			if (!individualData.monthly_income || individualData.monthly_income <= 0) {
				formErrors.monthly_income = 'Месячный доход должен быть положительным числом';
			}

			if (!individualData.monthly_expenses || individualData.monthly_expenses <= 0) {
				formErrors.monthly_expenses = 'Месячные расходы должны быть положительным числом';
			}

			if (!individualData.credit_amount || individualData.credit_amount <= 0) {
				formErrors.credit_amount = 'Сумма кредита должна быть положительным числом';
			}

			if (
				individualData.credit_history_score < 0 ||
				individualData.credit_history_score > 1
			) {
				formErrors.credit_history_score = 'Оценка кредитной истории должна быть от 0 до 1';
			}

			if (individualData.age < 18 || individualData.age > 100) {
				formErrors.age = 'Возраст должен быть от 18 до 100 лет';
			}

			if (individualData.employment_years < 0) {
				formErrors.employment_years = 'Трудовой стаж не может быть отрицательным';
			}
		}

		return Object.keys(formErrors).length === 0;
	}

	async function handleSubmit() {
		error = null;
		prediction = null;
		individualPrediction = null;

		if (!validateForm()) {
			error = 'Пожалуйста, исправьте ошибки в форме';
			return;
		}

		try {
			isLoading.set(true);
			if (borrowerType === 'company') {
				const result = await predictCreditRisk(formData);
				prediction = result;

				// Добавляем в историю
				predictionHistory.add({
					id: Date.now().toString(),
					timestamp: new Date().toISOString(),
					type: 'company',
					data: {
						total_assets: formData.total_assets,
						liabilities: formData.liabilities,
						sales: formData.sales
					},
					result
				});
			} else {
				const result = await predictIndividualCreditRisk(individualData);
				individualPrediction = result;

				// Добавляем в историю
				predictionHistory.add({
					id: Date.now().toString(),
					timestamp: new Date().toISOString(),
					type: 'individual',
					data: {
						monthly_income: individualData.monthly_income,
						credit_amount: individualData.credit_amount,
						credit_score: result.credit_score
					},
					result
				});
			}
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
	<div class="container mx-auto px-4 md:px-6 py-8 md:py-12 max-w-7xl">
		<!-- Заголовок -->
		<div class="text-center mb-8">
			<h1 class="text-4xl md:text-5xl font-bold mb-3 bg-gradient-to-r from-primary to-secondary bg-clip-text animate-fade-in-title">
				Система оценки кредитных рисков
			</h1>
			<p class="text-lg md:text-xl text-base-content/70 animate-fade-in-subtitle">
				Программный модуль на основе статистических моделей для юридических и физических лиц
			</p>
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<!-- Основной контент -->
			<div class="lg:col-span-2 space-y-6">
				<!-- Переключатель типа заемщика -->
				<div class="card bg-base-100 shadow-xl smooth-appear">
					<div class="card-body py-5">
						<div class="form-control">
							<label class="label cursor-pointer justify-center py-2">
								<span class="label-text text-lg font-semibold mr-4">Тип заемщика:</span>
								<div class="join">
									<button
										class="join-item btn {borrowerType === 'company'
											? 'btn-primary'
											: 'btn-outline btn-ghost'}"
										onclick={() => {
											borrowerType = 'company';
											prediction = null;
											individualPrediction = null;
											error = null;
										}}
									>
										Юридическое лицо
									</button>
									<button
										class="join-item btn {borrowerType === 'individual'
											? 'btn-primary'
											: 'btn-outline btn-ghost'}"
										onclick={() => {
											borrowerType = 'individual';
											prediction = null;
											individualPrediction = null;
											error = null;
										}}
									>
										Физическое лицо
									</button>
								</div>
							</label>
						</div>
					</div>
				</div>

				<!-- Форма ввода данных -->
				<div class="smooth-appear">
					{#if borrowerType === 'company'}
						<FinancialForm
							bind:formData
							bind:formErrors
							isLoading={$isLoading}
							bind:error
							{handleSubmit}
						/>
					{:else}
						<IndividualForm
							bind:formData={individualData}
							bind:formErrors
							isLoading={$isLoading}
							bind:error
							{handleSubmit}
						/>
					{/if}
				</div>

				<!-- Результаты оценки -->
				{#if prediction}
					<div class="smooth-appear">
						<PredictionResults {prediction} />
					</div>
				{/if}
				{#if individualPrediction}
					<div class="smooth-appear">
						<IndividualResult prediction={individualPrediction} />
					</div>
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
