<script lang="ts">

  import { Button, Card } from 'flowbite-svelte';

  let { data } = $props();


  function handleClick(instanceName: { page: any; }) {
    window.location.href = "/examples/" + instanceName.page;
  }

  let btnClass = "bg-accent-dark text-medium-light dark:bg-accent-dark hover:text-darker-dark hover:bg-accent-light dark:hover:bg-accent-light focus:ring-2 focus:ring-accent focus:outline-none dark:focus:ring-2 dark:focus:ring-accent dark:focus:outline-none mt-4 w-md text-lg";

</script>


<div class="grid grid-cols-1 place-items-center p-10">
    <Card class="bg-medium-light dark:bg-medium-dark rounded-md grid md:grid-cols-2" size="xl">
        <div class="flex flex-col items-center justify-center p-8 text-center border-r-3 border-darker-light dark:border-lighter-dark">
            <h5 class="text-3xl font-semibold tracking-tight text-lighter-dark dark:text-darker-light text-center">
                Nie musisz podawać danych swojej instancji Wikibase.
                <br>
                <br>
                Działanie aplikacji możesz też przetestować na jednym z podanych przykładów.</h5>
        </div>
        <div class="flex flex-col items-center justify-center p-8 text-center">
            <h5 class="text-3xl font-bold tracking-tight text-lighter-dark dark:text-darker-light text-center mb-4">Wybierz przykład z listy</h5>
            <div class="m-auto">
                <ul>
                    {#each data.samples as {page, name} }
                    <li>
                        <Button class={btnClass} on:click={() => {handleClick({page})}}>{name}</Button>
                    </li>
                    {/each}
                </ul>
            </div>
        </div>
    </Card>
</div>


