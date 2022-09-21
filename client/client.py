import asyncio

from .Protocall import _4DMinerClientProtocol


class Client:
    def __init__(self):
        self.known_host = None
        self.id = None

    def add_protocall(self, protocall: _4DMinerClientProtocol):
        self.protocall: _4DMinerClientProtocol = protocall


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
