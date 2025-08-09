<script lang="ts">  

    import { onMount } from "svelte";
    import { Select } from 'flowbite-svelte';

    import Graph from "$lib/Graph.svelte";

    interface PropertyItem { 
        "link" : string,
        "id" : string,
        "number" : number,
        "label" : string,
        "datatype" : string }

    interface ConnectedProperties {
            'from_link': string,
            'from_id': string, 
            'from_label': string,
            'to_link': string, 
            'to_id': string, 
            'to_label': string }

    interface ConnectingProperty {
        "id" : string,
        'link': string,
        'label': string,
        'connections': ConnectedProperties[] }


    let { data } = $props();

    let allProperties : PropertyItem[] = $state([]);
    let datatypes: string[] = $state([]);
    let nodes: string[] = $state([]);
    let edges: string[] = $state([]);
    let edgeLabels: string[] = $state([]);
    let connectedProperties: ConnectingProperty[] = $state([]);
    let filteredProperties : PropertyItem[] = $state([]);

    let propertyToHighlight : string = $state("");
    let selectedDatatype : string = $state("");

    function initializeVariables(){
        allProperties = data.properties;
        allProperties = [...allProperties].sort((a, b) => a.number - b.number);
        datatypes = [...new Set(allProperties.map(item => item.datatype))].sort();
        nodes = data.nodes;
        edges = data.edges;
        edgeLabels = data.labels;
        connectedProperties = data.connected;
        filteredProperties = allProperties;
    }

    function filterData() {
        filteredProperties = selectedDatatype
      ? allProperties.filter((item: { datatype: string; }) => item.datatype === selectedDatatype) : allProperties;
    }

    function highlightNode(id: string) {
      propertyToHighlight = id;
    }
  
    onMount(() => {
      initializeVariables();
    });

</script>



<div >
    {#if connectedProperties.length > 0 }
        <div class="container mx-auto p-4">
          <Graph edges={edges} nodes={nodes} edgeLabels={edgeLabels} highlightedNode={propertyToHighlight}/>
        </div>
    {/if}


    <Select bind:value={selectedDatatype} on:change={filterData} size="md" placeholder="Wybierz typ danych" class="text-lg">
        <option value="" class="text-lg">Wszystkie typy danych</option>
        {#each datatypes as datatype}
          <option value={datatype} class="text-lg">{datatype}</option>
        {/each}
    </Select>


    <ul class="mt-4">
        {#each filteredProperties as { link, id, label }}
          <li class="text-lg"><a class="font-bold" href={link}>{id}</a> <button onclick={() => highlightNode(id)}>{label}</button></li>
        {/each}
    </ul>


    {#if connectedProperties.length > 0 }
        <p class="font-bold text-lg mt-10">Zależności pomiędzy właściwościami</p>
        <ul>
            {#each connectedProperties as connectingP}
            <li class="text-lg mt-4"><a class="font-bold" href={connectingP.link}>{connectingP.id}</a> {connectingP.label}</li>
                {#each connectingP.connections as connected}
                    <li class="ml-4"><a class="font-bold" href={connected.from_link}>{connected.from_id}</a> {connected.from_label} - 
                        <a class="font-bold" href={connected.to_link}>{connected.to_id}</a> {connected.to_label}</li>
                {/each}
            {/each}
        </ul>
    {/if}
</div>

