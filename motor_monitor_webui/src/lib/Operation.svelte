<script lang="ts">
    // assets
    import { limits } from "../assets/config.json";
    // store
    import { motorMonitorAPI } from "../store/share";
    import { notify } from "../store/notify";
    import { FontAwesomeIcon } from "fontawesome-svelte";

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
            $notify.success("Automation started");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    async function disableMotor() {
        try {
            await $motorMonitorAPI.disableMotor();
            $notify.success("Motor disabled");
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
        <button onclick={startPlatform}>
            <FontAwesomeIcon icon={["fas", "play"]}></FontAwesomeIcon>
            <span>Start Platform</span>
        </button>
        <button onclick={zeroPlatform}>
            <FontAwesomeIcon icon={["fas", "0"]}></FontAwesomeIcon>
            <span>Zero Platform</span>
        </button>
        <button onclick={centerPlatform}>
            <FontAwesomeIcon icon={["fas", "down-left-and-up-right-to-center"]}
            ></FontAwesomeIcon>
            <span>Center Platform</span>
        </button>
        <button onclick={stopPlatform}>
            <FontAwesomeIcon icon={["fas", "stop"]}></FontAwesomeIcon>
            <span>Stop Platform</span>
        </button>
        <button onclick={automaticPositioning}>
            <FontAwesomeIcon icon={["fas", "gauge-high"]}></FontAwesomeIcon>
            <span>Automation</span>
        </button>
        <button onclick={disableMotor}>
            <FontAwesomeIcon icon={["fas", "ban"]}></FontAwesomeIcon>
            <span>Disable Motor</span>
        </button>
        <button onclick={clearStateMachineError}>
            <FontAwesomeIcon icon={["fas", "rotate-right"]}></FontAwesomeIcon>
            <span>Clear Error</span>
        </button>
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

                <button onclick={() => removeMotor(index)}>
                    <FontAwesomeIcon icon={["fas", "trash-can"]}
                    ></FontAwesomeIcon>
                    <span>Remove</span>
                </button>
            </div>
        {/each}
        <div class="input-box-bottom">
            <button onclick={addMotor}>
                <FontAwesomeIcon icon={["fas", "plus"]}></FontAwesomeIcon>
                <span>Add Motor</span>
            </button>
            <button onclick={setPosition}>
                <FontAwesomeIcon icon={["fas", "crosshairs"]}></FontAwesomeIcon>
                <span>Set Positions</span>
            </button>
        </div>
    </div>
</div>

<style>
    .operation-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    .operation-container button {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .button-box {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        padding: 10px;
    }

    .button-box button {
        width: 190px;
    }

    .input-box {
        display: flex;
        flex-direction: column;
        gap: 10px;
        border-top: 1px solid #ccc;
        padding: 10px;
    }

    .input-group button {
        width: 130px;
    }

    .input-group {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    .input-box-bottom {
        display: flex;
        justify-content: center;
        gap: 30px;
    }

    .input-box-bottom button {
        width: 190px;
    }
</style>
