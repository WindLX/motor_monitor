<script lang="ts">
    // assets
    import { limits } from "../assets/config.json";
    // store
    import { motorMonitorAPI } from "../store/share";
    import { notify } from "../store/notify";

    let motors = $state([{ motorId: 0, position: 0 }]);

    async function startPlatform() {
        try {
            await $motorMonitorAPI.startPlatform();
            $notify.success("Platform started");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    async function zeroPlatform() {
        try {
            await $motorMonitorAPI.zeroPlatform();
            $notify.success("Platform zeroed");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    async function centerPlatform() {
        try {
            await $motorMonitorAPI.centerPlatform();
            $notify.success("Platform centered");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    async function stopPlatform() {
        try {
            await $motorMonitorAPI.stopPlatform();
            $notify.success("Platform stopped");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    async function automaticPositioning() {
        try {
            await $motorMonitorAPI.automaticPositioning();
            $notify.success("Automatic positioning started");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    async function disablePlatform() {
        try {
            await $motorMonitorAPI.disablePlatform();
            $notify.success("Platform disabled");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    async function clearStateMachineError() {
        try {
            await $motorMonitorAPI.clearStateMachineError();
            $notify.success("State machine error cleared");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    async function setPosition() {
        try {
            const motorIds = motors.map((motor) => motor.motorId);
            const uniqueMotorIds = new Set(motorIds);
            if (uniqueMotorIds.size !== motorIds.length) {
                $notify.warning("Motor IDs must be unique");
                return;
            }
            if (motors.length > limits.motor_length_max) {
                $notify.warning(
                    `Cannot set more than ${limits.motor_length_max} motors`,
                );
                return;
            }
            const motorPositions = motors.map((motor) => ({
                motor_id: motor.motorId,
                position: motor.position,
            }));

            await $motorMonitorAPI.setPosition(motorPositions);
            $notify.success("Positions set");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    function addMotor() {
        if (motors.length > limits.motor_length_max - 1) {
            $notify.warning(
                `Cannot add more than ${limits.motor_length_max} motors`,
            );
            return;
        }
        motors.push({ motorId: 0, position: 0 });
    }

    function removeMotor(index: number) {
        if (motors.length === 1) {
            $notify.warning("Cannot remove last motor");
            return;
        }
        motors = motors.filter((_, i) => i !== index);
    }

    function validateMotorId(index: number) {
        motors = motors.map((motor, i) => {
            if (i === index) {
                if (motor.motorId < limits.motor_id_min) {
                    motor.motorId = limits.motor_id_min;
                } else if (motor.motorId > limits.motor_id_max) {
                    motor.motorId = limits.motor_id_max;
                }
            }
            return motor;
        });
    }

    function validateMotorPosition(index: number) {
        motors = motors.map((motor, i) => {
            if (i === index) {
                if (motor.position < limits.motor_position_min) {
                    motor.position = limits.motor_position_min;
                } else if (motor.position > limits.motor_position_max) {
                    motor.position = limits.motor_position_max;
                }
            }
            return motor;
        });
    }
</script>

<div class="operation-container">
    <div class="button-box">
        <button onclick={startPlatform}>Start Platform</button>
        <button onclick={zeroPlatform}>Zero Platform</button>
        <button onclick={centerPlatform}>Center Platform</button>
        <button onclick={stopPlatform}>Stop Platform</button>
        <button onclick={automaticPositioning}>Automatic Positioning</button>
        <button onclick={disablePlatform}>Disable Platform</button>
        <button onclick={clearStateMachineError}
            >Clear State Machine Error</button
        >
    </div>

    <div class="input-box">
        {#each motors as motor, index}
            <div class="input-group">
                <span class="motor-id">{index}</span>
                <label for="motorId-{index}">Motor ID:</label>
                <input
                    type="number"
                    id="motorId-{index}"
                    min={limits.motor_id_min}
                    max={limits.motor_id_max}
                    bind:value={motor.motorId}
                    oninput={() => validateMotorId(index)}
                />

                <label for="position-{index}">Position:</label>
                <input
                    type="range"
                    id="position-{index}"
                    min={limits.motor_position_min}
                    max={limits.motor_position_max}
                    bind:value={motor.position}
                    oninput={() => validateMotorPosition(index)}
                />
                <input
                    class="position"
                    type="number"
                    min={limits.motor_position_min}
                    max={limits.motor_position_max}
                    bind:value={motor.position}
                    oninput={() => validateMotorPosition(index)}
                />

                <button onclick={() => removeMotor(index)}>Remove</button>
            </div>
        {/each}
        <button onclick={setPosition}>Set Positions</button>
        <button onclick={addMotor}>Add Motor</button>
    </div>
</div>

<style>
    .operation-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
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
