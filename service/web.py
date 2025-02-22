from contextlib import asynccontextmanager

from rich import print
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from proto.base import MotorMessage
from proto.request import CommandRequest
from service.udp import UDPClient
from service.config import load_config

config = load_config("./config/config.toml")

udp_client = UDPClient(config.downstream.host, config.downstream.port)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await udp_client.start_client()
        yield
    finally:
        udp_client.close()


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
async def handle_command(request: CommandRequest):
    try:
        motor_message = MotorMessage.create_message(
            command=request.command, data=request.data
        )
        print(f"[bold green][FastAPI Server][/bold green] Received request: {request}")
        udp_client.send_bit(motor_message)
        err = udp_client.get_error()
        if err:
            raise HTTPException(status_code=500, detail=str(err))
        print(f"[bold green][FastAPI Server][/bold green] Command sent")
        return {"message": "Command sent"}
    except ValueError as e:
        print(f"[bold red][FastAPI Server] Error:[/bold red] {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
