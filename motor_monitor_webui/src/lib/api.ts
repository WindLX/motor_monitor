import type { GetStateData, MotorMessage, MotorStateRecord } from "./model";
import { motorStateStore } from "../store/share";

class MotorMonitorAPI {
    private baseUrl: string;
    private webSocket: WebSocket;

    constructor(baseUrl: string, wsUrl: string) {
        this.baseUrl = baseUrl;
        this.webSocket = new WebSocket(`${wsUrl}/state`);
        this.initializeWebSocket();
    }

    initializeWebSocket() {
        this.webSocket.onopen = () => {
            console.log('WebSocket connected');
        };
        this.webSocket.onmessage = (event) => {
            const message: MotorMessage = JSON.parse(event.data);
            const rawData: GetStateData[] = message.data;
            const data: Record<number, MotorStateRecord> = {};
            rawData.forEach((item) => {
                data[item.motor_id] = {
                    position: item.position,
                    velocity: item.velocity,
                    current: item.current,
                };
            })
            motorStateStore.update((state) => {
                state.push(data);
                return state;
            });
        }
        this.webSocket.onclose = () => {
            console.log('WebSocket closed');
        }
    }

    async readRoot(): Promise<string> {
        const response = await fetch(`${this.baseUrl}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'text/html'
            }
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        return response.text();
    }

    async getDownstream(): Promise<any> {
        const response = await fetch(`${this.baseUrl}/downstream`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        return response.json();
    }

    private async sendCommand(command: number, data?: Array<{ motor_id: number, position: number }>): Promise<any> {
        const response = await fetch(`${this.baseUrl}/cmd`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                command, data,
            })
        });

        if (!response.ok) {
            const errorDetail = await response.json();
            throw new Error(`Error: ${errorDetail.detail}`);
        }

        return response.json();
    }

    async startPlatform(): Promise<any> {
        return this.sendCommand(1);
    }

    async zeroPlatform(): Promise<any> {
        return this.sendCommand(2);
    }

    async centerPlatform(): Promise<any> {
        return this.sendCommand(3);
    }

    async stopPlatform(): Promise<any> {
        return this.sendCommand(4);
    }

    async automaticPositioning(): Promise<any> {
        return this.sendCommand(5);
    }

    async disablePlatform(): Promise<any> {
        return this.sendCommand(6);
    }

    async clearStateMachineError(): Promise<any> {
        return this.sendCommand(7);
    }

    async setPosition(data: Array<{ motor_id: number, position: number }>): Promise<any> {
        return this.sendCommand(101, data);
    }
}

export default MotorMonitorAPI;