<script lang="ts">
	export let label: string;
	export let value: number;
	export let error: string | undefined = undefined;
	export let required: boolean = false;
	export let placeholder: string = 'Введите сумму';
	export let step: number = 1000;
	export let hint: string = '';
	export let span: number = 1;

	const spanClass = span === 2 ? 'md:col-span-2' : '';
</script>

<label class="form-control w-full md:col-span-2">
	<div class="label">
		<span class="label-text font-medium">{label}</span>
		{#if required}
			<span class="label-text-alt text-error">*</span>
		{/if}
	</div>
	<input
		type="number"
		class="input input-bordered w-full transition-all duration-200 hover:scale-[1.02] {error ? 'input-error animate-shake-input' : 'focus:input-primary focus:scale-[1.02]'}"
		bind:value
		{step}
		{placeholder}
		{required}
	/>
	{#if error}
		<div class="label">
			<span class="label-text-alt text-error animate-shake">{error}</span>
		</div>
	{:else if hint}
		<div class="label">
			<span class="label-text-alt text-base-content/60">{hint}</span>
		</div>
	{/if}
</label>

