<script lang="ts">
	import type { IndividualPredictionResponse } from '$lib/api';

	export let prediction: IndividualPredictionResponse;

	function getRiskColor(riskLevel: string): string {
		switch (riskLevel) {
			case 'low':
				return 'success';
			case 'medium':
				return 'warning';
			case 'high':
				return 'error';
			default:
				return 'neutral';
		}
	}

	function getRiskLabel(riskLevel: string): string {
		switch (riskLevel) {
			case 'low':
				return 'Низкий риск';
			case 'medium':
				return 'Средний риск';
			case 'high':
				return 'Высокий риск';
			default:
				return 'Неизвестно';
		}
	}

	function getScoreColor(score: number): string {
		if (score > 700) return 'text-success';
		if (score > 500) return 'text-warning';
		return 'text-error';
	}
</script>

<div class="card bg-base-200 shadow-md smooth-appear">
	<div class="card-body p-5">
		<div class="flex items-center gap-2 mb-4">
			<div class="badge badge-secondary badge-lg">Скоринг</div>
			<h3 class="card-title text-xl text-base-content">Кредитный скоринг</h3>
		</div>
		<div class="space-y-4">
			<div class="stats stats-vertical w-full smooth-appear" style="animation-delay: 0.1s;">
				<div class="stat">
					<div class="stat-title">Кредитный скоринг</div>
					<div class="stat-value text-3xl animate-count-up {getScoreColor(prediction.credit_score)}">
						{prediction.credit_score.toFixed(0)}
					</div>
					<div class="stat-desc">
						Диапазон: 300-850
						{#if prediction.credit_score > 700}
							| Низкий риск (Score &gt; 700)
						{:else if prediction.credit_score > 500}
							| Средний риск (500 &lt; Score &lt; 700)
						{:else}
							| Высокий риск (Score &lt; 500)
						{/if}
					</div>
				</div>
			</div>
			<div
				class="alert shadow-lg smooth-appear {getRiskColor(prediction.risk_level) === 'success'
					? 'alert-success'
					: getRiskColor(prediction.risk_level) === 'warning'
						? 'alert-warning'
						: getRiskColor(prediction.risk_level) === 'error'
							? 'alert-error'
							: 'alert-neutral'}"
				style="animation-delay: 0.2s;"
			>
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
						d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
					/>
				</svg>
				<div>
					<h4 class="font-bold">{getRiskLabel(prediction.risk_level)}</h4>
					<div class="text-sm">{prediction.recommendation}</div>
				</div>
			</div>
		</div>
	</div>
</div>

