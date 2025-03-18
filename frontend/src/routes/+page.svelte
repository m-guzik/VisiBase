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
</script>



<!-- <h1 class="text-center">{apiData.message}</h1> -->

<div class="columns-2 m-10 justify-items-center">
  <div>
    <Card class="bg-my-medium rounded-md text-center h-100">
      <h5 class="text-3xl font-bold tracking-tight text-my-dark">Podaj dane swojej instancji Wikibase</h5>
      <div class="justify-items-center p-10">
        <Label for="api-address" class="mb-2 text-my-dark">Adres API</Label>
        <Input id="api-address" placeholder="ex. https://wikihum.lab.dariah.pl/api.php" class="w-full"/>
      </div>
      <div class="justify-items-center">
        <Label for="sparql-endpoint" class="mb-2 text-my-dark">SPARQL endpoint</Label>
        <Input id="sparql-endpoint" placeholder="ex. https://wikihum.lab.dariah.pl/bigdata/sparql" class="w-full"/>
      </div>
    </Card>
  </div>
  <div>
    <Card class="bg-my-medium rounded-md text-center h-100">
      <h5 class="text-3xl font-bold tracking-tight text-my-dark">Wybierz przykład z listy</h5>
      <div class="m-auto">
        <ul>
          {#each instancesList as item}
            <li>
              <Button class="bg-my-dark text-my-medium m-2 w-xs" on:click={() => {handleClick(item.href)}}>{item.name}</Button>
            </li>
          {/each}
        </ul>
      </div>
    </Card> 
  </div>
</div>


<style> 
</style> 
