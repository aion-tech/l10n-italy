from odoo import SUPERUSER_ID, api

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    template_fattura_accompagnatoria = env.ref('l10n_it_shipping_invoice.shipping_invoice_report')    
    template_fattura_accompagnatoria.unlink_action()
    template_account_invoice_without_payment = env.ref('account.account_invoices_without_payment')
    template_account_invoice_without_payment.unlink_action()

def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    template_fattura_accompagnatoria = env.ref('l10n_it_shipping_invoice.shipping_invoice_report')
    template_fattura_accompagnatoria.create_action()
    template_account_invoice_without_payment = env.ref('account.account_invoices_without_payment')
    template_account_invoice_without_payment.create_action()