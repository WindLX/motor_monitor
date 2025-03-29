import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from model.base import MotorMessage, CC_M_MANUAL_Data, MotorMessageTypeEnum
from proto.bit import MotorBitMessage

data = MotorMessage.build(
    message_type=MotorMessageTypeEnum.CC_M_MANUAL,
    payload=[CC_M_MANUAL_Data(motor_id=1, target_position=1000)],
)
encoded = MotorBitMessage.from_base_model(data)
print(encoded)
decoded = MotorBitMessage.into_base_model(encoded)
print(decoded)
assert data == decoded
