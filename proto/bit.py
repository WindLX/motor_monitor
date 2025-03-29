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


class MotorBitMessage:
    UUID_FORMAT: str = "!16s"  # 16 bytes for UUID
    TIMESTAMP_FORMAT: str = "!d"  # 8 bytes for timestamp (f64 in milliseconds)
    MESSAGE_TYPE_FORMAT: str = "!B"  # 1 byte for message type
    LENGTH_FORMAT: str = "!B"  # 1 byte for array length
    MOTOR_ID_FORMAT: str = "!B"  # 1 byte for motor id
    POSITION_FORMAT: str = "!Q"  # 8 bytes for position (uint64)
    DIRECTION_FORMAT: str = "!B"  # 1 byte for direction
    STATE_FORMAT: str = "!Q"  # 8 bytes for position, velocity, torque
    FIXED_LENGTH: int = 176  # Fixed length for the message

    @staticmethod
    def from_base_model(message: MotorMessage) -> bytes:
        id = message.id.bytes.ljust(16, b"\x00")
        timestamp = message.timestamp
        message_type = message.message_type
        data = struct.pack(
            f"!{MotorBitMessage.UUID_FORMAT[1:]}{MotorBitMessage.TIMESTAMP_FORMAT[1:]}{MotorBitMessage.MESSAGE_TYPE_FORMAT[1:]}",
            id,
            timestamp,
            message_type,
        )

        if message.payload is None:
            return data.ljust(MotorBitMessage.FIXED_LENGTH, b"\x00")

        if isinstance(message.payload, list):
            array_length = len(message.payload)
            if array_length > 6:
                raise ValueError("Payload length cannot exceed 6")
            data += struct.pack(MotorBitMessage.LENGTH_FORMAT, array_length)

            for item in message.payload:
                motor_id = item.motor_id
                data += struct.pack(MotorBitMessage.MOTOR_ID_FORMAT, motor_id)

                if isinstance(item, CC_M_MANUAL_Data):
                    data += struct.pack(
                        MotorBitMessage.POSITION_FORMAT, item.target_position
                    )
                elif isinstance(item, CC_M_STEP_CORRECTION_Data):
                    data += struct.pack(
                        MotorBitMessage.DIRECTION_FORMAT, item.direction
                    )
                elif isinstance(item, QS_M_STATE_Data):
                    data += struct.pack(MotorBitMessage.STATE_FORMAT, item.position)
                    data += struct.pack(MotorBitMessage.STATE_FORMAT, item.velocity)
                    data += struct.pack(MotorBitMessage.STATE_FORMAT, item.torque)

        elif isinstance(message.payload, QS_SM_STATE_Data):
            data += struct.pack("!B", message.payload.state)

        return data.ljust(MotorBitMessage.FIXED_LENGTH, b"\x00")

    @staticmethod
    def into_base_model(message: bytes) -> MotorMessage:
        if len(message) != MotorBitMessage.FIXED_LENGTH:
            raise ValueError("Message length does not match the fixed length")

        id, timestamp, header = struct.unpack(
            f"!{MotorBitMessage.UUID_FORMAT[1:]}{MotorBitMessage.TIMESTAMP_FORMAT[1:]}{MotorBitMessage.MESSAGE_TYPE_FORMAT[1:]}",
            message[:25],
        )
        id = id.hex()
        id = uuid.UUID(hex=id)
        type_ = header

        if type_ in range(1, 50):  # Commands without payload
            return MotorMessage(message_type=type_, id=id, timestamp=timestamp)

        if type_ in range(51, 100):  # Commands with payload
            array_length = struct.unpack(MotorBitMessage.LENGTH_FORMAT, message[25:26])[
                0
            ]
            payload = []
            offset = 26
            for _ in range(array_length):
                motor_id = struct.unpack(
                    MotorBitMessage.MOTOR_ID_FORMAT, message[offset : offset + 1]
                )[0]
                offset += 1

                if type_ == MotorMessageTypeEnum.CC_M_MANUAL:
                    target_position = struct.unpack(
                        MotorBitMessage.POSITION_FORMAT, message[offset : offset + 8]
                    )[0]
                    offset += 8
                    payload.append(
                        CC_M_MANUAL_Data(
                            motor_id=motor_id, target_position=target_position
                        )
                    )
                elif type_ == MotorMessageTypeEnum.CC_M_STEP_CORRECTION:
                    direction = struct.unpack(
                        MotorBitMessage.DIRECTION_FORMAT, message[offset : offset + 1]
                    )[0]
                    offset += 1
                    payload.append(
                        CC_M_STEP_CORRECTION_Data(
                            motor_id=motor_id, direction=direction
                        )
                    )

            return MotorMessage(
                message_type=type_, id=id, timestamp=timestamp, payload=payload
            )

        if type_ in range(101, 200):  # Query status messages
            if type_ == MotorMessageTypeEnum.QS_SM_STATE:
                state = struct.unpack("!B", message[25:26])[0]
                payload = QS_SM_STATE_Data(state=state)
                return MotorMessage(
                    message_type=type_, id=id, timestamp=timestamp, payload=payload
                )
            elif type_ == MotorMessageTypeEnum.QS_M_STATE:
                array_length = struct.unpack(
                    MotorBitMessage.LENGTH_FORMAT, message[25:26]
                )[0]
                payload = []
                offset = 26
                for _ in range(array_length):
                    motor_id = struct.unpack(
                        MotorBitMessage.MOTOR_ID_FORMAT, message[offset : offset + 1]
                    )[0]
                    offset += 1
                    position = struct.unpack(
                        MotorBitMessage.STATE_FORMAT, message[offset : offset + 8]
                    )[0]
                    velocity = struct.unpack(
                        MotorBitMessage.STATE_FORMAT, message[offset + 8 : offset + 16]
                    )[0]
                    torque = struct.unpack(
                        MotorBitMessage.STATE_FORMAT, message[offset + 16 : offset + 24]
                    )[0]
                    offset += 24
                    payload.append(
                        QS_M_STATE_Data(
                            motor_id=motor_id,
                            position=position,
                            velocity=velocity,
                            torque=torque,
                        )
                    )
                return MotorMessage(
                    message_type=type_, id=id, timestamp=timestamp, payload=payload
                )

        raise ValueError("Invalid message or missing parameters")
