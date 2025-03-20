from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControlCommand(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMMAND_UNSPECIFIED: _ClassVar[ControlCommand]
    START: _ClassVar[ControlCommand]
    ZERO: _ClassVar[ControlCommand]
    CENTER: _ClassVar[ControlCommand]
    STOP: _ClassVar[ControlCommand]
    AUTO: _ClassVar[ControlCommand]
    DISABLE: _ClassVar[ControlCommand]
    CLEAR_ERROR: _ClassVar[ControlCommand]
    MANUAL: _ClassVar[ControlCommand]

class StatusQuery(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUERY_UNSPECIFIED: _ClassVar[StatusQuery]
    CURRENT_STATE: _ClassVar[StatusQuery]
    MACHINE_STATE: _ClassVar[StatusQuery]

class MachineState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[MachineState]
    INITIALIZING: _ClassVar[MachineState]
    IDLE: _ClassVar[MachineState]
    ZEROING: _ClassVar[MachineState]
    CENTERING: _ClassVar[MachineState]
    BRAKING: _ClassVar[MachineState]
    AUTOMATING: _ClassVar[MachineState]
    MANUALING: _ClassVar[MachineState]
    ERROR: _ClassVar[MachineState]
COMMAND_UNSPECIFIED: ControlCommand
START: ControlCommand
ZERO: ControlCommand
CENTER: ControlCommand
STOP: ControlCommand
AUTO: ControlCommand
DISABLE: ControlCommand
CLEAR_ERROR: ControlCommand
MANUAL: ControlCommand
QUERY_UNSPECIFIED: StatusQuery
CURRENT_STATE: StatusQuery
MACHINE_STATE: StatusQuery
UNKNOWN: MachineState
INITIALIZING: MachineState
IDLE: MachineState
ZEROING: MachineState
CENTERING: MachineState
BRAKING: MachineState
AUTOMATING: MachineState
MANUALING: MachineState
ERROR: MachineState

class ManualParams(_message.Message):
    __slots__ = ("motor_id", "position", "velocity")
    MOTOR_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    motor_id: int
    position: int
    velocity: int
    def __init__(self, motor_id: _Optional[int] = ..., position: _Optional[int] = ..., velocity: _Optional[int] = ...) -> None: ...

class MotorStatus(_message.Message):
    __slots__ = ("motor_id", "position", "velocity", "torque")
    MOTOR_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    TORQUE_FIELD_NUMBER: _ClassVar[int]
    motor_id: int
    position: int
    velocity: int
    torque: int
    def __init__(self, motor_id: _Optional[int] = ..., position: _Optional[int] = ..., velocity: _Optional[int] = ..., torque: _Optional[int] = ...) -> None: ...

class DeviceStatus(_message.Message):
    __slots__ = ("state", "error_code", "motors")
    STATE_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    MOTORS_FIELD_NUMBER: _ClassVar[int]
    state: MachineState
    error_code: int
    motors: _containers.RepeatedCompositeFieldContainer[MotorStatus]
    def __init__(self, state: _Optional[_Union[MachineState, str]] = ..., error_code: _Optional[int] = ..., motors: _Optional[_Iterable[_Union[MotorStatus, _Mapping]]] = ...) -> None: ...

class MotorMessage(_message.Message):
    __slots__ = ("message_id", "timestamp", "control", "query", "position_set", "status_report")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    POSITION_SET_FIELD_NUMBER: _ClassVar[int]
    STATUS_REPORT_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    timestamp: _timestamp_pb2.Timestamp
    control: ControlCommand
    query: StatusQuery
    position_set: ManualParams
    status_report: DeviceStatus
    def __init__(self, message_id: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., control: _Optional[_Union[ControlCommand, str]] = ..., query: _Optional[_Union[StatusQuery, str]] = ..., position_set: _Optional[_Union[ManualParams, _Mapping]] = ..., status_report: _Optional[_Union[DeviceStatus, _Mapping]] = ...) -> None: ...
