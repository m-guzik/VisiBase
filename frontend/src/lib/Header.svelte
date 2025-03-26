<script>
    import { Heading } from 'flowbite-svelte';
    import { DarkMode } from 'flowbite-svelte';
</script>


<div class="bg-gradient-to-t from-lighter-light to-darker-light dark:bg-gradient-to-t dark:from-lighter-dark dark:to-darker-dark mb-10" > 
    <DarkMode class='text-lighter-dark dark:text-darker-light hover:bg-lighter-dark hover:text-darker-light dark:hover:bg-darker-light dark:hover:text-lighter-dark text-xl m-1 p-2'/>
    <div class="text-center p-10">
        <a href="/"><Heading class="mb-4 text-7xl font-extrabold tracking-tight text-accent dark:text-accent">Visibase</Heading></a>
        <p class="mt-5 text-2xl font-semibold text-lighter-dark dark:text-medium-light">Visualize your Wikibase</p>
    </div>
</div>