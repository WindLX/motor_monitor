import asyncio
from proto.bit import MotorBit
from proto.base import MotorMessage


class UDPServer:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.transport = None

    async def start_server(self):
        loop = asyncio.get_running_loop()
        self.transport, _ = await loop.create_datagram_endpoint(
            lambda: self, local_addr=(self.ip, self.port)
        )
        print(f"UDP server started at {self.ip}:{self.port}")

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print(f"Received {data} from {addr}")

    def send_data(self, data: bytes, target_ip: str, target_port: int):
        if self.transport:
            self.transport.sendto(data, (target_ip, target_port))
        else:
            raise RuntimeError("UDP server is not running")

    def send_bit(self, message: MotorMessage, target_ip: str, target_port: int):
        data = MotorBit.from_base_model(message)
        print(f"Sending {data} to {target_ip}:{target_port}")
        self.send_data(data, target_ip, target_port)

    def close(self):
        if self.transport:
            self.transport.close()
        else:
            raise RuntimeError("UDP server is not running")
