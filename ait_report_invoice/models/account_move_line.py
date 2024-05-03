from odoo import models, api, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    pricelist_item_client_ref = fields.Char(string="Pricelist Client Ref.")
    comment_id = fields.Many2one('base.comment.template', 'Comment')
    comment_text = fields.Html(string='Comment text')
    show_line_comment = fields.Boolean('Show comment', default=False)

    @api.onchange("comment_id")
    def _compute_comment_text(self):
        if self.comment_id:
            self.comment_text = self.comment_id.text

    @api.depends('comment_id')
    def can_show_comment(self, invoice_report_state_exclude):
        for rec in self:
            rec.show_line_comment = False
            if rec.comment_text and not rec.comment_id:
                rec.show_line_comment = True
            if rec.comment_id and rec.comment_id.invoice_template not in invoice_report_state_exclude:
                rec.show_line_comment = True

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

class AccountMove(models.Model):
    _inherit = "account.move"

    compute_pricelist_client_ref_on_lines = fields.Boolean(compute="_compute_pricelist_client_ref_on_lines")

    def _compute_pricelist_client_ref_on_lines(self):
        for rec in self:
            rec.compute_pricelist_client_ref_on_lines = True
            for line in rec.invoice_line_ids:
                line.pricelist_item_client_ref = ""
                client_ref = line.sale_line_ids.filtered(lambda line: line.pricelist_item_client_ref)
                if client_ref:
                    line.pricelist_item_client_ref = client_ref[0].pricelist_item_client_ref