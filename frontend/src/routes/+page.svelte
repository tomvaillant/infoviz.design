<script lang="ts">
import GraphicsView from '$lib/components/graphics/GraphicsView.svelte';
import AboutModal from '$lib/components/modals/AboutModal.svelte';

	let showAboutModal = false;

	function openAboutModal() {
		showAboutModal = true;
	}

	function closeAboutModal() {
		showAboutModal = false;
	}
</script>

<div class="min-h-screen flex flex-col bg-black01 pb-20">
	<!-- Main content area -->
	<div class="flex-1">
		<GraphicsView />
	</div>

	<!-- Footer - Fixed at bottom -->
	<footer class="fixed bottom-0 left-0 right-0 bg-black02/90 backdrop-blur-md px-12 py-5 border-t border-black03/50 animate-fade-in delay-100 z-40">
		<div class="flex items-center justify-between gap-4">
			<div class="logo-text text-sm">
				Infoviz<span class="gradient-text">.design</span>
			</div>
      <div class="flex items-center gap-6">
				<button
					on:click={openAboutModal}
					class="font-sans font-medium text-sm text-grey03 hover:text-green01 transition-colors duration-300"
				>
					About
				</button>
        <a href="https://huggingface.co/tomvaillant" target="_blank" rel="noopener noreferrer" class="opacity-60 hover:opacity-100 transition-opacity duration-300">
          <img src="/logos/huggingface.svg" alt="Hugging Face" class="h-5" />
        </a>
        <a href="https://www.youtube.com/@buriedsignals" target="_blank" rel="noopener noreferrer" aria-label="YouTube" class="opacity-60 hover:opacity-100 transition-opacity duration-300">
          <img src="/logos/youtube.svg" alt="YouTube" class="h-5" />
        </a>
        <a href="https://www.linkedin.com/in/tomvaillant/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" class="opacity-60 hover:opacity-100 transition-opacity duration-300">
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
		font-family: 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif';
	}

	.logo-text {
		font-family: 'Fraunces', 'ui-serif', 'Georgia', 'serif';
		font-weight: 600;
		font-size: 1.5rem;
		letter-spacing: -0.02em;
	}
</style>
