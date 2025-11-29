<script lang="ts">
	import RiskBadge from './RiskBadge.svelte';
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

<div class="card bg-base-200 shadow-md smooth-appear">
	<div class="card-body p-5">
		<div class="flex items-center gap-2 mb-4">
			<div class="badge badge-primary badge-lg">Альтман</div>
			<h3 class="card-title text-xl text-base-content">Z-score модель</h3>
		</div>
		<div class="space-y-4">
			<div class="stats stats-vertical w-full smooth-appear">
				<div class="stat">
					<div class="stat-title">Z-score</div>
					<div class="stat-value text-3xl animate-count-up">
						{prediction.altman_z_score.toFixed(4)}
					</div>
					<div class="stat-desc">
						{#if prediction.altman_z_score < -0.5}
							Безопасная зона (Z &lt; -0.5) - хорошее положение
						{:else if prediction.altman_z_score < 0.0}
							Серая зона (-0.5 ≤ Z &lt; 0.0)
						{:else}
							Зона опасности (Z ≥ 0.0) - критичная ситуация
						{/if}
					</div>
				</div>
			</div>
			<div
				class="alert shadow-lg smooth-appear {getRiskColor(prediction.altman_risk_level) === 'success'
					? 'alert-success'
					: getRiskColor(prediction.altman_risk_level) === 'warning'
						? 'alert-warning'
						: getRiskColor(prediction.altman_risk_level) === 'error'
							? 'alert-error'
							: 'alert-neutral'}"
				style="animation-delay: 0.1s;"
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
					<h4 class="font-bold">{getRiskLabel(prediction.altman_risk_level)}</h4>
					<div class="text-sm">{prediction.altman_recommendation}</div>
				</div>
			</div>
		</div>
	</div>
</div>
