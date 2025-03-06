<script lang="ts">
    // svelte
    import { onMount } from "svelte";

    // lib
    import Chart from "./Chart.svelte";
    import type { MotorStateRecord } from "../lib/model";

    // store
    import { latestMotorStateStore } from "../store/share";

    let startTime = Date.now();

    let positionLabels: number[] = [];
    let positionDatasets: any[] = [];

    let velocityLabels: number[] = [];
    let velocityDatasets: any[] = [];

    let currentLabels: number[] = [];
    let currentDatasets: any[] = [];

    onMount(() => {
        latestMotorStateStore.subscribe((state) => {
            if (state === null) return;
            positionDatasets = updateChart(
                state,
                positionLabels,
                positionDatasets,
                "position",
            );
            velocityDatasets = updateChart(
                state,
                velocityLabels,
                velocityDatasets,
                "velocity",
            );
            currentDatasets = updateChart(
                state,
                currentLabels,
                currentDatasets,
                "current",
            );
        });
    });

    function updateChart(
        state: Record<number, MotorStateRecord>,
        labels: number[],
        datasets: any[],
        key: keyof MotorStateRecord,
    ) {
        const currentTime = (Date.now() - startTime) / 1000;

        labels.push(currentTime);

        const updatedDatasets = datasets.map((dataset) => {
            const motorId = parseInt(dataset.label.split(" ")[1]);
            const motor = state[motorId];

            return motor
                ? {
                      ...dataset,
                      data: [...dataset.data, motor[key]],
                  }
                : dataset;
        });

        Object.entries(state).forEach(([id, motor]) => {
            if (!updatedDatasets.some((d) => d.label === `Motor ${id}`)) {
                updatedDatasets.push({
                    label: `Motor ${id}`,
                    data: [motor[key]],
                    borderColor: getRandomColor(),
                    fill: false,
                });
            }
        });

        return updatedDatasets;
    }

    function getRandomColor() {
        const letters = "0123456789ABCDEF";
        let color = "#";
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
</script>

<div class="state-container">
    <table>
        <thead>
            <tr>
                <th>Motor ID</th>
                <th>Position</th>
                <th>Velocity</th>
                <th>Current</th>
            </tr>
        </thead>
        <tbody>
            {#if $latestMotorStateStore !== null}
                {#each Object.entries($latestMotorStateStore) as [id, motor] (id)}
                    <tr>
                        <td>{id}</td>
                        <td>{motor.position}</td>
                        <td>{motor.velocity}</td>
                        <td>{motor.current}</td>
                    </tr>
                {/each}
            {:else}
                <tr>
                    <td colspan="4">No data available</td>
                </tr>
            {/if}
        </tbody>
    </table>

    <Chart
        chartTitle="position"
        labels={positionLabels}
        datasets={positionDatasets}
    />
    <Chart
        chartTitle="velocity"
        labels={velocityLabels}
        datasets={velocityDatasets}
    />
    <Chart
        chartTitle="current"
        labels={currentLabels}
        datasets={currentDatasets}
    />
</div>

<style>
    .state-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
    }

    .state-container table {
        width: 100%;
        border-collapse: collapse;
    }

    .state-container th,
    .state-container td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
    }

    .state-container th {
        background-color: #f2f2f2;
    }
</style>
