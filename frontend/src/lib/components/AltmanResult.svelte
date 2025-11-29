<script lang="ts">
	import { fly, fade } from 'svelte/transition';
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

<div class="card bg-base-200 shadow-md" transition:fly={{ y: 20, duration: 400 }}>
	<div class="card-body">
		<div class="flex items-center gap-2 mb-4">
			<div class="badge badge-primary badge-lg animate-bounce-in">Альтман</div>
			<h3 class="card-title text-xl">Z-score модель</h3>
		</div>
		<div class="space-y-4">
			<div
				class="stats stats-vertical shadow w-full"
				transition:fade={{ duration: 300, delay: 100 }}
			>
				<div class="stat">
					<div class="stat-title">Z-score</div>
					<div class="stat-value text-3xl animate-count-up">
						{prediction.altman_z_score.toFixed(4)}
					</div>
					<div class="stat-desc">
						{#if prediction.altman_z_score > 0.0}
							Безопасная зона (Z &gt; 0.0)
						{:else if prediction.altman_z_score > -0.5}
							Серая зона (-0.5 &lt; Z &lt; 0.0)
						{:else}
							Зона опасности (Z &lt; -0.5)
						{/if}
					</div>
				</div>
			</div>
			<div
				class="alert shadow-lg {getRiskColor(prediction.altman_risk_level) === 'success'
					? 'alert-success'
					: getRiskColor(prediction.altman_risk_level) === 'warning'
						? 'alert-warning'
						: getRiskColor(prediction.altman_risk_level) === 'error'
							? 'alert-error'
							: 'alert-neutral'}"
				transition:fade={{ duration: 300, delay: 200 }}
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
