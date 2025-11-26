<script lang="ts">
	import { fade } from 'svelte/transition';
	import AltmanResult from './AltmanResult.svelte';
	import TafflerResult from './TafflerResult.svelte';
	import CombinedRiskAlert from './CombinedRiskAlert.svelte';
	import type { PredictionResponse } from '$lib/api';

	export let prediction: PredictionResponse;
</script>

<div class="card bg-base-100 shadow-xl" transition:fade={{ duration: 300 }}>
	<div class="card-body">
		<h2 class="card-title text-2xl mb-6 animate-slide-down">Результаты оценки</h2>

		<div class="space-y-6">
			<AltmanResult {prediction} />
			<TafflerResult {prediction} />
			<CombinedRiskAlert {prediction} />
		</div>
	</div>
</div>
