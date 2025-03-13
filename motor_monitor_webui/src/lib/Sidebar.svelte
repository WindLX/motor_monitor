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
    }

    .sidebar-button {
        display: flex;
        align-items: center;
        padding: 10px;
        border: none;
        background: none;
        cursor: pointer;
        font-size: 16px;
    }

    .sidebar-button:hover {
        background-color: #f0f0f0;
    }
</style>
