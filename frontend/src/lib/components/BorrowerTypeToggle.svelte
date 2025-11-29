<script lang="ts">
	export let activeTab: 'companies' | 'individuals';
	export let onTabChange: (tab: 'companies' | 'individuals') => Promise<void>;
</script>

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
						onclick={() => onTabChange('companies')}
					>
						Юридические лица
					</button>
					<button
						class="join-item btn {activeTab === 'individuals'
							? 'btn-primary'
							: 'btn-outline btn-ghost'}"
						onclick={() => onTabChange('individuals')}
					>
						Физические лица
					</button>
				</div>
			</label>
		</div>
	</div>
</div>

