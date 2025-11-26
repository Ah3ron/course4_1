<script lang="ts">
	import { fade, fly } from 'svelte/transition';
	import type { ModelInfo } from '$lib/api';

	export let modelInfo: ModelInfo;
</script>

<div class="card bg-base-100 shadow-xl" transition:fly={{ y: -20, duration: 400 }}>
	<div class="card-body">
		<h2 class="card-title mb-4 animate-slide-down">О моделях</h2>
		<div class="space-y-4">
			<div class="collapse collapse-plus bg-base-200" transition:fade={{ duration: 200 }}>
				<input type="radio" name="model-accordion" checked={true} />
				<div class="collapse-title text-sm font-semibold">Модель Альтмана</div>
				<div class="collapse-content">
					<p class="text-xs text-base-content/70">{modelInfo.altman_description}</p>
				</div>
			</div>
			<div class="collapse collapse-plus bg-base-200" transition:fade={{ duration: 200, delay: 100 }}>
				<input type="radio" name="model-accordion" />
				<div class="collapse-title text-sm font-semibold">Модель Таффлера</div>
				<div class="collapse-content">
					<p class="text-xs text-base-content/70">{modelInfo.taffler_description}</p>
				</div>
			</div>
		</div>
	</div>
</div>

