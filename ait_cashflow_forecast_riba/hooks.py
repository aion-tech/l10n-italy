from odoo import SUPERUSER_ID, api


def post_init_hook(cr, _):
    env = api.Environment(cr, SUPERUSER_ID, {})
    model = env["ir.model"].search([('model', '=', 'riba.distinta.line')])
    model.cashflow_enabled = True
