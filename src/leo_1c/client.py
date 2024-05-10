from typing_extensions import Self

from leo_1c.connection import Connection
from leo_1c.exception import Leo1CException


class ClientModule:
    def __init__(self):
        self._client = None

    def set_client(self, client: "Client") -> Self:
        self._client = client

        return self

    def get_client(self) -> "Client":
        return self._client


class ClientModules:
    pass


class Client:
    def __init__(self, connection: Connection, modules: ClientModules):
        self._conn = connection

        for module_name in dir(modules):
            module = getattr(modules, module_name)

            if isinstance(module, ClientModule):
                setattr(self, module_name, module.set_client(self))

    def get_connection(self) -> Connection:
        return self._conn


class ClientBuilder:

    def __init__(self):
        self._modules = ClientModules()
        self._conn = None

    def add_module(self, name: str, module: ClientModule) -> Self:
        setattr(self._modules, name, module)

        return self

    def set_connection(self, connection: Connection) -> Self:
        self._conn = connection

        return self

    def build(self) -> Client:
        if not self._conn:
            raise Leo1CException("Unable to build Leo1C Client: no connection")

        return Client(self._conn, self._modules)
