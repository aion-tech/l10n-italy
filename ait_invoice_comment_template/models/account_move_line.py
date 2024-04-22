from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('product_id')
    def _update_comments(self):
        for rec in self:
            templates = self.env["base.comment.template"].search(
                [
                    ("model_ids.model", "=", 'account.move'),
                    ('position', '=', 'line')
                ]
            )
            #filter templates for product_id and partner_id
            templates = templates.filtered(lambda p: rec.product_id.id in p.product_ids.ids)
            templates = templates.filtered(lambda p: rec.order_id.partner_id.id in p.partner_ids.ids or not p.partner_ids)
            if templates:
                sequence = templates.mapped('sequence')
                sequence.sort()
                template = templates.filtered(lambda p: p.sequence == sequence[0])
                rec.comment_id = template.id