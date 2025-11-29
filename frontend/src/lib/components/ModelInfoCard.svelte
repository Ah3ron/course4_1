<script lang="ts">
	import type { ModelInfo } from '$lib/api';

	export let modelInfo: ModelInfo;
</script>

<div class="card bg-base-100 shadow-xl smooth-appear">
	<div class="card-body p-5">
		<h2 class="card-title mb-4 text-base-content">О моделях</h2>
		<p class="text-xs text-base-content/60 mb-4">
			Система использует статистические модели для оценки кредитных рисков юридических и физических лиц
		</p>
		<div class="space-y-3">
			<!-- Модель Альтмана -->
			<div class="collapse collapse-plus bg-base-200 smooth-appear">
				<input type="radio" name="model-accordion" checked={true} />
				<div class="collapse-title text-sm font-semibold flex items-center gap-2">
					<span class="badge badge-primary badge-xs">Компании</span>
					<span>Модель Альтмана (Z-score)</span>
				</div>
				<div class="collapse-content">
					<p class="text-xs text-base-content/70 leading-relaxed">{modelInfo.altman_description}</p>
				</div>
			</div>
			
			<!-- Модель Таффлера -->
			<div class="collapse collapse-plus bg-base-200 smooth-appear">
				<input type="radio" name="model-accordion" />
				<div class="collapse-title text-sm font-semibold flex items-center gap-2">
					<span class="badge badge-primary badge-xs">Компании</span>
					<span>Модель Таффлера (T-score)</span>
				</div>
				<div class="collapse-content">
					<p class="text-xs text-base-content/70 leading-relaxed">{modelInfo.taffler_description}</p>
				</div>
			</div>
			
			<!-- Модель для физических лиц -->
			<div class="collapse collapse-plus bg-base-200 smooth-appear">
				<input type="radio" name="model-accordion" />
				<div class="collapse-title text-sm font-semibold flex items-center gap-2">
					<span class="badge badge-secondary badge-xs">Физ. лица</span>
					<span>Скоринговая модель</span>
				</div>
				<div class="collapse-content">
					<p class="text-xs text-base-content/70 leading-relaxed">{modelInfo.individual_description}</p>
				</div>
			</div>
		</div>
	</div>
</div>
