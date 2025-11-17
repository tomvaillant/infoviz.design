<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { authStore } from '$lib/stores/auth';
	import { onMount } from 'svelte';

	type AuthView = 'sign-in' | 'sign-up';

	let activeView: AuthView = 'sign-in';
	let clerkContainer: HTMLDivElement | null = null;
	let cleanupClerk: (() => void) | null = null;
	let isMounting = false;
	let hasAppliedQueryView = false;

	onMount(() => {
		const unsubscribe = authStore.subscribe(async (state) => {
			if (state.authenticated) {
				await goto('/');
			}
		});

		void mountClerk();

		return () => {
			unsubscribe();
			cleanupClerk?.();
		};
	});

	$: if (!hasAppliedQueryView) {
		const requestedView = $page.url.searchParams.get('view') === 'sign-up' ? 'sign-up' : 'sign-in';
		activeView = requestedView;
		hasAppliedQueryView = true;
		void mountClerk();
	}

	async function mountClerk() {
		if (!clerkContainer || isMounting) return;
		isMounting = true;

		try {
			cleanupClerk?.();
			const appearance = {
				elements: {
					rootBox: 'w-full',
					card: 'bg-white shadow-2xl rounded-3xl border border-white/70',
					formButtonPrimary: 'clerk-button-submit bg-gradient-to-r from-green01 to-[#87d0aa] border-none text-black01 hover:opacity-90'
				}
			};

			if (activeView === 'sign-in') {
				cleanupClerk = await authStore.mountSignIn(clerkContainer, {
					signUpUrl: '/login?view=sign-up',
					redirectUrl: '/',
					afterSignInUrl: '/',
					appearance
				});
			} else {
				cleanupClerk = await authStore.mountSignUp(clerkContainer, {
					signInUrl: '/login',
					redirectUrl: '/',
					afterSignUpUrl: '/',
					appearance
				});
			}
		} catch (error) {
			console.error('Failed to mount Clerk component', error);
		} finally {
			isMounting = false;
		}
	}
</script>

<div class="min-h-screen bg-black01 text-green01 relative overflow-hidden">

	<div class="flex items-center relative max-w-6xl min-h-[100vh] mx-auto px-4 sm:px-6 lg:px-10 py-12 lg:py-20 flex flex-col-reverse lg:flex-row gap-12 items-start">
		<!-- Auth panel -->
		<div class="w-full lg:w-[420px]">
			<div class="w-full" bind:this={clerkContainer}>
				{#if isMounting}
					<div class="flex items-center justify-center text-gray-500 py-10 rounded-3xl border border-slate-200 bg-white/80 shadow-lg">
						Loading…
					</div>
				{/if}
			</div>
		</div>

		<!-- Story / marketing panel -->
		<div class="flex-1 text-green01 space-y-6 max-w-2xl">
			<div class="inline-flex items-center border border-green01 rounded-full px-4 py-1 text-sm font-semibold tracking-[0.2em] text-green01">
				PRIVATE BETA
			</div>

			<h1 class="text-7xl tracking-negative text-white">
			  Infoviz<span class="gradient-text">.design</span>
			</h1>

			<p class="font-light text-xl text-grey03">
				Focus on the reporting, let your assistant monitor the
				<span class="relative inline-block px-1">
					<span>noise</span>
					<span class="absolute inset-x-0 top-1/2 h-[2px] bg-slate-500/70 -translate-y-1/2"></span>
				</span>
				and identify
				<span class="relative inline-block px-1">
					<span>patterns</span>
					<span class="absolute inset-x-0 bottom-0 h-[2px] bg-slate-500/70"></span>
				</span>.
			</p>

			<div class="space-y-5">
				<h2 class="text-2xl font-semibold leading-snug">
					The journalist's AI assistant for data collection, monitoring, investigation and verification.
				</h2>
				<p class="font-light text-xl text-grey03">
					coJournalist consolidates technical investigative tools into an accessible interface, helping small newsrooms and independent journalists expand local coverage. Through natural language commands, reporters gain capabilities typically reserved for well-funded organizations.
				</p>
				<p class="font-light text-xl text-grey03">
					The platform enables journalists to scrape public data from social media profiles and government websites, query local databases, use OSINT tools and verify claims—all through conversational requests.
				</p>
			</div>
		</div>
	</div>
</div>
