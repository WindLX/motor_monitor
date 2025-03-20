from pydantic import BaseModel, conint
from typing import Optional
from datetime import datetime
from enum import Enum

from generated.bit_pb2 import ControlCommand as ProtoControlCommand
from generated.bit_pb2 import StatusQuery as ProtoStatusQuery
from generated.bit_pb2 import MachineState as ProtoMachineState
from generated.bit_pb2 import ManualParams as ProtoManualParams
from generated.bit_pb2 import MotorStatus as ProtoMotorStatus
from generated.bit_pb2 import DeviceStatus as ProtoDeviceStatus
from generated.bit_pb2 import MotorMessage as ProtoMotorMessage


class ControlCommand(int, Enum):
    COMMAND_UNSPECIFIED = 0
    START = 1
    ZERO = 2
    CENTER = 3
    STOP = 4
    AUTO = 5
    DISABLE = 6
    CLEAR_ERROR = 7
    MANUAL = 8

    def into_proto(self) -> ProtoControlCommand:
        return ProtoControlCommand.Value(self.name)

    def from_proto(proto: ProtoControlCommand) -> "ControlCommand":
        return ControlCommand[proto.name]


class StatusQuery(int, Enum):
    QUERY_UNSPECIFIED = 0
    CURRENT_STATE = 1
    MACHINE_STATE = 2

    def into_proto(self) -> ProtoStatusQuery:
        return ProtoStatusQuery.Value(self.name)

    def from_proto(proto: ProtoStatusQuery) -> "StatusQuery":
        return StatusQuery[proto.name]


class MachineState(int, Enum):
    UNKNOWN = 0
    INITIALIZING = 1
    IDLE = 2
    ZEROING = 3
    CENTERING = 4
    BREAKING = 5
    AUTOMATING = 6
    MANUALING = 7
    ERROR = 8

    def into_proto(self) -> ProtoMachineState:
        return ProtoMachineState.Value(self.name)

    def from_proto(proto: ProtoMachineState) -> "MachineState":
        return MachineState[proto.name]


class ManualParams(BaseModel):
    motor_id: conint(ge=1, le=255)  # type: ignore
    position: int
    velocity: int

    def into_proto(self) -> ProtoManualParams:
        return ProtoManualParams(
            motor_id=self.motor_id,
            position=self.position,
            velocity=self.velocity,
        )

    def from_proto(proto: ProtoManualParams) -> "ManualParams":
        return ManualParams(
            motor_id=proto.motor_id,
            position=proto.position,
            velocity=proto.velocity,
        )


class MotorStatus(BaseModel):
    motor_id: conint(ge=1, le=255)  # type: ignore
    position: int
    velocity: int
    torque: int

    def into_proto(self) -> ProtoMotorStatus:
        return ProtoMotorStatus(
            motor_id=self.motor_id,
            position=self.position,
            velocity=self.velocity,
            torque=self.torque,
        )

    def from_proto(proto: ProtoMotorStatus) -> "MotorStatus":
        return MotorStatus(
            motor_id=proto.motor_id,
            position=proto.position,
            velocity=proto.velocity,
            torque=proto.torque,
        )


class DeviceStatus(BaseModel):
    state: str
    error_code: int
    motors: list[MotorStatus]

    def into_proto(self) -> ProtoDeviceStatus:
        return ProtoDeviceStatus(
            state=self.state,
            error_code=self.error_code,
            motors=[motor.into_proto() for motor in self.motors],
        )

    def from_proto(proto: ProtoDeviceStatus) -> "DeviceStatus":
        return DeviceStatus(
            state=proto.state,
            error_code=proto.error_code,
            motors=[MotorStatus.from_proto(motor) for motor in proto.motors],
        )


class MotorMessage(BaseModel):
    message_id: str
    timestamp: datetime
    control: Optional[str]
    query: Optional[str]
    position_set: Optional[ManualParams]
    status_report: Optional[DeviceStatus]

    def into_proto(self) -> ProtoMotorMessage:
        return ProtoMotorMessage(
            message_id=self.message_id,
            timestamp=self.timestamp,
            control=self.control,
            query=self.query,
            position_set=self.position_set.into_proto() if self.position_set else None,
            status_report=(
                self.status_report.into_proto() if self.status_report else None
            ),
        )

    def from_proto(proto: ProtoMotorMessage) -> "MotorMessage":
        return MotorMessage(
            message_id=proto.message_id,
            timestamp=proto.timestamp,
            control=proto.control,
            query=proto.query,
            position_set=proto.position_set,
            status_report=proto.status_report,
        )
