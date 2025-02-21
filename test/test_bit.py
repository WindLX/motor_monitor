import pytest
import struct

from proto.base import MotorMessage
from proto.bit import MotorBit, MotorBitCommand


def test_from_base_model_start():
    message = MotorMessage.create_message(MotorBitCommand.START)
    result = MotorBit.from_base_model(message)
    expected = struct.pack(MotorBit.HEADER_FORMAT, (1 << 4) | MotorBitCommand.START, 3)
    assert result == expected


def test_from_base_model_set_position():
    message = MotorMessage.create_message(
        command=MotorBitCommand.SET_POSITION,
        data=[{"motor_id": 1, "position": 123.456}],
    )
    result = MotorBit.from_base_model(message)
    header = struct.pack(
        MotorBit.HEADER_FORMAT, (2 << 4) | MotorBitCommand.SET_POSITION, 12
    )
    data = struct.pack(
        MotorBit.POSITION_FORMAT, 1, struct.unpack("!Q", struct.pack("!d", 123.456))[0]
    )
    expected = header + data
    assert result == expected


def test_into_base_model_start():
    message = struct.pack(MotorBit.HEADER_FORMAT, (1 << 4) | MotorBitCommand.START, 3)
    result = MotorBit.into_base_model(message)
    expected = MotorMessage.create_message(command=MotorBitCommand.START)
    assert result.command.command == expected.command.command


def test_into_base_model_set_position():
    header = struct.pack(
        MotorBit.HEADER_FORMAT, (2 << 4) | MotorBitCommand.SET_POSITION, 12
    )
    data = struct.pack(
        MotorBit.POSITION_FORMAT, 1, struct.unpack("!Q", struct.pack("!d", 123.456))[0]
    )
    message = header + data
    result = MotorBit.into_base_model(message)
    expected = MotorMessage.create_message(
        command=MotorBitCommand.SET_POSITION,
        data=[{"motor_id": 1, "position": 123.456}],
    )
    assert result.command.command == expected.command.command
    assert result.data == expected.data


def test_invalid_command_from_base_model():
    with pytest.raises(ValueError):
        message = MotorMessage.create_message(command=99)
        MotorBit.from_base_model(message)


def test_invalid_command_into_base_model():
    message = struct.pack(MotorBit.HEADER_FORMAT, (1 << 4) | 6, 3)
    with pytest.raises(ValueError):
        MotorBit.into_base_model(message)
