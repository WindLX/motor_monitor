import struct

from proto.base import (
    MotorMessage,
    MotorCommandEnum,
    SetPositionData,
    GetStateData,
)


class MotorBitMessage:
    HEADER_FORMAT: str = "!B"  # 1 byte for header
    LENGTH_FORMAT: str = "!B"  # 1 byte for array length
    MOTOR_ID_FORMAT: str = "!B"  # 1 byte for motor id
    STATE_FORMAT: str = "!i"  # 4 bytes for integers (position, velocity, torque)
    FIXED_LENGTH: int = 138  # Fixed length for the message

    @staticmethod
    def from_base_model(message: MotorMessage) -> bytes:
        header: int = message.command.command
        data: bytes = struct.pack(MotorBitMessage.HEADER_FORMAT, header)

        if message.command.command in [
            MotorCommandEnum.START,
            MotorCommandEnum.ZERO,
            MotorCommandEnum.CENTER,
            MotorCommandEnum.STOP,
            MotorCommandEnum.AUTO,
            MotorCommandEnum.DISABLE,
            MotorCommandEnum.CLEAR_STATE_MACHINE_ERROR,
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
                data += struct.pack(MotorBitMessage.STATE_FORMAT, item.position)
                data += struct.pack(MotorBitMessage.STATE_FORMAT, 0)  # velocity
                data += struct.pack(MotorBitMessage.STATE_FORMAT, 0)  # torque
            elif isinstance(item, GetStateData):
                data += struct.pack(MotorBitMessage.STATE_FORMAT, item.position)
                data += struct.pack(MotorBitMessage.STATE_FORMAT, item.velocity)
                data += struct.pack(MotorBitMessage.STATE_FORMAT, item.torque)

        return data.ljust(MotorBitMessage.FIXED_LENGTH, b"\x00")

    @staticmethod
    def into_base_model(message: bytes) -> MotorMessage:
        if len(message) != MotorBitMessage.FIXED_LENGTH:
            raise ValueError("Message length does not match the fixed length")

        header = struct.unpack(MotorBitMessage.HEADER_FORMAT, message[:1])[0]
        command = header & 0xFF

        if command in [
            MotorCommandEnum.START,
            MotorCommandEnum.ZERO,
            MotorCommandEnum.CENTER,
            MotorCommandEnum.STOP,
            MotorCommandEnum.AUTO,
            MotorCommandEnum.DISABLE,
            MotorCommandEnum.CLEAR_STATE_MACHINE_ERROR,
        ]:
            return MotorMessage.create_message(command)

        array_length = struct.unpack(MotorBitMessage.LENGTH_FORMAT, message[1:2])[0]
        data: list[dict[str, int]] = []

        for i in range(2, 2 + array_length * 13, 13):
            motor_id = struct.unpack(
                MotorBitMessage.MOTOR_ID_FORMAT, message[i : i + 1]
            )[0]
            position = struct.unpack(
                MotorBitMessage.STATE_FORMAT, message[i + 1 : i + 5]
            )[0]
            velocity = struct.unpack(
                MotorBitMessage.STATE_FORMAT, message[i + 5 : i + 9]
            )[0]
            torque = struct.unpack(
                MotorBitMessage.STATE_FORMAT, message[i + 9 : i + 13]
            )[0]
            data.append(
                {
                    "motor_id": motor_id,
                    "position": position,
                    "velocity": velocity,
                    "torque": torque,
                }
            )

        data_classes = {
            MotorCommandEnum.GET_STATE: GetStateData,
            MotorCommandEnum.SET_POSITION: SetPositionData,
        }

        if command in data_classes:
            data_class = data_classes[command]
            data_instances = [data_class(**item).model_dump() for item in data]
            return MotorMessage.create_message(command=command, data=data_instances)

        raise ValueError("Invalid command or missing parameters")
