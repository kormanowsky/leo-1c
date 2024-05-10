from uuid import UUID

from leo_1c.connection import Connection


class ODataResource:

    def __init__(
            self,
            connection: Connection,
            resource_type: str,
            resource_name_singular: str,
            resource_name_plural: str
    ):
        self._conn = connection
        self._resource_type = resource_type
        self._resource_name_singular = resource_name_singular
        self._resource_name_plural = resource_name_plural

    def get_many(self, params: dict = None) -> dict:
        return self._conn.call_odata_handler(
            "GET",
            f"{self._resource_type}_{self._resource_name_plural}",
            params
        )

    def get_by_guid(self, guid: UUID) -> dict:
        return self._conn.call_odata_handler(
            "GET",
            f"{self._resource_type}_{self._resource_name_plural}(guid'{guid}')"
        )

    def create(self, data: dict, params: dict = None) -> dict:
        return self._conn.call_odata_handler(
            "POST",
            f"{self._resource_type}_{self._resource_name_plural}",
            params=params,
            body=data
        )
