<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { theme } from '$lib/stores';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

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

	function isActive(path: string): boolean {
		return $page.url.pathname === path;
	}
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
	<div class="navbar bg-base-100 shadow-lg border-b border-base-300 sticky top-0 z-50 backdrop-blur-sm bg-base-100/95">
		<div class="navbar-start">
			<a
				class="btn btn-ghost text-xl font-bold text-base-content hover:text-primary transition-colors"
				href="/"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-6 w-6 mr-2 text-primary"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
					/>
				</svg>
				Кредитные риски
			</a>
		</div>
		<div class="navbar-center">
			<div class="flex gap-2">
				<a
					class="btn btn-ghost  {isActive('/') ? 'btn-active' : ''} transition-all duration-200"
					href="/"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5 mr-1"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
						/>
					</svg>
					Главная
				</a>
				<a
					class="btn btn-ghost  {isActive('/statistics') ? 'btn-active' : ''} transition-all duration-200"
					href="/statistics"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5 mr-1"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
						/>
					</svg>
					Статистика
				</a>
			</div>
		</div>
		<div class="navbar-end">
			<button
				class="btn btn-ghost btn-circle hover:bg-primary/20 transition-all duration-200"
				onclick={() => theme.toggle()}
				aria-label="Переключить тему"
				title={$theme === 'lofi' ? 'Переключить на темную тему' : 'Переключить на светлую тему'}
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
