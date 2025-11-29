<script lang="ts">
	import type { CompanyStatistics } from '$lib/api';

	export let stats: CompanyStatistics;
	export let isLoading: boolean;
	export let sortField: 'company_name' | 'assessment_date' | 'altman_z_score' | 'taffler_z_score' | 'combined_risk_level' | null;
	export let sortDirection: 'asc' | 'desc';
	export let onSort: (field: 'company_name' | 'assessment_date' | 'altman_z_score' | 'taffler_z_score' | 'combined_risk_level') => void;
	export let onViewHistory: (companyName: string) => void;
	export let onDelete: (id: number) => void;

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

	function getSortIcon(field: string): string {
		if (field !== sortField) return '';
		return sortDirection === 'asc' ? '↑' : '↓';
	}
</script>

<div class="card bg-base-100 shadow-xl smooth-appear">
	<div class="card-body p-5">
		<h2 class="card-title mb-4 text-base-content">Список компаний</h2>
		<div class="overflow-x-auto">
			<table class="table table-zebra">
				<thead>
					<tr>
						<th>
							<button class="btn btn-ghost btn-sm" onclick={() => onSort('company_name')}>
								Название {getSortIcon('company_name')}
							</button>
						</th>
						<th>
							<button class="btn btn-ghost btn-sm" onclick={() => onSort('assessment_date')}>
								Дата {getSortIcon('assessment_date')}
							</button>
						</th>
						<th>
							<button class="btn btn-ghost btn-sm" onclick={() => onSort('altman_z_score')}>
								Z-score (Альтман) {getSortIcon('altman_z_score')}
							</button>
						</th>
						<th>
							<button class="btn btn-ghost btn-sm" onclick={() => onSort('taffler_z_score')}>
								T-score (Таффлер) {getSortIcon('taffler_z_score')}
							</button>
						</th>
						<th>
							<button class="btn btn-ghost btn-sm" onclick={() => onSort('combined_risk_level')}>
								Риск {getSortIcon('combined_risk_level')}
							</button>
						</th>
						<th>Действия</th>
					</tr>
				</thead>
				<tbody>
					{#each stats.assessments as assessment}
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
										onclick={() => onViewHistory(assessment.company_name)}
									>
										История
									</button>
									<button
										class="btn btn-sm btn-error"
										onclick={() => onDelete(assessment.id)}
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

