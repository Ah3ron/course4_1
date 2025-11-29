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

	// Компоненты
	import BorrowerTypeToggle from '$lib/components/BorrowerTypeToggle.svelte';
	import StatisticsFilters from '$lib/components/StatisticsFilters.svelte';
	import StatisticsHeader from '$lib/components/StatisticsHeader.svelte';
	import HistoryChart from '$lib/components/HistoryChart.svelte';
	import CompanyTable from '$lib/components/CompanyTable.svelte';
	import IndividualTable from '$lib/components/IndividualTable.svelte';

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

	async function handleTabChange(tab: TabType) {
		activeTab = tab;
		await loadStatistics();
	}

	async function loadCompanyHistory(companyName: string) {
		isLoading = true;
		error = null;
		try {
			selectedCompany = companyName;
			companyHistory = await getCompanyHistory(companyName);
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
		} catch (e) {
			error = e instanceof Error ? e.message : 'Ошибка при загрузке истории';
		} finally {
			isLoading = false;
		}
	}

	function closeCompanyChart() {
		selectedCompany = null;
		companyHistory = null;
	}

	function closeIndividualChart() {
		selectedIndividual = null;
		individualHistory = null;
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

	async function deleteCompany(assessmentId: number) {
		if (!confirm('Вы уверены, что хотите удалить эту запись?')) {
			return;
		}
		
		isLoading = true;
		error = null;
		try {
			await deleteCompanyAssessment(assessmentId);
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

		<BorrowerTypeToggle {activeTab} onTabChange={handleTabChange} />

		{#if error}
			<div class="alert alert-error mb-4">
				<span>{error}</span>
			</div>
		{/if}

		<StatisticsFilters
			{activeTab}
			bind:searchCompanyName
			bind:searchIndividualName
			bind:startDate
			bind:endDate
			{isLoading}
			onSearch={loadStatistics}
			onClearSearch={clearSearch}
		/>

		{#if isLoading}
			<div class="flex justify-center">
				<span class="loading loading-spinner loading-lg"></span>
			</div>
		{:else if activeTab === 'companies' && companyStats}
			<div class="space-y-6">
				<StatisticsHeader total={companyStats.total} />

				{#if companyHistory && selectedCompany}
					<HistoryChart
						title={selectedCompany}
						history={companyHistory.history}
						onClose={closeCompanyChart}
					/>
				{/if}

				<CompanyTable
					stats={companyStats}
					{isLoading}
					sortField={companySortField}
					sortDirection={companySortDirection}
					onSort={sortCompanies}
					onViewHistory={loadCompanyHistory}
					onDelete={deleteCompany}
				/>
			</div>
		{:else if activeTab === 'individuals' && individualStats}
			<div class="space-y-6">
				<StatisticsHeader total={individualStats.total} />

				{#if individualHistory && selectedIndividual}
					<HistoryChart
						title={selectedIndividual}
						history={individualHistory.history}
						onClose={closeIndividualChart}
					/>
				{/if}

				<IndividualTable
					stats={individualStats}
					{isLoading}
					sortField={individualSortField}
					sortDirection={individualSortDirection}
					onSort={sortIndividuals}
					onViewHistory={loadIndividualHistory}
					onDelete={deleteIndividual}
				/>
			</div>
		{/if}
	</div>
</div>
