<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { theme } from '$lib/stores';
	import { onMount } from 'svelte';

	let { children } = $props();

	onMount(() => {
		// Устанавливаем тему при загрузке
		const stored = localStorage.getItem('theme');
		if (stored === 'lofi' || stored === 'business') {
			theme.set(stored);
		} else if (stored === 'light') {
			// Конвертируем старую светлую тему
			theme.set('lofi');
		} else if (stored === 'dark') {
			// Конвертируем старую темную тему
			theme.set('business');
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
	<div class="navbar bg-base-100 shadow-md border-b border-base-300">
		<div class="flex-1">
			<a class="btn btn-ghost text-xl font-semibold hover:bg-primary/10 transition-colors" href="/">Кредитные риски</a>
			<a class="btn btn-ghost hover:bg-primary/10 transition-colors" href="/statistics">Статистика</a>
		</div>
		<div class="flex-none">
			<button
				class="btn btn-ghost btn-circle hover:bg-primary/10 transition-all duration-200"
				onclick={() => theme.toggle()}
				aria-label="Переключить тему"
			>
				{#if $theme === 'lofi'}
					<!-- Иконка луны для переключения на темную тему -->
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
					<!-- Иконка солнца для переключения на светлую тему -->
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

	<footer class="footer footer-center p-6 bg-base-100 text-base-content/70 mt-12 border-t border-base-300">
		<div>
			<p class="text-sm">Система оценки кредитных рисков © 2024</p>
		</div>
	</footer>
</div>
