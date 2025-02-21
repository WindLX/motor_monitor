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
    HEADER_FORMAT: str = "!BH"  # 1 byte for header, 2 bytes for length
    POSITION_FORMAT: str = "!BQ"  # 1 byte for motor id, 8 bytes for position (float)

    @staticmethod
    def from_base_model(message: MotorMessage) -> bytes:
        if message.command.command in [
            MotorBitCommand.START,
            MotorBitCommand.ZERO,
            MotorBitCommand.CENTER,
            MotorBitCommand.STOP,
        ]:
            header: int = (1 << 4) | message.command.command
            length: int = 3  # 1 byte for header + 2 bytes for length
            return struct.pack(MotorBit.HEADER_FORMAT, header, length)
        elif (
            message.command.command == MotorBitCommand.SET_POSITION
            and message.data is not None
        ):
            header: int = (2 << 4) | message.command.command
            data: bytes = b""
            for motor in message.data:
                motor_id = motor.motor_id
                position = motor.position
                data += struct.pack(
                    MotorBit.POSITION_FORMAT,
                    motor_id,
                    struct.unpack("!Q", struct.pack("!d", position))[0],
                )
            length: int = 3 + len(
                data
            )  # 1 byte for header + 2 bytes for length + data length
            return struct.pack(MotorBit.HEADER_FORMAT, header, length) + data
        else:
            raise ValueError("Invalid command or missing parameters")

    @staticmethod
    def into_base_model(message: bytes) -> MotorMessage:
        header, length = struct.unpack(MotorBit.HEADER_FORMAT, message[:3])
        if len(message) != length:
            raise ValueError(
                "Message length does not match the length specified in the header"
            )
        command = header & 0x0F
        if command in [
            MotorBitCommand.START,
            MotorBitCommand.ZERO,
            MotorBitCommand.CENTER,
            MotorBitCommand.STOP,
        ]:
            return MotorMessage.create_message(command)
        elif command == MotorBitCommand.SET_POSITION:
            data: list[dict[str, float]] = []
            for i in range(3, length, 9):
                motor_id, position_bits = struct.unpack(
                    MotorBit.POSITION_FORMAT, message[i : i + 9]
                )
                position = struct.unpack("!d", struct.pack("!Q", position_bits))[0]
                data.append({"motor_id": motor_id, "position": position})
            return MotorMessage.create_message(command=command, data=data)
        else:
            raise ValueError("Invalid command")
