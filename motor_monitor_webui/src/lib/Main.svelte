<script lang="ts">
    import MotorMonitorAPI from "./api";
    import { onMount } from "svelte";
    import Notify from "./Notify.svelte";
    import { base_url, ip, port } from "../assets/config.json";
    import { writable } from "svelte/store";

    let motorMonitorAPI: MotorMonitorAPI;
    let baseUrl: string = base_url;

    let notify: Notify;

    let motors = writable<{ motorId: number; position: number }[]>([
        { motorId: 0, position: 0 },
    ]);

    onMount(() => {
        motorMonitorAPI = new MotorMonitorAPI(baseUrl, ip, port);
    });

    async function startMotor() {
        try {
            await motorMonitorAPI.startMotor();
            notify.notify("Motor started", "info");
        } catch (error) {
            notify.notify((error as any).message, "error");
        }
    }

    async function stopMotor() {
        try {
            await motorMonitorAPI.stopMotor();
            notify.notify("Motor stopped", "info");
        } catch (error) {
            notify.notify((error as any).message, "error");
        }
    }

    async function pauseMotor() {
        try {
            await motorMonitorAPI.pauseMotor();
            notify.notify("Motor paused", "info");
        } catch (error) {
            notify.notify((error as any).message, "error");
        }
    }

    async function resumeMotor() {
        try {
            await motorMonitorAPI.resumeMotor();
            notify.notify("Motor resumed", "info");
        } catch (error) {
            notify.notify((error as any).message, "error");
        }
    }

    async function setPosition() {
        try {
            const motorPositions = $motors.map((motor) => ({
                motor_id: motor.motorId,
                position: motor.position,
            }));
            await motorMonitorAPI.setPosition(motorPositions);
            notify.notify("Positions set", "info");
        } catch (error) {
            notify.notify((error as any).message, "error");
        }
    }

    function addMotor() {
        console.log("Adding motor");
        motors.update((currentMotors) => [
            ...currentMotors,
            { motorId: currentMotors.length + 1, position: 0 },
        ]);
    }

    function removeMotor(index: number) {
        motors.update((currentMotors) => {
            currentMotors.splice(index, 1);
            return currentMotors;
        });
    }
</script>

<div class="container">
    <div class="addr-box">
        <label for="ip">IP Address:</label>
        {#if motorMonitorAPI}
            <input type="text" id="ip" bind:value={motorMonitorAPI.ip} />
            <label for="port">Port:</label>
            <input type="number" id="port" bind:value={motorMonitorAPI.port} />
        {/if}
    </div>

    <div class="button-box">
        <button on:click={startMotor}>Start Motor</button>
        <button on:click={stopMotor}>Stop Motor</button>
        <button on:click={pauseMotor}>Pause Motor</button>
        <button on:click={resumeMotor}>Resume Motor</button>
    </div>

    <div class="input-box">
        {#each $motors as motor, index}
            <div class="input-group">
                <span class="motor-id">{index}</span>
                <label for="motorId-{index}">Motor ID:</label>
                <input
                    type="number"
                    id="motorId-{index}"
                    bind:value={motor.motorId}
                />

                <label for="position-{index}">Position:</label>
                <input
                    type="range"
                    id="position-{index}"
                    min="0"
                    max="100"
                    bind:value={motor.position}
                />
                <span class="position">{motor.position}</span>

                <button on:click={() => removeMotor(index)}>Remove</button>
            </div>
        {/each}
        <button on:click={setPosition}>Set Positions</button>
        <button on:click={addMotor}>Add Motor</button>
    </div>

    <Notify bind:this={notify} />
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }

    .button-box {
        display: flex;
        gap: 10px;
    }

    .input-box {
        display: flex;
        flex-direction: column;
        gap: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
    }

    .input-group {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .position {
        width: 30px;
        display: inline-block;
        text-align: center;
    }
</style>
