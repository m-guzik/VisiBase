<script lang="ts">  
    import InstancePage from "$lib/InstancePage.svelte";

    let { data } = $props();
    let instanceName = $state(data.name);
    let sparqlEndpoint = $state(data.endpoint);
    let wikiURL = $state(data.url);
    let apiAddress = $state(data.api);
</script>


<div>
  <InstancePage instanceName={instanceName} wikiURL={wikiURL} sparqlEndpoint={sparqlEndpoint} apiEndpoint={apiAddress}></InstancePage>
</div>

