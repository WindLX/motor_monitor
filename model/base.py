from datetime import datetime
import uuid

from pydantic import BaseModel, conint

type CC_M_MANUAL_Payload = list[CC_M_MANUAL_Data]
type CC_M_STEP_CORRECTION_Payload = list[CC_M_STEP_CORRECTION_Data]
type QS_M_STATE_Payload = list[QS_M_STATE_Data]
type QS_SM_STATE_Payload = QS_SM_STATE_Data

type CC_Payload = (CC_M_MANUAL_Payload | CC_M_STEP_CORRECTION_Payload | None)
type QS_Payload = (QS_SM_STATE_Payload | QS_M_STATE_Payload)
type MotorMessagePayload = (CC_Payload | QS_Payload)


class MotorMessageTypeEnum:
    # Control Commands (1-49, no payload)
    CC_P_START = 1
    CC_P_ZERO = 2
    CC_P_CENTER = 3
    CC_P_BRAKE = 4
    CC_P_AUTO = 5
    CC_P_DISABLE = 6
    CC_SM_CLEAN_ERROR = 7
    CC_P_ENTER_CORRECTION = 8
    CC_P_EXIT_CORRECTION = 9

    # Control Commands (51-99, with payload)
    CC_M_MANUAL = 51
    CC_M_STEP_CORRECTION = 52

    # Query Status (101-199, with payload)
    QS_SM_STATE = 101
    QS_M_STATE = 102


class StateMachineStateEnum:
    SM_UNKNOWN = 0
    SM_INITIALIZING = 1
    SM_ZEROING = 2
    SM_CENTERING = 3
    SM_BRAKING = 4
    SM_AUTOMATING = 5
    SM_IDLE = 6
    SM_CORRECTION = 8
    SM_MANUALING = 101


class CC_M_MANUAL_Data(BaseModel):
    motor_id: conint(ge=0, le=255)  # type: ignore
    target_position: conint(ge=0)  # type: ignore


class CC_M_STEP_CORRECTION_Data(BaseModel):
    motor_id: conint(ge=0, le=255)  # type: ignore
    direction: conint(ge=1, le=2)  # type: ignore


class QS_SM_STATE_Data(BaseModel):
    state: conint(ge=0, le=255)  # type: ignore

    @staticmethod
    def build(state: StateMachineStateEnum) -> "QS_SM_STATE_Data":
        return QS_SM_STATE_Data(state=state)


class QS_M_STATE_Data(BaseModel):
    motor_id: conint(ge=0, le=255)  # type: ignore
    position: conint(ge=0)  # type: ignore
    velocity: conint(ge=0)  # type: ignore
    torque: conint(ge=0)  # type: ignore


class MotorMessage(BaseModel):
    id: uuid.UUID
    timestamp: float
    message_type: conint(ge=0, le=255)  # type: ignore
    payload: MotorMessagePayload = None

    @staticmethod
    def build(
        message_type: MotorMessageTypeEnum,
        payload: MotorMessagePayload = None,
    ) -> "MotorMessage":
        id = uuid.uuid4()
        timestamp = datetime.now().timestamp()
        return MotorMessage(
            message_type=message_type, id=id, timestamp=timestamp, payload=payload
        )
