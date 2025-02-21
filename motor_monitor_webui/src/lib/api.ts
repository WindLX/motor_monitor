class MotorMonitorAPI {
    private baseUrl: string;
    private _ip: string;
    private _port: number;

    constructor(baseUrl: string, ip: string, port: number) {
        this.baseUrl = baseUrl;
        this._ip = ip;
        this._port = port;
    }
    get ip(): string {
        return this._ip;
    }

    set ip(value: string) {
        this._ip = value;
    }

    get port(): number {
        return this._port;
    }

    set port(value: number) {
        this._port = value;
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

    private async sendCommand(command: number, data?: Array<{ motor_id: number, position: number }>): Promise<any> {
        const response = await fetch(`${this.baseUrl}/cmd`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ip: this.ip, port: this.port, command, data,
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