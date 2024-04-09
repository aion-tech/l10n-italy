import base64
import io
import zipfile
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models


class FatturapaAttachmentIn(models.Model):
    _name = "fatturapa.attachment.in"
    _inherit = ["fatturapa.attachment.in", "fatturapa.attachment.mixin"]

    bluenext_archive_id = fields.Char(
        string="Bluenext Archive ID",
        readonly=True,
    )
    bluenext_sdi_id = fields.Char(
        string="Sdi ID",
        readonly=True,
    )
    bluenext_filename = fields.Char(
        string="Bluenext Filename",
        readonly=True,
    )
    bluenext_create_date = fields.Datetime(
        string="Bluenext Create Date",
        readonly=True,
    )

    def _set_bluenext_last_download_date(self, last: datetime):
        now = datetime.now()
        if last + relativedelta(months=1) > now:
            date_from = now
        else:
            date_from = last + relativedelta(months=1)

        company_id = self.company_id or self.env.company
        company_id.bluenext_last_download_date = date_from
        return date_from

    @api.model
    def bluenext_download_invoices_btn(self):
        invoice_ids = self.bluenext_download_invoices()
        return len(invoice_ids)

    @api.model
    def bluenext_download_invoices_cron(self):
        company_ids = (
            self.env["res.company"]
            .search([])
            .filtered(lambda company: company._has_complete_bluenext_conf())
        )
        for company_id in company_ids:
            self.with_company(company_id).bluenext_download_invoices()

    @api.model
    def bluenext_download_invoices(self):
        company_id = self.company_id or self.env.company
        bluenext = company_id._init_bluenext()
        dt_format = "%Y-%m-%d %H:%M:%S.%f%z"
        country_code: str = company_id.vat[:2]
        vat: str = company_id.vat[2:]

        last_download = company_id.bluenext_last_download_date
        last_download = last_download and last_download or datetime.now()

        documents = bluenext.list_documents(
            registered=False,
            registered_type="SoftwareHouseDownloaded",
            category="Passive",
            recipient={
                "CountryCode": country_code,
                "TaxId": vat,
            },
            _from=last_download.strftime(dt_format),
        )

        invoice_ids = self

        for document in documents.get("file", []):
            archive_id = document["ArchiveId"]
            fatturapa_attachment_in_id = self.search(
                [
                    ("bluenext_filename", "=", document["FileName"]),
                    ("bluenext_filename", "!=", False),
                ]
            )
            if fatturapa_attachment_in_id:
                continue

            document_vals = bluenext.get_document(
                archive_id,
                document["FileName"],
                2,  # 0: xml, 1: p7m, 2: P7mOrXml
            )

            fatturapa_attachment_in_vals = {
                "company_id": company_id.id,
                "datas": document_vals["Content"],
                "name": document_vals["Filename"],
                "bluenext_filename": document["FileName"],
                "bluenext_archive_id": archive_id,
                # "bluenext_sdi_id": document["SdiId"],
                "bluenext_create_date": datetime.strptime(
                    document["CreatedTime"],
                    dt_format,
                ).replace(tzinfo=None),
                "e_invoice_received_date": datetime.strptime(
                    document["ReceptionTime"],
                    dt_format,
                ).replace(tzinfo=None),
            }
            invoice_ids |= self.create(fatturapa_attachment_in_vals)

        self._set_bluenext_last_download_date(last_download)
        return invoice_ids
