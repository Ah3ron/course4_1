<script lang="ts">
	export let riskLevel: 'low' | 'medium' | 'high';
	export let size: 'sm' | 'md' | 'lg' = 'md';

	function getRiskColor(riskLevel: string): string {
		switch (riskLevel) {
			case 'low':
				return 'success';
			case 'medium':
				return 'warning';
			case 'high':
				return 'error';
			default:
				return 'neutral';
		}
	}

	function getRiskLabel(riskLevel: string): string {
		switch (riskLevel) {
			case 'low':
				return 'Низкий риск';
			case 'medium':
				return 'Средний риск';
			case 'high':
				return 'Высокий риск';
			default:
				return 'Неизвестно';
		}
	}

	const sizeClasses = {
		sm: 'badge-sm',
		md: 'badge-md',
		lg: 'badge-lg'
	};
</script>

<div
	class="badge {sizeClasses[size]} animate-fade-in {getRiskColor(riskLevel) === 'success' ? 'badge-success' : getRiskColor(riskLevel) === 'warning' ? 'badge-warning' : getRiskColor(riskLevel) === 'error' ? 'badge-error' : 'badge-neutral'}"
	role="status"
	aria-label="Уровень риска: {getRiskLabel(riskLevel)}"
>
	{getRiskLabel(riskLevel)}
</div>

