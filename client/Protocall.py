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
