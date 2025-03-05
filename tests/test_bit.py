import pytest
import struct

from proto.base import MotorMessage
from proto.bit import MotorBitMessage, MotorBitCommand


def test_from_base_model_start():
    message = MotorMessage.create_message(command=MotorBitCommand.START)
    result = MotorBitMessage.from_base_model(message)
    expected = struct.pack(MotorBitMessage.HEADER_FORMAT, MotorBitCommand.START).ljust(
        MotorBitMessage.FIXED_LENGTH, b"\x00"
    )
    assert result == expected


def test_from_base_model_set_position():
    data = [{"motor_id": 1, "position": 123456}]
    message = MotorMessage.create_message(
        command=MotorBitCommand.SET_POSITION,
        data=data,
    )
    result = MotorBitMessage.from_base_model(message)
    header = struct.pack(MotorBitMessage.HEADER_FORMAT, MotorBitCommand.SET_POSITION)
    array_length = struct.pack(MotorBitMessage.LENGTH_FORMAT, 1)
    motor_id = struct.pack(MotorBitMessage.MOTOR_ID_FORMAT, 1)
    position = struct.pack(MotorBitMessage.INT_FORMAT, 123456)
    velocity = struct.pack(MotorBitMessage.INT_FORMAT, 0)
    current = struct.pack(MotorBitMessage.INT_FORMAT, 0)
    expected = (header + array_length + motor_id + position + velocity + current).ljust(
        MotorBitMessage.FIXED_LENGTH, b"\x00"
    )
    assert result == expected


def test_into_base_model_start():
    message = struct.pack(MotorBitMessage.HEADER_FORMAT, MotorBitCommand.START).ljust(
        MotorBitMessage.FIXED_LENGTH, b"\x00"
    )
    result = MotorBitMessage.into_base_model(message)
    expected = MotorMessage.create_message(command=MotorBitCommand.START)
    assert result.command.command == expected.command.command


def test_into_base_model_set_position():
    header = struct.pack(MotorBitMessage.HEADER_FORMAT, MotorBitCommand.SET_POSITION)
    array_length = struct.pack(MotorBitMessage.LENGTH_FORMAT, 1)
    motor_id = struct.pack(MotorBitMessage.MOTOR_ID_FORMAT, 1)
    position = struct.pack(MotorBitMessage.INT_FORMAT, 123456)
    velocity = struct.pack(MotorBitMessage.INT_FORMAT, 0)
    current = struct.pack(MotorBitMessage.INT_FORMAT, 0)
    message = (header + array_length + motor_id + position + velocity + current).ljust(
        MotorBitMessage.FIXED_LENGTH, b"\x00"
    )
    result = MotorBitMessage.into_base_model(message)
    expected_data = [{"motor_id": 1, "position": 123456}]
    expected = MotorMessage.create_message(
        command=MotorBitCommand.SET_POSITION,
        data=expected_data,
    )
    assert result.command.command == expected.command.command
    assert result.data == expected.data


def test_invalid_command_from_base_model():
    with pytest.raises(ValueError):
        message = MotorMessage.create_message(command=99)
        MotorBitMessage.from_base_model(message)


def test_invalid_command_into_base_model():
    message = struct.pack(MotorBitMessage.HEADER_FORMAT, 10).ljust(
        MotorBitMessage.FIXED_LENGTH, b"\x00"
    )
    with pytest.raises(ValueError):
        MotorBitMessage.into_base_model(message)
