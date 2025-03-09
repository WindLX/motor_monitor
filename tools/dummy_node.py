from typing import Optional

import sys
import os
import random
import asyncio

from rich import print

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


from service.config import load_config
from proto.base import MotorMessage
from proto.bit import MotorBitMessage


def generate_random_motor_state():
    return MotorBitMessage.from_base_model(
        MotorMessage.create_message(
            command=100,
            data=[
                {
                    "motor_id": 1,
                    "position": random.randint(0, 10000),
                    "velocity": random.randint(0, 100),
                    "current": random.randint(0, 10),
                },
                {
                    "motor_id": 2,
                    "position": random.randint(0, 10000),
                    "velocity": random.randint(0, 100),
                    "current": random.randint(0, 10),
                },
                {
                    "motor_id": 3,
                    "position": random.randint(0, 10000),
                    "velocity": random.randint(0, 100),
                    "current": random.randint(0, 10),
                },
                {
                    "motor_id": 4,
                    "position": random.randint(0, 10000),
                    "velocity": random.randint(0, 100),
                    "current": random.randint(0, 10),
                },
            ],
        )
    )


class DummyNode:
    def __init__(self):
        self.transport = None
        self.remote_addr = None

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        self.transport = transport
        print("[bold yellow][UDP Server][/bold yellow] Connection made")

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        msg = MotorBitMessage.into_base_model(data)
        print(f"[bold yellow][UDP Server][/bold yellow] Received {msg} from {addr}")
        self.remote_addr = addr
        # self.transport.sendto(b"ACK", addr)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        print(f"[bold yellow][UDP Server][/bold yellow] Connection lost: {exc}")

    async def send_periodic_data(self):
        while True:
            if self.remote_addr:
                self.transport.sendto(generate_random_motor_state(), self.remote_addr)
                print(
                    f"[bold yellow][UDP Server][/bold yellow] Sent periodic data to {self.remote_addr}"
                )
            await asyncio.sleep(1)  # Send data every 1 seconds


async def main():
    config = load_config("./config/config.toml")
    loop = asyncio.get_running_loop()
    listen = loop.create_datagram_endpoint(
        DummyNode,
        local_addr=(config.downstream.host, config.downstream.port),
    )
    transport, protocol = await listen
    print(
        "[bold yellow][UDP Server][/bold yellow] Server started on {}:{}".format(
            config.downstream.host, config.downstream.port
        )
    )

    try:
        await asyncio.gather(
            asyncio.sleep(3600), protocol.send_periodic_data()  # Run for 1 hour
        )
    finally:
        transport.close()
        print("[bold yellow][UDP Server][/bold yellow] Server closed")


if __name__ == "__main__":
    asyncio.run(main())
