from urllib.parse import quote, urlencode

from typing_extensions import Self
from requests import Session

from leo_1c.exception import Leo1CException


class ConnectionParams:

    def __init__(self, host: str, info_base: str):
        self._host = host
        self._info_base = info_base

    def get_host(self) -> str:
        return self._host

    def get_info_base(self) -> str:
        return self._info_base


class ConnectionParamsBuilder:

    def __init__(self):
        self._host = None
        self._info_base = None

    def set_host(self, host: str) -> Self:
        self._host = host
        return self

    def set_info_base(self, info_base: str) -> Self:
        self._info_base = info_base
        return self

    def build(self) -> ConnectionParams:
        if self._host is None or self._info_base is None:
            raise Leo1CException(
                "Cannot build connection params: "
                "host or info base were not provided"
            )

        return ConnectionParams(host=self._host, info_base=self._info_base)


class Connection:

    def __init__(self, params: ConnectionParams):
        self._params = params
        self._session = Session()

    def call_odata_handler(
            self,
            method: str,
            name: str,
            params: dict = None,
            body: dict = None
    ) -> dict:
        return self._call_http_handler(
            f"odata/standard.odata/{name}",
            method,
            params,
            body
        )

    def call_http_service_handler(
            self,
            method: str,
            name: str,
            route: str,
            params: dict = None,
            body: dict = None
    ):
        return self._call_http_handler(
            f"hs/{name}/{route}",
            method,
            params,
            body
        )

    def _call_http_handler(
            self,
            path: str,
            method: str,
            params: dict = None,
            body: dict = None
    ):
        url = f"{self._params.get_host()}/{self._params.get_info_base()}/{path}"

        if params is None:
            params = {"$format": "json"}
        else:
            params["$format"] = "json"

        encoded_params = []

        for k, v in params.items():
            encoded_params.append(
                (
                    k.encode("utf-8") if isinstance(k, str) else k,
                    v.encode("utf-8") if isinstance(v, str) else v,
                )
            )

        encoded_params = urlencode(encoded_params, doseq=True, quote_via=quote)

        try:
            response = self._session.request(
                method=method,
                url=url,
                params=encoded_params,
                json=body,
            )
        except BaseException as exc:
            raise Leo1CException(f"Unable to call HTTP handler: {exc}")

        content_type = response.headers.get("Content-Type")
        is_content_json = "application/json" in content_type

        content = response.json() if is_content_json else response.content

        return {
            "success": response.ok,
            "status_code": response.status_code,
            "content_type": content_type,
            "content_is_json": is_content_json,
            "content": content
        }
