<script lang="ts">
	import AltmanResult from './AltmanResult.svelte';
	import TafflerResult from './TafflerResult.svelte';
	import CombinedRiskAlert from './CombinedRiskAlert.svelte';
	import type { PredictionResponse } from '$lib/api';

	export let prediction: PredictionResponse;
</script>

<div class="card bg-base-100 shadow-xl smooth-appear">
	<div class="card-body p-6">
		<h2 class="card-title text-2xl mb-6 text-base-content">Результаты оценки</h2>

		<div class="space-y-6">
			<AltmanResult {prediction} />
			<TafflerResult {prediction} />
			<CombinedRiskAlert {prediction} />
		</div>
	</div>
</div>
