<script lang="ts">
  import { Image as Image, Search } from 'lucide-svelte';
  import { apiClient } from '$lib/api-client';
  import { onMount } from 'svelte';

  let examples: Array<{title: string; image?: string; source?: string; date?: string; url?: string}> = [];
  let examplesError: string | null = null;
  let examplesLoading = false;

  examples = []

  // Form state
  let prompt = '';

  $: isLoading = examplesLoading;
  $: promptReady = prompt.trim().length > 0;
  $: canSubmit = promptReady && !(isLoading);

  function handleSubmit() {
    if (!prompt.trim() || isLoading) return;
      fetchExamples(prompt.trim());
  }

  async function fetchExamples(prompt: string) {
    examplesError = null;
    examplesLoading = true;

    try {
      const response = await apiClient.fetchGraphicsExamples(prompt);
      examples = response.items;
    } catch (err: any) {
      examplesError = err.message || 'Failed to fetch spotlights';
    } finally {
      examplesLoading = false;
    }
  }

  onMount(async () => {
    try {
      const response = await apiClient.fetchGraphicsExamples("I want you to give me in on the last 9 posts published");
      examples = response.items;
    } catch (err: any) {
      examplesError = err.message || 'Failed to fetch spotlights';
    }
  });
</script>

<div class="flex h-full overflow-hidden bg-black01">

  <main class="flex-1 overflow-y-auto bg-black01">
    <div class="flex items-start justify-center px-12 p-[112px]">
      <div class="max-w-3xl w-full">
        <!-- Form Section -->
        <section>
          <div>
            <div class="pb-8 border-b border-b-grey01">
              <h2 class="text-7xl tracking-negative text-white">
                Inspiration
              </h2>
              <p class="font-light text-xl text-grey03 pt-10">
                Discover spotlights on your chosen topics from a repository of data-driven visual stories from around the world.
              </p>
            </div>

            <form on:submit|preventDefault={handleSubmit} class="mt-8">
              <div>
                <label for="graphics-prompt" class="font-light text-xl text-grey03">
                  Describe your topic for inspiration
                </label>
                <textarea
                  id="graphics-prompt"
                  bind:value={prompt}
                  disabled={isLoading}
                  placeholder='E.g., "climate change visualizations", "urban mobility maps", ...'
                  class="w-full h-28 mt-4 px-5 py-4 rounded bg-black03 font-light text-base text-grey03"
                ></textarea>
              </div>

              <button type="submit" disabled={!canSubmit} class="btn-primary w-full gap-2 mt-3 font-light text-base">
                {#if (isLoading)}
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Loading...
                {:else}
                  <Search class="w-4 h-4" />
                  Find spotlights
                {/if}
              </button>
            </form>
          </div>
        </section>

          {#if examplesError}
            <div class="mt-8 pt-8 border-t border-t-grey01">
              <p class="font-bold text-sm tracking-small text-red-800 text-center">{examplesError}</p>
            </div>
          {:else if examples.length > 0}
            <div class="space-y-6 mt-8 pt-8 border-t border-t-grey01">
              <div class="grid grid-cols-1">
                {#each examples as example}
                  <a
                    href={example.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="card flex flex-col md:flex-row mb-8 bg-black03 overflow-hidden transform transition-all rounded-lg hover:scale-[1.01]">
                    {#if example.image}
                      <img
                        src={example.image}
                        alt={example.title}
                        class="w-full md:w-1/2 h-[156px] md:h-[216px] object-cover"
                      />
                    {:else}
                      <div class="w-full md:w-1/2 h-[156px] md:h-[216px] bg-gray-200 flex items-center justify-center text-gray-500">
                        No image available
                      </div>
                    {/if}
                    <div class="flex flex-col justify-between gap-4 w-full min-h-[180px] md:min-h-auto md:w-1/2 p-6">
                      <div class="flex justify-between gap-4">
                        <p class="md:min-h-[30px] font-bold text-sm tracking-small text-grey01 uppercase">
                          {example.source}
                        </p>
                        <p class="font-light text-sm text-grey01 no-wrap hidden md:block">
                          {new Date(example.date).toLocaleDateString('en-UK', { year: 'numeric', month: 'numeric', day: 'numeric' })}
                        </p>
                      </div>
                      <h4 class="font-bold text-xl md:text-2xl mb-3">
                        {example.title}
                      </h4>
                      <div class="flex justify-between md:justify-end gap-4">
                        <p class="font-light text-sm text-grey01 no-wrap md:hidden">
                          {new Date(example.date).toLocaleDateString('en-UK', { year: 'numeric', month: 'numeric', day: 'numeric' })}
                        </p>
                        <p class="button-discover font-light text-sm text-grey03">
                          Discover it →
                        </p>
                      </div>
                    </div>
                  </a>
                {/each}
              </div>
            </div>
          {/if}
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
