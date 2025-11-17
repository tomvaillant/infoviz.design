<script lang="ts">
import { onMount } from 'svelte';
import { authStore } from '$lib/stores/auth';
import GraphicsView from '$lib/components/graphics/GraphicsView.svelte';
import AboutModal from '$lib/components/modals/AboutModal.svelte';
import { Bell } from 'lucide-svelte';

	let showAboutModal = false;
	let userButtonContainer: HTMLDivElement;

	onMount(() => {
		// Mount Clerk UserButton
		if (userButtonContainer) {
			authStore.mountUserButton(userButtonContainer);
		}
	});

	function openAboutModal() {
		showAboutModal = true;
	}

	function closeAboutModal() {
		showAboutModal = false;
	}
</script>

<div class="h-screen flex flex-col bg-gray-50">
	<!-- Combined top bar -->
	<div class="bg-black02 px-12 py-5 flex items-center justify-between gap-4">
		<!-- Left: Logo -->
		<div class="flex-shrink-0">
			Infoviz<span class="gradient-text">.design</span>
		</div>

		<!-- Right: Clerk User info + UserButton -->
		<div class="flex items-center gap-4">
			{#if $authStore.user}
				<div class="text-right">
					<div class="text-base text-white">
						{$authStore.user.credits} credits
					</div>
				</div>
			{/if}
			<div bind:this={userButtonContainer}></div>
		</div>
	</div>

	<!-- Main content area -->
	<div class="flex-1 overflow-hidden">
			<GraphicsView />
	</div>

	<!-- Footer -->
	<footer class="bg-black02 px-12 py-4">
		<div class="flex items-center justify-between gap-4 space-x-4 text-sm text-gray-600">
			<button
				on:click={openAboutModal}
				class="text-base text-white hover:text-green01 transition-colors"
			>
				About
			</button>
      <div class="flex gap-3">
        <a href="https://huggingface.co/tomvaillant" target="_blank" rel="noopener noreferrer">
          <img src="/logos/huggingface.svg" alt="Hugging Face" class="h-5" />
        </a>
        <a href="https://www.youtube.com/@buriedsignals" target="_blank" rel="noopener noreferrer" aria-label="YouTube">
          <img src="/logos/youtube.svg" alt="YouTube" class="h-5" />
        </a>
        <a href="https://www.linkedin.com/in/tomvaillant/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
          <img src="/logos/linkedin.svg" alt="LinkedIn" class="h-5" />
        </a>
      </div>
		</div>
	</footer>
</div>

<!-- About Modal -->
{#if showAboutModal}
	<AboutModal on:close={closeAboutModal} />
{/if}

<style>
	:global(body) {
		font-family: 'Space Grotesk', 'ui-sans-serif', 'system-ui', 'sans-serif';
	}
</style>
