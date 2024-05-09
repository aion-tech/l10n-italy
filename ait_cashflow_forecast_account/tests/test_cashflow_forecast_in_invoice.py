from datetime import timedelta

from odoo import SUPERUSER_ID, Command, api, fields
from odoo.tests import tagged

from .common import TestCashflowForecastAccountCommon


@tagged("-at_install", "post_install", "ait_cashflow")
class TestCashflowForecastAccountInInvoice(TestCashflowForecastAccountCommon):

    def setUp(self):
        super().setUp()

        self.default_inv_vals = dict(
            move_type="in_invoice",
            invoice_amount=50,
            currency_id=None,
            partner_id=self.partner,
            invoice_date="1999-12-25",
            payment_term_id=False,
            auto_validate=False,
        )

    def test_supplier_invoice_cashflow_record_sign(self):
        # Arrange
        # Act
        invoice = self._create_invoice(**self.default_inv_vals)
        # Assert
        self.assertTrue(invoice.cashflow_config_id)
        self.assertTrue(invoice.cashflow_record_ids)
        self.assertEqual(invoice.cashflow_records_count, 1)
        self.assertTrue(invoice.cashflow_record_ids.amount < 0)

    def test_supplier_invoice_cashflow_record_update_amount(self):
        """updating an invoice amount should
        update the amount on its cashflow record(s)"""
        # Arrange
        invoice = self._create_invoice(**self.default_inv_vals)
        # Pre-condition: cashflow record created
        self.assertTrue(invoice.cashflow_config_id)
        self.assertTrue(invoice.cashflow_record_ids)
        self.assertEqual(invoice.cashflow_records_count, 1)
        # Act
        new_total = invoice.amount_total * 2 * -1
        invoice.invoice_line_ids[0].quantity = 2
        invoice.invoice_line_ids[0]._compute_totals()
        # Assert
        self.assertTrue(invoice.cashflow_config_id)
        self.assertTrue(invoice.cashflow_record_ids)
        self.assertEqual(invoice.cashflow_records_count, 1)
        self.assertEqual(invoice.cashflow_record_ids.amount, new_total)

    def test_supplier_invoice_with_payment_terms(self):
        """creating an invoice with payment terms should create
        n cashflow records based on terms"""
        # Arrange
        vals = self.default_inv_vals.copy()
        invoice_amount = 1000
        vals.update(
            dict(
                invoice_date="2000-01-01",
                payment_term_id=self.custom_payment_terms.id,
                invoice_amount=invoice_amount,
            )
        )
        # Act
        invoice = self._create_invoice(**vals)
        # Assert
        self.assertTrue(invoice.cashflow_config_id)
        self.assertTrue(invoice.cashflow_record_ids)
        self.assertEqual(invoice.cashflow_records_count, 4)
        expected_terms = [
            ("2000-01-03", invoice_amount * 0.1 * -1),  # 2 days, 10%
            ("2000-01-05", invoice_amount * 0.2 * -1),  # 4 days, 20%
            ("2000-01-07", invoice_amount * 0.2 * -1),  # 6 days, 20%
            ("2000-01-09", invoice_amount * 0.5 * -1),  # 8 days, 50%
        ]
        for cashflow_rec, payment_term in zip(
            invoice.cashflow_record_ids, expected_terms
        ):
            date, amt = payment_term
            self.assertEqual(fields.Date.to_string(cashflow_rec.date), date)
            self.assertEqual(cashflow_rec.amount, amt)

    def test_supplier_invoice_cancel(self):
        """cancelling an invoice should unlink
        the invoice's cashflow record(s)"""
        # Arrange
        invoice = self._create_invoice(**self.default_inv_vals)
        # Pre-condition: cashflow record created
        self.assertTrue(invoice.cashflow_config_id)
        self.assertTrue(invoice.cashflow_record_ids)
        self.assertEqual(invoice.cashflow_records_count, 1)
        # Act
        cashflow_records = invoice.cashflow_record_ids.ids
        invoice.button_cancel()
        # Assert
        self.assertFalse(invoice.cashflow_record_ids)
        self.assertEqual(invoice.cashflow_records_count, 0)
        self.assertFalse(self.env["cashflow.record"].browse(cashflow_records).exists())
