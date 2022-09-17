import asyncio
import traceback

import json

from .JsonServerProto import JsonProtocol, Server


class _4DMinerServerProtocol(JsonProtocol):
    def handle_bytes(self, data):
        print(f"Got bytes: b{data!r}")
        self.send_data({"data": data, "KeepAlive": True})

    def handle_json(self, data):
        print(f"Got Json {data!r}")
        self.send_data({"KeepAlive": True})

    def handle_connection_made(self):
        pass

    def handle_connection_removed(self):
        print(f"connection from {self.ip} stoped")
