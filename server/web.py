from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


from proto.base import MotorMessage
from proto.request import CommandRequest
from server.udp import UDPServer

udp_server = UDPServer("0.0.0.0", 9999)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await udp_server.start_server()
        yield
    finally:
        udp_server.close()


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
            <h1>Welcome to the Motor Monitor</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/cmd")
async def handle_command(request: CommandRequest):
    try:
        motor_message = MotorMessage.create_message(
            command=request.command, data=request.data
        )
        print(f"Received command: {motor_message}")
        udp_server.send_bit(motor_message, request.ip, request.port)
        return {"message": "Command sent"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
