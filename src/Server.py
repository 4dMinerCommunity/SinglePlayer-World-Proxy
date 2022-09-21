from asyncio import AbstractServer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Protocall import _4DMinerServerProtocol

from easy_db import DataBase


class Server:
    def __init__(self):
        self.db = DataBase(db_location_str="sqlite.db", create_if_none=False)

        self.connected = {}
        self.users = self.db.pull("Users")

        self.CurrentWorldHost: int = None
        """
          Current Client World Host Server ID
        """

    def add_server(self, server: AbstractServer):
        self.server: AbstractServer = server

    def send_to_all(self, packet):
        for id in self.currently_connected:
            user = self.cons[id]
            user["proto"].send_data(packet)

    def become_host(self, val, client: "_4DMinerServerProtocol" = None):
        if not self.CurrentWorldHost is None:
            client.send_data(
                {"KeepAlive": False, "type": "Error", "val": client.Codes["HostExists"]}
            )
            return

        self.CurrentWorldHost = client.id
        client.send_data(
            {"KeepAlive": True, "type": "StatusCode", "val": client.Codes["OK"]}
        )

        self.send_to_all(
            {
                "KeepAlive": True,
                "type": "command",
                "command": "HostUpdate",
                "val": self.CurrentWorldHost,
            }
        )

    def login(self, val, client):
        if not any(d["IP"] == client.ip for d in self.db.get("Player")):
            id = len(self.db.pull("Users"))
            client.id = id

            self.db.append(
                "Users",
                {"ID": id, "IP": str(client.ip), "x": 0, "y": 100, "z": 0, "w": 0},
            )
        usr = self.db.pull_where("Users", f"{str(client.ip)} = IP")
        self.connected[usr.id] = {"client": client}

    def move(self, val, client):
        if not hasattr(client, "id"):
            client.send_data(
                {"KeepAlive": True, "type": "Error", "val": client.Codes["NotLoggedIn"]}
            )
            return

        if not val["dir"] in ["x", "y", "z", "w"]:
            client.send_data(
                {"KeepAlive": True, "type": "Error", "val": client.Codes["BadRequest"]}
            )
            return
        usr = self.db.pull_where("Users", f"{client.id} = ID")
        del usr["IP"]
        self.connected[self.CurrentWorldHost]["client"].send_data(
            {"KeepAlive": True, "type": "Command", "command": "GetMapFor", "val": usr}
        )

        self.send_to_all({
          "KeepAlive":True,
          "type":"Command",
          "Command":"Update_player",
          "val":usr
        })
        

    def host_return_map(self, val, client):
        if not (set(["ID", "MAP"]) - grades.keys()):
            client.send_data(
                {"KeepAlive": True, "type": "Error", "val": client.Codes["BadRequest"]}
            )
            return

        self.connected[val["ID"]]["client"].send_data({
          "KeepAlive":True,
          "type":"Command",
          "Command":"UpdateMap",
          "val": val["MAP"]
        })
        
        
  def update_map(self, val, client):
    """
    Updates the map for Client host and also sends it to all clients
    """
    self.send_to_all({
      "KeepAlive":True,
      "type":"Command",
      "Command":"Update_map",
      "val": val
    })

    
    self.connected[self.CurrentWorldHost]["client"].send_data(
          {"KeepAlive": True, "type": "Command", "command": "SaveMap", "val": val}
    )