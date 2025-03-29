from contextlib import asynccontextmanager

from rich import print
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from model.net import (
    MotorNetMessageControlCommand,
    MotorNetMessageQueryStatus,
    CC_M_MANUAL_Payload,
    CC_M_STEP_CORRECTION_Payload,
    QS_M_STATE_Payload,
    QS_SM_STATE_Payload,
    MotorNetMessageResponse,
)
from service.udp import UDPNode
from service.config import load_config

config = load_config("./config/config.toml")

udp_node = UDPNode(
    config.udp_node.host,
    config.udp_node.port,
    config.downstream.host,
    config.downstream.port,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await udp_node.start_node()
        yield
    finally:
        udp_node.close()


app = FastAPI(lifespan=lifespan)


# Set up CORS
origins = ["http://localhost", "http://localhost:8000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
        <head>
            <title>Motor Monitor</title>
        </head>
        <body>
            <h1>Motor Monitor Api is working</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/downstream")
async def handle_downstream():
    return config.downstream


async def handle_command(request: MotorNetMessageControlCommand):
    try:
        motor_message = request.into_base_model()
        print(f"[bold green][FastAPI Server][/bold green] Received request: {request}")
        udp_node.send_bit(motor_message)
        err = udp_node.get_error()
        if err:
            raise HTTPException(status_code=500, detail=str(err))
        print(f"[bold green][FastAPI Server][/bold green] Command sent")
        return MotorNetMessageResponse.build(raw_message=request)
    except ValueError as e:
        print(f"[bold red][FastAPI Server] Error:[/bold red] {str(e)}")
        return MotorNetMessageResponse.build(raw_message=request, error_message=str(e))


@app.post("/cc/p/start")
async def handle_start():
    return await handle_command(MotorNetMessageControlCommand.cc_p_start())


@app.post("/cc/p/zero")
async def handle_zero():
    return await handle_command(MotorNetMessageControlCommand.cc_p_zero())


@app.post("/cc/p/center")
async def handle_center():
    return await handle_command(MotorNetMessageControlCommand.cc_p_center())


@app.post("/cc/p/brake")
async def handle_brake():
    return await handle_command(MotorNetMessageControlCommand.cc_p_brake())


@app.post("/cc/p/auto")
async def handle_auto():
    return await handle_command(MotorNetMessageControlCommand.cc_p_auto())


@app.post("/cc/p/disable")
async def handle_disable():
    return await handle_command(MotorNetMessageControlCommand.cc_p_disable())


@app.post("/cc/sm/clean_error")
async def handle_clean_error():
    return await handle_command(MotorNetMessageControlCommand.cc_sm_clean_error())


@app.post("cc/p/enter_correction")
async def handle_enter_correction():
    return await handle_command(MotorNetMessageControlCommand.cc_p_enter_correction())


@app.post("cc/p/exit_correction")
async def handle_exit_correction():
    return await handle_command(MotorNetMessageControlCommand.cc_p_exit_correction())


@app.post("/cc/m/manual")
async def handle_manual(payload: CC_M_MANUAL_Payload):
    return await handle_command(MotorNetMessageControlCommand.cc_m_manual(payload))


@app.post("/cc/m/step_correction")
async def handle_step_correction(payload: CC_M_STEP_CORRECTION_Payload):
    return await handle_command(
        MotorNetMessageControlCommand.cc_m_step_correction(payload)
    )


class QueryStatusTypeEnum(str):
    M_STATE = "M_STATE"
    SM_STATE = "SM_STATE"


@app.websocket("/qs/{query_type}")
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
        print(f"[bold red][FastAPI Server][/bold red] WebSocket disconnected")
    except ValueError as e:
        print(f"[bold red][FastAPI Server] Error:[/bold red] {str(e)}")
        await websocket.close(code=4000, reason=str(e))
