<script lang="ts">
  import { onMount } from "svelte";
  import { FontAwesomeIcon } from "fontawesome-svelte";
  import { motorMonitorAPI, resetAPI } from "../store/instance";
  import { notify } from "../store/notify";
  import {
    apiConnectStatus,
    motorStateWsConnectStatus,
    downstreamConnectStatus,
    stateMachineWsConnectStatus,
    stateMachineStateStore,
  } from "../store/share";
  import { stateMachineStateEnumConverter } from "../lib/model/base";
  import { ConnectStatus } from "../lib/model/status";

  let baseUrl = "http://unknown:8000";
  let motorStateWsUrl = "ws://unknown:8000/qs/m_state";
  let stateMachineWsUrl = "ws://unknown:8000/qs/sm_state";

  let downstreamHost = "unknown";
  let downstreamPort = 8002;

  async function resetConnection() {
    $notify.info("Resetting connection...");
    resetAPI();
    await refreshState();
  }

  async function refreshState() {
    apiConnectStatus.set(ConnectStatus.DISCONNECTED);
    motorStateWsConnectStatus.set(ConnectStatus.DISCONNECTED);
    stateMachineWsConnectStatus.set(ConnectStatus.DISCONNECTED);
    downstreamConnectStatus.set(ConnectStatus.DISCONNECTED);

    if ($motorMonitorAPI) {
      try {
        const response = await $motorMonitorAPI.readRoot();
        baseUrl = response;
        apiConnectStatus.set(ConnectStatus.CONNECTED);
        $notify.info("API connected");

        $motorMonitorAPI.subcribeOnMotorWebSocketConnected(() => {
          motorStateWsConnectStatus.set(ConnectStatus.CONNECTED);
          $notify.success("Motor WebSocket connected");
        });

        $motorMonitorAPI.subscribeOnMotorWebSocketDisconnected(() => {
          motorStateWsConnectStatus.set(ConnectStatus.DISCONNECTED);
          $notify.warning("Motor WebSocket disconnected");
        });

        $motorMonitorAPI.subscribeOnMotorWebSocketError(() => {
          motorStateWsConnectStatus.set(ConnectStatus.DISCONNECTED);
          $notify.error("Motor WebSocket error");
        });

        $motorMonitorAPI.subscribeOnStateMachineWebSocketConnected(() => {
          stateMachineWsConnectStatus.set(ConnectStatus.CONNECTED);
          $notify.success("State Machine WebSocket connected");
        });

        $motorMonitorAPI.subscribeOnStateMachineWebSocketDisconnected(() => {
          stateMachineWsConnectStatus.set(ConnectStatus.DISCONNECTED);
          $notify.warning("State Machine WebSocket disconnected");
        });

        $motorMonitorAPI.subscribeOnStateMachineWebSocketError(() => {
          stateMachineWsConnectStatus.set(ConnectStatus.DISCONNECTED);
          $notify.error("State Machine WebSocket error");
        });

        try {
          const downstream = await $motorMonitorAPI.getDownstream();
          downstreamHost = downstream.host;
          downstreamPort = downstream.port;
          downstreamConnectStatus.set(ConnectStatus.CONNECTED);
          $notify.info("Downstream connected");
        } catch (error) {
          downstreamConnectStatus.set(ConnectStatus.CONNECTED);
          $notify.warning((error as any).message);
        }
      } catch (error) {
        apiConnectStatus.set(ConnectStatus.DISCONNECTED);
        $notify.warning((error as any).message);
      }
    } else {
      apiConnectStatus.set(ConnectStatus.DISCONNECTED);
      $notify.warning("API not connected");
    }
  }

  async function connectMotorWs() {
    if ($motorStateWsConnectStatus === ConnectStatus.CONNECTED) {
      $notify.info("Disconnecting Motor WebSocket...");
      $motorMonitorAPI.closeMotorWebSocket();
    } else {
      $notify.info("Connecting Motor WebSocket...");
      try {
        $motorMonitorAPI.connectMotorWebSocket();
        motorStateWsUrl = $motorMonitorAPI.motorWsUrl;
      } catch (error) {
        $notify.error(
          `Failed to connect Motor WebSocket: ${(error as any).message}`
        );
      }
    }
  }

  async function connectStateMachineWs() {
    if ($stateMachineWsConnectStatus === ConnectStatus.CONNECTED) {
      $notify.info("Disconnecting State Machine WebSocket...");
      $motorMonitorAPI.closeStateMachineWebSocket();
    } else {
      $notify.info("Connecting State Machine WebSocket...");
      try {
        $motorMonitorAPI.connectStateMachineWebSocket();
        stateMachineWsUrl = $motorMonitorAPI.stateMachineWsUrl;
      } catch (error) {
        $notify.error(
          `Failed to connect State Machine WebSocket: ${(error as any).message}`
        );
      }
    }
  }

  onMount(async () => {
    await refreshState();
  });
</script>

<div class="state-container">
  <div class="state-box">
    <div class="state-item">
      <div
        class="status-dot"
        class:connected={$apiConnectStatus === ConnectStatus.CONNECTED}
        class:connecting={$apiConnectStatus === ConnectStatus.CONNECTING}
        class:disconnecting={$apiConnectStatus === ConnectStatus.DISCONNECTING}
        class:disconnected={$apiConnectStatus === ConnectStatus.DISCONNECTED}
      ></div>
      <span class="status-icon">
        <FontAwesomeIcon icon={["fas", "server"]}></FontAwesomeIcon>
      </span>
      <!-- <span><b>API</b></span> -->
      <span class="url">{baseUrl}</span>
    </div>

    <span class="split">
      <FontAwesomeIcon icon={["fas", "minus"]}></FontAwesomeIcon>
    </span>

    <div class="state-item">
      <div
        class="status-dot"
        class:connected={$downstreamConnectStatus === ConnectStatus.CONNECTED}
        class:connecting={$downstreamConnectStatus === ConnectStatus.CONNECTING}
        class:disconnecting={$downstreamConnectStatus ===
          ConnectStatus.DISCONNECTING}
        class:disconnected={$downstreamConnectStatus ===
          ConnectStatus.DISCONNECTED}
      ></div>
      <span class="status-icon">
        <FontAwesomeIcon icon={["fas", "ethernet"]}></FontAwesomeIcon>
      </span>
      <!-- <span><b>Downstream</b></span> -->
      <span class="url">udp://{downstreamHost}:{downstreamPort}</span>
    </div>

    <span class="split">
      <FontAwesomeIcon icon={["fas", "minus"]}></FontAwesomeIcon>
    </span>

    <div class="state-item">
      <div
        class="status-dot"
        class:connected={$motorStateWsConnectStatus === ConnectStatus.CONNECTED}
        class:connecting={$motorStateWsConnectStatus ===
          ConnectStatus.CONNECTING}
        class:disconnecting={$motorStateWsConnectStatus ===
          ConnectStatus.DISCONNECTING}
        class:disconnected={$motorStateWsConnectStatus ===
          ConnectStatus.DISCONNECTED}
      ></div>
      <button
        class="status-icon"
        onclick={connectMotorWs}
        class:connected={$motorStateWsConnectStatus === ConnectStatus.CONNECTED}
      >
        <FontAwesomeIcon icon={["fas", "plug"]}></FontAwesomeIcon>
      </button>
      <!-- <span><b>Motor State WebSocket</b></span> -->
      <span class="url">{motorStateWsUrl}</span>
    </div>

    <span class="split">
      <FontAwesomeIcon icon={["fas", "minus"]}></FontAwesomeIcon>
    </span>

    <div class="state-item">
      <div
        class="status-dot"
        class:connected={$stateMachineWsConnectStatus ===
          ConnectStatus.CONNECTED}
        class:connecting={$stateMachineWsConnectStatus ===
          ConnectStatus.CONNECTING}
        class:disconnecting={$stateMachineWsConnectStatus ===
          ConnectStatus.DISCONNECTING}
        class:disconnected={$stateMachineWsConnectStatus ===
          ConnectStatus.DISCONNECTED}
      ></div>
      <button
        class="status-icon"
        onclick={connectStateMachineWs}
        class:connected={$stateMachineWsConnectStatus ===
          ConnectStatus.CONNECTED}
      >
        <FontAwesomeIcon icon={["fas", "hexagon-nodes"]}></FontAwesomeIcon>
      </button>
      <!-- <span><b>State Machine WebSocket</b></span> -->
      <span class="url">{stateMachineWsUrl}</span>
      <span
        ><b>{stateMachineStateEnumConverter($stateMachineStateStore.state)}</b
        ></span
      >
    </div>
  </div>

  <div class="state-right">
    <button onclick={resetConnection}>
      <FontAwesomeIcon icon={["fas", "rotate-right"]}></FontAwesomeIcon>
    </button>
  </div>
</div>

<style>
  .state-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    padding: 10px;
    padding-top: 0;
    padding-bottom: 0;
    border-radius: 8px;
    background-color: var(--main-white-color-0);
    box-shadow: 0 0 8px 0 var(--main-white-color-3);
  }

  .state-container .state-box {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    padding: 10px;
  }

  .state-container .state-item {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .state-container .state-item span.url {
    font-size: 14px;
    font-family: var(--mono-font);
  }

  .state-container .state-item span.url:hover {
    text-decoration: underline;
  }

  .state-container .split {
    transform: rotate(90deg);
    color: var(--main-white-color-4);
    font-size: 16px;
  }

  .status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    transition: background 0.2s ease;
  }

  .status-dot.connecting {
    background-color: var(--status-connecting);
  }

  .status-dot.connected {
    background-color: var(--status-connected);
  }

  .status-dot.disconnected {
    background-color: var(--status-disconnected);
  }

  .status-dot.disconnecting {
    background-color: var(--status-disconnecting);
  }

  .state-container button {
    width: 32px;
    justify-content: center;
    padding: 6px;
  }

  .state-container button.connected {
    border-color: var(--primary-color);
    background-color: var(--primary-color);
    color: var(--main-white-color-0);
  }

  .state-container .state-right {
    display: flex;
    align-items: center;
    padding: 10px;
  }
</style>
