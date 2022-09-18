from typing import TYPE_CHECKING
from asyncio import AbstractServer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .Protocall import _4DMinerServerProtocol
class Server:
    def __init__(self):
        self.cons = {}
        self.currently_connected: set = set([])

        self.CurrentWorldHost:int = None
      
    def add_server(self, server:AbstractServer):
        self.server:AbstractServer = server

    def become_host(self, val, client:"_4DMinerServerProtocol"=None):
      if not self.CurrentWorldHost is None:
          client.send_data({
                "KeepAlive": False,
                "type": "Error",
                "val": client.Codes["HostExists"]
          })
          return
        
      self.CurrentWorldHost = client.id
      