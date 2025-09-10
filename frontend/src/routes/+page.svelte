<script lang="ts">

  import { onMount } from "svelte";
  import { Button, Card } from 'flowbite-svelte';
  import InstanceInfoForm from "$lib/InstanceInfoForm.svelte";

  let { data } = $props();
  let apiData = [];
  const endpoint = "http://127.0.0.1:8000/";

  function handleClick(instanceName: { page: any; }) {
    window.location.href = "/examples/" + instanceName.page;
  }

  onMount(async function () {
    const response = await fetch(endpoint);
    apiData = await response.json();
    console.log(apiData);
  });


  let btnClass = "bg-accent-dark text-medium-light dark:bg-accent-dark hover:text-darker-dark hover:bg-accent-light dark:hover:bg-accent-light focus:ring-2 focus:ring-lighter-dark focus:outline-none dark:focus:ring-2 dark:focus:ring-darker-light dark:focus:outline-none mt-4 w-md text-lg";

</script>



<div class="grid grid-cols-1 md:grid-cols-2 place-items-center p-10">
  <Card class="bg-medium-light dark:bg-medium-dark rounded-md w-lg h-full flex flex-col" size="xl">
    <h5 class="text-3xl font-bold tracking-tight text-lighter-dark dark:text-darker-light text-center ">Podaj dane swojej instancji Wikibase</h5>
      
    <InstanceInfoForm></InstanceInfoForm>

  </Card>

  <Card class="bg-medium-light dark:bg-medium-dark rounded-md text-center min-w-lg h-full flex flex-col ">
    <h5 class="text-3xl font-bold tracking-tight text-lighter-dark dark:text-darker-light text-center">Wybierz przykład z listy</h5>
    <div class="m-auto">
      <ul>
        {#each data.samples as {page, name} }
          <li>
            <Button class={btnClass} on:click={() => {handleClick({page})}}>{name}</Button>
          </li>
        {/each}
      </ul>
    </div>
  </Card> 
</div>


