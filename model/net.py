from datetime import datetime
import uuid

from pydantic import BaseModel, conint

from model.base import (
    MotorMessageTypeEnum,
    MotorMessage,
    CC_M_MANUAL_Payload,
    CC_M_STEP_CORRECTION_Payload,
    QS_M_STATE_Payload,
    QS_SM_STATE_Payload,
    CC_Payload,
    QS_Payload,
)


class MotorNetMessageControlCommand(BaseModel):
    id: str
    timestamp: float
    message_type: conint(ge=0, le=255)  # type: ignore
    payload: CC_Payload = None

    @staticmethod
    def build(
        message_type: MotorMessageTypeEnum,
        payload: CC_Payload = None,
    ) -> "MotorNetMessageControlCommand":
        id = str(uuid.uuid4())
        timestamp = datetime.now().timestamp()
        return MotorNetMessageControlCommand(
            id=id, timestamp=timestamp, message_type=message_type, payload=payload
        )

    def into_base_model(self) -> MotorMessage:
        id = uuid.UUID(self.id)
        return MotorMessage(
            id=id,
            timestamp=self.timestamp,
            message_type=self.message_type,
            payload=self.payload,
        )

    @staticmethod
    def from_base_model(message: MotorMessage) -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand(
            id=str(message.id),
            timestamp=message.timestamp,
            message_type=message.message_type,
            payload=message.payload,
        )

    @staticmethod
    def cc_p_start() -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand.build(
            message_type=MotorMessageTypeEnum.CC_P_START
        )

    @staticmethod
    def cc_p_zero() -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand.build(
            message_type=MotorMessageTypeEnum.CC_P_ZERO
        )

    @staticmethod
    def cc_p_center() -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand.build(
            message_type=MotorMessageTypeEnum.CC_P_CENTER
        )

    @staticmethod
    def cc_p_brake() -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand.build(
            message_type=MotorMessageTypeEnum.CC_P_BRAKE
        )

    @staticmethod
    def cc_p_auto() -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand.build(
            message_type=MotorMessageTypeEnum.CC_P_AUTO
        )

    @staticmethod
    def cc_p_disable() -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand.build(
            message_type=MotorMessageTypeEnum.CC_P_DISABLE
        )

    @staticmethod
    def cc_sm_clean_error() -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand.build(
            message_type=MotorMessageTypeEnum.CC_SM_CLEAN_ERROR
        )

    @staticmethod
    def cc_p_enter_correction() -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand.build(
            message_type=MotorMessageTypeEnum.CC_P_ENTER_CORRECTION
        )

    @staticmethod
    def cc_p_exit_correction() -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand.build(
            message_type=MotorMessageTypeEnum.CC_P_EXIT_CORRECTION
        )

    @staticmethod
    def cc_m_manual(payload: CC_M_MANUAL_Payload) -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand.build(
            message_type=MotorMessageTypeEnum.CC_M_MANUAL, payload=payload
        )

    @staticmethod
    def cc_m_step_correction(
        payload: CC_M_STEP_CORRECTION_Payload,
    ) -> "MotorNetMessageControlCommand":
        return MotorNetMessageControlCommand.build(
            message_type=MotorMessageTypeEnum.CC_M_STEP_CORRECTION, payload=payload
        )


class MotorNetMessageQueryStatus(BaseModel):
    id: str
    timestamp: float
    message_type: conint(ge=0, le=255)  # type: ignore
    payload: QS_Payload

    @staticmethod
    def build(
        message_type: MotorMessageTypeEnum,
        payload: QS_Payload,
    ) -> "MotorNetMessageQueryStatus":
        id = str(uuid.uuid4())
        timestamp = datetime.now().timestamp()
        return MotorNetMessageQueryStatus(
            id=id, timestamp=timestamp, message_type=message_type, payload=payload
        )

    def into_base_model(self) -> MotorMessage:
        id = uuid.UUID(self.id)
        return MotorMessage(
            id=id,
            timestamp=self.timestamp,
            message_type=self.message_type,
            payload=self.payload,
        )

    @staticmethod
    def from_base_model(message: MotorMessage) -> "MotorNetMessageQueryStatus":
        return MotorNetMessageQueryStatus(
            id=str(message.id),
            timestamp=message.timestamp,
            message_type=message.message_type,
            payload=message.payload,
        )

    @staticmethod
    def qs_sm_state(payload: QS_SM_STATE_Payload) -> "MotorNetMessageQueryStatus":
        return MotorNetMessageQueryStatus.build(
            message_type=MotorMessageTypeEnum.QS_SM_STATE, payload=payload
        )

    @staticmethod
    def qs_m_state(payload: QS_M_STATE_Payload) -> "MotorNetMessageQueryStatus":
        return MotorNetMessageQueryStatus.build(
            message_type=MotorMessageTypeEnum.QS_M_STATE, payload=payload
        )


class MotorNetMessageResponse(BaseModel):
    raw_message: MotorNetMessageControlCommand | MotorNetMessageQueryStatus
    is_success: bool = True
    error_message: str | None = None

    @property
    def id(self) -> str:
        return self.raw_message.id

    @property
    def timestamp(self) -> float:
        return self.raw_message.timestamp

    @property
    def message_type(self) -> MotorMessageTypeEnum:
        return self.raw_message.message_type

    @staticmethod
    def build(
        raw_message: MotorNetMessageControlCommand | MotorNetMessageQueryStatus,
        error_message: str | None = None,
    ) -> "MotorNetMessageResponse":
        is_success = error_message is None
        return MotorNetMessageResponse(
            raw_message=raw_message, is_success=is_success, error_message=error_message
        )
