<script lang="ts">
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import Notify from "./Notify.svelte";
    import { base_url } from "../assets/config.json";
    import MotorMonitorAPI from "./api";

    const MOTOR_ID_MIN = 0;
    const MOTOR_ID_MAX = 255;
    const MOTOR_POSITION_MIN = 0;
    const MOTOR_POSITION_MAX = 100000;

    let motorMonitorAPI: MotorMonitorAPI;
    let baseUrl: string = base_url;
    let notify: Notify;

    let motors = $state([{ motorId: 0, position: 0 }]);

    let downstreamHost = $state("");
    let downstreamPort = $state(0);

    onMount(async () => {
        motorMonitorAPI = new MotorMonitorAPI(baseUrl);
        try {
            const downstream = await motorMonitorAPI.getDownstream();
            downstreamHost = downstream.downstream.host;
            downstreamPort = downstream.downstream.port;
        } catch (error) {
            notify.notify((error as any).message, "error");
        }
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
            const motorIds = motors.map((motor) => motor.motorId);
            const uniqueMotorIds = new Set(motorIds);
            if (uniqueMotorIds.size !== motorIds.length) {
                notify.notify("Motor IDs must be unique", "error");
                return;
            }
            if (motors.length > 16) {
                notify.notify("Cannot set more than 16 motors", "warning");
                return;
            }
            const motorPositions = motors.map((motor) => ({
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
        if (motors.length > 15) {
            notify.notify("Cannot add more than 16 motors", "warning");
            return;
        }
        motors.push({ motorId: 0, position: 0 });
    }

    function removeMotor(index: number) {
        if (motors.length === 1) {
            notify.notify("Cannot remove last motor", "warning");
            return;
        }
        motors = motors.filter((_, i) => i !== index);
    }

    function validateMotorId(index: number) {
        motors = motors.map((motor, i) => {
            if (i === index) {
                if (motor.motorId < MOTOR_ID_MIN) {
                    motor.motorId = MOTOR_ID_MIN;
                } else if (motor.motorId > MOTOR_ID_MAX) {
                    motor.motorId = MOTOR_ID_MAX;
                }
            }
            return motor;
        });
    }

    function validateMotorPosition(index: number) {
        motors = motors.map((motor, i) => {
            if (i === index) {
                if (motor.position < MOTOR_POSITION_MIN) {
                    motor.position = MOTOR_POSITION_MIN;
                } else if (motor.position > MOTOR_POSITION_MAX) {
                    motor.position = MOTOR_POSITION_MAX;
                }
            }
            return motor;
        });
    }
</script>

<div class="container">
    <div class="addr-box">
        {#if downstreamHost}
            <span>IP Address: {downstreamHost}</span>
        {/if}
        {#if downstreamPort}
            <span>Port: {downstreamPort}</span>
        {/if}
    </div>

    <div class="button-box">
        <button onclick={startMotor}>Start Motor</button>
        <button onclick={stopMotor}>Stop Motor</button>
        <button onclick={pauseMotor}>Pause Motor</button>
        <button onclick={resumeMotor}>Resume Motor</button>
    </div>

    <div class="input-box">
        {#each motors as motor, index}
            <div class="input-group">
                <span class="motor-id">{index}</span>
                <label for="motorId-{index}">Motor ID:</label>
                <input
                    type="number"
                    id="motorId-{index}"
                    min={MOTOR_ID_MIN}
                    max={MOTOR_ID_MAX}
                    bind:value={motor.motorId}
                    oninput={() => validateMotorId(index)}
                />

                <label for="position-{index}">Position:</label>
                <input
                    type="range"
                    id="position-{index}"
                    min={MOTOR_POSITION_MIN}
                    max={MOTOR_POSITION_MAX}
                    bind:value={motor.position}
                    oninput={() => validateMotorPosition(index)}
                />
                <input
                    class="position"
                    type="number"
                    min={MOTOR_POSITION_MIN}
                    max={MOTOR_POSITION_MAX}
                    bind:value={motor.position}
                    oninput={() => validateMotorPosition(index)}
                />

                <button onclick={() => removeMotor(index)}>Remove</button>
            </div>
        {/each}
        <button onclick={setPosition}>Set Positions</button>
        <button onclick={addMotor}>Add Motor</button>
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
