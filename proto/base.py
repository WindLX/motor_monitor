from pydantic import BaseModel, conint


class MotorCommand(BaseModel):
    command: conint(ge=1, le=8)  # type: ignore


class SetPositionData(BaseModel):
    motor_id: conint(ge=0, le=7)  # type: ignore
    position: conint()  # type: ignore


class SetVelocityData(BaseModel):
    motor_id: conint(ge=0, le=7)  # type: ignore
    velocity: conint()  # type: ignore


class SetCurrentData(BaseModel):
    motor_id: conint(ge=0, le=7)  # type: ignore
    current: conint()  # type: ignore


class GetStateData(BaseModel):
    motor_id: conint(ge=0, le=7)  # type: ignore
    position: conint()  # type: ignore
    velocity: conint()  # type: ignore
    current: conint()  # type: ignore


class MotorMessage(BaseModel):
    command: MotorCommand
    data: (
        list[
            SetPositionData
            | SetVelocityData
            | SetVelocityData
            | SetCurrentData
            | GetStateData
        ]
        | None
    ) = None

    @classmethod
    def create_message(
        cls,
        command: int,
        data: list[dict] | None = None,
    ):
        if command in [1, 2, 3, 4]:
            if data is not None:
                raise ValueError(
                    "Data should not be provided for commands 1, 2, 3, and 4"
                )
            return cls(command=MotorCommand(command=command), data=None)

        if data is None or len(data) > 8:
            raise ValueError("Data must be provided and its length cannot exceed 8")

        data_classes = {
            5: SetPositionData,
            6: SetVelocityData,
            7: SetCurrentData,
            8: GetStateData,
        }

        if command in data_classes:
            data_class = data_classes[command]
            data_instances = [data_class(**item) for item in data]
            return cls(command=MotorCommand(command=command), data=data_instances)

        raise ValueError("Invalid command or missing parameters")
