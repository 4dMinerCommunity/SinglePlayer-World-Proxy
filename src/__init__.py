import asyncio
import json
import traceback

from .Protocall import _4DMinerServerProtocol
from .Server import Server


async def _make_and_run():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = Server()
    Clients = await loop.create_server(
        lambda: _4DMinerServerProtocol(server), "127.0.0.1", 8888
    )

    server.add_server(Clients)

    async with Clients:
        await Clients.serve_forever()


def runserver():
    asyncio.run(_make_and_run())


if __name__ == "__main__":
    runserver()
