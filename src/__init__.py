import asyncio
import traceback

import json

from .JsonServerProto import Server
from .server import _4DMinerServerProtocol


async def _make_and_run():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    ServerSharedData = Server()
    server = await loop.create_server(
        lambda: _4DMinerServerProtocol(ServerSharedData), "127.0.0.1", 8888
    )

    ServerSharedData.add_server(server)

    async with server:
        await server.serve_forever()


def runserver():
    asyncio.run(_make_and_run())


if __name__ == "__main__":
    runserver()
