export enum MotorMessageTypeEnum {
  CC_P_START = 1,
  CC_P_ZERO = 2,
  CC_P_CENTER = 3,
  CC_P_BRAKE = 4,
  CC_P_AUTO = 5,
  CC_P_DISABLE = 6,
  CC_SM_CLEAN_ERROR = 7,
  CC_P_ENTER_CORRECTION = 8,
  CC_P_EXIT_CORRECTION = 9,

  CC_M_MANUAL = 51,
  CC_M_STEP_CORRECTION = 52,

  QS_SM_STATE = 101,
  QS_M_STATE = 102,
}

export enum StateMachineStateEnum {
  SM_UNKNOWN = 0,
  SM_INITIALIZING = 1,
  SM_ZEROING = 2,
  SM_CENTERING = 3,
  SM_BRAKING = 4,
  SM_AUTOMATING = 5,
  SM_IDLE = 6,
  SM_CORRECTION = 8,
  SM_MANUALING = 101,
}

export interface CC_M_MANUAL_Data {
  motor_id: number;
  target_position: number;
}

export interface CC_M_STEP_CORRECTION_Data {
  motor_id: number;
  direction: number;
}

export interface QS_SM_STATE_Data {
  state: StateMachineStateEnum;
}

export interface QS_M_STATE_Data {
  motor_id: number;
  position: number;
  velocity: number;
  torque: number;
}

export type CC_M_MANUAL_Payload = Array<CC_M_MANUAL_Data>;
export type CC_M_STEP_CORRECTION_Payload = Array<CC_M_STEP_CORRECTION_Data>;
export type QS_SM_STATE_Payload = QS_SM_STATE_Data;
export type QS_M_STATE_Payload = Array<QS_M_STATE_Data>;

export type CC_Payload =
  | CC_M_MANUAL_Payload
  | CC_M_STEP_CORRECTION_Payload
  | null;
export type QS_Payload = QS_SM_STATE_Payload | QS_M_STATE_Payload;
export type MotorMessagePayload = CC_Payload | QS_Payload;
