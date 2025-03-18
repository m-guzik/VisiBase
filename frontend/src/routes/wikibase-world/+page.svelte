<script lang="ts">
    import { onMount } from "svelte";
  
    let status = "waiting";
    let requestId = "wikibase-world";
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
  
<a href="https://wikibase.world"><h1>Wikibase World</h1></a>
  
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
