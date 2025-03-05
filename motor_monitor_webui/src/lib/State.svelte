<script lang="ts">
    import { onMount } from "svelte";
    import Chart from "./Chart.svelte";
    import {
        motorStateStore,
        latestMotorStateStore,
        motorPositionStore,
        latestMotorPositionStore,
        motorVelocityStore,
        latestMotorVelocityStore,
        motorCurrentStore,
        latestMotorCurrentStore,
    } from "../store/share";
    import type { MotorStateRecord } from "../lib/model";

    let startTime = Date.now();

    let positionLabels: string[] = $state([]);
    let positionDatasets: any[] = $state([]);

    let velocityLabels: string[] = [];
    let velocityDatasets: any[] = [];

    let currentLabels: string[] = [];
    let currentDatasets: any[] = [];

    function updatePositionChart(state: Record<number, MotorStateRecord>) {
        const currentTime = (Date.now() - startTime) / 1000; // time in seconds
        positionLabels.push(currentTime.toString());
        for (const [id, motor] of Object.entries(state)) {
            let dataset = positionDatasets.find(
                (d) => d.label === `Motor ${id}`,
            );
            if (!dataset) {
                dataset = {
                    label: `Motor ${id}`,
                    data: [],
                    borderColor: getRandomColor(),
                    fill: false,
                };
                positionDatasets.push(dataset);
            }
            dataset.data.push(motor.position);
        }
    }

    function updateVelocityChart(state: Record<number, MotorStateRecord>) {
        const currentTime = (Date.now() - startTime) / 1000; // time in seconds
        velocityLabels.push(currentTime.toString());
        for (const [id, motor] of Object.entries(state)) {
            let dataset = velocityDatasets.find(
                (d) => d.label === `Motor ${id}`,
            );
            if (!dataset) {
                dataset = {
                    label: `Motor ${id}`,
                    data: [],
                    borderColor: getRandomColor(),
                    fill: false,
                };
                velocityDatasets.push(dataset);
            }
            dataset.data.push(motor.velocity);
        }
    }

    function updateCurrentChart(state: Record<number, MotorStateRecord>) {
        const currentTime = (Date.now() - startTime) / 1000; // time in seconds
        currentLabels.push(currentTime.toString());
        for (const [id, motor] of Object.entries(state)) {
            let dataset = currentDatasets.find(
                (d) => d.label === `Motor ${id}`,
            );
            if (!dataset) {
                dataset = {
                    label: `Motor ${id}`,
                    data: [],
                    borderColor: getRandomColor(),
                    fill: false,
                };
                currentDatasets.push(dataset);
            }
            dataset.data.push(motor.current);
        }
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

    <!-- <Chart chartId="position-chart" {labels} {datasets} /> -->
    <!-- <Chart chartId="velocity-chart" {labels} {datasets} /> -->
    <!-- <Chart chartId="current-chart" {labels} {datasets} /> -->
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
