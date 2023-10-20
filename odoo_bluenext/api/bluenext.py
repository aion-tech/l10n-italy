import json
from datetime import date, datetime, timedelta
from typing import Dict, List, Union

import requests
from odoo.exceptions import ValidationError
from typing_extensions import Literal


class Bluenext:
    def __init__(self, url, username, password, access_token, access_token_expiration):
        self.url: str = url
        if self.url and not self.url.endswith("/"):
            self.url += "/"
        self.username: str = username
        self.password: str = password
        self.access_token: str = access_token
        self.access_token_expiration: Union[None, datetime] = access_token_expiration
        if not self.access_token:
            self.access_token, self.access_token_expiration = self.get_access_token()

    def _make_request(
        self,
        url,
        params: dict = {},
        data: dict = {},
        method="post",
        error: Literal["raise", "return"] = "return",
    ):
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }
        if hasattr(self, "access_token") and self.access_token:
            headers.update(
                {
                    "Authorization": f"Bearer {self.access_token}",
                }
            )
        response = getattr(requests, method)(
            url=self.url + url,
            params=params,
            data=json.dumps(data) if data else data,
            headers=headers,
        )
        if response.status_code != 200:
            msg = f"Error {response.status_code} - {response.reason}:\n{response.text}"
            raise ValidationError(msg)
        try:
            res = response.json()
            if res.get("access_token"):
                return res
            elif res.get("Success"):
                return res["Data"]
            else:
                if error == "raise":
                    raise ValidationError(
                        json.dumps(
                            res["Error"],
                            indent=4,
                        )
                    )
                elif error == "return":
                    return res["Error"]
        except json.decoder.JSONDecodeError:
            res = response.text

        return res

    # ==== REST ====
    def login(self):
        """
        API_Login
        """
        params = {
            "username": self.username,
            "password": self.password,
        }
        return self._make_request(
            "login",
            params=params,
            error="raise",
        )

    def get_ticket(self):
        """
        API_GetTicket
        """
        params = {
            "username": self.username,
            "password": self.password,
        }
        res = self._make_request(
            "getTicket",
            params=params,
            error="raise",
        )
        return res

    def get_access_token(self):
        """
        API_TicketValidate
        """
        params = {
            "ticket": self.get_ticket(),
        }
        res = self._make_request(
            "ticketValidate",
            params=params,
            error="raise",
        )
        buffer = 3600
        expiration_date = datetime.now() + timedelta(
            seconds=int(res["expires_in"]) - buffer
        )

        return res["access_token"], expiration_date

    def book_filename(
        self,
        country_code: str,
        tax_id: str,
        extension: Literal["zip", "xml"],
    ) -> str:
        """
        API_BookFileName

        Prenota un GUID che dovrà essere utilizzato come nome da attribuire
        al file (da richiamare sia per file xml “fattura” sia per il file zip
        “contenitore”).
        """
        _extension = (
            "20.zip" if extension == "zip" else "01.xml" if extension == "xml" else ""
        )
        data = {
            "CountryCode": country_code,
            "TaxId": tax_id,
        }
        return (
            self._make_request(
                "api/v1/invoicetransmission/bookFilename",
                data=data,
            )
            + _extension
        )

    def send_file(
        self,
        filename: str,
        file: bytes,
        send_mode: Literal[0, 1],
        additional_info: Dict,
    ) -> Dict[str, str]:
        """
        API_SendFile

        Importa un file zip sul portale
        (file zip con al suo interno un solo file xml).
        """
        data = {
            "filename": filename,
            "file": file,
            "sendMode": send_mode,
            "additionalInfo": additional_info,
        }
        res = self._make_request(
            "api/v1/invoicetransmission/sendFile",
            data=data,
        )
        return res

    def get_xml_file_sending_state(
        self,
        archive_id: str,
        filename: str,
    ) -> Dict[str, Dict]:
        """
        API_GetXmlFileSendingState

        Recupera lo stato di un file.
        """
        data = {
            "ArchiveId": archive_id,
            "FileName": filename,
        }
        return self._make_request(
            "api/v2/invoicedocument/getXmlFileSendingState",
            data=data,
        )

    def get_xml_file_archived_state(
        self,
        archive_id: str,
        filename: str,
    ) -> Dict[str, Dict]:
        """
        API_GetXmlFileArchiveState

        Recupera lo stato di conservazione di un file.
        """
        params = {
            "ArchiveId": archive_id,
            "FileName": filename,
        }
        return self._make_request(
            "api/v2/invoicedocument/getXmlFileArchiveState",
            params=params,
        )

    def get_receipt(
        self,
        archive_id: str,
        filename: str,
    ):  # -> ?
        """
        API_GetReceipt

        Recupera la ricevuta di un file.
        """
        data = {
            "ArchiveId": archive_id,
            "FileName": filename,
        }
        return self._make_request(
            "api/v2/invoicedocument/getReceipt",
            data=data,
        )

    def get_receipts(
        self,
        archive_id: str,
        filename: str,
    ) -> Dict[str, List[Dict]]:
        """
        API_GetReceipts

        Recupera tutte le ricevute di un file
        (tipo fattura FPA12).
        """
        params = {
            "ArchiveId": archive_id,
            "FileName": filename,
        }
        return self._make_request(
            "api/v2/invoicedocument/getReceipts",
            params=params,
        )

    def list_documents(
        self,
        registered: bool,
        registered_type: Literal[
            "Undefined",
            # "NotDownloaded",
            # "AccountingDownloaded",
            # "StoreDownloaded",
            # "ClientB2BDownloaded",
            "SoftwareHouseDownloaded",
        ],
        category: Literal[
            "Undefined",
            "Active",
            "Passive",
        ],
        recipient: Dict[str, str],
        _from: Union[bool, date] = False,
        to: Union[bool, date] = False,
    ) -> List[Dict]:
        """
        API_ListDocumentsV3

        Ritorna l’elenco dei files xml
        per il soggetto richiesto.
        """
        params = {
            "Registered": registered,
            "RegisteredType": registered_type,
            "Category": category,
            "Recipient": recipient,
        }
        if _from:
            params["From"] = _from
        if to:
            params["To"] = to
        return self._make_request(
            "api/v3/invoicedocument/getList",
            data=params,
        )

    def get_document(
        self,
        archive_id: str,
        filename: str,
        file_format: Literal[
            0,  # xml
            1,  # p7m
            2,  # P7mOrXml
        ],
    ) -> Dict:
        """
        API_GetDocumentV3

        Recupera il nome ed il contenuto del file,
        con la possibilità di scegliere il tipo di file.
        """
        data = {
            "ArchiveId": archive_id,
            "FileName": filename,
            "FileFormat": file_format,
        }
        res = self._make_request(
            "api/v4/invoicedocument/getFile",  # v4, not a typo
            data=data,
        )
        return res

    def mark_documents_as_registered(
        self,
        archive_id: str,
        filename: str,
        invoices: List[Dict],
    ) -> Dict[str, bool]:
        """
        MarkDocumentAsRegisteredV4

        Imposta come registrata una o più fatture per la
        tipologia indicata.
        Con il parametro Remove impostato a true,
        rimuove la registrazione per la tipologia indicata.
        """
        params = {
            "ArchiveId": archive_id,
            "FileName": filename,
            "Invoices": invoices,
        }
        return self._make_request(
            "api/v4/invoicedocument/markDocumentAsRegistered",
            params=params,
        )

    def export_book(
        self,
        year: str,
        month: str,
    ) -> str:
        """
        API_ExportBook

        Richiede l’esportazione delle fatture per uno studio ed i relativi clienti.
        Se l’operazione richiesta va a buon fine, esegue la prenotazione e restituisce
        un GUID che dovrà essere utilizzato successivamente per invocare ExportDownload.
        """
        params = {
            "year": year,
            "month": month,
        }
        return self._make_request(
            "api/v1/invoicedocument/export/book",
            params=params,
        )

    def export_book_download(
        self,
        booking_id: str,
    ) -> Dict:
        """
        API_ExportBookDownload

        Dato un GUID ottenuto da ExportBook, restituisce lo stato
        dell’operazione e, solo se questa è terminata, il link da
        cui poter scaricare il file ZIP.
        """
        params = {
            "Bookingid": booking_id,
        }
        return self._make_request(
            "api/v1/invoicedocument/export/download",
            params=params,
        )

    def list_errors(
        self,
        _from: date,
        to: date,
    ) -> Dict[str, List[Dict]]:
        """
        API_ListErrors

        Ritorna la lista degli errori presenti nel
        "Log operazioni errate" del Portale dei Servizi.
        """
        params = {
            "from": _from,
            "to": to,
        }
        return self._make_request(
            "api/v1/invoicedocument/getListErrors",
            params=params,
        )

    # ==== WFC ====
    def get_b2b_token(self):
        """
        WS_UrlS
        """
        ...

    def get_stati_pds(self):
        """
        WS_UrlA
        """
        ...

    # ==== NotImplemented ====
    def validate_file(self):
        raise NotImplementedError

    def view_file(self):
        raise NotImplementedError
