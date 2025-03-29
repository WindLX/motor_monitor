import type {
  CC_Payload,
  CC_M_MANUAL_Payload,
  CC_M_STEP_CORRECTION_Payload,
} from "./model/base";
import { messageManager } from "../store/instance";
import type { MotorNetMessageResponse } from "./model/net";

class MotorMonitorAPI {
  private baseUrl: string;
  private motorWebSocketUrl: string;
  private stateMachineWebSocketUrl: string;
  private motorWebSocket: WebSocket | null;
  private stateMachineWebSocket: WebSocket | null;

  constructor(baseUrl: string, wsUrl: string) {
    this.baseUrl = baseUrl;
    this.motorWebSocketUrl = `${wsUrl}/qs/m_state`;
    this.stateMachineWebSocketUrl = `${wsUrl}/qs/sm_state`;
    this.motorWebSocket = null;
    this.stateMachineWebSocket = null;
  }

  public connectMotorWebSocket() {
    this.motorWebSocket = new WebSocket(this.motorWebSocketUrl);
    if (this.motorWebSocket) {
      this.motorWebSocket.onopen = () => {};
      this.motorWebSocket.onmessage = (event) => {
        const message: MotorNetMessageResponse = JSON.parse(event.data);
        messageManager.update((m) => {
          m.addMessage(message);
          return m;
        });
      };
      this.motorWebSocket.onclose = () => {};
    }
  }

  public closeMotorWebSocket() {
    this.motorWebSocket?.close();
  }

  public connectStateMachineWebSocket() {
    this.motorWebSocket = new WebSocket(this.motorWebSocketUrl);
    if (this.motorWebSocket) {
      this.motorWebSocket.onopen = () => {};
      this.motorWebSocket.onmessage = (event) => {
        const message: MotorNetMessageResponse = JSON.parse(event.data);
        messageManager.update((m) => {
          m.addMessage(message);
          return m;
        });
      };
      this.motorWebSocket.onclose = () => {};
    }
  }

  public closeStateMachineWebSocket() {
    this.stateMachineWebSocket?.close();
  }

  public get motorWsStatus(): number {
    return this.motorWebSocket?.readyState || WebSocket.CLOSED;
  }

  public get motorWsUrl(): string {
    return this.motorWebSocketUrl;
  }

  public get stateMachineWsStatus(): number {
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

  async getDownstream(): Promise<any> {
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
