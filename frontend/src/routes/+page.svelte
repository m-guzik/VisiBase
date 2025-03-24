<script lang="ts">
// @ts-nocheck

  import { onMount } from "svelte";
  import { Button, Card, Input, Label } from 'flowbite-svelte';

  const endpoint = "http://127.0.0.1:8000/";
  let apiData = [];
  let instancesList = [ { name: 'LexBib', href: '/lexbib' },
    { name: 'Wikibase World', href: '/wikibase-world' },
    { name: 'WikiHum', href: '/wikihum'} ];

  onMount(async function () {
    const response = await fetch(endpoint);
    apiData = await response.json();
    console.log(apiData);
  });

  function handleClick(instanceAddress) {
        window.location.href = instanceAddress;
    }

    let btnClass = "bg-accent-dark text-medium-light dark:bg-accent-dark hover:bg-accent-light dark:hover:bg-accent-light m-2 w-xs";
</script>



<!-- <h1 class="text-center">{apiData.message}</h1> -->



<div class="grid grid-cols-1 md:grid-cols-2 place-items-center p-10">
  <Card class="bg-medium-light dark:bg-darker-dark rounded-md max-w-sm w-full h-full flex flex-col">
    <h5 class="text-3xl font-bold tracking-tight text-lighter-dark dark:text-darker-light text-center ">Podaj dane swojej instancji Wikibase</h5>
      
    <form class="m-2">
      <div>
        <Label for="name" class="text-accent-dark dark:text-accent-dark text-left mt-2">Nazwa</Label>
        <Input type="text" id="name" placeholder="e.g. WikiHum" required/>
      </div>
      <div>
        <Label for="api-address" class="text-accent-dark dark:text-accent-dark text-left mt-2">Adres API</Label>
        <Input type="text" id="api-address" placeholder="e.g. https://wikihum.lab.dariah.pl/api.php" required/>
      </div>
      <div>
        <Label for="sparql-endpoint" class="text-accent-dark dark:text-accent-dark text-left mt-2">SPARQL endpoint</Label>
        <Input type="text" id="sparql-endpoint" placeholder="e.g. https://wikihum.lab.dariah.pl/bigdata/sparql" required/>
      </div>
    </form>

    <Button class={btnClass}>Połącz</Button>
  </Card>

  <Card class="bg-medium-light dark:bg-darker-dark rounded-md text-center max-w-sm w-full h-full flex flex-col ">
    <h5 class="text-3xl font-bold tracking-tight text-lighter-dark dark:text-darker-light text-center">Wybierz przykład z listy</h5>
    <div class="m-auto">
      <ul>
        {#each instancesList as item}
          <li>
            <Button class={btnClass} on:click={() => {handleClick(item.href)}}>{item.name}</Button>
          </li>
        {/each}
      </ul>
    </div>
  </Card> 
</div>


