from typing import Union
from uuid import UUID


class Entity:
    def __init__(self, guid: UUID = None):
        self._guid = guid

    def get_guid(self) -> Union[UUID, None]:
        return self._guid
