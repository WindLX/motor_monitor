<script lang="ts">
    import { FontAwesomeIcon } from "fontawesome-svelte";
</script>

<div class="sidebar">
    <FontAwesomeIcon icon={["fas", "terminal"]}></FontAwesomeIcon>
    <FontAwesomeIcon icon={["fas", "chart-simple"]}></FontAwesomeIcon>
</div>

<style>
    .sidebar {
        display: flex;
        flex-direction: column;
    }
</style>
