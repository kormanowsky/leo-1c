from typing import Union

from typing_extensions import Self

from leo_1c.connection import Connection
from leo_1c.exception import Leo1CException
from leo_1c.client import ClientModule, Client
from leo_1c.entity.bill import Bill


class BillPDFClientModule(ClientModule):

    def __init__(
            self,
            pdf_service_name: str = 'leo1cbillfiles',
            pdf_route_name: str = 'pdf'
    ):
        super(BillPDFClientModule, self).__init__()

        self._pdf_service_name = pdf_service_name
        self._pdf_route_name = pdf_route_name
        self._conn: Union[Connection, None] = None

    def set_client(self, client: Client) -> Self:
        self._conn = client.get_connection()

    def get_bill_pdf(self, bill: Bill) -> bytes:
        if not self._conn:
            raise Leo1CException(
                'Unable to use BillPDFClientModule: no connection'
            )

        result = self._conn.call_http_service_handler(
            "GET",
            self._pdf_service_name,
            f"{self._pdf_route_name}/{bill.get_guid()}"
        )

        return result['content']
