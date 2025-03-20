import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# from proto.base import MotorMessage
# from proto.bit import MotorBitMessage
from generated.bit_pb2 import MotorMessage, ControlCommand
from google.protobuf.timestamp_pb2 import Timestamp

data = MotorMessage(
    message_id="unique_message_id",
    timestamp=Timestamp(seconds=0, nanos=0),
    control=ControlCommand.CENTER,
    query=None,
    position_set=None,
    status_report=None,
    metadata=None,
)

print(data)
print(data.SerializeToString())
print(MotorMessage.FromString(data.SerializeToString()))
print(MotorMessage.FromString(data.SerializeToString()).control)
print(
    MotorMessage.FromString(data.SerializeToString()).control == ControlCommand.CENTER
)
