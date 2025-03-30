<script lang="ts">
  // svelte
  import { onMount } from "svelte";
  import { FontAwesomeIcon } from "fontawesome-svelte";

  // instance
  import { messageManager } from "../store/instance";

  // assets
  import { chart as chartConfig } from "../assets/config.json";
  import {
    MotorMessageTypeEnum,
    type QS_M_STATE_Payload,
  } from "../lib/model/base";

  let currentMotorState: QS_M_STATE_Payload = $state([]);

  var unsub: () => void;

  onMount(() => {
    unsub = $messageManager.subscribeOnMessageAdded((message) => {
      if (
        message.raw_message.message_type === MotorMessageTypeEnum.QS_M_STATE
      ) {
        const newState = message.raw_message.payload as QS_M_STATE_Payload;
        currentMotorState = newState;
      }
    });
  });
</script>

<div class="current-state-container">
  <table>
    <thead>
      <tr>
        <th>
          <FontAwesomeIcon icon={["fas", "caret-right"]}></FontAwesomeIcon>
          <span>Motor ID</span></th
        >
        <th>
          <FontAwesomeIcon icon={["fas", "crosshairs"]}></FontAwesomeIcon>
          <span>{chartConfig.yUnits.position}</span></th
        >
        <th>
          <FontAwesomeIcon icon={["fas", "gauge-high"]}></FontAwesomeIcon>
          <span>{chartConfig.yUnits.velocity}</span></th
        >
        <th>
          <FontAwesomeIcon icon={["fas", "rotate-right"]}></FontAwesomeIcon>
          <span>{chartConfig.yUnits.torque}</span></th
        >
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
</div>

<style>
  .current-state-container {
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

  .current-state-container table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    overflow: hidden;
  }

  .current-state-container th {
    padding: 12px 15px;
    text-align: center;
    transition: background 0.2s ease;
  }

  .current-state-container td {
    padding: 12px 15px;
    text-align: center;
    border-bottom: 1px solid var(--main-white-color-2);
    transition: background 0.2s ease;
  }

  .current-state-container th {
    background: var(--primary-color-light);
    font-weight: 600;
    font-size: 0.95em;
    letter-spacing: 0.5px;
    border-top: 1px solid var(--main-white-color-2);
  }

  .current-state-container tr:first-child th:first-child {
    border-top-left-radius: 8px;
  }

  .current-state-container tr:first-child th:last-child {
    border-top-right-radius: 8px;
  }

  .current-state-container tr:not(:last-child) td {
    border-bottom: 1px solid #f0f2f5;
  }

  .current-state-container tbody tr:hover td {
    background: var(--primary-color-light);
    cursor: pointer;
  }

  .current-state-container td[colspan="4"] {
    padding: 16px;
    color: #909399;
    font-style: italic;
    background: #fafbfc;
  }

  .current-state-container th:first-child,
  .current-state-container td:first-child {
    width: 80px;
  }
</style>
