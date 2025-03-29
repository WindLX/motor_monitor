<script lang="ts">
    import { FontAwesomeIcon } from "fontawesome-svelte";
</script>

<div class="sidebar">
    <button class="sidebar-button">
        <FontAwesomeIcon icon={["fas", "terminal"]}></FontAwesomeIcon>
        <span>Operation</span>
    </button>
    <button class="sidebar-button">
        <FontAwesomeIcon icon={["fas", "chart-simple"]}></FontAwesomeIcon>
        <span>Monitor</span>
    </button>
</div>

<style>
    .sidebar {
        display: flex;
        flex-direction: column;
        gap: 5px;
        padding: 5px;
    }

    .sidebar-button {
        width: 100%;
        border: none;
    }

    .sidebar-button:hover {
    }
</style>
