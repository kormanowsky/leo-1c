from typing import Union
from uuid import UUID

from leo_1c.entity.entity import Entity


class Partner(Entity):

    def __init__(
            self,
            inn: Union[str, None],
            kpp: Union[str, None],
            short_name: Union[str, None],
            full_name: Union[str, None],
            address: Union[str, None],
            guid: UUID = None
    ):
        super(Partner, self).__init__(guid)

        self._inn = inn
        self._kpp = kpp
        self._short_name = short_name
        self._full_name = full_name
        self._address = address

    def get_inn(self) -> Union[str, None]:
        return self._inn

    def get_kpp(self) -> Union[str, None]:
        return self._kpp

    def get_address(self) -> Union[str, None]:
        return self._address

    def get_short_name(self) -> Union[str, None]:
        return self._short_name

    def get_full_name(self) -> Union[str, None]:
        return self._full_name

    def is_valid_for_bills(self) -> bool:
        return all([
            self._kpp,
            self._inn,
            self._full_name,
            self._address
        ])
