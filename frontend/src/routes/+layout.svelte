<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import { theme } from '$lib/stores';
	import { onMount } from 'svelte';

	let { children } = $props();

	onMount(() => {
		// Устанавливаем тему при загрузке
		const stored = localStorage.getItem('theme') as 'light' | 'dark' | null;
		if (stored) {
			theme.set(stored);
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<meta
		name="description"
		content="Система оценки кредитных рисков с использованием машинного обучения"
	/>
</svelte:head>

<div class="min-h-screen bg-base-200" data-theme={$theme}>
	<div class="navbar bg-base-100 shadow-lg">
		<div class="flex-1">
			<a class="btn btn-ghost text-xl" href="/">Кредитные риски</a>
		</div>
		<div class="flex-none">
			<button
				class="btn btn-ghost btn-circle"
				on:click={() => theme.toggle()}
				aria-label="Переключить тему"
			>
				{#if $theme === 'light'}
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
						/>
					</svg>
				{:else}
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
						/>
					</svg>
				{/if}
			</button>
		</div>
	</div>

	<main>
		{@render children()}
	</main>

	<footer class="footer footer-center p-4 bg-base-100 text-base-content mt-8">
		<div>
			<p>Система оценки кредитных рисков © 2024</p>
		</div>
	</footer>
</div>
