from odoo import models, api, fields

class InvoiceReport(models.AbstractModel):
    _name = 'report.ait_report_invoice.report_account_move'
    _description = 'Invoice Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        for doc in docs:
            doc._compute_pricelist_client_ref_on_lines()
            for line in doc.invoice_line_ids:
                if doc.state in ('draft', 'cancel'):
                    invoice_report_state_exclude = ['posted']
                else:
                    invoice_report_state_exclude = ['draft']
                line.can_show_comment(invoice_report_state_exclude)
        return {
            'company': docs[0].company_id,
            'doc_ids': docs.ids,
            'doc_model': 'account.move',
            'docs': docs,
            'shipping_info_on_invoice': self.env['ir.config_parameter'].sudo().get_param('ait_report_invoice.shipping_info_on_invoice'),
        }