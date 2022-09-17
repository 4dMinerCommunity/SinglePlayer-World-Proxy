import asyncio
import traceback

import json


class JsonClientProtocol(asyncio.Protocol):
    def __init__(self):
        pass

    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        print("Connection to {}".format(peername))
        self.transport = transport
        self.continue_for_bytes = False

        self.ip = peername
        self.handle_connection_made()

    def is_json(self, data):
        try:
            json.loads(data)
            return True
        except:
            return False

    def handle_json(self, data):
        raise NotImplementedError(
            "_4DMinerClientProtocol.handle_json is an abstact Method. Please overide it"
        )

    def handle_bytes(self, data):
        raise NotImplementedError(
            "_4DMinerClientProtocol.handle_bytes is an abstract Method, Please override it"
        )

    def handle_connection_removed(self):
        raise NotImplementedError(
            "_4DMinerClientProtocol.handle_connection_removed is an abstract Method, Please override it"
        )

    def handle_connection_made(self):
        raise NotImplementedError(
            "_4DMinerClientProtocol.handle_connection_made is an abstract Method, Please override it"
        )

    def send_data(self, sendback):
        if type(sendback) == dict:
            if "type" in sendback.keys():
                if type == "bytes":
                    ret = sendback["data"]
                else:
                    ret = json.dumps(sendback).encode()
            else:
                ret = json.dumps(sendback).encode()

            self.transport.write(ret)

            if not ("KeepAlive" in sendback.keys()):
                self.transport.close()
                return

            if sendback["KeepAlive"]:
                return

            self.transport.close()
            return

        else:
            if type(sendback) is str:
                sendback = sendback.encode()
            self.transport.write(sendback)

    def data_received(self, data):
        message = data.decode()

        if self.is_json(message):
            self.handle_json(json.loads(message))
        else:
            self.handle_bytes(message)

    def connection_lost(self, exc: BaseException):
        if exc is not None:
            print(exc)
        self.handle_connection_removed()
