import base64
import io
import zipfile

from odoo import _, api, fields, models, release
from odoo.exceptions import UserError

STATUS_CODE_MSG_MAP = {
    0: "Nessuno",
    1: "Upload in corso",
    2: "Errore nell'upload",
    5: "Controllo formale del file e dei contenuti",
    6: "Errore durante il controllo formale del file e dei contenuti",
    7: "Lettura ed estrazione dei dati delle fatture in corso",
    8: "Errore nella lettura ed estrazione dei dati delle fatture",
    9: "Firma in corso",
    10: "Errore durante le operazioni di firma",
    13: "Invio allo SdI in corso",
    14: "Errore durante l'invio allo SdI",
    15: "Documento in attesa di esito dallo SdI",
    16: "Notifica di avvenuta consegna",
    17: "Notifica di scarto",
    18: "Notifica di mancata consegna",
    19: "Documento importato ma non inviato allo SdI",
    20: "Fattura passiva ricevuta dallo SdI",
    21: "--- (Non utilizzato)",
    22: "Accettata (FPA12)",
    23: "Rifiutata (FPA12)",
    24: "Accettata per decorrenza termini (FPA12)",
    25: "Mancata consegna finale (FPA12)",
}


def _create_zip(
    xml_filename: str,
    xml_content: bytes,
) -> str:
    zip_data = io.BytesIO()
    with zipfile.ZipFile(zip_data, "w") as zf:
        zf.writestr(xml_filename, base64.b64decode(xml_content))
    zip_data.seek(0)
    zip_bytes = zip_data.read()
    return base64.b64encode(zip_bytes).decode("utf-8")


class FatturapaAttachmentOut(models.Model):
    _name = "fatturapa.attachment.out"
    _inherit = ["fatturapa.attachment.out", "fatturapa.attachment.mixin"]

    bluenext_archive_id = fields.Char(
        string="Bluenext Archive ID",
        readonly=True,
    )
    bluenext_zip_filename = fields.Char(
        string="Bluenext Zip Filename",
        readonly=True,
    )
    bluenext_xml_filename = fields.Char(
        string="Bluenext Xml Filename",
        readonly=True,
    )
    bluenext_state = fields.Char(
        string="Bluenext State",
        readonly=True,
    )

    def bluenext_send_documents_btn(self):
        self._bluenext_send_document_one()

    def _bluenext_send_document_one(self):
        self.ensure_one()
        if self.bluenext_archive_id:
            raise UserError(
                _("Document already sent - Archive ID: %s") % self.bluenext_archive_id
            )
        bluenext = self.company_id._init_bluenext()
        country_code: str = self.company_id.vat[:2]
        vat: str = self.company_id.vat[2:]
        zip_filename = bluenext.book_filename(country_code, vat, "zip")
        xml_filename = bluenext.book_filename(country_code, vat, "xml")

        zipfile: str = _create_zip(
            xml_filename,
            self.datas,
        )
        res = bluenext.send_file(
            zip_filename,
            zipfile,
            1,
            {
                "EMAIL": "",  # @TODO customer ?
                "APP": release.version,
                "AUTOFATTURA": self.invoice_partner_id.id == self.company_id.id,
            },
        )
        self.bluenext_zip_filename = zip_filename
        self.bluenext_xml_filename = xml_filename
        self.bluenext_archive_id = res["ArchiveId"]
        msg = {
            "Info": "Invoice Sent",
            "date": fields.Datetime.to_string(
                fields.Datetime.context_timestamp(
                    self,
                    fields.Datetime.now(),
                ),
            ),
            "Filename - xml": xml_filename,
            "Filename - zip": zip_filename,
            "Archive ID": self.bluenext_archive_id,
        }
        self._post_bluenext_msg(msg)
        self._bluenext_get_invoice_state()

    def update_bluenext_state_btn(self):
        self._bluenext_get_invoice_state()

    def _bluenext_get_invoice_state(self):
        self.ensure_one()
        bluenext = self.company_id._init_bluenext()
        if self.bluenext_archive_id and self.bluenext_xml_filename:
            if not self.bluenext_state:
                # 1st call
                filename = self.bluenext_xml_filename[:-6]
            else:
                filename = self.bluenext_xml_filename
            res = bluenext.get_xml_file_sending_state(
                self.bluenext_archive_id,
                filename,
            )

            # states map
            if res.get("State"):
                res.update(
                    {"StateDescription": STATUS_CODE_MSG_MAP.get(res["State"], "")}
                )
                state = str(res["State"])
                if state != self.bluenext_state:
                    self._post_bluenext_msg(res)
                self.bluenext_state = state
                bluenext_map_id = self.company_id.bluenext_state_map_ids.filtered(
                    lambda state_map: state_map.bluenext_invoice_state == state
                )
                if bluenext_map_id:
                    self.state = bluenext_map_id.odoo_attachment_out_state
                return res
            else:
                self._post_bluenext_msg(res)

        return False

    def _bluenext_get_receipt(self):
        self.ensure_one()
        bluenext = self.company_id._init_bluenext()
        if self.bluenext_archive_id and self.bluenext_xml_filename:
            res = bluenext.get_receipt(
                self.bluenext_archive_id,
                self.bluenext_xml_filename,
            )
            self._post_bluenext_msg(res)
            return res

    @api.model
    def cron_bluenext_update_state(self):
        Company = self.env["res.company"].sudo()
        company_ids = Company.search(
            [
                ("bluenext_username", "!=", False),
                ("bluenext_password", "!=", False),
            ]
        )
        for company_id in company_ids:
            attachment_out_ids = self.search(
                [
                    ("company_id", "=", company_id.id),
                    ("state", "in", ["ready", "sent", "validated"]),
                ]
            )
            for att in attachment_out_ids:
                att._bluenext_get_invoice_state()
