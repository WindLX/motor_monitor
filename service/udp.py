import asyncio
from typing import Optional

from rich import print

from proto.bit import MotorBitMessage
from proto.base import MotorMessage


class UDPNode:
    def __init__(
        self,
        local_host: str,
        local_port: int,
        downstream_host: str,
        downstream_port: int,
    ):
        self.local_host = local_host
        self.local_port = local_port
        self.downstream_host = downstream_host
        self.downstream_port = downstream_port
        self.transport: Optional[asyncio.DatagramTransport] = None
        self.error_queue: asyncio.Queue = asyncio.Queue()
        self.state_queue: asyncio.Queue = asyncio.Queue()

    async def start_node(self) -> None:
        loop = asyncio.get_running_loop()
        self.transport, _ = await loop.create_datagram_endpoint(
            lambda: self, local_addr=(self.local_host, self.local_port)
        )
        print(
            f"[bold blue][UDP Node][/bold blue]\t Node started and listening on {self.local_host}:{self.local_port}"
        )

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        self.transport = transport
        print(f"[bold blue][UDP Node][/bold blue]\t Connection made")

    def connection_lost(self, exc: Optional[Exception]) -> None:
        print(f"[bold red][UDP Node][/bold red]\t Connection lost: {exc}")

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        try:
            motor_state = MotorBitMessage.into_base_model(data)
            asyncio.create_task(self.state_queue.put(motor_state))
        except Exception as e:
            print(f"[bold red][UDP Node][/bold red]\t Error: {e}")
            asyncio.create_task(self.error_queue.put(e))
        print(f"[bold blue][UDP Node][/bold blue]\t Received {motor_state} from {addr}")

    def error_received(self, exc: Exception) -> None:
        print(f"[bold red][UDP Node][/bold red]\t Error received: {exc}")
        asyncio.create_task(self.error_queue.put(exc))

    def send_data(self, data: bytes) -> None:
        if self.transport:
            self.transport.sendto(data, (self.downstream_host, self.downstream_port))
            print(
                f"[bold blue][UDP Node][/bold blue]\t Sending data to {self.downstream_host}:{self.downstream_port}"
            )
        else:
            raise RuntimeError("UDP node is not running")

    def send_bit(self, message: MotorMessage) -> None:
        data = MotorBitMessage.from_base_model(message)
        self.send_data(data)

    async def get_state(self) -> MotorMessage:
        return await self.state_queue.get()

    def close(self) -> None:
        if self.transport:
            self.transport.close()
            print(f"[bold red][UDP Node][/bold red]\t Node closed")
        else:
            raise RuntimeError("UDP node is not running")

    def get_error(self) -> Optional[Exception]:
        try:
            return self.error_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None
