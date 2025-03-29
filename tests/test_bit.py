import pytest
import struct
import uuid

from model.base import (
    MotorMessage,
    MotorMessageTypeEnum,
    CC_M_MANUAL_Data,
    CC_M_STEP_CORRECTION_Data,
    QS_SM_STATE_Data,
    QS_M_STATE_Data,
)
from proto.bit import MotorBitMessage


def test_from_base_model_without_payload():
    message = MotorMessage(
        id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),
        timestamp=1672531200000.0,
        message_type=1,
        payload=None,
    )
    encoded = MotorBitMessage.from_base_model(message)
    assert len(encoded) == MotorBitMessage.FIXED_LENGTH
    assert uuid.UUID(bytes=encoded[:16]) == message.id


def test_into_base_model_without_payload():
    uuid_value = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    timestamp = 1672531200000.0
    message_type = 1
    encoded = struct.pack(f"!16sdB", uuid_value.bytes, timestamp, message_type).ljust(
        MotorBitMessage.FIXED_LENGTH, b"\x00"
    )
    decoded = MotorBitMessage.into_base_model(encoded)
    assert decoded.id == uuid_value
    assert decoded.timestamp == timestamp
    assert decoded.message_type == message_type


def test_from_base_model_with_payload_manual():
    payload = [
        CC_M_MANUAL_Data(motor_id=1, target_position=1000),
        CC_M_MANUAL_Data(motor_id=2, target_position=2000),
    ]
    message = MotorMessage(
        id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),
        timestamp=1672531200000.0,
        message_type=51,
        payload=payload,
    )
    encoded = MotorBitMessage.from_base_model(message)
    assert len(encoded) == MotorBitMessage.FIXED_LENGTH


def test_into_base_model_with_payload_manual():
    uuid_value = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    timestamp = 1672531200000.0
    message_type = 51
    array_length = 2
    payload = [
        struct.pack("!BQ", 1, 1000),
        struct.pack("!BQ", 2, 2000),
    ]
    encoded = (
        struct.pack(f"!16sdBB", uuid_value.bytes, timestamp, message_type, array_length)
        + b"".join(payload)
    ).ljust(MotorBitMessage.FIXED_LENGTH, b"\x00")
    decoded = MotorBitMessage.into_base_model(encoded)
    assert decoded.id == uuid_value
    assert decoded.timestamp == timestamp
    assert decoded.message_type == message_type
    assert len(decoded.payload) == array_length
    assert decoded.payload[0].motor_id == 1
    assert decoded.payload[0].target_position == 1000


def test_from_base_model_with_payload_state():
    payload = QS_SM_STATE_Data(state=5)
    message = MotorMessage(
        id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),
        timestamp=1672531200000.0,
        message_type=101,
        payload=payload,
    )
    encoded = MotorBitMessage.from_base_model(message)
    assert len(encoded) == MotorBitMessage.FIXED_LENGTH


def test_into_base_model_with_payload_state():
    uuid_value = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    timestamp = 1672531200000.0
    message_type = 101
    state = 5
    encoded = struct.pack(
        f"!16sdBB", uuid_value.bytes, timestamp, message_type, state
    ).ljust(MotorBitMessage.FIXED_LENGTH, b"\x00")
    decoded = MotorBitMessage.into_base_model(encoded)
    assert decoded.id == uuid_value
    assert decoded.timestamp == timestamp
    assert decoded.message_type == message_type
    assert decoded.payload.state == state
