<script lang="ts">
    import { Footer, FooterCopyright, FooterIcon } from 'flowbite-svelte';
    import { GithubSolid } from 'flowbite-svelte-icons';
</script>
<!-- dark:bg-gradient-to-t from-secondary-dark to-primary-dark -->

<Footer footerType="socialmedia" class="bg-gradient-to-b from-lighter-light to-darker-light dark:bg-gradient-to-b dark:from-lighter-dark dark:to-darker-dark">
    <div class="sm:flex sm:items-center sm:justify-between">
        <p  class="font-medium text-lighter-dark dark:text-darker-light"> &copy {new Date().getFullYear()} Maria Guzik-Jureczka </p>
        <!-- <FooterCopyright by="Maria Guzik-Jureczka"/> -->
        <FooterIcon href="https://github.com/m-guzik/VisiBase">
            <GithubSolid class="text-lighter-dark dark:text-darker-light hover:text-accent w-10 h-10" />
        </FooterIcon>
    </div>
  </Footer>


