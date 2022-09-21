import asyncio
import json
import traceback
from typing import TYPE_CHECKING

from .JsonServerProto import JsonProtocol

if TYPE_CHECKING:
    from Server import Server


class _4DMinerServerProtocol(JsonProtocol):
    server: "Server"

    Codes = {
        "BadRequest": [503, "Error 503: Bad Request"],
        "test": [0, "Info 0: test"],
        "OK": [200, "Info 200: OK"],
        "HostExists": [303, "Error 303: World Host taken"],
        "NotValidCommand": [404, "Error 404: Command Not Found"],
        "Internal": [500, "Error 500: An internal Error Accured"],
        "NotLoggedIn": [301, "Error 301: Not Logged in"],
    }

    def handle_bytes(self, data):

        print(f"Got bytes: b{data!r}")
        self.send_data({"data": data, "KeepAlive": True})

    def handle_json(self, data):
        print(f"Got Json {data!r}")

        # Checking all of the data for cmds, and stuff like that
        try:
            if "val" not in data.keys():
                raise AssertionError
            if "type" not in data.keys():
                raise AssertionError

            if data["type"] == "command" and "command" not in data.keys():
                raise AssertionError

        except AssertionError:
            self.send_data(
                {"KeepAlive": False, "type": "Error", "val": self.Codes["BadRequest"]}
            )
            return

        self.handle_cmds()

    def handle_connection_made(self):

        pass

    def handle_connection_removed(self):
        print(f"connection from {self.ip} stoped")
        self.server.connected.remove(self.id)
        if self.server.CurrentWorldHost == self.id:
            self.server.CurrentWorldHost = None
            self.server.send_to_all(
                {
                    "KeepAlive": True,
                    "type": "Command",
                    "command": "WorldHostLeft",
                    "val": self.id,
                }
            )

    def handle_cmds(self, data):
        NoneCommands = ["__init__", "add_server", "send_to_all"]

        not_found = lambda *args, **kwargs: self.send_data(
            {"KeepAlive": False, "Type": "Error", "val": self.codes["NotValidCommand"]}
        )
        if data["command"] in NoneCommands:
            not_found()
            return
        try:
            getattr(self, data["command"], not_found)(data["val"], client=self)
        except:
            self.send_data(
                {"KeepAlive": False, "Type": "Error", "val": self.Codes["Internal"]}
            )
