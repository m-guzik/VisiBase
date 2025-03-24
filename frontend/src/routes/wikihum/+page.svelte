<script lang="ts">
    import { onMount } from "svelte";
    import { A, Img } from 'flowbite-svelte';
    import { ArrowRightOutline } from 'flowbite-svelte-icons';
  
    let status = "waiting";
    let requestId = "wikihum";
    let data : string[] = [];
  
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
            data = message.data.data;
          }    
        }
      };
  
      ws.onclose = () => {
        console.log("WebSocket closed");
      };
    }
  
    onMount(() => {
      startWebSocket();
    });

</script>


<div class=m-4>

  <a href="https://wikihum.lab.dariah.pl"><p class="mb-4 font-bold">WikiHum</p></a>
    
    {#if status === "waiting"}
      <p>⏳ Trwa pobieranie danych...</p>
    {/if}
    
    {#if status === "done"}
      <ul>
        {#each data as item}
          <li>{item}</li>
        {/each}
      </ul>
    {/if}
</div>

