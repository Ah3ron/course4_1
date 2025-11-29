<script lang="ts">
	import type { ModelInfo } from '$lib/api';

	export let modelInfo: ModelInfo;

	// Функция для перевода названий полей на русский
	function translateField(field: string): string {
		const translations: Record<string, string> = {
			// Поля модели Альтмана
			'current_assets': 'Оборотные активы',
			'current_liabilities': 'Краткосрочные обязательства',
			'debt_capital': 'Заемный капитал',
			'liabilities': 'Обязательства',
			// Поля модели Таффлера
			'sales_profit': 'Прибыль от продаж',
			'short_term_liabilities': 'Краткосрочные обязательства',
			'long_term_liabilities': 'Долгосрочные обязательства',
			'total_assets': 'Всего активов',
			'sales': 'Выручка'
		};
		return translations[field] || field;
	}
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
				<input type="checkbox" />

				<div class="collapse-title text-sm font-semibold flex items-center gap-2">
					<span class="badge badge-primary badge-xs">Компании</span>
					<span>Модель Альтмана (Z-score)</span>
				</div>
				<div class="collapse-content">
					<div class="space-y-3 pt-2">
						<p class="text-xs text-base-content/70 leading-relaxed">{modelInfo.altman_description}</p>
						
						<div class="divider my-2"></div>
						
						<div class="bg-base-300/50 p-3 rounded-lg">
							<p class="text-xs font-semibold text-base-content mb-2">Формула:</p>
							<p class="text-xs text-base-content/80 font-mono">
								Z = -0.3877 - 1.0736 × К<sub>т.л.</sub> + 0.0579 × (ЗК / П)
							</p>
							<p class="text-xs text-base-content/60 mt-2">
								где К<sub>т.л.</sub> — коэффициент текущей ликвидности,<br>
								ЗК — заемный капитал, П — пассивы
							</p>
						</div>
						
						<div class="bg-base-300/50 p-3 rounded-lg">
							<p class="text-xs font-semibold text-base-content mb-2">Интерпретация:</p>
							<div class="space-y-1.5">
								<div class="flex items-center gap-2">
									<span class="badge badge-success badge-xs">Низкий</span>
									<span class="text-xs text-base-content/70">Z &lt; -0.5 — хорошее финансовое положение</span>
								</div>
								<div class="flex items-center gap-2">
									<span class="badge badge-warning badge-xs">Средний</span>
									<span class="text-xs text-base-content/70">-0.5 ≤ Z &lt; 0.0 — требует внимания</span>
								</div>
								<div class="flex items-center gap-2">
									<span class="badge badge-error badge-xs">Высокий</span>
									<span class="text-xs text-base-content/70">Z ≥ 0.0 — критичная ситуация</span>
								</div>
							</div>
						</div>
						
						<div class="bg-base-300/50 p-3 rounded-lg">
							<p class="text-xs font-semibold text-base-content mb-2">Требуемые поля:</p>
							<div class="flex flex-wrap gap-1.5">
								{#each modelInfo.required_fields.altman as field}
									<span class="badge badge-outline badge-xs">{translateField(field)}</span>
								{/each}
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<!-- Модель Таффлера -->
			<div class="collapse collapse-plus bg-base-200 smooth-appear">
				<input type="checkbox" />

				<div class="collapse-title text-sm font-semibold flex items-center gap-2">
					<span class="badge badge-primary badge-xs">Компании</span>
					<span>Модель Таффлера (T-score)</span>
				</div>
				<div class="collapse-content">
					<div class="space-y-3 pt-2">
						<p class="text-xs text-base-content/70 leading-relaxed">{modelInfo.taffler_description}</p>
						
						<div class="divider my-2"></div>
						
						<div class="bg-base-300/50 p-3 rounded-lg">
							<p class="text-xs font-semibold text-base-content mb-2">Формула:</p>
							<p class="text-xs text-base-content/80 font-mono">
								T = 0.53 × X<sub>1</sub> + 0.13 × X<sub>2</sub> + 0.18 × X<sub>3</sub> + 0.16 × X<sub>4</sub>
							</p>
							<p class="text-xs text-base-content/60 mt-2">
								где X<sub>1</sub> — прибыль от продаж / краткосрочные обязательства,<br>
								X<sub>2</sub> — оборотные активы / обязательства,<br>
								X<sub>3</sub> — долгосрочные обязательства / активы,<br>
								X<sub>4</sub> — выручка / активы
							</p>
						</div>
						
						<div class="bg-base-300/50 p-3 rounded-lg">
							<p class="text-xs font-semibold text-base-content mb-2">Интерпретация:</p>
							<div class="space-y-1.5">
								<div class="flex items-center gap-2">
									<span class="badge badge-success badge-xs">Низкий</span>
									<span class="text-xs text-base-content/70">T &gt; 0.3 — низкий риск дефолта</span>
								</div>
								<div class="flex items-center gap-2">
									<span class="badge badge-warning badge-xs">Средний</span>
									<span class="text-xs text-base-content/70">0.2 &lt; T ≤ 0.3 — средний риск</span>
								</div>
								<div class="flex items-center gap-2">
									<span class="badge badge-error badge-xs">Высокий</span>
									<span class="text-xs text-base-content/70">T ≤ 0.2 — значительный риск потери платежеспособности</span>
								</div>
							</div>
						</div>
						
						<div class="bg-base-300/50 p-3 rounded-lg">
							<p class="text-xs font-semibold text-base-content mb-2">Требуемые поля:</p>
							<div class="flex flex-wrap gap-1.5">
								{#each modelInfo.required_fields.taffler as field}
									<span class="badge badge-outline badge-xs">{translateField(field)}</span>
								{/each}
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<!-- Модель для физических лиц -->
			<div class="collapse collapse-plus bg-base-200 smooth-appear">
				<input type="checkbox" />

				<div class="collapse-title text-sm font-semibold flex items-center gap-2">
					<span class="badge badge-secondary badge-xs">Физ. лица</span>
					<span>Скоринговая модель</span>
				</div>
				<div class="collapse-content">
					<div class="space-y-3 pt-2">
						<p class="text-xs text-base-content/70 leading-relaxed">{modelInfo.individual_description}</p>
						
						<div class="divider my-2"></div>
						
						<div class="bg-base-300/50 p-3 rounded-lg">
							<p class="text-xs font-semibold text-base-content mb-2">Интерпретация:</p>
							<div class="space-y-1.5">
								<div class="flex items-center gap-2">
									<span class="badge badge-success badge-xs">Низкий</span>
									<span class="text-xs text-base-content/70">Балл &gt; 700 — низкий кредитный риск</span>
								</div>
								<div class="flex items-center gap-2">
									<span class="badge badge-warning badge-xs">Средний</span>
									<span class="text-xs text-base-content/70">500 &lt; Балл ≤ 700 — средний риск</span>
								</div>
								<div class="flex items-center gap-2">
									<span class="badge badge-error badge-xs">Высокий</span>
									<span class="text-xs text-base-content/70">Балл ≤ 500 — высокий кредитный риск</span>
								</div>
							</div>
						</div>
						
						<div class="bg-base-300/50 p-3 rounded-lg">
							<p class="text-xs font-semibold text-base-content mb-2">Учитываемые факторы:</p>
							<div class="grid grid-cols-2 gap-1.5">
								<span class="badge badge-outline badge-xs">Доходы/Расходы</span>
								<span class="badge badge-outline badge-xs">Кредитная история</span>
								<span class="badge badge-outline badge-xs">Наличие залога</span>
								<span class="badge badge-outline badge-xs">Трудовой стаж</span>
								<span class="badge badge-outline badge-xs">Возраст</span>
								<span class="badge badge-outline badge-xs">Долговая нагрузка</span>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
