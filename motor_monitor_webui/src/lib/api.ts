class MotorMonitorAPI {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
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

    async startMotor(): Promise<any> {
        return this.sendCommand(1);
    }

    async stopMotor(): Promise<any> {
        return this.sendCommand(2);
    }

    async pauseMotor(): Promise<any> {
        return this.sendCommand(3);
    }

    async resumeMotor(): Promise<any> {
        return this.sendCommand(4);
    }

    async setPosition(data: Array<{ motor_id: number, position: number }>): Promise<any> {
        return this.sendCommand(5, data);
    }
}

export default MotorMonitorAPI;