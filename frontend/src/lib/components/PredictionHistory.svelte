<script lang="ts">
	import { fade, fly } from 'svelte/transition';
	import RiskBadge from './RiskBadge.svelte';
	import type { PredictionHistoryItem } from '$lib/stores';

	export let history: PredictionHistoryItem[];
	export let clearHistory: () => void;

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

<div class="card bg-base-100 shadow-xl" transition:fly={{ y: -20, duration: 400, delay: 100 }}>
	<div class="card-body">
		<div class="flex justify-between items-center mb-4">
			<h2 class="card-title text-lg animate-slide-down">История оценок</h2>
			{#if history.length > 0}
				<button
					class="btn btn-sm btn-ghost transition-all duration-200 hover:scale-110"
					onclick={clearHistory}
					aria-label="Очистить историю"
				>
					Очистить
				</button>
			{/if}
		</div>

		{#if history.length === 0}
			<div class="text-center py-8" transition:fade>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-12 w-12 mx-auto text-base-content/30 mb-2 animate-pulse"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
					/>
				</svg>
				<p class="text-sm text-base-content/50">История оценок пуста</p>
			</div>
		{:else}
			<div class="space-y-2 max-h-96 overflow-y-auto">
				{#each history.slice(0, 10) as item, index (item.id)}
					<div
						class="card bg-base-200 shadow-sm hover:shadow-md transition-all duration-200 hover:scale-[1.02] cursor-pointer"
						transition:fly={{ y: 20, duration: 300, delay: index * 50 }}
					>
						<div class="card-body p-4">
							<div class="flex justify-between items-start gap-2">
								<div class="flex-1 min-w-0">
									<p class="text-xs text-base-content/50 mb-1">
										{new Date(item.timestamp).toLocaleString('ru-RU')}
									</p>
									<p class="text-sm font-semibold mb-1">
										Риск: {item.result.combined_risk_level
											? getRiskLabel(item.result.combined_risk_level)
											: 'Неизвестно'}
									</p>
									{#if item.result.altman_z_score !== undefined &&
										item.result.taffler_z_score !== undefined}
										<p class="text-xs text-base-content/70">
											Альтман: {item.result.altman_z_score.toFixed(2)} | Таффлер:
											{item.result.taffler_z_score.toFixed(2)}
										</p>
									{:else}
										<p class="text-xs text-base-content/50 italic">Старый формат данных</p>
									{/if}
								</div>
								{#if item.result.combined_risk_level}
									<RiskBadge riskLevel={item.result.combined_risk_level} size="sm" />
								{/if}
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>

