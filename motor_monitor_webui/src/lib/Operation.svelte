<script lang="ts">
    // assets
    import { limits } from "../assets/config.json";
    // store
    import { motorMonitorAPI } from "../store/share";
    import { notify } from "../store/notify";

    let motors = $state([{ motorId: 0, position: 0 }]);

    async function startMotor() {
        try {
            await $motorMonitorAPI.startMotor();
            $notify.success("Motor started");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    async function stopMotor() {
        try {
            await $motorMonitorAPI.stopMotor();
            $notify.success("Motor stopped");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    async function pauseMotor() {
        try {
            await $motorMonitorAPI.pauseMotor();
            $notify.success("Motor paused");
        } catch (error) {
            $notify.error((error as any).message);
        }
    }

    async function resumeMotor() {
        try {
            await $motorMonitorAPI.resumeMotor();
            $notify.success("Motor resumed");
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
            if (motors.length > limits.MOTOR_LENGTH_MAX) {
                $notify.warning(
                    `Cannot set more than ${limits.MOTOR_LENGTH_MAX} motors`,
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
        if (motors.length > limits.MOTOR_LENGTH_MAX - 1) {
            $notify.warning(
                `Cannot add more than ${limits.MOTOR_LENGTH_MAX} motors`,
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
                if (motor.motorId < limits.MOTOR_ID_MIN) {
                    motor.motorId = limits.MOTOR_ID_MIN;
                } else if (motor.motorId > limits.MOTOR_ID_MAX) {
                    motor.motorId = limits.MOTOR_ID_MAX;
                }
            }
            return motor;
        });
    }

    function validateMotorPosition(index: number) {
        motors = motors.map((motor, i) => {
            if (i === index) {
                if (motor.position < limits.MOTOR_POSITION_MIN) {
                    motor.position = limits.MOTOR_POSITION_MIN;
                } else if (motor.position > limits.MOTOR_POSITION_MAX) {
                    motor.position = limits.MOTOR_POSITION_MAX;
                }
            }
            return motor;
        });
    }
</script>

<div class="operation-container">
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
                    min={limits.MOTOR_ID_MIN}
                    max={limits.MOTOR_ID_MAX}
                    bind:value={motor.motorId}
                    oninput={() => validateMotorId(index)}
                />

                <label for="position-{index}">Position:</label>
                <input
                    type="range"
                    id="position-{index}"
                    min={limits.MOTOR_POSITION_MIN}
                    max={limits.MOTOR_POSITION_MAX}
                    bind:value={motor.position}
                    oninput={() => validateMotorPosition(index)}
                />
                <input
                    class="position"
                    type="number"
                    min={limits.MOTOR_POSITION_MIN}
                    max={limits.MOTOR_POSITION_MAX}
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
