<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { authStore } from '$lib/stores/auth';
	import TimezoneModal from '$lib/components/modals/TimezoneModal.svelte';
	import '../app.css';

let timezoneModalOpen = false;
let timezoneSaving = false;
let timezoneError: string | null = null;
let isInitializing = false;
let needsInitialization = false;

	// Initialize auth on mount
	onMount(() => {
		let unsubscribe: (() => void) | null = null;
		let cancelled = false;

		(async () => {
			await authStore.init();
			if (cancelled) return;

			unsubscribe = authStore.subscribe(async (state) => {
				if (!state.authenticated && $page.url.pathname !== '/login') {
					// Redirect to login if not authenticated
					await goto('/login');
					return;
				}

				needsInitialization = Boolean(state.user?.needs_initialization);
				const shouldPromptTimezone =
					state.authenticated &&
					state.user &&
					(needsInitialization || !state.user.timezone);

				if (shouldPromptTimezone) {
					timezoneModalOpen = true;
				} else if (!timezoneSaving && !isInitializing) {
					timezoneModalOpen = false;
					timezoneError = null;
				}
			});
		})();

		return () => {
			cancelled = true;
			unsubscribe?.();
		};
	});

async function handleTimezoneSave(event: CustomEvent<{ timezone: string }>) {
	const { timezone } = event.detail;
	console.log('[Layout] Saving timezone:', timezone);
	timezoneSaving = true;
	timezoneError = null;
	const requiresInitialization = needsInitialization;

	try {
		if (requiresInitialization) {
			isInitializing = true;
			await authStore.initializeUser(timezone);
		} else {
			await authStore.updateTimezone(timezone);
		}

		// Verify timezone was saved correctly
		const currentUser = $authStore.user;
		console.log('[Layout] After save, user timezone:', currentUser?.timezone);

		if (currentUser?.timezone === timezone) {
			console.log('[Layout] Timezone verified, closing modal');
			timezoneModalOpen = false;
		} else {
			console.warn('[Layout] Timezone mismatch after save. Expected:', timezone, 'Got:', currentUser?.timezone);
			timezoneError = 'Timezone was saved but could not be verified. Please refresh the page.';
		}
	} catch (error) {
		console.error('[Layout] Error saving timezone:', error);
		if (error instanceof Error) {
			timezoneError = error.message;
		} else {
			timezoneError = 'Unable to save timezone. Please try again.';
		}
	} finally {
		timezoneSaving = false;
		if (requiresInitialization) {
			isInitializing = false;
		}
	}
}
</script>

<slot />

<TimezoneModal
	open={timezoneModalOpen}
	saving={timezoneSaving}
	errorMessage={timezoneError}
	initialTimezone={$authStore.user?.timezone ?? null}
	on:save={handleTimezoneSave}
/>
