<script lang="ts">
	export let label: string;
	export let value: number | string;
	export let error: string | undefined = undefined;
	export let required: boolean = false;
	export let placeholder: string = 'Введите значение';
	export let step: number = 1000;
	export let hint: string = '';
	export let span: number = 1;
	export let type: 'number' | 'text' | 'date' = 'number';

	const spanClass = span === 2 ? 'md:col-span-2' : '';
	const inputType = type;
</script>

<label class="form-control w-full {spanClass}">
	<div class="label">
		<span class="label-text font-medium">{label}</span>
		{#if required}
			<span class="label-text-alt text-error">*</span>
		{/if}
	</div>
	<input
		type={inputType}
		class="input input-bordered w-full {error
			? 'input-error animate-shake-input'
			: 'focus:input-primary'}"
		bind:value
		{placeholder}
		{required}
		{...(type === 'number' ? { step } : {})}
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
