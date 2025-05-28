<script lang="ts">  

    interface ClassItem { 
        "link" : string,
        "id" : string,
        "number" : number,
        "label" : string }

    interface ConnectedClasses {
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
        'connections': ConnectedClasses[]
    }


    let { data, connected, onSelect } = $props();

    let allClasses: ClassItem[] = $state(data);
    let connectedClasses: ConnectingProperty[] = $state(connected);


</script>



<div >
    <ul class="mt-4">
        {#each allClasses as { link, id, label }}
          <li class="text-lg"><a class="font-bold" href={link}>{id}</a><button onclick={() => onSelect(id)}>{label}</button></li>
        {/each}
    </ul>
</div>