from typing import Union
from uuid import UUID

from leo_1c.client_module.odata import ODataClientModule
from leo_1c.entity.partner import Partner


class PartnerClientModule(ODataClientModule[Partner]):
    def __init__(
            self,
            address_contact_type_guid: UUID = None,
            **resource_kwargs
    ):
        super(PartnerClientModule, self).__init__(**resource_kwargs)

        # TODO: automatically detect address contact guid?
        self._address_contact_type_guid = address_contact_type_guid

    def get_by_inn_kpp(self, inn: str, kpp: str) -> Union[Partner, None]:
        results = self.get_many({
            "$filter": f"ИНН eq '{inn}' and КПП eq '{kpp}'"
        })

        for result in results:
            if result.is_valid_for_bills():
                return result

        return None

    @staticmethod
    def _to_entity(data: dict) -> Partner:
        address = None
        for partner_contact in data["КонтактнаяИнформация"]:
            if partner_contact["Тип"] == "Адрес":
                address = partner_contact["Представление"]
                break

        return Partner(
            inn=data["ИНН"] or None,
            kpp=data["КПП"] or None,
            short_name=data["Description"] or None,
            full_name=data["НаименованиеПолное"] or None,
            guid=UUID(hex=data["Ref_Key"]),
            address=address
        )

    def _to_dict(self, entity: Partner) -> dict:
        guid = entity.get_guid()
        inn = entity.get_inn()
        kpp = entity.get_kpp()
        description = entity.get_short_name()
        full_name = entity.get_full_name()
        address = entity.get_address()

        data = {}

        if guid:
            data["Ref_Key"] = str(guid)

        if inn:
            data["ИНН"] = inn

        if kpp:
            data["КПП"] = kpp

        if description:
            data["Description"] = description

        if full_name:
            data["НаименованиеПолное"] = full_name

        if address:
            data["КонтактнаяИнформация"] = [
                {
                    "Тип": "Адрес",
                    "LineNumber": "1",
                    "Вид_Key": str(self._address_contact_type_guid),
                    "Представление": address
                }
            ]

        return data
