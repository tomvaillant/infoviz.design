<script lang="ts">
import GraphicsView from '$lib/components/graphics/GraphicsView.svelte';
import AboutModal from '$lib/components/modals/AboutModal.svelte';
import { MoreVertical } from 'lucide-svelte';

	let showAboutModal = false;
	let showMobileMenu = false;

	function openAboutModal() {
		showAboutModal = true;
		showMobileMenu = false;
	}

	function closeAboutModal() {
		showAboutModal = false;
	}

	function toggleMobileMenu() {
		showMobileMenu = !showMobileMenu;
	}

	function closeMobileMenu() {
		showMobileMenu = false;
	}
</script>

<div class="min-h-screen flex flex-col bg-black01 pb-20">
	<!-- Main content area -->
	<div class="flex-1">
		<GraphicsView />
	</div>

	<!-- Footer - Fixed at bottom -->
	<footer class="fixed bottom-0 left-0 right-0 bg-black02/70 backdrop-blur-md px-6 md:px-12 py-3 border-t border-black03/50 animate-fade-in delay-100 z-40">
		<div class="flex items-center justify-between gap-4">
			<div class="logo-text text-sm md:text-base">
				Infoviz<span class="gradient-text">.design</span>
			</div>

      <!-- Desktop links -->
      <div class="hidden md:flex items-center gap-6">
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

      <!-- Mobile menu button -->
      <button
        on:click={toggleMobileMenu}
        class="md:hidden p-2 rounded-lg text-grey03 hover:text-green01 hover:bg-black03/50 transition-all duration-300 active:scale-95"
        aria-label="Menu"
      >
        <MoreVertical class="w-5 h-5" />
      </button>
		</div>
	</footer>
</div>

<!-- Mobile Menu Modal -->
{#if showMobileMenu}
	<div
		class="fixed inset-0 z-50 animate-fade-in"
		on:click={closeMobileMenu}
		on:keydown={(e) => e.key === 'Escape' && closeMobileMenu()}
		role="button"
		tabindex="0"
		aria-label="Close mobile menu"
	>
		<!-- Backdrop -->
		<div class="absolute inset-0 bg-black01/80 backdrop-blur-sm"></div>

		<!-- Menu Panel -->
		<div
			class="absolute bottom-0 left-0 right-0 bg-black02 border-t border-green01/20 rounded-t-3xl animate-slide-up overflow-hidden"
			on:click|stopPropagation
			role="dialog"
			aria-modal="true"
			aria-label="Mobile navigation menu"
			tabindex="-1"
		>
			<!-- Handle bar -->
			<div class="flex justify-center pt-3 pb-2">
				<div class="w-12 h-1 bg-grey01/30 rounded-full"></div>
			</div>

			<div class="px-6 pb-8 pt-4">
				<!-- Menu items -->
				<nav class="space-y-1">
					<button
						on:click={openAboutModal}
						class="w-full text-left px-4 py-4 rounded-xl text-white font-sans font-medium text-base hover:bg-black03/50 transition-all duration-300 active:scale-[0.98] flex items-center gap-3"
					>
						<span class="text-green01 text-xl">ℹ️</span>
						About
					</button>

					<a
						href="https://huggingface.co/tomvaillant"
						target="_blank"
						rel="noopener noreferrer"
						class="w-full flex items-center gap-3 px-4 py-4 rounded-xl text-white font-sans font-medium text-base hover:bg-black03/50 transition-all duration-300 active:scale-[0.98]"
					>
						<img src="/logos/huggingface.svg" alt="" class="h-6 opacity-80" />
						Hugging Face
					</a>

					<a
						href="https://www.youtube.com/@buriedsignals"
						target="_blank"
						rel="noopener noreferrer"
						class="w-full flex items-center gap-3 px-4 py-4 rounded-xl text-white font-sans font-medium text-base hover:bg-black03/50 transition-all duration-300 active:scale-[0.98]"
					>
						<img src="/logos/youtube.svg" alt="" class="h-6 opacity-80" />
						YouTube
					</a>

					<a
						href="https://www.linkedin.com/in/tomvaillant/"
						target="_blank"
						rel="noopener noreferrer"
						class="w-full flex items-center gap-3 px-4 py-4 rounded-xl text-white font-sans font-medium text-base hover:bg-black03/50 transition-all duration-300 active:scale-[0.98]"
					>
						<img src="/logos/linkedin.svg" alt="" class="h-6 opacity-80" />
						LinkedIn
					</a>
				</nav>
			</div>
		</div>
	</div>
{/if}

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
