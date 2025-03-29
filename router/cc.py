from fastapi import APIRouter, HTTPException
from service.udp import UDPNode

from model.net import (
    MotorNetMessageControlCommand,
    CC_M_MANUAL_Payload,
    CC_M_STEP_CORRECTION_Payload,
    MotorNetMessageResponse,
)

router = APIRouter()
udp_node = (
    UDPNode.get_instance()
)  # Assuming UDPNode is a singleton or has a global instance


async def handle_command(request: MotorNetMessageControlCommand):
    try:
        motor_message = request.into_base_model()
        udp_node.send_bit(motor_message)
        err = udp_node.get_error()
        if err:
            raise HTTPException(status_code=500, detail=str(err))
        return MotorNetMessageResponse.build(raw_message=request)
    except ValueError as e:
        return MotorNetMessageResponse.build(raw_message=request, error_message=str(e))


@router.post("/p/start")
async def handle_start():
    return await handle_command(MotorNetMessageControlCommand.cc_p_start())


@router.post("/p/zero")
async def handle_zero():
    return await handle_command(MotorNetMessageControlCommand.cc_p_zero())


@router.post("/p/center")
async def handle_center():
    return await handle_command(MotorNetMessageControlCommand.cc_p_center())


@router.post("/p/brake")
async def handle_brake():
    return await handle_command(MotorNetMessageControlCommand.cc_p_brake())


@router.post("/p/auto")
async def handle_auto():
    return await handle_command(MotorNetMessageControlCommand.cc_p_auto())


@router.post("/p/disable")
async def handle_disable():
    return await handle_command(MotorNetMessageControlCommand.cc_p_disable())


@router.post("/sm/clean_error")
async def handle_clean_error():
    return await handle_command(MotorNetMessageControlCommand.cc_sm_clean_error())


@router.post("/p/enter_correction")
async def handle_enter_correction():
    return await handle_command(MotorNetMessageControlCommand.cc_p_enter_correction())


@router.post("/p/exit_correction")
async def handle_exit_correction():
    return await handle_command(MotorNetMessageControlCommand.cc_p_exit_correction())


@router.post("/m/manual")
async def handle_manual(payload: CC_M_MANUAL_Payload):
    return await handle_command(MotorNetMessageControlCommand.cc_m_manual(payload))


@router.post("/m/step_correction")
async def handle_step_correction(payload: CC_M_STEP_CORRECTION_Payload):
    return await handle_command(
        MotorNetMessageControlCommand.cc_m_step_correction(payload)
    )
