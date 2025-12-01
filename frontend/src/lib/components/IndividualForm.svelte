<script lang="ts">
	import FormField from './FormField.svelte';
	import type { IndividualData } from '$lib/api';

	export let formData: IndividualData;
	export let formErrors: Record<string, string> = {};
	export let isLoading: boolean = false;
	export let error: string | null = null;
	export let handleSubmit: () => void = () => {};

	// Локальная переменная для синхронизации с числовым значением
	let hasCollateral: boolean = formData.has_collateral === 1;

	// Синхронизация: когда formData.has_collateral изменяется извне, обновляем локальную переменную
	$: {
		const newValue = formData.has_collateral === 1;
		if (hasCollateral !== newValue) {
			hasCollateral = newValue;
		}
	}

	// Синхронизация: когда локальная переменная изменяется через bind:checked, обновляем formData.has_collateral
	$: {
		const expectedValue = hasCollateral ? 1 : 0;
		if (formData.has_collateral !== expectedValue) {
			formData.has_collateral = expectedValue;
		}
	}
</script>

<div class="card bg-base-100 shadow-xl smooth-appear">
	<div class="card-body p-6">
		<h2 class="card-title text-2xl mb-6 text-base-content">Данные физического лица</h2>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
			<FormField
				label="ФИО"
				bind:value={formData.full_name}
				error={formErrors.full_name}
				required={true}
				hint="Фамилия Имя Отчество"
				type="text"
				placeholder="Введите ФИО"
			/>

			<FormField
				label="Дата оценки"
				bind:value={formData.assessment_date}
				error={formErrors.assessment_date}
				required={true}
				hint="Дата оценки"
				type="date"
			/>
		</div>

		{#if error}
			<div class="alert alert-error mb-4 animate-shake smooth-appear">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="stroke-current shrink-0 h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
					/>
				</svg>
				<span>{error}</span>
			</div>
		{/if}

		<form
			onsubmit={(e) => {
				e.preventDefault();
				handleSubmit();
			}}
			class="space-y-6"
		>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<FormField
					label="Месячный доход"
					bind:value={formData.monthly_income}
					error={formErrors.monthly_income}
					required={true}
					hint="Сумма всех доходов в месяц"
					step={1000}
				/>

				<FormField
					label="Месячные расходы"
					bind:value={formData.monthly_expenses}
					error={formErrors.monthly_expenses}
					required={true}
					hint="Сумма всех расходов в месяц"
					step={1000}
				/>

				<FormField
					label="Сумма кредита"
					bind:value={formData.credit_amount}
					error={formErrors.credit_amount}
					required={true}
					hint="Запрашиваемая сумма кредита"
					step={10000}
				/>

				<FormField
					label="Оценка кредитной истории"
					bind:value={formData.credit_history_score}
					error={formErrors.credit_history_score}
					required={true}
					hint="От 0 (плохая) до 1 (отличная)"
					step={0.1}
				/>

				<FormField
					label="Трудовой стаж (лет)"
					bind:value={formData.employment_years}
					error={formErrors.employment_years}
					required={true}
					hint="Количество лет на текущем месте работы"
					step={1}
				/>

				<FormField
					label="Возраст"
					bind:value={formData.age}
					error={formErrors.age}
					required={true}
					hint="Возраст заемщика (от 18 до 100)"
					step={1}
				/>

				<div class="form-control md:col-span-2">
					<label class="label cursor-pointer justify-start gap-4">
						<span class="label-text font-medium">Наличие залога</span>
						<input
							type="checkbox"
							class="toggle toggle-primary"
							bind:checked={hasCollateral}
						/>
					</label>
					<div class="label">
						<span class="label-text-alt text-base-content/60">
							Отметьте, если есть залог (недвижимость, автомобиль и т.д.)
						</span>
					</div>
				</div>
			</div>

			<!-- Кнопка отправки -->
			<div class="flex justify-end mt-8 smooth-appear">
				<button
					type="submit"
					class="btn btn-primary btn-lg"
					disabled={isLoading}
				>
					{#if isLoading}
						<span class="loading loading-spinner"></span>
						Обработка...
					{:else}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-5 w-5 mr-2"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
							/>
						</svg>
						Оценить кредитный риск
					{/if}
				</button>
			</div>
		</form>
	</div>
</div>

