<script lang="ts">  

    import { onMount } from "svelte";
    import { Select, Tabs, TabItem, } from 'flowbite-svelte';

    import Graph from "$lib/Graph.svelte";

    interface ClassItem { 
        "link" : string,
        "id" : string,
        "number" : number,
        "label" : string }

    interface ClassConnection {
      'id': string,
      'sourceId': string,
      'targetId': string,
      'label': string}


    let { data, instanceName } = $props();

    let allClasses: ClassItem[] = $state([]);
    let edges: ClassConnection[] = $state([]);
    let nodes: ClassItem[] = $state([]);
    let edgeLabels: string[] = $state([]);

    let classToHighlight : string = $state("");

    function initializeVariables(){
        allClasses = data.classes;
        allClasses = [...allClasses].sort((a, b) => a.number - b.number);
        nodes = data.nodes;
        edges = data.edges;
        edgeLabels = data.labels;
    }


    let selectedClass : ClassItem = $state({ "link" : '', "id" : '', "number" : 0, "label" : '' });
    let selectedClassID : string = $state("");
    let connectedClasses : ClassItem[] = $state([]);
    let selectedClassConnections : ClassConnection[] = $state([]);

    function chooseClass() {
      selectedClassID = selectedClass.id;
      selectedClassConnections = edges.filter(
          e => e.sourceId === selectedClass.id || e.targetId === selectedClass.id);
      const neighborIds = new Set(selectedClassConnections.flatMap(e => [e.sourceId, e.targetId]));
      neighborIds.add(selectedClassID);
      connectedClasses = nodes.filter(n => neighborIds.has(n.id));
    }

    function highlightNode(id: string) {
      classToHighlight = id;
    }
  
    onMount(() => {
      initializeVariables();
    });


    let tabActive = "w-full h-full inline-block font-semibold text-lg text-center bg-accent-dark text-medium-light dark:bg-accent-dark dark:text-lighter-light";
    let tabInactive = "w-full h-full inline-block font-medium text-lg text-center bg-darker-light text-darker-dark dark:bg-darker-dark dark:text-medium-light hover:font-bold";

</script>



<div >          
    <Tabs tabStyle="full" contentClass="p-4 bg-medium-light text-lighter-dark dark:bg-medium-dark dark:text-medium-light" defaultClass="flex divide-x divide-lighter-light dark:divide-lighter-dark h-10 ">
        <TabItem class="w-full" title="Wszystkie klasy" activeClasses={tabActive} inactiveClasses={tabInactive} open>
            {#if instanceName != 'FactGrid'}            
                <div class="container mx-auto p-4">
                    {#key nodes}
                        <Graph edges={edges} nodes={nodes} edgeLabels={edgeLabels} highlightedNode={classToHighlight}/>
                    {/key}
                </div>
            {/if}
            <ul class="mt-4">
                {#each allClasses as { link, id, label }}
                    <li class="text-lg"><a class="font-bold" href={link}>{id}</a> <button onclick={() => highlightNode(id)}>{label}</button></li>
                {/each}
            </ul>
        </TabItem>
        <TabItem class="w-full" title="Diagram dla wybranej klasy" activeClasses={tabActive} inactiveClasses={tabInactive} >
            <Select bind:value={selectedClass} on:change={chooseClass} size="md" placeholder="Wybierz klasę" class="text-lg"> 
                <option value="" class="text-lg">Wybierz klasę</option>
                {#each nodes as node}
                  <option value={node} class="text-lg">{node.label}</option>
                {/each}
            </Select>
            <div class="container mx-auto p-4">
                {#key selectedClassID}
                    <Graph edges={selectedClassConnections} nodes={connectedClasses} edgeLabels={edgeLabels} highlightedNode={selectedClassID}/>
                {/key}
            </div>
        </TabItem>
    </Tabs>
</div>