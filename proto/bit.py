import struct

from proto.base import (
    MotorMessage,
    MotorCommand,
    SetPositionData,
    SetVelocityData,
    SetCurrentData,
    GetStateData,
)


class MotorBitCommand:
    START = 1
    ZERO = 2
    CENTER = 3
    STOP = 4
    SET_POSITION = 5
    SET_VELOCITY = 6
    SET_CURRENT = 7
    GET_STATE = 8

    def into_base_model(self) -> MotorCommand:
        return MotorCommand(command=self)


class MotorBitMessage:
    HEADER_FORMAT: str = "!B"  # 1 byte for header
    LENGTH_FORMAT: str = "!B"  # 1 byte for array length
    MOTOR_ID_FORMAT: str = "!B"  # 1 byte for motor id
    INT_FORMAT: str = "!i"  # 4 bytes for integers (position, velocity, current)
    FIXED_LENGTH: int = 138  # Fixed length for the message

    @staticmethod
    def from_base_model(message: MotorMessage) -> bytes:
        header: int = message.command.command
        data: bytes = struct.pack(MotorBitMessage.HEADER_FORMAT, header)

        if message.command.command in [
            MotorBitCommand.START,
            MotorBitCommand.ZERO,
            MotorBitCommand.CENTER,
            MotorBitCommand.STOP,
        ]:
            return data.ljust(MotorBitMessage.FIXED_LENGTH, b"\x00")

        if message.data is None or len(message.data) > 8:
            raise ValueError("Data must be provided and its length cannot exceed 8")

        array_length: int = len(message.data)
        data += struct.pack(MotorBitMessage.LENGTH_FORMAT, array_length)

        for item in message.data:
            motor_id = item.motor_id
            data += struct.pack(MotorBitMessage.MOTOR_ID_FORMAT, motor_id)

            if isinstance(item, SetPositionData):
                data += struct.pack(MotorBitMessage.INT_FORMAT, item.position)
                data += struct.pack(MotorBitMessage.INT_FORMAT, 0)  # velocity
                data += struct.pack(MotorBitMessage.INT_FORMAT, 0)  # current
            elif isinstance(item, SetVelocityData):
                data += struct.pack(MotorBitMessage.INT_FORMAT, 0)  # position
                data += struct.pack(MotorBitMessage.INT_FORMAT, item.velocity)
                data += struct.pack(MotorBitMessage.INT_FORMAT, 0)  # current
            elif isinstance(item, SetCurrentData):
                data += struct.pack(MotorBitMessage.INT_FORMAT, 0)  # position
                data += struct.pack(MotorBitMessage.INT_FORMAT, 0)  # velocity
                data += struct.pack(MotorBitMessage.INT_FORMAT, item.current)
            elif isinstance(item, GetStateData):
                data += struct.pack(MotorBitMessage.INT_FORMAT, item.position)
                data += struct.pack(MotorBitMessage.INT_FORMAT, item.velocity)
                data += struct.pack(MotorBitMessage.INT_FORMAT, item.current)

        return data.ljust(MotorBitMessage.FIXED_LENGTH, b"\x00")

    @staticmethod
    def into_base_model(message: bytes) -> MotorMessage:
        if len(message) != MotorBitMessage.FIXED_LENGTH:
            raise ValueError("Message length does not match the fixed length")

        header = struct.unpack(MotorBitMessage.HEADER_FORMAT, message[:1])[0]
        command = header & 0x0F

        if command in [
            MotorBitCommand.START,
            MotorBitCommand.ZERO,
            MotorBitCommand.CENTER,
            MotorBitCommand.STOP,
        ]:
            return MotorMessage.create_message(command)

        array_length = struct.unpack(MotorBitMessage.LENGTH_FORMAT, message[1:2])[0]
        data: list[dict[str, int]] = []

        for i in range(2, 2 + array_length * 13, 13):
            motor_id = struct.unpack(
                MotorBitMessage.MOTOR_ID_FORMAT, message[i : i + 1]
            )[0]
            position = struct.unpack(
                MotorBitMessage.INT_FORMAT, message[i + 1 : i + 5]
            )[0]
            velocity = struct.unpack(
                MotorBitMessage.INT_FORMAT, message[i + 5 : i + 9]
            )[0]
            current = struct.unpack(
                MotorBitMessage.INT_FORMAT, message[i + 9 : i + 13]
            )[0]
            data.append(
                {
                    "motor_id": motor_id,
                    "position": position,
                    "velocity": velocity,
                    "current": current,
                }
            )

        data_classes = {
            5: SetPositionData,
            6: SetVelocityData,
            7: SetCurrentData,
            8: GetStateData,
        }

        if command in data_classes:
            data_class = data_classes[command]
            data_instances = [data_class(**item).model_dump() for item in data]
            return MotorMessage.create_message(command=command, data=data_instances)

        raise ValueError("Invalid command or missing parameters")
