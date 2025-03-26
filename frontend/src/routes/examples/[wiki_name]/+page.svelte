<script lang="ts">  

    import { onMount } from "svelte";
    import { Card, Img, Spinner, Tabs, TabItem, Tooltip } from 'flowbite-svelte';

    let { data } = $props();


    let status = $state("waiting");
    let requestId = data.instance.name;
    let response : string[] = $state([]);

    let p_status = $state("waiting");
    let p_response : string[] = $state([]);
  
    function startWebSocket() {
      const ws = new WebSocket(`http://0.0.0.0:8000/ws/${requestId}`);
  
      ws.onmessage = (event) => {
        if (event.data == "Processing started..."){
          console.log(event);
        } else {

          const message = JSON.parse(event.data);

          if (message.status === "done") {
            console.log(event);
            status = "done";
            response = message.data.data;
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
            p_status = "done";
            p_response = message.data.data;
          }    
        }
      };
  
      ws.onclose = () => {
        console.log("WebSocket closed");
      };
    }


  
    onMount(() => {
      startWebSocket();
      startPropertiesWebSocket();
    });


    let btnActive = "w-full h-full inline-block font-medium text-center bg-accent-light text-lighter-light dark:bg-accent-dark dark:text-lighter-light";
    let btnInactive = "w-full h-full inline-block font-medium text-center bg-darker-light text-darker-dark dark:bg-darker-dark dark:text-medium-light hover:font-bold";
</script>


<!-- <Img src='/images/WikiHum_light.svg' /> -->



<div class="m-4">

  <Card class="text-center rounded-none bg-medium-light text-lighter-dark dark:bg-medium-dark dark:text-medium-light hover:bg-darker-light dark:hover:bg-darker-dark" size="none" href={data.instance.url} >
    <h5 class="text-3xl font-bold tracking-tight text-lighter-dark dark:text-medium-light text-center ">{data.instance.title}</h5>
  </Card>
  <Tooltip placement="top-end" type="custom" defaultClass="" class="bg-medium-light text-lighter-dark dark:bg-medium-dark dark:text-lighter-light p-2 shadow-none border-darker-light border-1" arrow={false}>Przejdź do strony {data.instance.url}</Tooltip>
  
  
  <Tabs tabStyle="full" contentClass="p-4 bg-medium-light text-lightest-dark dark:bg-medium-dark dark:text-medium-light" defaultClass="flex divide-x divide-lighter-light dark:divide-lighter-dark h-10 ">
    <TabItem class="w-full " title="Informacje" activeClasses={btnActive} inactiveClasses={btnInactive} open>
      <p>Liczba właściwości, liczba klas, adresy</p>
    </TabItem>
    <TabItem class="w-full" title="Właściwości" activeClasses={btnActive} inactiveClasses={btnInactive} >
        {#if p_status === "waiting"}
          <p> <Spinner />⏳ Trwa pobieranie danych...</p>
        {/if}
              
        {#if p_status === "done"}
          <ul>
            {#each p_response as item}
              <li>{item}</li>
            {/each}
          </ul>
        {/if}
    </TabItem>
    <TabItem class="w-full" title="Klasy" activeClasses={btnActive} inactiveClasses={btnInactive} >
      {#if status === "waiting"}
        <p> <Spinner />⏳ Trwa pobieranie danych...</p>
      {/if}
            
      {#if status === "done"}
        <ul>
          {#each response as item}
            <li>{item}</li>
          {/each}
        </ul>
      {/if}
    </TabItem>
  </Tabs>
  
</div>


