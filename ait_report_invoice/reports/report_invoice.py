from odoo import models, api, fields

class InvoiceReport(models.AbstractModel):
    _name = 'report.ait_report_invoice.report_account_move'
    _description = 'Invoice Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        for doc in docs:
            doc._compute_pricelist_client_ref_on_lines()
        return {
            'company': docs[0].company_id,
            'doc_ids': docs.ids,
            'doc_model': 'account.move',
            'docs': docs,
        }