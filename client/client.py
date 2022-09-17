import asyncio
import traceback

import json

from .JsonClientProto import JsonClientProtocol


class _4DMinerClientProtocol(JsonClientProtocol):
    def handle_bytes(self, data):
        print(f"Got bytes: b{data!r}")

    def handle_json(self, data):
        print(f"Got Json {data!r}")
        self.send_data({"KeepAlive": True})

    def handle_connection_made(self):
        self.send_data("Hello, World!")

    def handle_connection_removed(self):

        print(f"connection to {self.ip} stoped")


async def runclient():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_connection(
        lambda: _4DMinerClientProtocol(), "127.0.0.1", 8888
    )

    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        while True:
            if transport.is_closing():
                break
            else:
                await asyncio.sleep(1)
    except:
        pass
    finally:
        transport.close()


def run_client():
    asyncio.run(runclient())
