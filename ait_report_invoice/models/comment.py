from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import is_html_empty, html2plaintext


class BaseCommentTemplate(models.Model):
    _inherit = 'base.comment.template'

    invoice_template = fields.Selection(string="Invoice template",
        selection=[
            ("draft", "Draft"),
            ("posted", "Posted"),
            ("all", "ALL"),
        ],
        default="all",)

    model_selection = fields.Selection(
        selection_add=[("account.move", "Invoice")],
        ondelete = {'account.move': 'cascade'})
    
    @api.onchange('model_selection')
    def _onchange_model_selection(self):
        super()._onchange_model_selection()
        for rec in self:
            if rec.model_selection == 'account.move':
                rec.position = 'before_lines'
                rec.models = 'account.move'
            else:
                rec.invoice_template = False