<script lang="ts">
    import { onMount } from "svelte";
    import { FontAwesomeIcon } from "fontawesome-svelte";
    import { motorMonitorAPI, resetAPI } from "../store/share";
    import { notify } from "../store/notify";
    import {
        apiConnected,
        wsConnected,
        downstreamConnected,
    } from "../store/share";

    let baseUrl = "";
    let wsUrl = "";

    let downstreamHost = "";
    let downstreamPort = 0;

    async function resetConnection() {
        $notify.info("Resetting connection...");
        resetAPI();
        await refreshState();
    }

    async function refreshState() {
        apiConnected.set(false);
        wsConnected.set(false);
        downstreamConnected.set(false);

        if ($motorMonitorAPI) {
            try {
                const response = await $motorMonitorAPI.readRoot();
                baseUrl = response;
                apiConnected.set(true);
                $notify.info("API connected");

                if ($motorMonitorAPI.wsReady) {
                    wsUrl = $motorMonitorAPI.wsUrl;
                    wsConnected.set(true);
                    $notify.info("WebSocket connected");
                } else {
                    wsConnected.set(false);
                    $notify.error("WebSocket not connected");
                }

                try {
                    const downstream = await $motorMonitorAPI.getDownstream();
                    downstreamHost = downstream.downstream.host;
                    downstreamPort = downstream.downstream.port;
                    downstreamConnected.set(true);
                    $notify.info("Downstream connected");
                } catch (error) {
                    downstreamConnected.set(false);
                    $notify.error((error as any).message);
                }
            } catch (error) {
                apiConnected.set(false);
                $notify.error((error as any).message);
            }
        } else {
            apiConnected.set(false);
            $notify.error("API not connected");
        }
    }

    onMount(async () => {
        await refreshState();
    });
</script>

<div class="state-container">
    <div class="state-box">
        <div class="status-dot" class:is-connected={$apiConnected}></div>
        <span>API</span>
        {#if $apiConnected}
            <span>{baseUrl}</span>
        {/if}
        <span>|</span>
        <div class="status-dot" class:is-connected={$wsConnected}></div>
        <span>WebSocket</span>
        {#if $wsConnected}
            <span>{wsUrl}</span>
        {/if}
        <span>|</span>
        <div class="status-dot" class:is-connected={$downstreamConnected}></div>
        <span>Downstream</span>
        {#if $downstreamConnected}
            <span>{downstreamHost}:{downstreamPort}</span>
        {/if}
    </div>

    <button onclick={resetConnection}>
        <FontAwesomeIcon icon={["fas", "rotate-right"]}></FontAwesomeIcon>
    </button>
</div>

<style>
    .state-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        padding: 10px;
        padding-top: 0;
        padding-bottom: 0;
        border-radius: 8px;
        background-color: var(--main-white-color-0);
        box-shadow: 0 0 8px 0 var(--main-white-color-3);
    }

    .state-box {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px;
        width: 800px;
    }

    .state-container span {
        font-size: 14px;
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

    .state-container button {
        width: fit-content;
        font-size: 12px;
        width: 30px;
        justify-content: center;
    }
</style>
