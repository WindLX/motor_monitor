<script lang="ts">
    // components
    import Status from "./Status.svelte";
    import State from "./State.svelte";
    import Operation from "./Operation.svelte";
    import Notify from "./Notify.svelte";
</script>

<div class="container">
    <Notify />

    <Status />
    <Operation />
    <State />
</div>

<style>
    .container {
        display: flex;
        align-items: center;
        flex-direction: column;
        gap: 10px;
    }
</style>
