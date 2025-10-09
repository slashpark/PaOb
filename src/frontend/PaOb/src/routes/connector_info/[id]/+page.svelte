<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';

    let connectorData: any = null;
    let loading = true;
    let error = '';

    const id = $page.params.id;

    // Fetch connector data on mount
    onMount(async () => {
        try {
            console.log('Fetching connector data for id:', id);
            const res = await fetch('/api/notifiers/connectors/' + id);
            if (!res.ok) throw new Error('Unable to load connector data');
            connectorData = await res.json();
        } catch (err: any) {
            error = err.message;
        } finally {
            loading = false;
        }
    });

    // Delete connector
    async function deleteConnector() {
        if (!confirm('Are you sure you want to delete this connector?')) return;

        try {
            const res =  await fetch(`/api/notifiers/connectors/${id}`, {
                method: 'DELETE'
            });
            if (!res.ok) throw new Error('Error during deletion');
            goto('/');
        } catch (err: any) {
            error = err.message;
        }
    }
</script>

<svelte:head>
    <title>Connector Info</title>
    <meta name="description" content="PaOb Connector Info" />
</svelte:head>

<section>
{#if loading}
    <p>Loading...</p>
{:else if error}
    <p>{error}</p>
{:else if connectorData}
    <div style="max-width: 600px; margin: auto;">
        <h1>Connector Info</h1>
        <table style="width:100%;border-collapse:collapse;">
            <tbody>
                <tr>
                    <th style="text-align:left;">ID</th>
                    <td>{connectorData.id}</td>
                </tr>
                <tr>
                    <th style="text-align:left;">Name</th>
                    <td>{connectorData.name}</td>
                </tr>
                <tr>
                    <th style="text-align:left;">Type</th>
                    <td>{connectorData.type}</td>
                </tr>
                <tr>
                    <th style="text-align:left;">Params</th>
                    <td>
                        {#if connectorData.params && typeof connectorData.params === 'object'}
                            <table style="width:100%;border-collapse:collapse;background:#fafafa;">
                                <tbody>
                                    {#each Object.entries(connectorData.params) as [key, value]}
                                        <tr>
                                            <th style="text-align:left;">{key}</th>
                                            <td>{value}</td>
                                        </tr>
                                    {/each}
                                </tbody>
                            </table>
                        {:else}
                            {connectorData.params}
                        {/if}
                    </td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top:2rem;">
            <button type="button" class="large_button" style="background-color:#ef4444;" on:click={deleteConnector}>🗑️ Delete Connector</button>
        </div>
    </div>
{/if}
</section>

<style>
    .large_button{
        width: 100%;
        padding: 1rem;
        font-size: 1.1rem;
        border-radius: 6px;
        border: none;
        cursor: pointer;
        color: white;
    }
    th, td {
        padding: 0.5rem;
        border-bottom: 1px solid #eee;
    }
    th {
        background: #f3f4f6;
    }
</style>
