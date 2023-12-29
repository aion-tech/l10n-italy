from odoo import models, api, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    pricelist_item_client_ref = fields.Char(string="Pricelist Client Ref.")



class AccountMove(models.Model):
    _inherit = "account.move"

    compute_pricelist_client_ref_on_lines = fields.Boolean(compute="_compute_pricelist_client_ref_on_lines")

    def _compute_pricelist_client_ref_on_lines(self):
        for rec in self:
            rec.compute_pricelist_client_ref_on_lines = True
            # for line in rec.line_ids:
            for line in rec.invoice_line_ids:
                line.pricelist_item_client_ref = ""
                client_ref = line.sale_line_ids.filtered(lambda line: line.pricelist_item_client_ref)
                if client_ref:
                    line.pricelist_item_client_ref = client_ref[0].pricelist_item_client_ref