<script lang="ts">
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import Notify from "./Notify.svelte";
    import { base_url, ip, port } from "../assets/config.json";
    import MotorMonitorAPI from "./api";

    const PORT_MIN = 0;
    const PORT_MAX = 65535;
    const MOTOR_ID_MIN = 0;
    const MOTOR_ID_MAX = 255;
    const MOTOR_POSITION_MIN = 0;
    const MOTOR_POSITION_MAX = 100000;

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

    function validatePort() {
        if (motorMonitorAPI.port < PORT_MIN) {
            motorMonitorAPI.port = PORT_MIN;
        } else if (motorMonitorAPI.port > PORT_MAX) {
            motorMonitorAPI.port = PORT_MAX;
        }
    }

    function validateMotorId(index: number) {
        motors.update((currentMotors) => {
            if (currentMotors[index].motorId < MOTOR_ID_MIN) {
                currentMotors[index].motorId = MOTOR_ID_MIN;
            } else if (currentMotors[index].motorId > MOTOR_ID_MAX) {
                currentMotors[index].motorId = MOTOR_ID_MAX;
            }
            return currentMotors;
        });
    }

    function validateMotorPosition(index: number) {
        motors.update((currentMotors) => {
            if (currentMotors[index].position < MOTOR_POSITION_MIN) {
                currentMotors[index].position = MOTOR_POSITION_MIN;
            } else if (currentMotors[index].position > MOTOR_POSITION_MAX) {
                currentMotors[index].position = MOTOR_POSITION_MAX;
            }
            return currentMotors;
        });
    }
</script>

<div class="container">
    <div class="addr-box">
        <label for="ip">IP Address: </label>
        {#if motorMonitorAPI}
            <input type="text" id="ip" bind:value={motorMonitorAPI.ip} />
            <label for="port">Port:</label>
            <input
                type="number"
                id="port"
                min={PORT_MIN}
                max={PORT_MAX}
                bind:value={motorMonitorAPI.port}
                on:input={validatePort}
            />
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
                    min={MOTOR_ID_MIN}
                    max={MOTOR_ID_MAX}
                    bind:value={motor.motorId}
                    on:input={() => validateMotorId(index)}
                />

                <label for="position-{index}">Position:</label>
                <input
                    type="range"
                    id="position-{index}"
                    min={MOTOR_POSITION_MIN}
                    max={MOTOR_POSITION_MAX}
                    bind:value={motor.position}
                    on:input={() => validateMotorPosition(index)}
                />
                <input
                    class="position"
                    type="number"
                    min={MOTOR_POSITION_MIN}
                    max={MOTOR_POSITION_MAX}
                    bind:value={motor.position}
                    on:input={() => validateMotorPosition(index)}
                />

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
        align-items: center;
        flex-direction: column;
        gap: 10px;
    }

    .addr-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        padding: 10px;
        width: 800px;
    }

    .button-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        padding: 10px;
        width: 800px;
    }

    .input-box {
        display: flex;
        flex-direction: column;
        gap: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        width: 800px;
    }

    .input-group {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
</style>
