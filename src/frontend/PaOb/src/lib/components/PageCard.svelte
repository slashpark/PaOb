<!-- src/lib/components/PageCard.svelte -->
<script lang="ts">
  import { onMount } from 'svelte'; 
  import { timeAgo } from './utils';
  export let page_id: number;
  export let title: string;
  export let url: string = '';
  export let lastUpdate: string = 'N/A';

  import SyncLoader from '$lib/components/SyncLoader.svelte';

  let next: Date = new Date();

  const screenshotUrl = `https://api.microlink.io/?url=${url}&screenshot=true&meta=false&embed=screenshot.url`;
  let loading = true;

  let remainingTime: string = "";
  let lastUpdateTime: string = "";

  function updateTimeRemaining() {
    
    lastUpdateTime = timeAgo(lastUpdate);
    
    const now = new Date();
    const diff = next.getTime() - now.getTime();

    if (diff <= 0) {
      remainingTime = 'Performing the check...';
      setNextCheckTimer();
      updateInfo();
      return;
    }

    const hours = Math.floor(diff / 3600000);
    const mins = Math.floor(diff / 60000);
    const secs = Math.floor((diff % 60000) / 1000);

    if (hours > 0) {
      remainingTime = `${hours} hr ${mins % 60} min ${secs} sec`;
    } 
    else 
    {
      remainingTime = `${mins} min ${secs} sec`;
    }
  }

  function setNextCheckTimer(){
    fetch(`api/pages/${page_id}/next_check`)
      .then(res => res.json())
      .then(data => {
        next = data.next_check ? new Date(data.next_check) : new Date();
      })
      .catch(err => {
        console.error('Error fetching page info:', err);
      });
  }

  let intervalId: ReturnType<typeof setInterval>;
  onMount(() => {
    updateTimeRemaining();
    setNextCheckTimer();
    intervalId = setInterval(updateTimeRemaining, 1000);
    return () => clearInterval(intervalId);
  });

  function updateInfo()
  {
    fetch(`api/pages/${page_id}`)
      .then(res => res.json())
      .then(data => {
        title = data.page_name;
        lastUpdate = data.last_update;
      })
      .catch(err => {
        console.error('Error fetching page info:', err);
      });
  }
</script>

<style>
  .card {
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    background-color: white;
    transition: transform 0.2s ease;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .title {
    font-weight: bold;
    font-size: 1.2rem;
    text-align: center;
  }


  img {
    width: 100%;
    height: auto;
    border-radius: 4px;
    margin-top: 0.5rem;
  }

  .remainingTime {
    font-size: 1rem;
    color: #4a4a4a;
    text-align: center;
  }

  .lastUpdate {
    font-size: 1rem;
    color: #4a4a4a;
    text-align: center;
  }
</style>

<a class="card" href={`/page_info/${page_id}`} style="text-decoration: none; color: inherit; cursor: pointer;">
  <div class="title">{title}</div>

  {#if loading}
  <div style="display: flex; justify-content: center; align-items: center; min-height: 100px;">
      <SyncLoader color="#FF3E00" size="60" duration="0.6s" unit="px" />
    </div>
  {/if}

  <img
    src={screenshotUrl}
    alt="Page preview"
    class="preview"
    on:load={() => (loading = false)}
    style:display={loading ? 'none' : 'block'}
  />
  <div class="lastUpdate">Last page update:<br> {lastUpdateTime}</div>
  <div class="remainingTime">Next check in:<br> {remainingTime}</div>
</a>
