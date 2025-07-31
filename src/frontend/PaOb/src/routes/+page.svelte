<script lang="ts">
	import { onMount } from 'svelte';
	import PageCard from '$lib/components/PageCard.svelte';
	
	let elements: any[] = [];
	let loading = true;
	let error: string | null = null;

	onMount(async () => {
		try {
			const res = await fetch('api/pages/');
			if (!res.ok) {
				throw new Error(`HTTP error! status: ${res.status}`);
			}
			elements = await res.json();

		} catch (e: any) {
			error = e.message;
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="PaOb" />
</svelte:head>



<section>
	<div class="section_header">
		<h1>Monitored Pages</h1>
		<a href="/add_page">
			<button>+ Add new page</button>
		</a>
	</div>
	{#if loading}
		<p>Loading...</p>
	{:else if error}
		<p>Error: {error}</p>
	{:else if elements.length === 0}
		<p>No elements found.</p>
	{:else}
		<div class="cards-grid">
			{#each elements as element}
				<PageCard 
					page_id={element.id}
					title={element.page_name} 
					url={element.page_url}
					lastUpdate={element.last_update} 
				/>
			{/each}
		</div>
	{/if}

</section>

<style>
	
	.cards-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1.5rem;
		width: 100%;
		max-width: 900px;
		margin: 0 auto;
	}

	.section_header {
		margin-bottom: 1.5rem;
		display: flex;
		justify-content: space-between; 
		align-items: center; 
		width: 100%; 
		max-width: 900px; 
		margin-bottom: 1.5rem;
	}
</style>
