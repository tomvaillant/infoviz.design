<script lang="ts">
	import { X } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	function close() {
		dispatch('close');
	}

	function handleBackdropClick(e: MouseEvent) {
		if (e.target === e.currentTarget) {
			close();
		}
	}
</script>

<!-- Modal backdrop -->
<div
	class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
	on:click={handleBackdropClick}
	on:keydown={(e) => e.key === 'Escape' && close()}
	role="button"
	tabindex="0"
>
	<!-- Modal content -->
	<div class="bg-black01 rounded-2xl shadow-xl max-w-2xl w-full max-h-[80vh] overflow-auto">
		<!-- Header -->
		<div
			class="flex items-center justify-between p-6 sticky top-0 bg-black01 border-b border-black03"
		>
			<h2 class="text-2xl font-bold text-white">
				Infoviz<span class="gradient-text">.design</span>
			</h2>
			<button
				on:click={close}
				class="text-grey03 hover:text-green01 transition-colors"
				aria-label="Close modal"
			>
				<X class="w-6 h-6" />
			</button>
		</div>

		<!-- Content -->
		<div class="p-6 space-y-8">
			<section class="space-y-3">
				<p class="text-md font-semibold tracking-[0.2em] text-white uppercase">Introduction</p>
				<p class="text-grey03 leading-relaxed">
					I’m building coJournalist to give smaller newsrooms and independent reporters access to the same investigative tooling as well-funded organizations.
					The assistant handles scraping, monitoring, data access, and fact verification through natural language so you can focus on the reporting.
				</p>
			</section>

			<section class="space-y-3">
				<p class="text-md font-semibold tracking-[0.2em] text-white uppercase">Methodology & Privacy</p>
				<ul class="space-y-2 text-grey03 leading-relaxed list-disc ml-5">
					<li>I only store the scraper configurations you create (URLs, criteria, schedule). The scraped outputs are streamed back to you and never retained on the server.</li>
					<li>Firecrawl powers website scraping, Apify handles social media monitoring, and Factiverse assists with claim verification. Hugging Face models are used for language tasks.</li>
					<li>Each request is scoped to the minimum data necessary. Credentials stay with Clerk; I do not store passwords or tokens.</li>
				</ul>
			</section>

			<section class="space-y-2">
				<p class="text-md font-semibold tracking-[0.2em] text-white uppercase">Support</p>
				<p class="text-grey03 leading-relaxed">
					Supported by GRS.
				</p>
			</section>

			<section class="space-y-2">
				<p class="text-md font-semibold tracking-[0.2em] text-white uppercase">Contact</p>
				<p class="text-grey03 leading-relaxed">
					I share progress notes on my
					<a
						href="https://buriedsignals.substack.com/"
						target="_blank"
						rel="noopener noreferrer"
						class="text-green01 hover:text-white font-medium"
					>
						newsletter
					</a>
					and publish data-driven investigations on
					<a
						href="https://www.youtube.com/@buriedsignals"
						target="_blank"
						rel="noopener noreferrer"
						class="text-green01 hover:text-white font-medium"
					>
						YouTube
					</a>.
				</p>
			</section>
		</div>

		<!-- Footer -->
		<div class="p-6 bg-black01 border-t border-black03">
			<button
				on:click={close}
				class="btn-primary w-full font-light text-base"
			>
				Close
			</button>
		</div>
	</div>
</div>

<style>
</style>
