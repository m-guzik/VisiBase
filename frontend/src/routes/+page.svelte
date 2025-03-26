<script lang="ts">
// @ts-nocheck

  import { onMount } from "svelte";
  import { Button, Card, Input, Label } from 'flowbite-svelte';

  let { data } = $props();
  let apiData = [];
  const endpoint = "http://127.0.0.1:8000/";


  function handleClick(instanceName) {
    window.location.href = "/examples/" + instanceName.name;
  }


  onMount(async function () {
    const response = await fetch(endpoint);
    apiData = await response.json();
    console.log(apiData);
  });


  let btnClass = "bg-accent-dark text-medium-light dark:bg-accent-dark hover:bg-accent-light dark:hover:bg-accent-light m-2 w-xs";

</script>



<!-- <h1 class="text-center">{apiData.message}</h1> -->



<div class="grid grid-cols-1 md:grid-cols-2 place-items-center p-10">
  <Card class="bg-medium-light dark:bg-medium-dark rounded-md max-w-sm w-full h-full flex flex-col">
    <h5 class="text-3xl font-bold tracking-tight text-lighter-dark dark:text-darker-light text-center ">Podaj dane swojej instancji Wikibase</h5>
      
    <form class="m-2">
      <div>
        <Label for="name" class="text-accent-dark dark:text-accent-light text-left mt-2">Nazwa</Label>
        <Input type="text" id="name" placeholder="e.g. WikiHum" required/>
      </div>
      <div>
        <Label for="api-address" class="text-accent-dark dark:text-accent-light text-left mt-2">Adres API</Label>
        <Input type="text" id="api-address" placeholder="e.g. https://wikihum.lab.dariah.pl/api.php" required/>
      </div>
      <div>
        <Label for="sparql-endpoint" class="text-accent-dark dark:text-accent-light text-left mt-2">SPARQL endpoint</Label>
        <Input type="text" id="sparql-endpoint" placeholder="e.g. https://wikihum.lab.dariah.pl/bigdata/sparql" required/>
      </div>
    </form>

    <Button class={btnClass}>Połącz</Button>
  </Card>

  <Card class="bg-medium-light dark:bg-medium-dark rounded-md text-center max-w-sm w-full h-full flex flex-col ">
    <h5 class="text-3xl font-bold tracking-tight text-lighter-dark dark:text-darker-light text-center">Wybierz przykład z listy</h5>
    <div class="m-auto">
      <ul>
        {#each data.samples as {name, title} }
          <li>
            <!-- <a href="/examples/{name}"><Button class={btnClass} >{title}</Button></a> -->
            <Button class={btnClass} on:click={() => {handleClick({name})}}>{title}</Button>
          </li>
        {/each}
      </ul>
    </div>
  </Card> 
</div>


