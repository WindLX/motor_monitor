import asyncio
from typing import Optional

from rich import print

from proto.bit import MotorBit
from proto.base import MotorMessage


class UDPClient:
    def __init__(self, downstream_host: str, downstream_port: int):
        self.host = downstream_host
        self.port = downstream_port
        self.transport: Optional[asyncio.DatagramTransport] = None
        self.error_queue: asyncio.Queue = asyncio.Queue()

    async def start_client(self) -> None:
        loop = asyncio.get_running_loop()
        self.transport, _ = await loop.create_datagram_endpoint(
            lambda: self, remote_addr=(self.host, self.port)
        )
        print(
            f"[bold blue][UDP Client][/bold blue]\t Client started and connected to {self.host}:{self.port}"
        )

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        self.transport = transport
        print(f"[bold blue][UDP Client][/bold blue]\t Connection made")

    def connection_lost(self, exc: Optional[Exception]) -> None:
        print(f"[bold red][UDP Client][/bold red]\t Connection lost: {exc}")

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        print(f"[bold blue][UDP Client][/bold blue]\t Received {data} from {addr}")

    def error_received(self, exc: Exception) -> None:
        print(f"[bold red][UDP Client][/bold red]\t Error received: {exc}")
        asyncio.create_task(self.error_queue.put(exc))

    def send_data(self, data: bytes) -> None:
        if self.transport:
            self.transport.sendto(data)
            print(
                f"[bold blue][UDP Client][/bold blue]\t Sending {data} to {self.host}:{self.port}"
            )
        else:
            raise RuntimeError("UDP client is not running")

    def send_bit(self, message: MotorMessage) -> None:
        data = MotorBit.from_base_model(message)
        self.send_data(data)

    def close(self) -> None:
        if self.transport:
            self.transport.close()
            print(f"[bold red][UDP Client][/bold red]\t Client closed")
        else:
            raise RuntimeError("UDP client is not running")

    def get_error(self) -> Optional[Exception]:
        try:
            return self.error_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None
