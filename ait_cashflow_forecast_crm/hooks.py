from odoo import SUPERUSER_ID, api


def post_init_hook(cr, _):
    env = api.Environment(cr, SUPERUSER_ID, {})
    model = env["ir.model"].search([("model", "=", "crm.lead")])
    model.cashflow_enabled = True
