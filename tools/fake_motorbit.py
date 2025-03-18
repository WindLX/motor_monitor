import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from proto.base import MotorMessage
from proto.bit import MotorBitMessage

data = MotorMessage.create_message(
    command=100,
    data=[{"motor_id": 1, "position": 600, "velocity": 1000, "torque": 100}],
)
msg = MotorBitMessage.from_base_model(data)
print(msg)
# print every msg(bytes) in uint8 list
print(list(msg))
