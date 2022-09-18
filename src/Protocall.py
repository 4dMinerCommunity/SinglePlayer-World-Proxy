import asyncio
import traceback

import json

from .JsonServerProto import JsonProtocol

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from Server import Server

class _4DMinerServerProtocol(JsonProtocol):
    server: "Server"

    Codes = {
        "BadRequest": [503, "Error 503: Bad Request"],
        "test": [0, "Info 0: test"],
        "OK": [200, "Info 200: OK"],
        "HostExists": [303, "Error 303: World Host taken"],
        "NotValidCommand":[404, "Error 404: Command Not Found"],
        "Internal":[500, "Error 500: An internal Error Accured"]
    }

    def handle_bytes(self, data):
        print(f"Got bytes: b{data!r}")
        self.send_data({"data": data, "KeepAlive": True})

    def handle_json(self, data):
        print(f"Got Json {data!r}")

        #Checking all of the data for cmds, and stuff like that
        try:
            assert 'val' in data.keys()
            assert 'type' in data.keys()

            if data["type"] == "command":
                assert 'command' in data.keys()

        except AssertionError:
            self.send_data({
                "KeepAlive": False,
                "type": "Error",
                "val": self.Codes["BadRequest"]
            })
            return
          

        self.handle_cmds()

    def handle_connection_made(self):
        pass

    def handle_connection_removed(self):
        print(f"connection from {self.ip} stoped")

        if self.server.CurrentWorldHost == self.id:
          self.server.CurrentWorldHost = None
          self.send_data({
            "type":"Command",
            "command":"WorldHostLeft",
            "val":self.id
          })

    def handle_cmds(self, data):
      NoneCommands = ["__init__","add_server"]

      not_found = lambda *args, **kwargs: self.send_data(
          {
            "KeepAlive":False, 
            "Type":"Error", 
            "val":self.codes["NotValidCommand"]}
      )
      if data["command"] in NoneCommands:
        not_found()
        return
      try:
        getattr(self, data['command'], not_found)(data["val"], client=self)
      except:
        self.send_data({
          "KeepAlive":False,
          "Type":"Error",
          "val":self.Codes["Internal"]
        })