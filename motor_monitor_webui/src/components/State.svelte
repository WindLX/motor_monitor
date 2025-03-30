<script lang="ts">
  // svelte
  import { onMount } from "svelte";

  // lib
  import Chart from "./Chart.svelte";

  // instance
  import { messageManager } from "../store/instance";

  // assets
  import { chart as chartConfig } from "../assets/config.json";
  import {
    MotorMessageTypeEnum,
    type QS_M_STATE_Payload,
  } from "../lib/model/base";

  let startTime = Date.now();

  let positionLabels: number[] = [];
  let positionDatasets: any[] = [];

  let velocityLabels: number[] = [];
  let velocityDatasets: any[] = [];

  let torqueLabels: number[] = [];
  let torqueDatasets: any[] = [];

  let currentMotorState: QS_M_STATE_Payload = $state([]);

  var unsub: () => void;

  onMount(() => {
    unsub = $messageManager.subscribeOnMessageAdded((message) => {
      if (
        message.raw_message.message_type === MotorMessageTypeEnum.QS_M_STATE
      ) {
        const newState = message.raw_message.payload as QS_M_STATE_Payload;
        positionDatasets = updateChart(
          newState,
          positionLabels,
          positionDatasets,
          "position"
        );
        velocityDatasets = updateChart(
          newState,
          velocityLabels,
          velocityDatasets,
          "velocity"
        );
        torqueDatasets = updateChart(
          newState,
          torqueLabels,
          torqueDatasets,
          "torque"
        );
      }
    });
  });

  function updateChart(
    state: any,
    labels: number[],
    datasets: any[],
    key: string
  ) {
    const time = (Date.now() - startTime) / 1000;

    labels.push(time);

    const updatedDatasets: any[] = [];
    // const updatedDatasets = datasets.map((dataset) => {
    //   const motorId = parseInt(dataset.label.split(" ")[1]);
    //   const motor = state[motorId];

    //   return motor
    //     ? {
    //         ...dataset,
    //         data: [...dataset.data, motor[key]],
    //       }
    //     : dataset;
    // });

    // Object.entries(state).forEach(([id, motor]) => {
    //   if (!updatedDatasets.some((d) => d.label === `Motor ${id}`)) {
    //     updatedDatasets.push({
    //       label: `Motor ${id}`,
    //       data: [motor[key]],
    //       borderColor: getRandomColor(),
    //       fill: false,
    //     });
    //   }
    // });

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
        <th>{chartConfig.yUnits.position}</th>
        <th>{chartConfig.yUnits.velocity}</th>
        <th>{chartConfig.yUnits.torque}</th>
      </tr>
    </thead>
    <tbody>
      {#if currentMotorState.length > 0}
        {#each Object.entries(currentMotorState) as [id, motor] (id)}
          <tr>
            <td>{id}</td>
            <td>{motor.position}</td>
            <td>{motor.velocity}</td>
            <td>{motor.torque}</td>
          </tr>
        {/each}
      {:else}
        <tr>
          <td colspan="4">No data available</td>
        </tr>
      {/if}
    </tbody>
  </table>

  <!-- <Chart
    chartTitle="Position"
    labels={positionLabels}
    datasets={positionDatasets}
    yUnit={chartConfig.yUnits.position}
  />
  <Chart
    chartTitle="Velocity"
    labels={velocityLabels}
    datasets={velocityDatasets}
    yUnit={chartConfig.yUnits.velocity}
  />
  <Chart
    chartTitle="Torque"
    labels={torqueLabels}
    datasets={torqueDatasets}
    yUnit={chartConfig.yUnits.torque}
  /> -->
</div>

<style>
  .state-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 20px;
    width: 98%;
    gap: 10px;
    padding: 10px;
    border-radius: 8px;
    background-color: var(--main-white-color-0);
    box-shadow: 0 0 8px 0 var(--main-white-color-3);
  }

  .state-container table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    overflow: hidden;
  }

  .state-container th,
  .state-container td {
    padding: 12px 15px;
    text-align: center;
    border-bottom: 1px solid var(--main-white-color-2);
    transition: background 0.2s ease;
  }

  .state-container th {
    background: var(--primary-color-light);
    /* color: #2c3e50; */
    font-weight: 600;
    font-size: 0.95em;
    letter-spacing: 0.5px;
    border-top: 1px solid var(--main-white-color-2);
  }

  .state-container tr:first-child th:first-child {
    border-top-left-radius: 8px;
  }

  .state-container tr:first-child th:last-child {
    border-top-right-radius: 8px;
  }

  .state-container tr:not(:last-child) td {
    border-bottom: 1px solid #f0f2f5;
  }

  .state-container tbody tr:hover td {
    background: var(--primary-color-light);
    cursor: pointer;
  }

  .state-container td[colspan="4"] {
    padding: 16px;
    color: #909399;
    font-style: italic;
    background: #fafbfc;
  }

  .state-container th:first-child,
  .state-container td:first-child {
    width: 80px;
  }
</style>
