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
	class="fixed inset-0 bg-black01/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fade-in"
	on:click={handleBackdropClick}
	on:keydown={(e) => e.key === 'Escape' && close()}
	role="button"
	tabindex="0"
>
	<!-- Modal content -->
	<div class="bg-black02 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[80vh] overflow-auto border border-black03 animate-scale-in">
		<!-- Header -->
		<div
			class="flex items-center justify-between p-8 sticky top-0 bg-black02 border-b border-black03/50 backdrop-blur-sm"
		>
			<h2 class="font-display text-3xl font-semibold text-white tracking-tight">
				Infoviz<span class="gradient-text">.design</span>
			</h2>
			<button
				on:click={close}
				class="text-grey01 hover:text-green01 transition-all duration-300 hover:rotate-90"
				aria-label="Close modal"
			>
				<X class="w-6 h-6" />
			</button>
		</div>

		<!-- Content -->
		<div class="p-8 space-y-10">
			<section class="space-y-4">
				<h3 class="font-sans text-xs font-semibold tracking-widest text-green01 uppercase">Introduction</h3>
				<p class="font-sans text-lg text-grey03 leading-relaxed">
					Infoviz.design gives journalists easy access to visual inspiration and graphics. Browse curated examples to spark ideas and elevate your storytelling.
				</p>
			</section>

			<section class="space-y-4">
				<h3 class="font-sans text-xs font-semibold tracking-widest text-green01 uppercase">How it works</h3>
				<p class="font-sans text-base text-grey03 leading-relaxed">
					This application combines several technologies to search and retrieve visual journalism examples:
				</p>
				<ul class="font-sans text-base text-grey03 leading-relaxed space-y-2 list-disc list-inside pl-2">
					<li><span class="text-white font-medium">Vanna.AI</span> — Uses RAG (Retrieval-Augmented Generation) with ChromaDB vector store to semantically search a curated database of visual stories</li>
					<li><span class="text-white font-medium">Supabase</span> — PostgreSQL database storing metadata, sources, and publication information</li>
					<li><span class="text-white font-medium">HuggingFace Spaces</span> — Hosts the search model and provides inference API</li>
					<li><span class="text-white font-medium">FastAPI + SvelteKit</span> — Backend API and frontend interface</li>
					<li><span class="text-white font-medium">Gradio Client</span> — Connects to the HuggingFace Space for query processing</li>
				</ul>
				<p class="font-sans text-sm text-grey01 leading-relaxed mt-4 italic">
					This is a prototype. The search leverages semantic similarity rather than keyword matching, which can yield creative results but may occasionally return less relevant items.
				</p>
			</section>

			<section class="space-y-4">
				<h3 class="font-sans text-xs font-semibold tracking-widest text-green01 uppercase">Team</h3>
				<p class="font-sans text-lg text-grey03 leading-relaxed">
					Developed by <span class="text-white font-medium">Tom Vaillant</span> and <span class="text-white font-medium">Remy Dumas</span>.
				</p>
			</section>

			<section class="space-y-4">
				<h3 class="font-sans text-xs font-semibold tracking-widest text-green01 uppercase">Contact</h3>
				<p class="font-sans text-lg text-grey03 leading-relaxed">
					You can follow my work on
					<a
						href="https://buriedsignals.substack.com/"
						target="_blank"
						rel="noopener noreferrer"
						class="text-green01 hover:text-white font-medium transition-colors duration-300 underline underline-offset-4 decoration-green01/30"
					>
						Substack
					</a>
					and
					<a
						href="https://www.youtube.com/@buriedsignals"
						target="_blank"
						rel="noopener noreferrer"
						class="text-green01 hover:text-white font-medium transition-colors duration-300 underline underline-offset-4 decoration-green01/30"
					>
						YouTube
					</a>.
				</p>
			</section>
		</div>

		<!-- Footer -->
		<div class="p-8 bg-black02 border-t border-black03/50">
			<button
				on:click={close}
				class="btn-primary w-full font-sans font-medium text-base py-4 rounded-xl transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]"
			>
				Close
			</button>
		</div>
	</div>
</div>

<style>
</style>
