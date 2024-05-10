from uuid import UUID

from leo_1c.connection import Connection


class ODataResource:

    def __init__(
            self,
            connection: Connection,
            resource_type: str,
            resource_name: str
    ):
        self._conn = connection
        self._resource_type = resource_type
        self._resource_name = resource_name

    def get_many(self, params: dict = None) -> dict:
        return self._conn.call_odata_handler(
            "GET",
            self._get_odata_handler_name(),
            params
        )

    def get_by_guid(self, guid: UUID) -> dict:
        return self._conn.call_odata_handler(
            "GET",
            f"{self._get_odata_handler_name()}(guid'{guid}')"
        )

    def create(self, data: dict, params: dict = None) -> dict:
        return self._conn.call_odata_handler(
            "POST",
            self._get_odata_handler_name(),
            params=params,
            body=data
        )

    def _get_odata_handler_name(self) -> str:
        return f"{self._resource_type}_{self._resource_name}"