<script lang="ts">  

    import { Select } from 'flowbite-svelte';

    interface PropertyItem { 
        "link" : string,
        "id" : string,
        "number" : number,
        "label" : string,
        "datatype" : string }


    let { data, datatypes } = $props();

    let selectedDatatypes : string = $state("");
    let filteredProperties : PropertyItem[] = $state(data);

    let response = $derived.by(() => {
		return data;
	});

    function filterData() {
        filteredProperties = selectedDatatypes
      ? response.filter((item: { datatype: string; }) => item.datatype === selectedDatatypes)
      : response;
  }

</script>



<div >
    <Select bind:value={selectedDatatypes} on:change={filterData} size="md" placeholder="Wybierz typ danych">
        <option value="">Wszystkie typy danych</option>
        {#each datatypes as datatype}
          <option value={datatype}>{datatype}</option>
        {/each}
    </Select>

    <ul class="mt-4">
        {#each filteredProperties as { link, id, label }}
          <li><a class="font-bold" href={link}>{id}</a> {label}</li>
        {/each}
    </ul>

</div>

