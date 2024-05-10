from typing import Generic, TypeVar, List, Union
from uuid import UUID

from typing_extensions import Self

from leo_1c.client import ClientModule, Client
from leo_1c.odata_resource import ODataResource
from leo_1c.exception import Leo1CException

T = TypeVar('T')


class ODataClientModule(ClientModule, Generic[T]):

    def __init__(self, **resource_kwargs):
        ClientModule.__init__(self)

        self._resource: Union[ODataResource, None] = None
        self._resource_kwargs = resource_kwargs

    def set_client(self, client: "Client") -> Self:
        super().set_client(client)

        self._resource = ODataResource(
            connection=client.get_connection(),
            **self._resource_kwargs
        )

    def get_many(self, params: dict = None) -> List[T]:
        self._ensure_resource()

        raw = self._resource.get_many(params)

        self._ensure_success_response(raw)

        return list(
            map(
                self._to_entity,
                raw["content"]["value"]
            )
        )

    def get_by_guid(self, guid: UUID) -> T:
        self._ensure_resource()

        raw = self._resource.get_by_guid(guid)

        self._ensure_success_response(raw)

        return self._to_entity(raw["content"])

    def create(self, entity: T, params: dict = None) -> T:
        self._ensure_resource()

        data = self._to_dict(entity)
        raw_result = self._resource.create(data, params)

        self._ensure_success_response(raw_result)

        return self._to_entity(raw_result["content"])

    def _ensure_resource(self) -> None:
        if not self._resource:
            raise Leo1CException(
                'Unable to use ODataClientModule: no resource'
            )

    def _ensure_success_response(self, response: dict) -> None:
        if not response["success"]:
            raise Leo1CException(
                f"Unable to get data from ODataResource: {response['content']}"
            )

    @staticmethod
    def _to_entity(data: dict) -> T:
        raise NotImplemented()

    @staticmethod
    def _to_dict(entity: T) -> dict:
        raise NotImplemented()
