from contextlib import asynccontextmanager

from rich import print
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from model.bit import MotorMessage
from proto.request import MotorMessageRequest
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
    return {"downstream": config.downstream.model_dump()}


@app.post("/cmd")
async def handle_command(request: MotorMessageRequest):
    try:
        motor_message = MotorMessage.create_message(
            command=request.command, data=request.data
        )
        print(f"[bold green][FastAPI Server][/bold green] Received request: {request}")
        udp_node.send_bit(motor_message)
        err = udp_node.get_error()
        if err:
            raise HTTPException(status_code=500, detail=str(err))
        print(f"[bold green][FastAPI Server][/bold green] Command sent")
        return {"message": "Command sent"}
    except ValueError as e:
        print(f"[bold red][FastAPI Server] Error:[/bold red] {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.websocket("/state")
async def websocket_state(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            motor_state = await udp_node.get_state()
            await websocket.send_json(motor_state.model_dump())
    except WebSocketDisconnect:
        print(f"[bold red][FastAPI Server][/bold red] WebSocket disconnected")
