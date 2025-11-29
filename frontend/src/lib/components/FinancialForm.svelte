<script lang="ts">
	import { fade } from 'svelte/transition';
	import FormField from './FormField.svelte';
	import type { FinancialData } from '$lib/api';

	export let formData: FinancialData;
	export let formErrors: Record<string, string> = {};
	export let isLoading: boolean = false;
	export let error: string | null = null;
	export let handleSubmit: () => void = () => {};
</script>

<div class="card bg-base-100 shadow-xl" transition:fade={{ duration: 300 }}>
	<div class="card-body">
		<h2 class="card-title text-2xl mb-6 animate-slide-down">Финансовые показатели компании</h2>

		{#if error}
			<div class="alert alert-error mb-4 animate-shake" transition:fade>
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
			<div transition:fade={{ duration: 200 }}>
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
			<div transition:fade={{ duration: 200, delay: 100 }}>
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
			<div class="flex justify-end mt-8" transition:fade={{ duration: 200, delay: 200 }}>
				<button
					type="submit"
					class="btn btn-primary btn-lg transition-all duration-200 hover:scale-105 active:scale-95"
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
