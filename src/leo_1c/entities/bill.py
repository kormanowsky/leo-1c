from datetime import datetime as dt
from typing import Union, List
from uuid import UUID

from leo_1c.entities.entity import Entity


class BillLine:
    def __init__(
            self,
            name: str,
            price: float,
            amount: Union[int, float],
            subtotal: float,
            vat: float
    ):
        self._name = name
        self._price = price
        self._amount = amount
        self._subtotal = subtotal
        self._vat = vat

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> float:
        return self._price

    def get_amount(self) -> Union[int, float]:
        return self._amount

    def get_subtotal(self) -> float:
        return self._subtotal

    def get_vat(self) -> float:
        return self._vat


class Bill(Entity):
    def __init__(
            self,
            partner_guid: Union[UUID, None],
            number: Union[str, None],
            datetime: Union[dt, None],
            lines: Union[List[BillLine], None],
            total: Union[int, float, None],
            guid: UUID = None):
        super(Bill, self).__init__(guid)

        self._partner_guid = partner_guid
        self._number = number
        self._datetime = datetime
        self._lines = lines
        self._total = total

    def get_partner_guid(self) -> Union[UUID, None]:
        return self._partner_guid

    def get_number(self) -> Union[str, None]:
        return self._number

    def get_datetime(self) -> Union[dt, None]:
        return self._datetime

    def get_lines(self) -> Union[List[BillLine], None]:
        return self._lines

    def get_total(self) -> Union[int, float, None]:
        return self._total
