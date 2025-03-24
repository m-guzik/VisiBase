<script lang="ts">
	import '../app.css';
	import '../global.css';
	import Footer from '$lib/Footer.svelte';
    import Header from '$lib/Header.svelte';
	let { children } = $props();
</script>



<Header/>

{@render children()}

<footer>
	<Footer />
</footer>

