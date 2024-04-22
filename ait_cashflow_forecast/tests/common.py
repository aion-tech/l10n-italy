from odoo import Command
from odoo.tests import TransactionCase


class CashflowTestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Mario s.r.l.",
                "is_company": True,
                "country_id": cls.env.ref("base.it").id,
            }
        )
        cls.custom_payment_terms = cls.env["account.payment.term"].create(
            {
                "name": "turlututu",
                "line_ids": [
                    Command.create(
                        {
                            "value": "percent",
                            "value_amount": 10,
                            "days": 2,
                        }
                    ),
                    Command.create(
                        {
                            "value": "percent",
                            "value_amount": 20,
                            "days": 4,
                        }
                    ),
                    Command.create(
                        {
                            "value": "percent",
                            "value_amount": 20,
                            "days": 6,
                        }
                    ),
                    Command.create(
                        {
                            "value": "balance",
                            "days": 8,
                        }
                    ),
                ],
            }
        )
        cls.product_a = cls.env["product.product"].create(
            {
                "name": "product_a",
                "lst_price": 1000.0,
                "standard_price": 800.0,
            }
        )
