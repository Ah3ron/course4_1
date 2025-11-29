<script lang="ts">
	import FormField from './FormField.svelte';
	import type { FinancialData } from '$lib/api';

	export let formData: FinancialData;
	export let formErrors: Record<string, string> = {};
	export let isLoading: boolean = false;
	export let error: string | null = null;
	export let handleSubmit: () => void = () => {};
</script>

<div class="card bg-base-100 shadow-xl smooth-appear">
	<div class="card-body p-6">
		<h2 class="card-title text-2xl mb-6 text-base-content">Финансовые показатели компании</h2>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
			<FormField
				label="Название организации"
				bind:value={formData.company_name}
				error={formErrors.company_name}
				required={true}
				hint="Полное наименование организации"
				type="text"
				placeholder="Введите название организации"
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
			<!-- Модель Альтмана -->
			<div class="smooth-appear">
				<div class="divider">
					<span class="text-lg font-semibold">Данные для модели Альтмана</span>
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
					<FormField
						label="Текущие активы"
						bind:value={formData.current_assets}
						hint="Активы, обращаемые в деньги в течение года"
					/>

					<FormField
						label="Текущие обязательства"
						bind:value={formData.current_liabilities}
						error={formErrors.current_liabilities}
						required={true}
						hint="Краткосрочные обязательства компании"
					/>

					<FormField
						label="Заемный капитал"
						bind:value={formData.debt_capital}
						hint="Сумма заемных средств компании"
					/>

					<FormField
						label="Пассивы"
						bind:value={formData.liabilities}
						error={formErrors.liabilities}
						required={true}
						hint="Общая сумма пассивов компании"
					/>
				</div>
			</div>

			<!-- Модель Таффлера -->
			<div class="smooth-appear">
				<div class="divider">
					<span class="text-lg font-semibold">Данные для модели Таффлера</span>
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
					<FormField
						label="Прибыль от продаж"
						bind:value={formData.sales_profit}
						hint="Прибыль от реализации продукции"
					/>

					<FormField
						label="Краткосрочные обязательства"
						bind:value={formData.short_term_liabilities}
						error={formErrors.short_term_liabilities}
						required={true}
						hint="Обязательства со сроком погашения до года"
					/>

					<FormField
						label="Текущие активы"
						bind:value={formData.current_assets}
						hint="Активы, обращаемые в деньги в течение года"
					/>

					<FormField
						label="Обязательства"
						bind:value={formData.liabilities}
						error={formErrors.liabilities}
						required={true}
						hint="Общая сумма обязательств компании"
					/>

					<FormField
						label="Долгосрочные обязательства"
						bind:value={formData.long_term_liabilities}
						hint="Обязательства со сроком погашения более года"
					/>

					<FormField
						label="Общая сумма активов"
						bind:value={formData.total_assets}
						error={formErrors.total_assets}
						required={true}
						hint="Сумма всех активов компании"
					/>

					<FormField
						label="Выручка от продаж"
						bind:value={formData.sales}
						span={2}
						hint="Объем продаж компании"
					/>
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
