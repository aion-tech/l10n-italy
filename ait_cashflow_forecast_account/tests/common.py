from datetime import timedelta

from odoo import SUPERUSER_ID, Command, api, fields
from odoo.addons.ait_cashflow_forecast.tests.common import CashflowTestCommon
from odoo.tests import tagged


@tagged("-at_install", "post_install", "ait_cashflow")
class TestCashflowForecastAccountCommon(CashflowTestCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def _create_invoice(
        cls,
        move_type="out_invoice",
        invoice_amount=50,
        currency_id=None,
        partner_id=None,
        invoice_date=None,
        payment_term_id=False,
        auto_validate=False,
    ):
        vals = dict(
            move_type=move_type,
            partner_id=partner_id.id,
            invoice_date=fields.Date.from_string(invoice_date),
            date=fields.Date.from_string(invoice_date),
            invoice_line_ids=[
                (
                    0,
                    0,
                    {
                        "name": "invoice line for %s" % invoice_amount,
                        "quantity": 1,
                        "price_unit": invoice_amount,
                        "tax_ids": [Command.set([])],
                    },
                )
            ],
        )
        if payment_term_id:
            vals["invoice_payment_term_id"] = payment_term_id
        if currency_id:
            vals["currency_id"] = currency_id
        invoice = (
            cls.env["account.move"]
            # .with_context(default_move_type=move_type)
            .create(vals)
        )
        if auto_validate:
            invoice.action_post()
        return invoice
