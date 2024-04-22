# from odoo.addons.ait_cashflow_forecast.tests.common import CashflowTestCommon
from odoo.tests import TransactionCase
from odoo.tests.common import Form, tagged

from .common import CashflowTestCommon


@tagged("post_install", "-at_install", "ait_cashflow")
class TestCashflowRecord(CashflowTestCommon):
    def setUp(self):
        super(TestCashflowRecord, self).setUp()

    def test_cashflow_record_amount_0_no_create(self):
        # Arrange
        # Act
        res0 = self.env["cashflow.record"].create({"amount": 0})
        res1 = self.env["cashflow.record"].create({"amount": 0.99})
        # Assert
        self.assertFalse(res0)
        self.assertEqual(len(res0), 0)
        self.assertTrue(res1)
        self.assertEqual(len(res1), 1)
