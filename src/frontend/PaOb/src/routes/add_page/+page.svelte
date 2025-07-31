<script lang="ts">
    let pageName = '';
    let pageUrl = '';
    let elementToMonitor = '';
    let checkInterval: string = "60";

    let message = '';
    let error = '';

    async function handleSubmit() {
        message = '';
        error = '';

        if (!pageName || !pageUrl || Number(checkInterval) <= 0) {
            error = 'Please fill in all required fields';
            return;
        }

        try {
            const res = await fetch('api/pages/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    page_name: pageName,
                    page_url: pageUrl,
                    element_to_monitor: elementToMonitor || "",
                    check_interval: Number(checkInterval)
                }),
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || 'Request error');
            }

            message = 'Page added successfully!';
            // reset
            pageName = '';
            pageUrl = '';
            elementToMonitor = '';
            checkInterval = "60";

            setTimeout(() => {
                window.location.href = '/';
            }, 100);

        } catch (err: any) {
            error = err.message || 'Unknown error';
        }
    }
</script>

<svelte:head>
	<title>Add Page</title>
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
        <h1>Add a new page to monitor</h1>

        <label for="name">Name</label>
        <input id="name" type="text" bind:value={pageName}/>

        <label for="url">URL</label>
        <input id="url" type="url" bind:value={pageUrl} />

        <label for="interval">Check Interval</label>
        <select id="interval" bind:value={checkInterval}>
            <option value=5>5 sec</option>
            <option value=30>30 sec</option>
            <option value=60 selected>1 min</option>
            <option value=300>5 min</option>
            <option value=900>15 min</option>
            <option value=1800>30 min</option>
            <option value=3600>1 hour</option>
            <option value=18000>5 hours</option>
            <option value=43200>12 hours</option>
            <option value=86400>1 day</option>
        </select>

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
