from odoo import models, fields, api


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    default_account_jounal = fields.Many2one('account.journal', string='Default Account Journal', help='Automatically selects this account journal when the fiscal position is modified on the records.')

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('fiscal_position_id')
    def update_account_journal(self):
        if self.fiscal_position_id:
            if self.fiscal_position_id.default_account_jounal:
                self.journal_id = self.fiscal_position_id.default_account_jounal.id