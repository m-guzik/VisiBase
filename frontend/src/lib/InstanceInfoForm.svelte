<script lang="ts">
    import { Button, Input, Label } from 'flowbite-svelte';
    import { goto } from '$app/navigation';
  
    let name = '';
    let url = '';
    let apiAddress = '';
    let sparqlEndpoint = '';

    async function handleSubmit(event: Event) {
      event.preventDefault();
      goto(`/${name}?endpoint=${encodeURIComponent(sparqlEndpoint)}&url=${encodeURIComponent(url)}`);
    }

    let btnClass = "bg-accent-dark text-medium-light dark:bg-accent-dark hover:text-darker-dark hover:bg-accent-light dark:hover:bg-accent-light focus:ring-2 focus:ring-accent focus:outline-none dark:focus:ring-2 dark:focus:ring-accent dark:focus:outline-none mt-4 w-md text-lg";

  </script>
  


  <form class="m-2" on:submit|preventDefault={handleSubmit}>
    <div>
      <Label for="name" class="text-lighter-dark dark:text-darker-light text-left mt-2 text-lg">Nazwa</Label>
      <Input type="text" id="name" placeholder="e.g. WikiHum" bind:value={name} required/>
    </div>
    <!-- <div>
      <Label for="api-address" class="text-lighter-dark dark:text-darker-light text-left mt-2 text-lg">Adres API</Label>
      <Input type="text" id="api-address" placeholder="e.g. https://wikihum.lab.dariah.pl/api.php" bind:value={apiAddress}  required/>
    </div> -->
    <div>
      <Label for="url" class="text-lighter-dark dark:text-darker-light text-left mt-2 text-lg">Adres instancji</Label>
      <Input type="text" id="url" placeholder="e.g. https://wikihum.lab.dariah.pl" bind:value={url}  required/>
    </div>
    <div>
      <Label for="sparql-endpoint" class="text-lighter-dark dark:text-darker-light text-left mt-2 text-lg">SPARQL endpoint</Label>
      <Input type="text" id="sparql-endpoint" placeholder="e.g. https://wikihum.lab.dariah.pl/bigdata/sparql" bind:value={sparqlEndpoint}  required/>
    </div>
    <Button class={btnClass} type="submit">Połącz</Button>
  </form>