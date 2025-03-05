<script lang="ts">
    // svelte
    import { onMount } from "svelte";
    // store
    import { motorMonitorAPI } from "../store/share";
    import { notify } from "../store/notify";
    import { connected } from "../store/share";

    let downstreamHost = "";
    let downstreamPort = 0;

    onMount(async () => {
        try {
            const downstream = await $motorMonitorAPI!.getDownstream();
            downstreamHost = downstream.downstream.host;
            downstreamPort = downstream.downstream.port;
            connected.set(true);
            $notify.info("Downstream fetched");
        } catch (error) {
            connected.set(false);
            $notify.error((error as any).message);
        }
    });
</script>

<div class="state-container">
    <div class="status-dot" class:is-connected={connected}></div>
    {#if connected}
        <span>IP Address: {downstreamHost}</span>
        <span>Port: {downstreamPort}</span>
    {/if}
    {#if !connected}
        <span>Downstream not connected</span>
    {/if}
</div>

<style>
    .state-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        padding: 10px;
        width: 800px;
    }

    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: red;
    }

    .status-dot.is-connected {
        background-color: green;
    }
</style>
