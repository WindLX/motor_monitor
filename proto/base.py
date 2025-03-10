from pydantic import BaseModel, conint


class MotorCommandEnum:
    START = 1
    ZERO = 2
    CENTER = 3
    STOP = 4
    AUTO = 5
    DISABLE = 6
    CLEAR_STATE_MACHINE_ERROR = 7
    GET_STATE = 100
    SET_POSITION = 101


class MotorCommand(BaseModel):
    command: conint(ge=1, le=255)  # type: ignore


class SetPositionData(BaseModel):
    motor_id: conint(ge=0, le=7)  # type: ignore
    position: conint()  # type: ignore


class GetStateData(BaseModel):
    motor_id: conint(ge=0, le=7)  # type: ignore
    position: conint()  # type: ignore
    velocity: conint()  # type: ignore
    torque: conint()  # type: ignore


class MotorMessage(BaseModel):
    command: MotorCommand
    data: list[SetPositionData | GetStateData] | None = None

    @classmethod
    def create_message(
        cls,
        command: int,
        data: list[dict] | None = None,
    ):
        if command in [
            MotorCommandEnum.START,
            MotorCommandEnum.ZERO,
            MotorCommandEnum.CENTER,
            MotorCommandEnum.STOP,
            MotorCommandEnum.AUTO,
            MotorCommandEnum.DISABLE,
            MotorCommandEnum.CLEAR_STATE_MACHINE_ERROR,
        ]:
            if data is not None:
                raise ValueError("Data should not be provided for commands 1-7")
            return cls(command=MotorCommand(command=command), data=None)

        if data is None or len(data) > 8:
            raise ValueError("Data must be provided and its length cannot exceed 8")

        data_classes = {
            MotorCommandEnum.GET_STATE: GetStateData,
            MotorCommandEnum.SET_POSITION: SetPositionData,
        }

        if command in data_classes:
            data_class = data_classes[command]
            data_instances = [data_class(**item) for item in data]
            return cls(command=MotorCommand(command=command), data=data_instances)

        raise ValueError("Invalid command or missing parameters")
