from typing import List
from uuid import UUID
from datetime import datetime as dt

from leo_1c.client_module.odata import ODataClientModule
from leo_1c.entity.bill import Bill, BillLine


class BillClientModule(ODataClientModule[Bill]):
    @staticmethod
    def _to_entity(data: dict) -> Bill:
        lines: List[BillLine] = []

        for line in data["Товары"]:
            lines.append(
                BillLine(
                    name=line["Содержание"],
                    price=line["Цена"],
                    amount=line["Количество"],
                    subtotal=line["Сумма"],
                    vat=line["СуммаНДС"]
                )
            )

        return Bill(
            guid=UUID(data["Ref_Key"]),
            partner_guid=UUID(data["Контрагент_Key"]),
            number=data["Number"],
            datetime=dt.fromisoformat(data["Date"]),
            total=data["СуммаДокумента"],
            lines=lines
        )

    def _to_dict(self, entity: Bill) -> dict:
        guid = entity.get_guid()
        total = entity.get_total()
        partner_guid = entity.get_partner_guid()
        datetime = entity.get_datetime()
        number = entity.get_number()
        lines = entity.get_lines()

        encoded_lines: List[dict] = []

        for i, line in enumerate(entity.get_lines()):
            encoded_lines.append({
                "LineNumber": f"{i + 1}",
                "Содержание": line.get_name(),
                "Цена": line.get_price(),
                "Количество": line.get_amount(),
                "Сумма": line.get_subtotal(),
                "СуммаНДС": line.get_vat(),
                "СтавкаНДС": "НДС20"
            })

        data = {}

        if guid:
            data["Ref_Key"] = str(guid)

        if total is not None:
            data["СуммаДокумента"] = total

        data["ДокументБезНДС"] = False
        data["СуммаВключаетНДС"] = True

        if partner_guid:
            data["Контрагент_Key"] = str(partner_guid)

        if datetime:
            data["Date"] = datetime.isoformat()

        if number:
            data["Number"] = number

        if encoded_lines:
            data["Товары"] = encoded_lines

        return data
