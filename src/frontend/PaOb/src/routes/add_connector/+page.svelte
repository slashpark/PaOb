<script lang="ts">
    import { slide } from 'svelte/transition';
    
    let connectorName = '';
    let connectorType = '';
    let connectorsParams: { bot_token?: string; chat_token?: string } = {};

    let message = '';
    let error = '';

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
                headers: {
                    'Content-Type': 'application/json',
                },
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
            // reset
            connectorName = '';
            connectorType = '';
            connectorsParams = {};

            setTimeout(() => {
                window.location.href = '/';
            }, 100);

        } catch (err: any) {
            error = err.message || 'Unknown error';
        }
    }
</script>

<svelte:head>
	<title>Add New Connector</title>
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
</style>

<section>
    <form on:submit|preventDefault={handleSubmit}>
        <h1>Add a new connector</h1>

        <label for="name">Connector Name</label>
        <input id="name" type="text" bind:value={connectorName}/>

        <label for="interval">Connector Type</label>
        <select id="interval" bind:value={connectorType}>
            <option value="telegram">Telegram</option>
            <option value="discord">Discord (WIP)</option>
        </select>

        {#key connectorType}
            <div transition:slide>
            {#if connectorType === 'telegram'}
                <label for="bot_token">Bot Token</label>
                <input id="bot_token" type="text" bind:value={connectorsParams.bot_token}/>

                <label for="chat_token">Chat Token</label>
                <input id="chat_token" type="text" bind:value={connectorsParams.chat_token}/>
            {:else if connectorType === 'discord'}
                <label for="bot_token">Bot Token</label>
                <input id="bot_token" type="text" bind:value={connectorsParams.bot_token}/>
            {/if}
            </div>
        {/key}

    <div style="display: flex; justify-content: center; margin-top: 1.5rem;">
            <button type="submit">Add</button>
    </div>

        {#if message}
            <div class="message">{message}</div>
        {/if}

        {#if error}
            <div class="error">{error}</div>
        {/if}
    </form>
</section>
