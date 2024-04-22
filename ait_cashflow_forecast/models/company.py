from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    cashflow_billing_lead_time = fields.Integer('Billing Lead Time (days)')
