from .NetworkInterface import NetworkInterface

class IntegrityMiddleware:

    counter: list[any]
    protocol: NetworkInterface

    def __init__(self, protocol: NetworkInterface) -> None:
        self.protocol = protocol
        

    def write(self) -> None:
        self.protocol.write()

    def read(self) -> None:
        self.protocol.read()