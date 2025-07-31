<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';

    let pageData: any = null;
    let loading = true;
    let message = '';
    let error = '';

    const id = $page.params.id;

    // Fetch page data on mount
    onMount(async () => {
        try {
            const res = await fetch('/api/pages/' + id);
            if (!res.ok) throw new Error('Unable to load data');
            pageData = await res.json();
            if (pageData && pageData.check_interval) {
                pageData.check_interval = String(pageData.check_interval);
            }
        } catch (err: any) {
            error = err.message;
        } finally {
            loading = false;
        }
    });

    // Edit page
    async function updatePage() {
        message = '';
        error = '';

        try {
            const res = await fetch(`/api/pages/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(pageData),
            });
            if (!res.ok) throw new Error('Error during update');
            message = 'Page updated successfully!';
        } catch (err: any) {
            error = err.message;
        }
    }

    // Delete page
    async function deletePage() {
        if (!confirm('Are you sure you want to delete this page?')) return;

        try {
            const res =  await fetch(`/api/pages/${id}`, {
                method: 'DELETE'
            });
            if (!res.ok) throw new Error('Error during deletion');
            goto('/');
        } catch (err: any) {
            error = err.message;
        }
    }

    // Manual check
    async function manualCheck() {
        //TODO: 
    }
</script>

<svelte:head>
	<title>Page Info</title>
	<meta name="description" content="PaOb" />
</svelte:head>

<section>
{#if loading}
    <p>Loading...</p>
{:else if error}
    <p>{error}</p>
{:else}

    <div style="display: flex; gap: 2rem; align-items: flex-start;">
        <div style="min-width: 350px; max-width: 400px;">
            <h3>Page preview</h3>
            {#if pageData?.page_url}
                <img
                    class = "preview-image"
                    src={`https://api.microlink.io/?url=${pageData.page_url}&screenshot=true&meta=false&embed=screenshot.url`}
                    alt="Page screenshot"
                />
            {:else}
                <div>No URL to preview</div>
            {/if}
        </div>

        <form on:submit|preventDefault={updatePage} style="flex:1;width: 600px;">
            <h1 >Edit monitored page</h1>

            <label>
                Name:
                <input type="text" bind:value={pageData.page_name} required class="input" />
            </label>

            <label>
                URL:
                <input type="url" bind:value={pageData.page_url} required class="input" />
            </label>

            <label>
                Interval:
                <select id="interval" bind:value={pageData.check_interval}>
                    <option value=5>5 sec</option>
                    <option value=30>30 sec</option>
                    <option value=60>1 min</option>
                    <option value=300>5 min</option>
                    <option value=900>15 min</option>
                    <option value=1800>30 min</option>
                    <option value=3600>1 hour</option>
                    <option value=18000>5 hours</option>
                    <option value=43200>12 hours</option>
                    <option value=86400>1 day</option>
                </select>
            </label>

            <div>
                <p><strong>Last update:</strong> {pageData.last_update ? new Date(pageData.last_update).toLocaleString() : 'N/A'}</p>
                <p><strong>Last check:</strong>  {pageData.last_check ? new Date(pageData.last_check).toLocaleString() : 'N/A'}</p>
                <p>
                    <strong>Current status:</strong>
                    <span
                        style="
                            display: inline-block;
                            width: 18px;
                            height: 18px;
                            border-radius: 50%;
                            position: relative;
                            top: 4px;
                            background:
                                {pageData.page_state === 'ok' ? '#22c55e' : 
                                 pageData.page_state === 'error' ? '#ef4444' : 
                                 pageData.page_state === 'pending' ? '#facc15' : 
                                 '#d1d5db'};
                        "
                        title={pageData.page_state || 'N/A'}
                    ></span>
                </p>
            </div>

            <div class="button_container">
                <button type="submit" class="large_button">💾 Save</button>
                <button type="button" class="large_button" style="background-color:#ef4444;" on:click={deletePage}>🗑️ Delete</button>
                <button type="button" class="large_button" style="background-color:#5cb705;" on:click={manualCheck}>⟲ Manual Check</button>        
            </div>

            {#if message}
                <p>{message}</p>
            {/if}

        </form>
    </div>
    {/if}
</section>

<style>
    .large_button{
        width: 32%;
    }

    .preview-image {
        width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
</style>
