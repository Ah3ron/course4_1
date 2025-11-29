<script lang="ts">
	import { onMount, onDestroy, afterUpdate } from 'svelte';
	import Chart from 'chart.js/auto';

	export let title: string;
	export let history: Array<{
		assessment_date: string;
		altman_z_score?: number;
		taffler_z_score?: number;
		credit_score?: number;
	}>;
	export let onClose: () => void;

	let chartCanvas: HTMLCanvasElement | null = null;
	let chartInstance: Chart | null = null;

	function createChart() {
		if (!chartCanvas || !history || history.length === 0) return;

		// Уничтожаем предыдущий график если он существует
		if (chartInstance) {
			chartInstance.destroy();
			chartInstance = null;
		}

		const existingChart = Chart.getChart(chartCanvas);
		if (existingChart) {
			existingChart.destroy();
		}

		const ctx = chartCanvas.getContext('2d');
		if (!ctx) return;

				const labels = history.map((h) => new Date(h.assessment_date).toLocaleDateString('ru-RU'));
				const isSinglePoint = labels.length === 1;

				// Определяем тип данных
				const hasAltman = history[0].altman_z_score !== undefined;
				const hasTaffler = history[0].taffler_z_score !== undefined;
				const hasCreditScore = history[0].credit_score !== undefined;

				let chartLabels = labels;
				let datasets: any[] = [];

				if (hasAltman && hasTaffler) {
					// График для компаний
					const altmanData = history.map((h) => h.altman_z_score!);
					const tafflerData = history.map((h) => h.taffler_z_score!);

					if (isSinglePoint) {
						chartLabels = ['', labels[0], ''];
					}

					datasets = [
						{
							label: 'Z-score (Альтман)',
							data: isSinglePoint ? [altmanData[0], altmanData[0], altmanData[0]] : altmanData,
							borderColor: 'rgb(75, 192, 192)',
							backgroundColor: 'rgba(75, 192, 192, 0.2)',
							tension: 0.1,
							pointRadius: isSinglePoint ? [0, 8, 0] : 8,
							pointHoverRadius: isSinglePoint ? [0, 10, 0] : 10
						},
						{
							label: 'T-score (Таффлер)',
							data: isSinglePoint ? [tafflerData[0], tafflerData[0], tafflerData[0]] : tafflerData,
							borderColor: 'rgb(255, 99, 132)',
							backgroundColor: 'rgba(255, 99, 132, 0.2)',
							tension: 0.1,
							pointRadius: isSinglePoint ? [0, 8, 0] : 8,
							pointHoverRadius: isSinglePoint ? [0, 10, 0] : 10
						}
					];
				} else if (hasCreditScore) {
					// График для физических лиц
					const creditScoreData = history.map((h) => h.credit_score!);

					if (isSinglePoint) {
						chartLabels = ['', labels[0], ''];
					}

					datasets = [
						{
							label: 'Кредитный скоринг',
							data: isSinglePoint ? [creditScoreData[0], creditScoreData[0], creditScoreData[0]] : creditScoreData,
							borderColor: 'rgb(54, 162, 235)',
							backgroundColor: 'rgba(54, 162, 235, 0.2)',
							tension: 0.1,
							pointRadius: isSinglePoint ? [0, 8, 0] : 8,
							pointHoverRadius: isSinglePoint ? [0, 10, 0] : 10
						}
					];
				}

				chartInstance = new Chart(ctx, {
					type: 'line',
					data: {
						labels: chartLabels,
						datasets
					},
					options: {
						responsive: true,
						maintainAspectRatio: false,
						plugins: {
							title: {
								display: true,
								text: hasAltman ? 'Динамика показателей' : 'Динамика кредитного скоринга'
							},
							legend: {
								display: true
							}
						},
						scales: isSinglePoint ? {
							x: {
								ticks: {
									callback: function(value, index) {
										if (index === 1) {
											return labels[0];
										}
										return '';
									}
								}
							}
						} : undefined
					}
				});
	}

	onMount(() => {
		setTimeout(() => createChart(), 200);
	});

	afterUpdate(() => {
		if (history && history.length > 0) {
			setTimeout(() => createChart(), 200);
		}
	});

	onDestroy(() => {
		if (chartInstance) {
			chartInstance.destroy();
			chartInstance = null;
		}
	});
</script>

<div class="card bg-base-100 shadow-xl smooth-appear">
	<div class="card-body p-5">
		<div class="flex justify-between items-center mb-4">
			<h2 class="card-title">История: {title}</h2>
			<button
				class="btn btn-sm btn-circle btn-ghost"
				onclick={onClose}
				aria-label="Закрыть график"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M6 18L18 6M6 6l12 12"
					/>
				</svg>
			</button>
		</div>
		<div class="h-96">
			<canvas bind:this={chartCanvas}></canvas>
		</div>
	</div>
</div>

