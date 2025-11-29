<script lang="ts">
	import { onMount } from 'svelte';
	import {
		getCompanyStatistics,
		getIndividualStatistics,
		getCompanyHistory,
		getIndividualHistory,
		deleteCompanyAssessment,
		deleteIndividualAssessment,
		type CompanyStatistics,
		type IndividualStatistics,
		type CompanyHistory,
		type IndividualHistory
	} from '$lib/api';
	import Chart from 'chart.js/auto';

	type TabType = 'companies' | 'individuals';
	let activeTab: TabType = 'companies';

	let companyStats: CompanyStatistics | null = null;
	let individualStats: IndividualStatistics | null = null;
	let selectedCompany: string | null = null;
	let selectedIndividual: string | null = null;
	let companyHistory: CompanyHistory | null = null;
	let individualHistory: IndividualHistory | null = null;
	let isLoading = false;
	let error: string | null = null;
	let companyChartCanvas: HTMLCanvasElement | null = null;
	let individualChartCanvas: HTMLCanvasElement | null = null;
	let companyChartInstance: Chart | null = null;
	let individualChartInstance: Chart | null = null;

	let searchCompanyName = '';
	let searchIndividualName = '';
	let startDate = '';
	let endDate = '';

	// Сортировка для таблиц
	type SortField = 'company_name' | 'assessment_date' | 'altman_z_score' | 'taffler_z_score' | 'combined_risk_level';
	type IndividualSortField = 'full_name' | 'assessment_date' | 'credit_score' | 'risk_level' | 'credit_amount';
	type SortDirection = 'asc' | 'desc';

	let companySortField: SortField | null = null;
	let companySortDirection: SortDirection = 'asc';
	let individualSortField: IndividualSortField | null = null;
	let individualSortDirection: SortDirection = 'asc';

	onMount(async () => {
		await loadStatistics();
	});

	async function loadStatistics() {
		isLoading = true;
		error = null;
		// Уничтожаем графики при переключении
		if (companyChartInstance) {
			companyChartInstance.destroy();
			companyChartInstance = null;
		}
		if (individualChartInstance) {
			individualChartInstance.destroy();
			individualChartInstance = null;
		}
		selectedCompany = null;
		selectedIndividual = null;
		companyHistory = null;
		individualHistory = null;
		
		try {
			// Обрезаем пробелы перед запросом
			const trimmedCompanyName = searchCompanyName?.trim() || undefined;
			const trimmedIndividualName = searchIndividualName?.trim() || undefined;
			
			if (activeTab === 'companies') {
				companyStats = await getCompanyStatistics(trimmedCompanyName, startDate || undefined, endDate || undefined);
			} else {
				individualStats = await getIndividualStatistics(trimmedIndividualName, startDate || undefined, endDate || undefined);
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Ошибка при загрузке статистики';
		} finally {
			isLoading = false;
		}
	}

	function clearSearch() {
		if (activeTab === 'companies') {
			searchCompanyName = '';
		} else {
			searchIndividualName = '';
		}
	}

	function clearDates() {
		startDate = '';
		endDate = '';
	}

	function clearAll() {
		clearSearch();
		clearDates();
	}

	async function loadCompanyHistory(companyName: string) {
		isLoading = true;
		error = null;
		try {
			selectedCompany = companyName;
			companyHistory = await getCompanyHistory(companyName);
			
			// Создаем график после следующего тика, чтобы canvas был в DOM
			setTimeout(() => {
				if (companyChartCanvas && companyHistory && companyHistory.history.length > 0) {
					// Уничтожаем предыдущий график если он существует
					if (companyChartInstance) {
						companyChartInstance.destroy();
						companyChartInstance = null;
					}
					
					// Проверяем, что canvas не используется другим графиком
					const existingChart = Chart.getChart(companyChartCanvas);
					if (existingChart) {
						existingChart.destroy();
					}
					
					const ctx = companyChartCanvas.getContext('2d');
					if (ctx) {
						const labels = companyHistory.history.map((h) =>
							new Date(h.assessment_date).toLocaleDateString('ru-RU')
						);
						const altmanData = companyHistory.history.map((h) => h.altman_z_score);
						const tafflerData = companyHistory.history.map((h) => h.taffler_z_score);
						
						// Если только одна точка, добавляем фиктивные точки для отображения линии по центру
						const isSinglePoint = labels.length === 1;
						let chartLabels = labels;
						let chartAltmanData = altmanData;
						let chartTafflerData = tafflerData;
						
						if (isSinglePoint) {
							// Добавляем две фиктивные точки (до и после) для горизонтальной линии
							chartLabels = ['', labels[0], ''];
							chartAltmanData = [altmanData[0], altmanData[0], altmanData[0]];
							chartTafflerData = [tafflerData[0], tafflerData[0], tafflerData[0]];
						}
						
						companyChartInstance = new Chart(ctx, {
							type: 'line',
							data: {
								labels: chartLabels,
								datasets: [
									{
										label: 'Z-score (Альтман)',
										data: chartAltmanData,
										borderColor: 'rgb(75, 192, 192)',
										backgroundColor: 'rgba(75, 192, 192, 0.2)',
										tension: 0.1,
										pointRadius: isSinglePoint ? [0, 8, 0] : 8,
										pointHoverRadius: isSinglePoint ? [0, 10, 0] : 10
									},
									{
										label: 'T-score (Таффлер)',
										data: chartTafflerData,
										borderColor: 'rgb(255, 99, 132)',
										backgroundColor: 'rgba(255, 99, 132, 0.2)',
										tension: 0.1,
										pointRadius: isSinglePoint ? [0, 8, 0] : 8,
										pointHoverRadius: isSinglePoint ? [0, 10, 0] : 10
									}
								]
							},
							options: {
								responsive: true,
								maintainAspectRatio: false,
								plugins: {
									title: {
										display: true,
										text: 'Динамика показателей'
									},
									legend: {
										display: true
									}
								},
								scales: isSinglePoint ? {
									x: {
										ticks: {
											callback: function(value, index) {
												// Показываем только среднюю метку (реальную дату)
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
				}
			}, 200);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Ошибка при загрузке истории';
		} finally {
			isLoading = false;
		}
	}

	async function loadIndividualHistory(fullName: string) {
		isLoading = true;
		error = null;
		try {
			selectedIndividual = fullName;
			individualHistory = await getIndividualHistory(fullName);
			
			// Создаем график после следующего тика, чтобы canvas был в DOM
			setTimeout(() => {
				if (individualChartCanvas && individualHistory && individualHistory.history.length > 0) {
					// Уничтожаем предыдущий график если он существует
					if (individualChartInstance) {
						individualChartInstance.destroy();
						individualChartInstance = null;
					}
					
					// Проверяем, что canvas не используется другим графиком
					const existingChart = Chart.getChart(individualChartCanvas);
					if (existingChart) {
						existingChart.destroy();
					}
					
					const ctx = individualChartCanvas.getContext('2d');
					if (ctx) {
						const labels = individualHistory.history.map((h) =>
							new Date(h.assessment_date).toLocaleDateString('ru-RU')
						);
						const creditScoreData = individualHistory.history.map((h) => h.credit_score);
						
						// Если только одна точка, добавляем фиктивные точки для отображения линии по центру
						const isSinglePoint = labels.length === 1;
						let chartLabels = labels;
						let chartCreditScoreData = creditScoreData;
						
						if (isSinglePoint) {
							// Добавляем две фиктивные точки (до и после) для горизонтальной линии
							chartLabels = ['', labels[0], ''];
							chartCreditScoreData = [creditScoreData[0], creditScoreData[0], creditScoreData[0]];
						}
						
						individualChartInstance = new Chart(ctx, {
							type: 'line',
							data: {
								labels: chartLabels,
								datasets: [
									{
										label: 'Кредитный скоринг',
										data: chartCreditScoreData,
										borderColor: 'rgb(54, 162, 235)',
										backgroundColor: 'rgba(54, 162, 235, 0.2)',
										tension: 0.1,
										pointRadius: isSinglePoint ? [0, 8, 0] : 8,
										pointHoverRadius: isSinglePoint ? [0, 10, 0] : 10
									}
								]
							},
							options: {
								responsive: true,
								maintainAspectRatio: false,
								plugins: {
									title: {
										display: true,
										text: 'Динамика кредитного скоринга'
									},
									legend: {
										display: true
									}
								},
								scales: isSinglePoint ? {
									x: {
										ticks: {
											callback: function(value, index) {
												// Показываем только среднюю метку (реальную дату)
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
				}
			}, 200);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Ошибка при загрузке истории';
		} finally {
			isLoading = false;
		}
	}

	function getRiskColor(risk: string): string {
		switch (risk) {
			case 'low':
				return 'text-success';
			case 'medium':
				return 'text-warning';
			case 'high':
				return 'text-error';
			default:
				return '';
		}
	}

	function getRiskLabel(risk: string): string {
		switch (risk) {
			case 'low':
				return 'Низкий';
			case 'medium':
				return 'Средний';
			case 'high':
				return 'Высокий';
			default:
				return risk;
		}
	}

	function sortCompanies(field: SortField) {
		if (!companyStats) return;
		
		if (companySortField === field) {
			companySortDirection = companySortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			companySortField = field;
			companySortDirection = 'asc';
		}

		companyStats.assessments.sort((a, b) => {
			let aVal: any = a[field];
			let bVal: any = b[field];

			if (field === 'assessment_date') {
				aVal = new Date(aVal).getTime();
				bVal = new Date(bVal).getTime();
			} else if (typeof aVal === 'string') {
				aVal = aVal.toLowerCase();
				bVal = bVal.toLowerCase();
			}

			if (aVal < bVal) return companySortDirection === 'asc' ? -1 : 1;
			if (aVal > bVal) return companySortDirection === 'asc' ? 1 : -1;
			return 0;
		});

		companyStats = { ...companyStats };
	}

	function sortIndividuals(field: IndividualSortField) {
		if (!individualStats) return;
		
		if (individualSortField === field) {
			individualSortDirection = individualSortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			individualSortField = field;
			individualSortDirection = 'asc';
		}

		individualStats.assessments.sort((a, b) => {
			let aVal: any = a[field];
			let bVal: any = b[field];

			if (field === 'assessment_date') {
				aVal = new Date(aVal).getTime();
				bVal = new Date(bVal).getTime();
			} else if (typeof aVal === 'string') {
				aVal = aVal.toLowerCase();
				bVal = bVal.toLowerCase();
			}

			if (aVal < bVal) return individualSortDirection === 'asc' ? -1 : 1;
			if (aVal > bVal) return individualSortDirection === 'asc' ? 1 : -1;
			return 0;
		});

		individualStats = { ...individualStats };
	}

	function getSortIcon(field: SortField | IndividualSortField, currentField: SortField | IndividualSortField | null, direction: SortDirection): string {
		if (field !== currentField) return;
		return direction === 'asc' ? '↑' : '↓';
	}

	function closeCompanyChart() {
		if (companyChartInstance) {
			companyChartInstance.destroy();
			companyChartInstance = null;
		}
		selectedCompany = null;
		companyHistory = null;
	}

	function closeIndividualChart() {
		if (individualChartInstance) {
			individualChartInstance.destroy();
			individualChartInstance = null;
		}
		selectedIndividual = null;
		individualHistory = null;
	}

	async function deleteCompany(assessmentId: number) {
		if (!confirm('Вы уверены, что хотите удалить эту запись?')) {
			return;
		}
		
		isLoading = true;
		error = null;
		try {
			await deleteCompanyAssessment(assessmentId);
			// Перезагружаем статистику
			await loadStatistics();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Ошибка при удалении записи';
		} finally {
			isLoading = false;
		}
	}

	async function deleteIndividual(assessmentId: number) {
		if (!confirm('Вы уверены, что хотите удалить эту запись?')) {
			return;
		}
		
		isLoading = true;
		error = null;
		try {
			await deleteIndividualAssessment(assessmentId);
			// Перезагружаем статистику
			await loadStatistics();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Ошибка при удалении записи';
		} finally {
			isLoading = false;
		}
	}
</script>

<svelte:head>
	<title>Статистика - Система оценки кредитных рисков</title>
</svelte:head>

<div class="min-h-screen bg-base-200">
	<div class="container mx-auto px-4 md:px-6 py-8 md:py-12 max-w-7xl">
		<div class="text-center mb-8 smooth-appear">
			<h1 class="text-4xl md:text-5xl font-bold mb-3 bg-gradient-to-r from-primary to-secondary bg-clip-text animate-fade-in-title">
				Статистика и аналитика
			</h1>
			<p class="text-lg md:text-xl text-base-content/70 animate-fade-in-subtitle">Просмотр данных по всем организациям и физическим лицам</p>
		</div>

		<!-- Переключатель типа заемщика -->
		<div class="card bg-base-100 shadow-xl mb-6 smooth-appear">
			<div class="card-body py-5">
				<div class="form-control">
					<label class="label cursor-pointer justify-center py-2">
						<span class="label-text text-lg font-semibold mr-4">Тип заемщика:</span>
						<div class="join">
							<button
								class="join-item btn {activeTab === 'companies'
									? 'btn-primary'
									: 'btn-outline btn-ghost'}"
								onclick={async () => {
									// Уничтожаем графики перед переключением
									if (companyChartInstance) {
										companyChartInstance.destroy();
										companyChartInstance = null;
									}
									if (individualChartInstance) {
										individualChartInstance.destroy();
										individualChartInstance = null;
									}
									activeTab = 'companies';
									selectedCompany = null;
									selectedIndividual = null;
									companyHistory = null;
									individualHistory = null;
									await loadStatistics();
								}}
							>
								Юридические лица
							</button>
							<button
								class="join-item btn {activeTab === 'individuals'
									? 'btn-primary'
									: 'btn-outline btn-ghost'}"
								onclick={async () => {
									// Уничтожаем графики перед переключением
									if (companyChartInstance) {
										companyChartInstance.destroy();
										companyChartInstance = null;
									}
									if (individualChartInstance) {
										individualChartInstance.destroy();
										individualChartInstance = null;
									}
									activeTab = 'individuals';
									selectedCompany = null;
									selectedIndividual = null;
									companyHistory = null;
									individualHistory = null;
									await loadStatistics();
								}}
							>
								Физические лица
							</button>
						</div>
					</label>
				</div>
			</div>
		</div>

		{#if error}
			<div class="alert alert-error mb-4">
				<span>{error}</span>
			</div>
		{/if}

		<!-- Фильтры -->
		<div class="card bg-base-100 shadow-xl mb-6 smooth-appear">
			<div class="card-body p-5">
				<div class="flex flex-col md:flex-row gap-4 items-end">
					<!-- Поле ввода -->
					<div class="flex-1 w-full md:w-auto">
						<label class="input input-bordered w-full flex items-center gap-2 pr-2">
							{#if activeTab === 'companies'}
								<input
									type="text"
									placeholder="Название компании"
									class="grow border-none outline-none bg-transparent"
									bind:value={searchCompanyName}
								/>
							{:else}
								<input
									type="text"
									placeholder="ФИО"
									class="grow border-none outline-none bg-transparent"
									bind:value={searchIndividualName}
								/>
							{/if}
							{#if (activeTab === 'companies' && searchCompanyName) || (activeTab === 'individuals' && searchIndividualName)}
								<button
									type="button"
									class="btn btn-ghost btn-sm btn-circle h-6 w-6 min-h-0 p-0 flex-shrink-0"
									onclick={clearSearch}
									title="Очистить"
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="h-4 w-4"
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
							{/if}
						</label>
					</div>
					
					<!-- Даты и кнопка поиска -->
					<div class="flex gap-4">
						<label class="input input-bordered flex items-center gap-2 pr-2">
							<input type="date" class="grow border-none outline-none bg-transparent" bind:value={startDate} placeholder="Дата начала" />
							{#if startDate}
								<button
									type="button"
									class="btn btn-ghost btn-sm btn-circle h-6 w-6 min-h-0 p-0 flex-shrink-0"
									onclick={() => startDate = ''}
									title="Очистить"
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="h-4 w-4"
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
							{/if}
						</label>
						<label class="input input-bordered flex items-center gap-2 pr-2">
							<input type="date" class="grow border-none outline-none bg-transparent" bind:value={endDate} placeholder="Дата окончания" />
							{#if endDate}
								<button
									type="button"
									class="btn btn-ghost btn-sm btn-circle h-6 w-6 min-h-0 p-0 flex-shrink-0"
									onclick={() => endDate = ''}
									title="Очистить"
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="h-4 w-4"
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
							{/if}
						</label>
						<button class="btn btn-primary" onclick={loadStatistics} disabled={isLoading}>
							{isLoading ? 'Загрузка...' : 'Поиск'}
						</button>
					</div>
				</div>
			</div>
		</div>

		{#if isLoading}
			<div class="flex justify-center">
				<span class="loading loading-spinner loading-lg"></span>
			</div>
		{:else if activeTab === 'companies' && companyStats}
			<div class="space-y-6">
				<div class="stats bg-base-100 shadow w-full smooth-appear">
					<div class="stat">
						<div class="stat-title">Всего оценок</div>
						<div class="stat-value">{companyStats.total}</div>
					</div>
				</div>

				<!-- График истории компании -->
				{#if companyHistory && selectedCompany}
					<div class="card bg-base-100 shadow-xl smooth-appear">
						<div class="card-body p-5">
							<div class="flex justify-between items-center mb-4">
								<h2 class="card-title">История: {selectedCompany}</h2>
								<button
									class="btn btn-sm btn-circle btn-ghost"
									onclick={closeCompanyChart}
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
								<canvas id="companyChart" bind:this={companyChartCanvas}></canvas>
							</div>
						</div>
					</div>
				{/if}

				<div class="card bg-base-100 shadow-xl smooth-appear">
					<div class="card-body p-5">
						<h2 class="card-title mb-4 text-base-content">Список компаний</h2>
						<div class="overflow-x-auto">
							<table class="table table-zebra">
								<thead>
									<tr>
										<th>
											<button
												class="btn btn-ghost btn-sm"
												onclick={() => sortCompanies('company_name')}
											>
												Название {getSortIcon('company_name', companySortField, companySortDirection)}
											</button>
										</th>
										<th>
											<button
												class="btn btn-ghost btn-sm"
												onclick={() => sortCompanies('assessment_date')}
											>
												Дата {getSortIcon('assessment_date', companySortField, companySortDirection)}
											</button>
										</th>
										<th>
											<button
												class="btn btn-ghost btn-sm"
												onclick={() => sortCompanies('altman_z_score')}
											>
												Z-score (Альтман) {getSortIcon('altman_z_score', companySortField, companySortDirection)}
											</button>
										</th>
										<th>
											<button
												class="btn btn-ghost btn-sm"
												onclick={() => sortCompanies('taffler_z_score')}
											>
												T-score (Таффлер) {getSortIcon('taffler_z_score', companySortField, companySortDirection)}
											</button>
										</th>
										<th>
											<button
												class="btn btn-ghost btn-sm"
												onclick={() => sortCompanies('combined_risk_level')}
											>
												Риск {getSortIcon('combined_risk_level', companySortField, companySortDirection)}
											</button>
										</th>
										<th>Действия</th>
									</tr>
								</thead>
								<tbody>
									{#each companyStats.assessments as assessment}
										<tr>
											<td>{assessment.company_name}</td>
											<td>{new Date(assessment.assessment_date).toLocaleDateString('ru-RU')}</td>
											<td>{assessment.altman_z_score.toFixed(4)}</td>
											<td>{assessment.taffler_z_score.toFixed(4)}</td>
											<td>
												<span class="badge {getRiskColor(assessment.combined_risk_level)}">
													{getRiskLabel(assessment.combined_risk_level)}
												</span>
											</td>
											<td>
												<div class="flex gap-2">
													<button
														class="btn btn-sm btn-primary"
														onclick={() => loadCompanyHistory(assessment.company_name)}
													>
														История
													</button>
													<button
														class="btn btn-sm btn-error"
														onclick={() => deleteCompany(assessment.id)}
														disabled={isLoading}
														title="Удалить запись"
													>
														<svg
															xmlns="http://www.w3.org/2000/svg"
															class="h-4 w-4"
															fill="none"
															viewBox="0 0 24 24"
															stroke="currentColor"
														>
															<path
																stroke-linecap="round"
																stroke-linejoin="round"
																stroke-width="2"
																d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
															/>
														</svg>
													</button>
												</div>
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		{:else if activeTab === 'individuals' && individualStats}
			<div class="space-y-6">
				<div class="stats bg-base-100 shadow w-full smooth-appear">
					<div class="stat">
						<div class="stat-title">Всего оценок</div>
						<div class="stat-value">{individualStats.total}</div>
					</div>
				</div>

				<!-- График истории физического лица -->
				{#if individualHistory && selectedIndividual}
					<div class="card bg-base-100 shadow-xl smooth-appear">
						<div class="card-body p-5">
							<div class="flex justify-between items-center mb-4">
								<h2 class="card-title">История: {selectedIndividual}</h2>
								<button
									class="btn btn-sm btn-circle btn-ghost"
									onclick={closeIndividualChart}
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
								<canvas id="individualChart" bind:this={individualChartCanvas}></canvas>
							</div>
						</div>
					</div>
				{/if}

				<div class="card bg-base-100 shadow-xl smooth-appear">
					<div class="card-body p-5">
						<h2 class="card-title mb-4 text-base-content">Список физических лиц</h2>
						<div class="overflow-x-auto">
							<table class="table table-zebra">
								<thead>
									<tr>
										<th>
											<button
												class="btn btn-ghost btn-sm"
												onclick={() => sortIndividuals('full_name')}
											>
												ФИО {getSortIcon('full_name', individualSortField, individualSortDirection)}
											</button>
										</th>
										<th>
											<button
												class="btn btn-ghost btn-sm"
												onclick={() => sortIndividuals('assessment_date')}
											>
												Дата {getSortIcon('assessment_date', individualSortField, individualSortDirection)}
											</button>
										</th>
										<th>
											<button
												class="btn btn-ghost btn-sm"
												onclick={() => sortIndividuals('credit_score')}
											>
												Скоринг {getSortIcon('credit_score', individualSortField, individualSortDirection)}
											</button>
										</th>
										<th>
											<button
												class="btn btn-ghost btn-sm"
												onclick={() => sortIndividuals('risk_level')}
											>
												Риск {getSortIcon('risk_level', individualSortField, individualSortDirection)}
											</button>
										</th>
										<th>
											<button
												class="btn btn-ghost btn-sm"
												onclick={() => sortIndividuals('credit_amount')}
											>
												Сумма кредита {getSortIcon('credit_amount', individualSortField, individualSortDirection)}
											</button>
										</th>
										<th>Действия</th>
									</tr>
								</thead>
								<tbody>
									{#each individualStats.assessments as assessment}
										<tr>
											<td>{assessment.full_name}</td>
											<td>{new Date(assessment.assessment_date).toLocaleDateString('ru-RU')}</td>
											<td>{assessment.credit_score.toFixed(0)}</td>
											<td>
												<span class="badge {getRiskColor(assessment.risk_level)}">
													{getRiskLabel(assessment.risk_level)}
												</span>
											</td>
											<td>{assessment.credit_amount.toLocaleString('ru-RU')}</td>
											<td>
												<div class="flex gap-2">
													<button
														class="btn btn-sm btn-primary"
														onclick={() => loadIndividualHistory(assessment.full_name)}
													>
														История
													</button>
													<button
														class="btn btn-sm btn-error"
														onclick={() => deleteIndividual(assessment.id)}
														disabled={isLoading}
														title="Удалить запись"
													>
														<svg
															xmlns="http://www.w3.org/2000/svg"
															class="h-4 w-4"
															fill="none"
															viewBox="0 0 24 24"
															stroke="currentColor"
														>
															<path
																stroke-linecap="round"
																stroke-linejoin="round"
																stroke-width="2"
																d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
															/>
														</svg>
													</button>
												</div>
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>

