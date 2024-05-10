from os import environ
from uuid import UUID

from leo_1c import (
    ConnectionBuilder,
    ClientBuilder,
    PartnersClientModule,
    BillsClientModule,
    BillPDFsClientModule,
    Bill,
    BillLine
)

conn = ConnectionBuilder().set_host(
    environ.get('YOUR_HOST_HERE')
).set_info_base(
    environ.get('YOUR_INFO_BASE_HERE')
).build()

client = ClientBuilder().set_connection(
    conn
).add_module(
    "partners",
    PartnersClientModule(
        resource_type="Catalog",
        resource_name="Контрагенты",
        address_contact_type_guid=UUID("dc4a9047-0ec7-11ef-8863-3633d71a77ae"),
    )
).add_module(
    "bills",
    BillsClientModule(
        resource_type="Document",
        resource_name="СчетНаОплатуПокупателю"
    )
).add_module(
    "bill_pdfs",
    BillPDFsClientModule()
).build()

partner = client.partners.get_by_guid(
    UUID("e830852a-0ec9-11ef-9ac2-3633d71a77ae")
)

bill = Bill(
    partner_guid=partner.get_guid(),
    lines=[
        BillLine(
            name="Тестовый товар 1",
            price=100,
            amount=6,
            vat=100,
            subtotal=600
        ),
        BillLine(
            name="Тестовый товар 2",
            price=1000,
            amount=6,
            vat=1000,
            subtotal=6000
        )
    ],
    datetime=None,
    number=None,
    total=None
)

created_bill = client.bills.create(bill)

print(created_bill.get_guid(), created_bill.get_number())

with open('bill.pdf', 'wb') as bill_out_file:
    pdf_data = client.bill_pdfs.get_bill_pdf(created_bill)

    bill_out_file.write(pdf_data)
