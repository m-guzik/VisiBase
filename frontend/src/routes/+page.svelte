<script>
// @ts-nocheck


  let apiData = [];

    async function fetchData() {
    const res = await fetch("http://127.0.0.1:8000/");
    apiData = await res.json();
    }

  fetchData();
</script>


<h1>{apiData.message}</h1>
<p>VisiBase - Visualiser for your Wikibase </p>

