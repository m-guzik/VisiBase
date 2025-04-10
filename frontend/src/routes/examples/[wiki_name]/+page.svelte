<script lang="ts">  

    import { onMount } from "svelte";
    import { Card, Spinner, Tabs, TabItem, Tooltip } from 'flowbite-svelte';
    import { ArrowRightOutline } from 'flowbite-svelte-icons';

    import Properties from '$lib/Properties.svelte';


    interface ClassItem { 
      "link" : string,
      "id" : string,
      "number" : number,
      "label" : string }


    interface PropertyItem { 
      "link" : string,
      "id" : string,
      "number" : number,
      "label" : string,
      "datatype" : string }


    let { data } = $props();

    let requestId = data.instance.name;

    let statusClasses = $state("waiting");
    let responseClasses : ClassItem[] = $state([]);

    let statusProperties = $state("waiting");
    let responseProperties : PropertyItem[] = $state([]);
    let datatypesProperties: string[] = $state([]);
    let connectedProperties : {} = $state({});

    let numberOfClasses : number = $state(0);
    let numberOfProperties : number = $state(0);


    function startWebSocket() {
      const ws = new WebSocket(`http://0.0.0.0:8000/ws/${requestId}`);
  
      ws.onmessage = (event) => {
        if (event.data == "Processing started..."){
          console.log(event);
        } else {

          const message = JSON.parse(event.data);

          if (message.status === "done") {
            console.log(event);
            statusClasses = "done";
            responseClasses = message.data;
            responseClasses = [...responseClasses].sort((a, b) => a.number - b.number);
            numberOfClasses = responseClasses.length;
          }    
        }
      };
  
      ws.onclose = () => {
        console.log("WebSocket closed");
      };
    }

    function startPropertiesWebSocket() {
      const ws = new WebSocket(`http://0.0.0.0:8000/pws/${requestId}`);
  
      ws.onmessage = (event) => {
        if (event.data == "Processing started..."){
          console.log(event);
        } else {

          const message = JSON.parse(event.data);

          if (message.status === "done") {
            console.log(event);
            statusProperties = "done";
            responseProperties = message.data.properties;
            responseProperties = [...responseProperties].sort((a, b) => a.number - b.number);
            datatypesProperties = [...new Set(responseProperties.map(item => item.datatype))].sort();
            numberOfProperties = responseProperties.length;
            connectedProperties = message.data.connected;
          }    
        }
      };
  
      ws.onclose = () => {
        console.log("WebSocket closed");
        console.log(connectedProperties);
      };
    }

  
    onMount(() => {
      startWebSocket();
      startPropertiesWebSocket();
    });


    let tabActive = "w-full h-full inline-block font-semibold text-lg text-center bg-accent-dark text-medium-light dark:bg-accent-dark dark:text-lighter-light";
    let tabInactive = "w-full h-full inline-block font-medium text-lg text-center bg-darker-light text-darker-dark dark:bg-darker-dark dark:text-medium-light hover:font-bold";
</script>


<!-- <Img src='/images/WikiHum_light.svg' /> -->



<div class="m-4">

  <Card class="text-center rounded-none bg-medium-light text-lighter-dark dark:bg-medium-dark dark:text-medium-light" size="none">
  <!-- <Card class="text-center rounded-none bg-medium-light text-lighter-dark dark:bg-medium-dark dark:text-medium-light hover:bg-darker-light dark:hover:bg-darker-dark" size="none" href={data.instance.url} > -->
    <div class="flex items-center justify-between w-full">
      <h5 class="text-3xl font-bold tracking-tight text-lighter-dark dark:text-medium-light text-center ">{data.instance.title}</h5>
      <a  href={data.instance.url}><ArrowRightOutline size="xl" class="text-lighter-dark dark:text-medium-light hover:text-accent"></ArrowRightOutline></a>
      <Tooltip placement="top-end" type="custom" defaultClass="" class="bg-medium-light text-lighter-dark dark:bg-medium-dark dark:text-lighter-light p-2 shadow-none border-darker-light border-1" arrow={false}>Przejdź do strony {data.instance.url}</Tooltip>
    </div>
  </Card>

  
  
  <Tabs tabStyle="full" contentClass="p-4 bg-medium-light text-lighter-dark dark:bg-medium-dark dark:text-medium-light" defaultClass="flex divide-x divide-lighter-light dark:divide-lighter-dark h-10 ">
    <TabItem class="w-full " title="Informacje" activeClasses={tabActive} inactiveClasses={tabInactive} open>
      {#if statusProperties === "waiting" || statusClasses === "waiting"}
        <p class="font-bold text-lg"> <Spinner color="custom" customColor="fill-accent" bg="text-lighter-light dark:text-lighter-dark" size={6}/> Trwa pobieranie danych...</p>
      {/if}
      <p class="text-lg">Adres instancji <a href={data.instance.url}>{data.instance.url}</a> </p>
      <p class="text-lg">Liczba klas: {numberOfClasses}</p>
      <p class="text-lg">Liczba właściwości: {numberOfProperties}</p>
    </TabItem>
    <TabItem class="w-full" title="Właściwości" activeClasses={tabActive} inactiveClasses={tabInactive} >


        {#if statusProperties === "waiting"}
          <p class="font-bold text-lg" > <Spinner color="custom" customColor="fill-accent" bg="text-lighter-light dark:text-lighter-dark" size={6}/> Trwa pobieranie danych...</p>
        {/if}
              
        {#if statusProperties === "done"}
          <Properties data={responseProperties} datatypes={datatypesProperties} connected={connectedProperties} ></Properties>
        {/if}

    </TabItem>
    <TabItem class="w-full" title="Klasy" activeClasses={tabActive} inactiveClasses={tabInactive} >
      {#if statusClasses === "waiting"}
        <p class="font-bold text-lg" > <Spinner color="custom" customColor="fill-accent" bg="text-lighter-light dark:text-lighter-dark" size={6}/> Trwa pobieranie danych...</p>
      {/if}
            
      {#if statusClasses === "done"}
        <ul>
          {#each responseClasses as { link, id, label}}
            <li class="text-lg"><a class="font-bold" href={link}>{id}</a> {label}</li>
          {/each}
        </ul>
      {/if}

    </TabItem>
  </Tabs>
  
</div>


