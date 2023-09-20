import pdb
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    date_accounting = fields.Date('Accounting Date', copy=False)
    valid_date_accounting = fields.Boolean('Valid Accounting Date', copy=False)

    def button_date_validate(self):
        for record in self:
            record.valid_date_accounting = True
    
    def action_post(self):
        for record in self:
            for line in self.line_ids:
                if not line.date_accounting:
                    line.date_accounting = record.date_accounting
        return super().action_post()

    def write(self, vals):
        res = super().write(vals)
        if vals.get('date_accounting', False):
            for line in self.invoice_line_ids:
                if not line.date_accounting:
                    line.date_accounting = vals['date_accounting']
        return res

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    date_accounting = fields.Date(
        string='Accounting Date', copy=False)
