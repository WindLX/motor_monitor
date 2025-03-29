from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from service.udp import UDPNode

from model.net import (
    MotorNetMessageQueryStatus,
    MotorNetMessageResponse,
)

router = APIRouter()
udp_node = (
    UDPNode.get_instance()
)  # Assuming UDPNode is a singleton or has a global instance


class QueryStatusTypeEnum(str):
    M_STATE = "M_STATE"
    SM_STATE = "SM_STATE"


@router.websocket("/qs/{query_type}")
async def handle_query_endpoint(websocket: WebSocket, query_type: str):
    await websocket.accept()
    try:
        query = QueryStatusTypeEnum(query_type.upper())
        while True:
            if query == QueryStatusTypeEnum.M_STATE:
                state = await udp_node.get_m_state()
            elif query == QueryStatusTypeEnum.SM_STATE:
                state = await udp_node.get_sm_state()
            else:
                raise ValueError(f"Unsupported query type: {query_type}")
            state = MotorNetMessageQueryStatus.from_base_model(state)
            net_msg = MotorNetMessageResponse.build(raw_message=state)
            await websocket.send_json(net_msg.model_dump())
    except WebSocketDisconnect:
        print("[FastAPI Server] WebSocket disconnected")
    except ValueError as e:
        print(f"[FastAPI Server] Error: {str(e)}")
        await websocket.close(code=4000, reason=str(e))
