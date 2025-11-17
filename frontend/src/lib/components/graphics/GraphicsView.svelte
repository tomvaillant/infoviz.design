<script lang="ts">
  import { Image as Image, Search } from 'lucide-svelte';
  import { apiClient } from '$lib/api-client';
  import { onMount } from 'svelte';

  // All fetched results
  let allExamples: Array<{title: string; image?: string; source?: string; date?: string; url?: string}> = [];
  // Currently displayed results
  let displayedExamples: Array<{title: string; image?: string; source?: string; date?: string; url?: string}> = [];

  let examplesError: string | null = null;
  let examplesLoading = false;
  let hasSearched = false; // Track if user has performed a search

  // Pagination state
  const ITEMS_PER_PAGE = 9;
  let currentPage = 1;

  // Form state
  let prompt = '';

  $: isLoading = examplesLoading;
  $: promptReady = prompt.trim().length > 0;
  $: canSubmit = promptReady && !(isLoading);
  $: totalResults = allExamples.length;
  $: hasMore = displayedExamples.length < totalResults;
  $: showingCount = displayedExamples.length;

  function handleSubmit() {
    if (!prompt.trim() || isLoading) return;
    hasSearched = true;
    currentPage = 1; // Reset pagination on new search
    fetchExamples(prompt.trim());
  }

  async function fetchExamples(prompt: string) {
    examplesError = null;
    examplesLoading = true;

    try {
      const response = await apiClient.fetchGraphicsExamples(prompt);
      allExamples = response.items;
      // Show first page of results
      displayedExamples = allExamples.slice(0, ITEMS_PER_PAGE);
      currentPage = 1;
    } catch (err: any) {
      examplesError = err.message || 'Failed to fetch spotlights';
      allExamples = [];
      displayedExamples = [];
    } finally {
      examplesLoading = false;
    }
  }

  function loadMore() {
    currentPage += 1;
    const endIndex = currentPage * ITEMS_PER_PAGE;
    displayedExamples = allExamples.slice(0, endIndex);
  }

  onMount(async () => {
    try {
      const response = await apiClient.fetchGraphicsExamples("I want you to give me in on the last 9 posts published");
      allExamples = response.items;
      // Show only first 2 on initial load
      displayedExamples = response.items.slice(0, 2);
    } catch (err: any) {
      examplesError = err.message || 'Failed to fetch spotlights';
    }
  });
</script>

<div class="flex h-full bg-black01">

  <main class="flex-1 overflow-y-auto bg-black01">
    <div class="flex items-start justify-center px-8 md:px-12 pt-12 pb-32">
      <div class="max-w-4xl w-full">
        <!-- Compact Hero Section -->
        <section class="mb-8 animate-fade-in-up opacity-0">
          <h1 class="font-display font-semibold text-4xl md:text-5xl text-white mb-4 tracking-tight leading-tight break-words">
            Visual stories that <span class="gradient-text italic whitespace-nowrap pr-2.5">inspire</span>
          </h1>
          <p class="font-sans font-light text-base md:text-lg text-grey03 max-w-xl leading-relaxed">
            Find visual stories from newsrooms around the world.
          </p>
        </section>

        <!-- Form Section -->
        <section class="mb-12 animate-fade-in-up opacity-0 delay-100">
            <form on:submit|preventDefault={handleSubmit} class="flex gap-3 mb-3">
              <div class="relative flex-1">
                <input
                  type="text"
                  id="graphics-prompt"
                  bind:value={prompt}
                  disabled={isLoading}
                  placeholder='Search for climate change, urban data, election graphics...'
                  class="w-full px-6 py-3 rounded-xl bg-black03 border border-black03 font-sans font-light text-base text-white placeholder-grey01 transition-all duration-300 hover:border-green01/30 focus:border-green01"
                />
                <div class="absolute right-6 top-1/2 -translate-y-1/2 pointer-events-none">
                  <Search class="w-5 h-5 text-grey01" />
                </div>
              </div>

              <button type="submit" disabled={!canSubmit} class="btn-primary gap-2 px-6 py-3 font-sans font-medium text-sm rounded-xl transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] whitespace-nowrap">
                {#if (isLoading)}
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-black02"></div>
                  Searching...
                {:else}
                  Find visuals
                {/if}
              </button>
            </form>

            <!-- Disclaimer bubble -->
            <div class="bg-black03/50 border border-black03 rounded-lg px-4 py-2.5">
              <p class="font-sans font-light text-xs text-grey03 leading-relaxed">
                <span class="text-orange01 font-medium">Note:</span> This is a prototype. Search may be slow and some results might be irrelevant.
              </p>
            </div>
        </section>

          {#if examplesError}
            <div class="animate-fade-in">
              <div class="bg-orange01/10 border border-orange01/30 rounded-xl p-6 text-center">
                <p class="font-sans font-medium text-sm text-orange01">{examplesError}</p>
              </div>
            </div>
          {:else if displayedExamples.length > 0}
            <div class="space-y-6 animate-fade-in opacity-0 delay-200">
              <div class="flex items-center justify-between">
                {#if !hasSearched}
                  <h2 class="font-display font-semibold text-2xl md:text-3xl text-white">
                    Daily features
                  </h2>
                {:else}
                  <p class="font-sans font-light text-sm text-grey03">
                    Showing {showingCount} of {totalResults} results
                  </p>
                {/if}
              </div>
              <div class="grid grid-cols-1 gap-5">
                {#each displayedExamples as example, i}
                  <a
                    href={example.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="card group flex flex-col md:flex-row bg-black03 overflow-hidden rounded-xl border border-black03 transition-all duration-500 hover:border-green01/50 hover:shadow-xl hover:shadow-green01/10 hover:-translate-y-0.5 animate-scale-in opacity-0"
                    style="animation-delay: {300 + i * 80}ms">
                    {#if example.image}
                      <div class="relative w-full md:w-2/5 h-[160px] md:h-[180px] overflow-hidden">
                        <img
                          src={example.image}
                          alt={example.title}
                          class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                        />
                        <div class="absolute inset-0 bg-gradient-to-t from-black01/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                      </div>
                    {:else}
                      <div class="w-full md:w-2/5 h-[160px] md:h-[180px] bg-black02 flex items-center justify-center">
                        <Image class="w-10 h-10 text-grey01" />
                      </div>
                    {/if}
                    <div class="flex flex-col justify-between w-full md:w-3/5 p-5">
                      <div>
                        <div class="flex items-center justify-between mb-2">
                          <span class="font-sans font-semibold text-xs tracking-wider text-green01 uppercase">
                            {example.source}
                          </span>
                          <span class="font-sans font-light text-xs text-grey01">
                            {new Date(example.date).toLocaleDateString('en-UK', { year: 'numeric', month: 'short', day: 'numeric' })}
                          </span>
                        </div>
                        <h3 class="font-display font-semibold text-lg md:text-xl text-white leading-tight group-hover:text-green01 transition-colors duration-300">
                          {example.title}
                        </h3>
                      </div>
                    </div>
                  </a>
                {/each}
              </div>

              <!-- Load More Button - Only show after user has searched -->
              {#if hasMore && hasSearched}
                <div class="flex justify-center mt-8">
                  <button
                    on:click={loadMore}
                    class="btn-primary px-8 py-3 font-sans font-medium text-sm rounded-xl transition-all duration-300 hover:scale-105 active:scale-95"
                  >
                    Load more results
                  </button>
                </div>
              {/if}
            </div>
          {/if}

          <!-- Newsletter Section -->
          <div class="mt-16 animate-fade-in-up opacity-0 delay-400">
            <div class="relative newsletter-container gradient-border rounded-xl p-8 md:p-10 text-center overflow-hidden">
              <!-- Decorative background elements -->
              <div class="absolute inset-0 opacity-5">
                <div class="absolute top-0 right-0 w-48 h-48 bg-green01 rounded-full blur-3xl animate-float"></div>
                <div class="absolute bottom-0 left-0 w-48 h-48 bg-green01 rounded-full blur-3xl animate-float" style="animation-delay: 2s;"></div>
              </div>

              <div class="relative z-10">
                <div class="logo flex justify-center mb-6">
                  <img src="/bs.svg" alt="Buried Signals" class="h-12 opacity-90" />
                </div>
                <h3 class="font-display font-semibold text-2xl md:text-3xl text-white mb-4">
                  Buried Signals
                </h3>
                <p class="font-sans font-light text-sm md:text-base text-grey03 mb-6 max-w-xl mx-auto leading-relaxed">
                  The monthly newsletter about visual investigations and the tools to create them.
                </p>
                <a
                  href="https://buriedsignals.substack.com/"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="btn-primary inline-flex gap-2 font-sans font-medium text-sm px-6 py-3 rounded-xl transition-all duration-300 hover:scale-105 active:scale-95"
                >
                  Subscribe
                </a>
              </div>
            </div>
          </div>
      </div>
    </div>
  </main>
</div>

<style>
  :global(.prose iframe) {
    width: 100%;
    border: none;
    min-height: 500px;
  }
</style>
