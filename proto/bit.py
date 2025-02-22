import struct

from proto.base import MotorMessage, MotorCommand


class MotorBitCommand:
    START = 1
    ZERO = 2
    CENTER = 3
    STOP = 4
    SET_POSITION = 5

    def into_base_model(self) -> MotorCommand:
        return MotorCommand(command=self)


class MotorBit:
    HEADER_FORMAT: str = "!B"  # 1 byte for header
    LENGTH_FORMAT: str = "!B"  # 1 byte for array length
    POSITION_FORMAT: str = "!BQ"  # 1 byte for motor id, 8 bytes for position (int)
    FIXED_LENGTH: int = 146  # Fixed length for the message

    @staticmethod
    def from_base_model(message: MotorMessage) -> bytes:
        if message.command.command in [
            MotorBitCommand.START,
            MotorBitCommand.ZERO,
            MotorBitCommand.CENTER,
            MotorBitCommand.STOP,
        ]:
            header: int = message.command.command
            data: bytes = struct.pack(MotorBit.HEADER_FORMAT, header)
            return data.ljust(MotorBit.FIXED_LENGTH, b"\x00")
        elif (
            message.command.command == MotorBitCommand.SET_POSITION
            and message.data is not None
        ):
            header: int = message.command.command
            array_length: int = len(message.data)
            if array_length > 16:
                raise ValueError("Array length cannot exceed 16")
            data: bytes = struct.pack(MotorBit.HEADER_FORMAT, header)
            data += struct.pack(MotorBit.LENGTH_FORMAT, array_length)
            for motor in message.data:
                motor_id = motor.motor_id
                position = motor.position
                data += struct.pack(
                    MotorBit.POSITION_FORMAT,
                    motor_id,
                    struct.unpack("!Q", struct.pack("!d", position))[0],
                )
            return data.ljust(MotorBit.FIXED_LENGTH, b"\x00")
        else:
            raise ValueError("Invalid command or missing parameters")

    @staticmethod
    def into_base_model(message: bytes) -> MotorMessage:
        if len(message) != MotorBit.FIXED_LENGTH:
            raise ValueError("Message length does not match the fixed length")
        header = struct.unpack(MotorBit.HEADER_FORMAT, message[:1])[0]
        command = header & 0x0F
        if command in [
            MotorBitCommand.START,
            MotorBitCommand.ZERO,
            MotorBitCommand.CENTER,
            MotorBitCommand.STOP,
        ]:
            return MotorMessage.create_message(command)
        elif command == MotorBitCommand.SET_POSITION:
            array_length = struct.unpack(MotorBit.LENGTH_FORMAT, message[1:2])[0]
            data: list[dict[str, float]] = []
            for i in range(2, 2 + array_length * 9, 9):
                motor_id, position_bits = struct.unpack(
                    MotorBit.POSITION_FORMAT, message[i : i + 9]
                )
                position = struct.unpack("!d", struct.pack("!Q", position_bits))[0]
                data.append({"motor_id": motor_id, "position": position})
            return MotorMessage.create_message(command=command, data=data)
        else:
            raise ValueError("Invalid command")
