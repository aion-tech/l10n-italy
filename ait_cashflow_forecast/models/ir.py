from odoo import fields, models


class IrModel(models.Model):
    _inherit = "ir.model"

    cashflow_enabled = fields.Boolean(
        string="Cashflow Forecasting",
        default=False,
        help="Whether this model supports cashflow forecasting.",
    )
