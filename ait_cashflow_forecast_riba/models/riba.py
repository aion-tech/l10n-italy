from odoo import api, fields, models


class RibaDistintaLine(models.Model):
    _name = "riba.distinta.line"
    _inherit = ["riba.distinta.line", "cashflow.mixin"]

    @api.depends("move_line_ids")
    def _compute_amount(self):
        for line in self:
            line.amount = 0.0
            for move_line in line.move_line_ids:
                line.amount += move_line.amount

            line.cashflow_record_ids.unlink()
            cashflow_config_id = line._get_cashflow_config_id()
            line._set_cashflow_config_id(cashflow_config_id.id)
            line._create_cashflow_record()

    amount = fields.Float(compute="_compute_amount", store=True)
