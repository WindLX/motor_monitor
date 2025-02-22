import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from typing import Optional

import asyncio
from rich import print

from service.config import load_config


class UDPServerProtocol:
    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        self.transport = transport
        print("[bold yellow][UDP Server][/bold yellow] Connection made")

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        print(f"[bold yellow][UDP Server][/bold yellow] Received {data} from {addr}")
        self.transport.sendto(b"ACK", addr)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        print(f"[bold yellow][UDP Server][/bold yellow] Connection lost: {exc}")


async def main():
    config = load_config("./config/config.toml")
    loop = asyncio.get_running_loop()
    listen = loop.create_datagram_endpoint(
        UDPServerProtocol, local_addr=(config.downstream.host, config.downstream.port)
    )
    transport, protocol = await listen
    print(
        "[bold yellow][UDP Server][/bold yellow] Server started on {}:{}".format(
            config.downstream.host, config.downstream.port
        )
    )

    try:
        await asyncio.sleep(3600)  # Run for 1 hour
    finally:
        transport.close()
        print("[bold yellow][UDP Server][/bold yellow] Server closed")


if __name__ == "__main__":
    asyncio.run(main())
