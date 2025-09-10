<script lang="ts">  
    import InstancePage from "$lib/InstancePage.svelte";

    let { data } = $props();
    let instanceName = data.instance.name;
    let wikiURL = data.instance.url;
    let sparqlEndpoint = data.instance.sparql;
    let apiAddress = data.instance.api;
</script>


<div>
  <InstancePage instanceName={instanceName} wikiURL={wikiURL} sparqlEndpoint={sparqlEndpoint} apiEndpoint={apiAddress}></InstancePage>
</div>



