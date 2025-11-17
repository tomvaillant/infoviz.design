<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';

	const FALLBACK_TIMEZONES = [
		'UTC',
		'America/New_York',
		'America/Chicago',
		'America/Denver',
		'America/Los_Angeles',
		'Europe/London',
		'Europe/Paris',
		'Europe/Berlin',
		'Asia/Kolkata',
		'Asia/Tokyo',
		'Asia/Singapore',
		'Australia/Sydney'
	];

	export let open = false;
	export let saving = false;
export let errorMessage: string | null = null;
export let initialTimezone: string | null = null;

	const dispatch = createEventDispatcher<{ save: { timezone: string } }>();

let timezoneOptions: string[] = FALLBACK_TIMEZONES;
let selectedTimezone: string = initialTimezone ?? '';

	onMount(() => {
		if (typeof Intl !== 'undefined' && typeof (Intl as any).supportedValuesOf === 'function') {
			timezoneOptions = (Intl as any).supportedValuesOf('timeZone');
		}

		if (!selectedTimezone) {
			try {
				selectedTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
			} catch {
				selectedTimezone = 'UTC';
			}
		}
	});

$: if (initialTimezone && !selectedTimezone) {
		selectedTimezone = initialTimezone;
}

	function handleSubmit(event: Event) {
		event.preventDefault();
		if (!selectedTimezone) return;
		dispatch('save', { timezone: selectedTimezone });
	}
</script>

{#if open}
	<div class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm flex items-center justify-center z-50 px-4">
		<form
			class="w-full max-w-md bg-white rounded-2xl shadow-2xl p-6 space-y-5"
			on:submit|preventDefault={handleSubmit}
		>
			<div>
				<h2 class="text-2xl font-semibold text-gray-900">Set Your Timezone</h2>
				<p class="text-gray-600 mt-1 text-sm">
					Choose the timezone you work in so coJournalist can schedule scrapes and reminders accurately.
				</p>
			</div>

			<label for="timezone-select" class="form-label">Timezone</label>
			<select id="timezone-select" class="form-select" bind:value={selectedTimezone} required>
				<option value="" disabled>Select your timezone</option>
				{#each timezoneOptions as tz}
					<option value={tz}>{tz}</option>
				{/each}
			</select>

			{#if errorMessage}
				<p class="text-sm text-red-600">{errorMessage}</p>
			{/if}

			<button type="submit" class="btn-primary w-full" disabled={saving || !selectedTimezone}>
				{#if saving}
					Saving…
				{:else}
					Save Timezone
				{/if}
			</button>
		</form>
	</div>
{/if}
