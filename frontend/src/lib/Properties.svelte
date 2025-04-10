<script lang="ts">  

    import { Select } from 'flowbite-svelte';

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
            'to_label': string
    }

    interface ConnectingProperty {
        "id" : string,
        'link': string,
        'label': string,
        'connections': ConnectedProperties[]
    }


    let { data, datatypes, connected } = $props();

    let selectedDatatypes : string = $state("");
    let filteredProperties : PropertyItem[] = $state(data);
    let connectedProperties: ConnectingProperty[] = $state(connected);;

    let response= $derived.by(() => {
		return data;
	});

    // let connectedEntries = Object.entries(connected).values;

    function filterData() {
        filteredProperties = selectedDatatypes
      ? response.filter((item: { datatype: string; }) => item.datatype === selectedDatatypes)
      : response;
  }

</script>



<div >
    <Select bind:value={selectedDatatypes} on:change={filterData} size="md" placeholder="Wybierz typ danych" class="text-lg">
        <option value="" class="text-lg">Wszystkie typy danych</option>
        {#each datatypes as datatype}
          <option value={datatype} class="text-lg">{datatype}</option>
        {/each}
    </Select>

    <ul class="mt-4">
        {#each filteredProperties as { link, id, label }}
          <li class="text-lg"><a class="font-bold" href={link}>{id}</a> {label}</li>
        {/each}
    </ul>



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
</div>

