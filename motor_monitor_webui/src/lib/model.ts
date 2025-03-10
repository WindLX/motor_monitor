export interface GetStateData {
    motor_id: number;
    position: number;
    velocity: number;
    torque: number;
}

export interface MotorMessage {
    command: number;
    data: Array<GetStateData>;
}

export interface MotorStateRecord {
    position: number;
    velocity: number;
    torque: number;
}