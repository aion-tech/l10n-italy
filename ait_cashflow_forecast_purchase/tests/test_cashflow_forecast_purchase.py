from datetime import timedelta

from odoo import SUPERUSER_ID, Command, api, fields
from odoo.addons.ait_cashflow_forecast.tests.common import CashflowTestCommon
from odoo.tests import tagged


@tagged("-at_install", "post_install", "ait_cashflow")
class TestCashflowForecastPurchaseOrder(CashflowTestCommon):

    def setUp(self):
        super().setUp()

        self.default_po_vals = dict(
            order_amount=50,
            currency_id=None,
            partner_id=self.partner,
            date_planned="1999-12-25",
            payment_term_id=False,
        )

    def _create_po(
        self,
        order_amount=50,
        currency_id=None,
        partner_id=None,
        date_planned=None,
        payment_term_id=False,
    ):
        vals = dict(
            partner_id=partner_id.id,
            date_planned=fields.Date.from_string(date_planned),
            order_line=[
                (
                    0,
                    0,
                    {
                        "product_id": self.product_a.id,
                        "product_qty": 1,
                        "price_unit": order_amount,
                        "taxes_id": [Command.set([])],
                    },
                )
            ],
        )
        if payment_term_id:
            vals["payment_term_id"] = payment_term_id
        if currency_id:
            vals["currency_id"] = currency_id
        order = self.env["purchase.order"].create(vals)
        return order

    def test_purchase_order_cashflow_record_sign(self):
        # Arrange
        # Act
        po = self._create_po(**self.default_po_vals)
        # Assert
        self.assertTrue(po.cashflow_config_id)
        self.assertTrue(po.cashflow_record_ids)
        self.assertEqual(po.cashflow_records_count, 1)
        self.assertTrue(po.cashflow_record_ids.amount < 0)

    def test_purchase_order_cashflow_record_update_amount(self):
        """updating a purchase order amount should
        update the amount on its cashflow record(s)"""
        # Arrange
        po = self._create_po(**self.default_po_vals)
        # Pre-condition: cashflow record created
        self.assertTrue(po.cashflow_config_id)
        self.assertTrue(po.cashflow_record_ids)
        self.assertEqual(po.cashflow_records_count, 1)
        # Act
        new_total = po.amount_total * 2 * -1
        po.order_line[0].product_qty = 2
        po._amount_all()
        # Assert
        self.assertTrue(po.cashflow_config_id)
        self.assertTrue(po.cashflow_record_ids)
        self.assertEqual(po.cashflow_records_count, 1)
        self.assertEqual(po.cashflow_record_ids.amount, new_total)

    def test_purchase_order_cashflow_record_update_date(self):
        """updating a purchase order date should
        update the date on its cashflow record(s)"""
        # Arrange
        po = self._create_po(**self.default_po_vals)
        # Pre-condition: cashflow record created
        self.assertTrue(po.cashflow_config_id)
        self.assertTrue(po.cashflow_record_ids)
        self.assertEqual(po.cashflow_records_count, 1)
        # Act
        new_date = po.date_planned + timedelta(days=2)
        po.date_planned = new_date
        # Assert
        self.assertTrue(po.cashflow_config_id)
        self.assertTrue(po.cashflow_record_ids)
        self.assertEqual(po.cashflow_records_count, 1)
        self.assertEqual(po.cashflow_record_ids.date, new_date.date())

    def test_purchase_order_with_payment_terms(self):
        """creating a purchase order with payment terms should
        create n cashflow records based on terms"""
        # Arrange
        vals = self.default_po_vals.copy()
        order_amount = 1000
        vals.update(
            dict(
                date_planned="2000-01-01",
                payment_term_id=self.custom_payment_terms.id,
                order_amount=order_amount,
            )
        )
        # Act
        po = self._create_po(**vals)
        # Assert
        self.assertTrue(po.cashflow_config_id)
        self.assertTrue(po.cashflow_record_ids)
        self.assertEqual(po.cashflow_records_count, 4)
        expected_terms = [
            ("2000-01-03", order_amount * 0.1 * -1),  # 2 days, 10%
            ("2000-01-05", order_amount * 0.2 * -1),  # 4 days, 20%
            ("2000-01-07", order_amount * 0.2 * -1),  # 6 days, 20%
            ("2000-01-09", order_amount * 0.5 * -1),  # 8 days, 50%
        ]
        for cashflow_rec, payment_term in zip(po.cashflow_record_ids, expected_terms):
            date, amt = payment_term
            self.assertEqual(fields.Date.to_string(cashflow_rec.date), date)
            self.assertEqual(cashflow_rec.amount, amt)

    def test_purchase_order_invoice_cashflow_record(self):
        # Arrange
        ait_cashflow_forecast_account = self.env["ir.module.module"].search(
            [("name", "=", "ait_cashflow_forecast_account")]
        )
        if not ait_cashflow_forecast_account.state == "installed":
            return
        po = self._create_po(**self.default_po_vals)
        po.button_confirm()
        po.order_line.mapped(lambda l: l.write(dict(qty_received=l.product_qty)))
        # Act
        po.action_create_invoice()
        # Assert
        self.assertFalse(po.cashflow_record_ids)
        self.assertEqual(po.cashflow_records_count, 0)
        self.assertTrue(po.invoice_ids.cashflow_record_ids)
        self.assertEqual(po.invoice_ids.cashflow_records_count, 1)

    def test_purchase_order_cancel(self):
        # Arrange
        po = self._create_po(**self.default_po_vals)
        cashflow_record_ids = po.cashflow_record_ids.ids
        # Act
        po.button_cancel()
        # Assert
        cr_ids = self.env["cashflow.record"].browse(cashflow_record_ids).exists()
        self.assertFalse(cr_ids)
        self.assertEqual(len(cr_ids), 0)
