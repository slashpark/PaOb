<script lang="ts">
    import { onMount } from 'svelte';
    import telegramIcon from '$lib/images/telegram.svg';
    import discordIcon from '$lib/images/discord.svg';

    let connectors: Array<{ name: string; type: string; status: string }> = [];
    let loading = true;
    let error = '';
    let showAddForm = false;

    // Form fields
    let connectorName = '';
    let connectorType = '';
    let connectorsParams: { bot_token?: string; chat_token?: string } = {};
    let message = '';

    async function fetchConnectors() {
        loading = true;
        error = '';
        try {
            const res = await fetch('api/notifiers/connectors');
            if (!res.ok) throw new Error('Failed to fetch connectors');
            connectors = await res.json();
        } catch (err: any) {
            error = err.message || 'Unknown error';
        } finally {
            loading = false;
        }
    }

    async function handleSubmit() {
        message = '';
        error = '';
        if (!connectorName || !connectorType) {
            error = 'Please fill in all required fields';
            return;
        }
        try {
            const res = await fetch('api/notifiers/add_connector', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    connector_name: connectorName,
                    connector_type: connectorType,
                    connector_status: "enabled",
                    connector_params: connectorsParams
                }),
            });
            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || 'Request error');
            }
            message = 'Connector added successfully!';
            connectorName = '';
            connectorType = '';
            connectorsParams = {};
            showAddForm = false;
            fetchConnectors();
        } catch (err: any) {
            error = err.message || 'Unknown error';
        }
    }

    onMount(fetchConnectors);
</script>

<svelte:head>
    <title>Connectors</title>
    <meta name="description" content="PaOb" />
</svelte:head>

<style>
    .message {
        margin-top: 1rem;
        color: green;
    }
    .error {
        margin-top: 1rem;
        color: red;
    }
    .connector-list {
        margin-bottom: 2rem;
    }

    .connector-list-element {
        display: block;
        padding: 1rem;
        border: 1px solid #ccc;
        border-radius: 8px;
        min-width: 200px;
        background: #fafafa;
        text-decoration: none;
        color: inherit;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s;
    }

    .connector-list-element:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.10);
    }
</style>

<section>
    <h1>Connectors</h1>
    <div class="connector-list">
        {#if loading}
            <p>Loading connectors...</p>
        {:else if error}
            <div class="error">{error}</div>
        {:else}
            <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
                {#each connectors as connector}
                    <a href={`/connector_info/${connector.id}`} class="connector-list-element" style="display: flex; align-items: center; gap: 0.75rem;">
                        {#if connector.type === 'telegram'}
                            <img src={telegramIcon} alt="Telegram" width="32" height="32" />
                        {:else if connector.type === 'discord'}
                            <img src={discordIcon} alt="Discord" width="32" height="32" />
                        {/if}
                        <div>
                            <div><strong>{connector.name}</strong></div>
                        </div>
                    </a>
                {/each}
            </div>
        {/if}
    </div>
    <a href="/add_connector">
		<button>+ Add new connector</button>
	</a>
</section>
