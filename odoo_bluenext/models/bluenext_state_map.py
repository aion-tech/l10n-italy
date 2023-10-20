from odoo import _, api, fields, models


class BluenextStateMap(models.Model):
    _name = "bluenext.state.map"
    _description = "bluenext.state.map"
    _rec_name = "bluenext_invoice_state"

    odoo_attachment_out_state = fields.Selection(
        selection=[
            ("ready", "Ready to Send"),
            ("sent", "Sent"),
            ("sender_error", "Sender Error"),
            ("recipient_error", "Not delivered"),
            ("rejected", "Rejected (PA)"),
            ("validated", "Delivered"),
            ("accepted", "Accepted"),
        ],
        required=True,
    )
    bluenext_invoice_state = fields.Selection(
        selection=[
            ("0", "Nessuno"),
            ("1", "Upload in corso"),
            ("2", "Errore nell'upload"),
            ("5", "Controllo formale del file e dei contenuti"),
            ("6", "Errore durante il controllo formale del file e dei contenuti"),
            ("7", "Lettura ed estrazione dei dati delle fatture in corso"),
            ("8", "Errore nella lettura ed estrazione dei dati delle fatture"),
            ("9", "Firma in corso"),
            ("10", "Errore durante le operazioni di firma"),
            ("13", "Invio allo SdI in corso"),
            ("14", "Errore durante l'invio allo SdI"),
            ("15", "Documento in attesa di esito dallo SdI"),
            ("16", "Notifica di avvenuta consegna"),
            ("17", "Notifica di scarto"),
            ("18", "Notifica di mancata consegna"),
            ("19", "Documento importato ma non inviato allo SdI"),
            ("20", "Fattura passiva ricevuta dallo SdI"),
            ("21", "--- (Non utilizzato)"),
            ("22", "Accettata (FPA12)"),
            ("23", "Rifiutata (FPA12)"),
            ("24", "Accettata per decorrenza termini (FPA12)"),
            ("25", "Mancata consegna finale (FPA12)"),
        ],
        required=True,
    )
