from pydantic import BaseModel, conint
from typing import Optional


class MotorCommand(BaseModel):
    command: conint(ge=1, le=5)


class SetPositionData(BaseModel):
    motor_id: conint(ge=0, le=15)
    position: conint()


class MotorMessage(BaseModel):
    command: MotorCommand
    data: Optional[list[SetPositionData]] = None

    @classmethod
    def create_message(
        cls,
        command: int,
        data: Optional[list[dict]] = None,
    ):
        if command in [1, 2, 3, 4]:
            return cls(command=MotorCommand(command=command))
        elif command == 5:
            if data is None or len(data) > 16:
                raise ValueError("Data must be provided and its length cannot exceed 16")
            set_position_data = [SetPositionData(**item) for item in data]
            return cls(command=MotorCommand(command=command), data=set_position_data)
        else:
            raise ValueError("Invalid command or missing parameters")
