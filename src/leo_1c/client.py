from typing_extensions import Self

from leo_1c.connection import Connection


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
    modules = ClientModules()

    @classmethod
    def add_module(cls, name: str, module: ClientModule) -> Self:
        setattr(cls.modules, name, module)

        return cls

    def __init__(self, connection: Connection):
        self._conn = connection

        for module_name in dir(self.modules):
            module = getattr(self.modules, module_name)

            if isinstance(module, ClientModule):
                module.set_client(self)

    def get_connection(self) -> Connection:
        return self._conn
