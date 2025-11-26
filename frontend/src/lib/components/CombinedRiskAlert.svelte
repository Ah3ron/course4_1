<script lang="ts">
	import { fade, scale } from 'svelte/transition';
	import type { PredictionResponse } from '$lib/api';

	export let prediction: PredictionResponse;

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
</script>

<div
	class="alert shadow-lg {getRiskColor(prediction.combined_risk_level) === 'success' ? 'alert-success' : getRiskColor(prediction.combined_risk_level) === 'warning' ? 'alert-warning' : getRiskColor(prediction.combined_risk_level) === 'error' ? 'alert-error' : 'alert-neutral'}"
	transition:scale={{ start: 0.9, duration: 400 }}
>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		class="stroke-current shrink-0 h-6 w-6 animate-pulse"
		fill="none"
		viewBox="0 0 24 24"
	>
		<path
			stroke-linecap="round"
			stroke-linejoin="round"
			stroke-width="2"
			d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
		/>
	</svg>
	<div class="flex-1">
		<h3 class="font-bold text-lg animate-fade-in-delay">
			Общая оценка: {getRiskLabel(prediction.combined_risk_level)}
		</h3>
		<div class="text-sm mt-1 animate-fade-in-delay-2">{prediction.combined_recommendation}</div>
	</div>
</div>

