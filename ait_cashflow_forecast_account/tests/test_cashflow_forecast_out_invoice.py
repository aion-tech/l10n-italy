from datetime import timedelta

from odoo import SUPERUSER_ID, Command, api, fields
from odoo.tests import tagged

from .common import TestCashflowForecastAccountCommon


@tagged("-at_install", "post_install", "ait_cashflow")
class TestCashflowForecastAccountOutInvoice(TestCashflowForecastAccountCommon):

    def setUp(self):
        super().setUp()
        self.default_inv_vals = dict(
            move_type="out_invoice",
            invoice_amount=50,
            currency_id=None,
            partner_id=self.partner,
            invoice_date="2099-12-25",
            payment_term_id=False,
            auto_validate=False,
        )

    def test_customer_invoice_cashflow_record(self):
        # Arrange
        vals = self.default_inv_vals.copy()
        vals.update(dict(auto_validate=True))
        # Act
        invoice = self._create_invoice(**vals)
        # Assert
        self.assertTrue(invoice.cashflow_config_id)
        self.assertTrue(invoice.cashflow_record_ids)
        self.assertEqual(invoice.cashflow_records_count, 1)

    def test_customer_invoice_cashflow_record_update_amount(self):
        """updating an invoice amount should update
        the amount on its cashflow record(s)"""
        # Arrange
        vals = self.default_inv_vals.copy()
        vals.update(dict(invoice_date="2000-01-01"))
        invoice = self._create_invoice(**vals)
        # Pre-condition: cashflow record created
        self.assertTrue(invoice.cashflow_config_id)
        self.assertTrue(invoice.cashflow_record_ids)
        self.assertEqual(invoice.cashflow_records_count, 1)
        # Act
        new_total = invoice.amount_total * 2
        invoice.invoice_line_ids[0].quantity = 2
        invoice._compute_tax_totals()
        # Assert
        self.assertTrue(invoice.cashflow_config_id)
        self.assertTrue(invoice.cashflow_record_ids)
        self.assertEqual(invoice.cashflow_records_count, 1)
        self.assertEqual(invoice.cashflow_record_ids.amount, new_total)

    def test_customer_invoice_cashflow_record_update_date(self):
        """updating an invoice date should update
        the date on its cashflow record(s)"""
        # Arrange
        vals = self.default_inv_vals.copy()
        vals.update(dict(invoice_date="2000-01-01"))
        invoice = self._create_invoice(**vals)
        # Pre-condition: cashflow record created
        self.assertTrue(invoice.cashflow_config_id)
        self.assertTrue(invoice.cashflow_record_ids)
        self.assertEqual(invoice.cashflow_records_count, 1)
        # Act
        new_date = invoice.invoice_date + timedelta(days=2)
        invoice.invoice_date = new_date
        # Assert
        self.assertTrue(invoice.cashflow_config_id)
        self.assertTrue(invoice.cashflow_record_ids)
        self.assertEqual(invoice.cashflow_records_count, 1)
        self.assertEqual(invoice.cashflow_record_ids.date, new_date)

    def test_customer_invoice_with_payment_terms(self):
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
            ("2000-01-03", invoice_amount * 0.1),  # 2 days, 10%
            ("2000-01-05", invoice_amount * 0.2),  # 4 days, 20%
            ("2000-01-07", invoice_amount * 0.2),  # 6 days, 20%
            ("2000-01-09", invoice_amount * 0.5),  # 8 days, 50%
        ]
        for cashflow_rec, payment_term in zip(
            invoice.cashflow_record_ids, expected_terms
        ):
            date, amt = payment_term
            self.assertEqual(fields.Date.to_string(cashflow_rec.date), date)
            self.assertEqual(cashflow_rec.amount, amt)
