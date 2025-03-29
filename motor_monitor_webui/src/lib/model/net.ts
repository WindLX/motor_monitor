import type { CC_Payload, MotorMessageTypeEnum, QS_Payload } from "./base";

export interface MotorNetMessageControlCommand {
  id: string;
  timestamp: number;
  message_type: MotorMessageTypeEnum;
  payload: CC_Payload;
}

export interface MotorNetMessageQueryStatus {
  id: string;
  timestamp: number;
  message_type: MotorMessageTypeEnum;
  payload: QS_Payload;
}

export interface MotorNetMessageResponse {
  raw_message: MotorNetMessageControlCommand | MotorNetMessageQueryStatus;
  is_success: boolean;
  error_message: string | null;
}
