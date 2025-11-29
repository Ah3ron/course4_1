<script lang="ts">
	export let activeTab: 'companies' | 'individuals';
	export let searchCompanyName: string;
	export let searchIndividualName: string;
	export let startDate: string;
	export let endDate: string;
	export let isLoading: boolean;
	export let onSearch: () => Promise<void>;
	export let onClearSearch: () => void;
</script>

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
							onclick={onClearSearch}
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
				<input type="date" class="input input-bordered" bind:value={startDate} placeholder="Дата начала" />
				<input type="date" class="input input-bordered" bind:value={endDate} placeholder="Дата окончания" />
				<button class="btn btn-primary" onclick={onSearch} disabled={isLoading}>
					{isLoading ? 'Загрузка...' : 'Поиск'}
				</button>
			</div>
		</div>
	</div>
</div>

