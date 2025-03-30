import type {
  CC_Payload,
  CC_M_MANUAL_Payload,
  CC_M_STEP_CORRECTION_Payload,
} from "./model/base";
import type { DownstreamConfig } from "./model/config";
import type { MotorNetMessageResponse } from "./model/net";
import type { ConnectStatus } from "./model/status";
import { messageManager } from "../store/instance";

class MotorMonitorAPI {
  private baseUrl: string;
  private motorWebSocketUrl: string;
  private stateMachineWebSocketUrl: string;
  private motorWebSocket: WebSocket | null;
  private stateMachineWebSocket: WebSocket | null;

  private onMotorWebSocketConnected: () => void;
  private onMotorWebSocketDisconnected: () => void;
  private onMotorWebSocketError: () => void;
  private onStateMachineWebSocketConnected: () => void;
  private onStateMachineWebSocketDisconnected: () => void;
  private onStateMachineWebSocketError: () => void;

  constructor(baseUrl: string, wsUrl: string) {
    this.baseUrl = baseUrl;
    this.motorWebSocketUrl = `${wsUrl}/qs/m_state`;
    this.stateMachineWebSocketUrl = `${wsUrl}/qs/sm_state`;
    this.motorWebSocket = null;
    this.stateMachineWebSocket = null;

    this.onMotorWebSocketConnected = () => {};
    this.onMotorWebSocketDisconnected = () => {};
    this.onMotorWebSocketError = () => {};
    this.onStateMachineWebSocketConnected = () => {};
    this.onStateMachineWebSocketDisconnected = () => {};
    this.onStateMachineWebSocketError = () => {};
  }

  public subcribeOnMotorWebSocketConnected(callback: () => void): () => void {
    this.onMotorWebSocketConnected = callback;
    return () => {
      this.onMotorWebSocketConnected = () => {};
    };
  }

  public subscribeOnMotorWebSocketDisconnected(
    callback: () => void
  ): () => void {
    this.onMotorWebSocketDisconnected = callback;
    return () => {
      this.onMotorWebSocketDisconnected = () => {};
    };
  }

  public subscribeOnMotorWebSocketError(callback: () => void): () => void {
    this.onMotorWebSocketError = callback;
    return () => {
      this.onMotorWebSocketError = () => {};
    };
  }

  public subscribeOnStateMachineWebSocketConnected(
    callback: () => void
  ): () => void {
    this.onStateMachineWebSocketConnected = callback;
    return () => {
      this.onStateMachineWebSocketConnected = () => {};
    };
  }

  public subscribeOnStateMachineWebSocketDisconnected(
    callback: () => void
  ): () => void {
    this.onStateMachineWebSocketDisconnected = callback;
    return () => {
      this.onStateMachineWebSocketDisconnected = () => {};
    };
  }

  public subscribeOnStateMachineWebSocketError(
    callback: () => void
  ): () => void {
    this.onStateMachineWebSocketError = callback;
    return () => {
      this.onStateMachineWebSocketError = () => {};
    };
  }

  public connectMotorWebSocket() {
    this.motorWebSocket = new WebSocket(this.motorWebSocketUrl);
    if (this.motorWebSocket) {
      this.motorWebSocket.onopen = this.onMotorWebSocketConnected;
      this.motorWebSocket.onmessage = (event) => {
        const message: MotorNetMessageResponse = JSON.parse(event.data);
        messageManager.update((m) => {
          m.addMessage(message);
          return m;
        });
      };
      this.motorWebSocket.onclose = this.onMotorWebSocketDisconnected;
      this.motorWebSocket.onerror = this.onMotorWebSocketError;
    }
  }

  public closeMotorWebSocket() {
    this.motorWebSocket?.close();
  }

  public connectStateMachineWebSocket() {
    this.stateMachineWebSocket = new WebSocket(this.stateMachineWebSocketUrl);
    if (this.stateMachineWebSocket) {
      this.stateMachineWebSocket.onopen = this.onStateMachineWebSocketConnected;
      this.stateMachineWebSocket.onmessage = (event) => {
        const message: MotorNetMessageResponse = JSON.parse(event.data);
        messageManager.update((m) => {
          m.addMessage(message);
          return m;
        });
      };
      this.stateMachineWebSocket.onclose =
        this.onStateMachineWebSocketDisconnected;
      this.stateMachineWebSocket.onerror = this.onStateMachineWebSocketError;
    }
  }

  public closeStateMachineWebSocket() {
    this.stateMachineWebSocket?.close();
  }

  public get motorWsStatus(): ConnectStatus {
    return this.motorWebSocket?.readyState || WebSocket.CLOSED;
  }

  public get motorWsUrl(): string {
    return this.motorWebSocketUrl;
  }

  public get stateMachineWsStatus(): ConnectStatus {
    return this.stateMachineWebSocket?.readyState || WebSocket.CLOSED;
  }

  public get stateMachineWsUrl(): string {
    return this.stateMachineWebSocketUrl;
  }

  async readRoot(): Promise<string> {
    const response = await fetch(`${this.baseUrl}/`, {
      method: "GET",
      headers: {
        "Content-Type": "text/html",
      },
    });

    if (!response.ok) {
      throw new Error(`Error: Api ${response.statusText}`);
    }

    return this.baseUrl;
  }

  async getDownstream(): Promise<DownstreamConfig> {
    const response = await fetch(`${this.baseUrl}/downstream`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Error: Downstream ${response.statusText}`);
    }

    return response.json();
  }

  private async sendControlCommand(
    route: string,
    payload: CC_Payload
  ): Promise<MotorNetMessageResponse> {
    const response = await fetch(`${this.baseUrl}/cc/${route}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorDetail = await response.json();
      throw new Error(`Error: Control Command ${errorDetail.detail}`);
    }

    const r: MotorNetMessageResponse = await response.json();

    messageManager.update((m) => {
      m.addMessage(r);
      return m;
    });

    if (r.is_success) {
      return r;
    } else {
      throw new Error(`Error: Control Command ${r.error_message}`);
    }
  }

  async startPlatform(): Promise<MotorNetMessageResponse> {
    return this.sendControlCommand("p/start", null);
  }

  async zeroPlatform(): Promise<MotorNetMessageResponse> {
    return this.sendControlCommand("p/zero", null);
  }

  async centerPlatform(): Promise<MotorNetMessageResponse> {
    return this.sendControlCommand("p/center", null);
  }

  async brakePlatform(): Promise<MotorNetMessageResponse> {
    return this.sendControlCommand("p/brake", null);
  }

  async automaticPositioning(): Promise<MotorNetMessageResponse> {
    return this.sendControlCommand("p/auto", null);
  }

  async disablePlatform(): Promise<MotorNetMessageResponse> {
    return this.sendControlCommand("p/disable", null);
  }

  async clearStateMachineError(): Promise<MotorNetMessageResponse> {
    return this.sendControlCommand("sm/clean_error", null);
  }

  async enterCorrection(): Promise<MotorNetMessageResponse> {
    return this.sendControlCommand("p/enter_correction", null);
  }

  async exitCorrection(): Promise<MotorNetMessageResponse> {
    return this.sendControlCommand("p/exit_correction", null);
  }

  async manualPositioning(
    payload: CC_M_MANUAL_Payload
  ): Promise<MotorNetMessageResponse> {
    return this.sendControlCommand("m/manual", payload);
  }

  async stepCorrection(
    payload: CC_M_STEP_CORRECTION_Payload
  ): Promise<MotorNetMessageResponse> {
    return this.sendControlCommand("m/step_correction", payload);
  }
}

export default MotorMonitorAPI;
