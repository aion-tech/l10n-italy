from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_ait_cashflow_forecast_account = fields.Boolean(string="Account")
    module_ait_cashflow_forecast_crm = fields.Boolean(string="CRM")
    # module_ait_cashflow_forecast_mis = fields.Boolean(string="MIS")
    module_ait_cashflow_forecast_purchase = fields.Boolean(string="Purchase")
    module_ait_cashflow_forecast_sale = fields.Boolean(string="Sale")
    cashflow_billing_lead_time = fields.Integer(
        related='company_id.cashflow_billing_lead_time',
        readonly=False,
        string='Billing Lead Time (days)'
        )
