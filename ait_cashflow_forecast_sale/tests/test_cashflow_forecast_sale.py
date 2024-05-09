from datetime import timedelta

from odoo import SUPERUSER_ID, Command, api, fields
from odoo.addons.ait_cashflow_forecast.tests.common import CashflowTestCommon
from odoo.tests import tagged


@tagged("-at_install", "post_install", "ait_cashflow")
class TestCashflowForecastSaleOrder(CashflowTestCommon):

    def setUp(self):
        super().setUp()

        self.default_so_vals = dict(
            order_amount=50,
            currency_id=None,
            partner_id=self.partner,
            commitment_date="1999-12-25",
            payment_term_id=False,
        )

    def _create_so(
        self,
        order_amount=50,
        currency_id=None,
        partner_id=None,
        commitment_date=None,
        payment_term_id=False,
    ):
        vals = dict(
            partner_id=partner_id.id,
            commitment_date=fields.Date.from_string(commitment_date),
            order_line=[
                (
                    0,
                    0,
                    {
                        "product_id": self.product_a.id,
                        "product_uom_qty": 1,
                        "price_unit": order_amount,
                        "tax_id": [Command.set([])],
                    },
                )
            ],
        )
        if payment_term_id:
            vals["payment_term_id"] = payment_term_id
        if currency_id:
            vals["currency_id"] = currency_id
        order = self.env["sale.order"].create(vals)
        return order

    def test_sale_order_cashflow_record(self):
        # Arrange
        # Act
        so = self._create_so(**self.default_so_vals)
        # Assert
        self.assertTrue(so.cashflow_config_id)
        self.assertTrue(so.cashflow_record_ids)
        self.assertEqual(so.cashflow_records_count, 1)

    def test_sale_order_cashflow_record_update_amount(self):
        """updating a sale order amount should update
        the amount on its cashflow record(s)"""
        # Arrange
        so = self._create_so(**self.default_so_vals)
        # Pre-condition: cashflow record created
        self.assertTrue(so.cashflow_config_id)
        self.assertTrue(so.cashflow_record_ids)
        self.assertEqual(so.cashflow_records_count, 1)
        # Act
        new_total = so.amount_total * 2
        so.order_line[0].product_uom_qty = 2
        so.order_line[0].price_unit = self.default_so_vals["order_amount"]
        so._compute_amounts()
        # Assert
        self.assertTrue(so.cashflow_config_id)
        self.assertTrue(so.cashflow_record_ids)
        self.assertEqual(so.cashflow_records_count, 1)
        self.assertEqual(so.cashflow_record_ids.amount, new_total)

    def test_sale_order_cashflow_record_update_date(self):
        """updating a sale order date should update
        the date on its cashflow record(s)"""
        # Arrange
        vals = self.default_so_vals.copy()
        vals.update(dict(commitment_date="2000-01-01"))
        so = self._create_so(**vals)
        # Pre-condition: cashflow record created
        self.assertTrue(so.cashflow_config_id)
        self.assertTrue(so.cashflow_record_ids)
        self.assertEqual(so.cashflow_records_count, 1)
        # Act
        new_date = so.commitment_date.date() + timedelta(days=2)
        so.commitment_date = new_date
        # Assert
        self.assertTrue(so.cashflow_config_id)
        self.assertTrue(so.cashflow_record_ids)
        self.assertEqual(so.cashflow_records_count, 1)
        self.assertEqual(so.cashflow_record_ids.date, new_date)

    def test_sale_order_with_payment_terms(self):
        """creating a sale order with payment terms should create
        n cashflow records based on terms"""
        # Arrange
        vals = self.default_so_vals.copy()
        order_amount = 1000
        vals.update(
            dict(
                commitment_date="2000-01-01",
                payment_term_id=self.custom_payment_terms.id,
                order_amount=order_amount,
            )
        )
        # Act
        so = self._create_so(**vals)
        # Assert
        self.assertTrue(so.cashflow_config_id)
        self.assertTrue(so.cashflow_record_ids)
        self.assertEqual(so.cashflow_records_count, 4)
        expected_terms = [
            ("2000-01-03", order_amount * 0.1),  # 2 days, 10%
            ("2000-01-05", order_amount * 0.2),  # 4 days, 20%
            ("2000-01-07", order_amount * 0.2),  # 6 days, 20%
            ("2000-01-09", order_amount * 0.5),  # 8 days, 50%
        ]
        for cashflow_rec, payment_term in zip(so.cashflow_record_ids, expected_terms):
            date, amt = payment_term
            self.assertEqual(fields.Date.to_string(cashflow_rec.date), date)
            self.assertEqual(cashflow_rec.amount, amt)

    def test_sale_order_invoice_cashflow_record(self):
        # Arrange
        ait_cashflow_forecast_account = self.env["ir.module.module"].search(
            [("name", "=", "ait_cashflow_forecast_account")]
        )
        if not ait_cashflow_forecast_account.state == "installed":
            return
        vals = self.default_so_vals.copy()
        vals.update(dict(commitment_date="2000-01-01"))
        so = self._create_so(**vals)
        # Act
        wizard_ctx = {
            "active_model": "sale.order",
            "active_ids": so.ids,
            "sale_order_ids": so.ids,
        }
        InvoiceWizard = self.env["sale.advance.payment.inv"].with_context(**wizard_ctx)
        so.action_confirm()
        for order_line in so.order_line:
            order_line.qty_delivered = order_line.product_uom_qty
        InvoiceWizard.create({"advance_payment_method": "delivered"}).create_invoices()
        so.invoice_ids.action_post()
        # Assert
        self.assertFalse(so.cashflow_record_ids)
        self.assertEqual(so.cashflow_records_count, 0)
        self.assertTrue(so.invoice_ids.cashflow_record_ids)
        self.assertEqual(so.invoice_ids.cashflow_records_count, 1)

    def test_sale_order_cancel(self):
        # Arrange
        so = self._create_so(**self.default_so_vals)
        # Act
        so.action_cancel()
        # Assert
        self.assertFalse(so.cashflow_record_ids)
        self.assertEqual(len(so.cashflow_record_ids), 0)
