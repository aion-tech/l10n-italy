# Copyright 2022 Simone Rubino - TAKOBI
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

import xmlschema

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged
from odoo.tests.common import Form

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

from ..tools.account_tools import fpa_schema


@tagged("post_install", "-at_install")
class TestAccount(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.group_1 = cls.env["account.group"].create(
            {
                "name": "1",
                "code_prefix_start": "it.account.",
            }
        )
        cls.iva_22I5 = cls.env["account.tax"].create(
            {
                "name": "IVA al 22% detraibile al 50%",
                "description": "22I5",
                "amount": 22,
                "amount_type": "percent",
                "type_tax_use": "purchase",
                "price_include": False,
                "invoice_repartition_line_ids": [
                    (5, 0, 0),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 50,
                            "repartition_type": "tax",
                            "account_id": cls.company_data["default_account_assets"].id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 50,
                            "repartition_type": "tax",
                        },
                    ),
                ],
                "refund_repartition_line_ids": [
                    (5, 0, 0),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 50,
                            "repartition_type": "tax",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 50,
                            "repartition_type": "tax",
                            "account_id": cls.company_data["default_account_assets"].id,
                        },
                    ),
                ],
            }
        )
        cls.vat_not_deductible = cls.env["account.tax"].create(
            {
                "name": "VAT 22% not deductible",
                "description": "NOTDED",
                "amount": 22,
                "amount_type": "percent",
                "type_tax_use": "purchase",
                "price_include": False,
                "invoice_repartition_line_ids": [
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                        },
                    ),
                ],
                "refund_repartition_line_ids": [
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                        },
                    ),
                ],
            }
        )

    def test_group_constraint(self):
        self.env["account.account"].create(
            {
                "name": "it_account_1",
                "code": "it.account.1",
                "account_type": "asset_current",
            }
        )
        with self.assertRaises(ValidationError):
            self.env["account.account"].create(
                {
                    "name": "it_account_2",
                    "code": "it.account.2",
                    "account_type": "liability_current",
                }
            )

    def test_group_recursion(self):
        """
        It is not possible to create recursive account groups.
        """
        child_group = self.env["account.group"].create(
            {
                "name": "child",
                "code_prefix_start": "it.account.child",
                "parent_id": self.group_1.id,
            }
        )
        with self.assertRaises(UserError) as ue:
            self.group_1.parent_id = child_group
        exc_message = ue.exception.args[0]
        self.assertEqual("Recursion Detected.", exc_message)

    def test_vat_22_50(self):
        today = fields.Date.today()
        move_form = Form(
            self.env["account.move"].with_context(default_move_type="in_invoice")
        )
        move_form.partner_id = self.env.ref("base.res_partner_12")
        move_form.invoice_date = today
        with move_form.invoice_line_ids.new() as line_form:
            line_form.name = "test line"
            line_form.price_unit = 100
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.iva_22I5)
        rslt = move_form.save()
        rslt.action_post()
        context = {
            "from_date": today,
            "to_date": today,
        }
        tax = self.env["account.tax"].with_context(**context).browse(self.iva_22I5.id)
        self.assertEqual(tax.balance, -22)
        self.assertEqual(tax.deductible_balance, -11)
        self.assertEqual(tax.undeductible_balance, -11)

    def test_vat_22_not_deductible(self):
        today = fields.Date.today()
        self.init_invoice(
            "in_invoice",
            invoice_date=today,
            amounts=[100],
            taxes=self.vat_not_deductible,
            post=True,
        )
        context = {
            "from_date": today,
            "to_date": today,
        }
        tax = (
            self.env["account.tax"]
            .with_context(**context)
            .browse(self.vat_not_deductible.id)
        )
        self.assertEqual(tax.balance, -22)
        self.assertEqual(tax.deductible_balance, 0)
        self.assertEqual(tax.undeductible_balance, -22)

    def test_partially_deductible_balance_recomputation(self):
        """Check that deductible and not deductible balances
        are computed correctly for different dates."""
        today = fields.Date.today()
        self.init_invoice(
            "in_invoice",
            partner=self.env.ref("base.res_partner_12"),
            invoice_date=today,
            post=True,
            amounts=[100],
            taxes=self.iva_22I5,
        )
        tomorrow = today + datetime.timedelta(days=1)
        self.init_invoice(
            "in_invoice",
            partner=self.env.ref("base.res_partner_12"),
            invoice_date=tomorrow,
            post=True,
            amounts=[200],
            taxes=self.iva_22I5,
        )

        # Check today's balance
        self.check_date_balance(self.iva_22I5, today, -11, -11)

        # Check tomorrow's balance
        self.check_date_balance(self.iva_22I5, tomorrow, -22, -22)

    def test_xmlschema_loading(self):
        self.assertIsInstance(fpa_schema, xmlschema.XMLSchema)

    def check_date_balance(self, tax, date, deductible, not_deductible):
        """Compare expected balances with tax's balance in specified date."""
        tax = tax.with_context(
            from_date=date,
            to_date=date,
        )
        self.assertEqual(tax.deductible_balance, deductible)
        self.assertEqual(tax.undeductible_balance, not_deductible)

    def test_children_group_sign(self):
        """Groups in a parent/child relationship have the same sign."""
        account = self.env["account.account"].create(
            {
                "name": "it_account_1",
                "code": "it.account.1",
                "account_type": "liability_current",
            }
        )
        group = self.group_1
        account_sign = -1
        # pre-condition
        self.assertEqual(account.account_balance_sign, account_sign)
        self.assertEqual(account.group_id, group)
        self.assertEqual(group.account_balance_sign, account_sign)
        self.assertEqual(group.account_ids, account)

        # Act
        child_group = group.copy(
            default={
                "code_prefix_start": "it.account.1",
                "code_prefix_end": "it.account.1",
            },
        )

        # Assert
        # The relationship of account groups is peculiar:
        # if a group has a parent_id it doesn't imply it is child_of the parent_id
        self.assertEqual(child_group.parent_id, group)
        children_groups = self.env["account.group"].search(
            [
                ("id", "child_of", group.ids),
            ],
        )
        self.assertNotIn(child_group, children_groups)
        # The account has been reassigned to the most specific group
        self.assertFalse(group.account_ids)
        self.assertEqual(child_group.account_ids, account)
        # Signs are consistent
        (group + child_group).invalidate_recordset(
            fnames=[
                "account_balance_sign",
            ],
        )
        self.assertEqual(group.account_balance_sign, account_sign)
        self.assertEqual(child_group.account_balance_sign, account_sign)

    def test_compute_totals_tax_journal_change(self):
        """Compute the amount of a tax for specific journals: it changes."""
        # Arrange
        invoice_date = datetime.date(2020, month=1, day=1)
        tax = self.iva_22I5
        bill = self.init_invoice(
            "in_invoice",
            invoice_date=invoice_date,
            amounts=[100],
            post=True,
            taxes=tax,
        )

        # Assert
        bill_journal = bill.journal_id
        other_journals = self.env["account.journal"].search(
            [("id", "!=", bill_journal.id)]
        )
        date_context = {
            "from_date": invoice_date,
            "to_date": invoice_date,
        }
        self.assertRecordValues(
            tax.with_context(**date_context),
            [
                {
                    "base_balance": -100,
                    "balance": -22,
                    "deductible_balance": -11,
                    "undeductible_balance": -11,
                }
            ],
        )
        self.assertRecordValues(
            tax.with_context(
                **date_context, l10n_it_account_journal_ids=bill_journal.ids
            ),
            [
                {
                    "base_balance": -100,
                    "balance": -22,
                    "deductible_balance": -11,
                    "undeductible_balance": -11,
                }
            ],
        )
        self.assertRecordValues(
            tax.with_context(
                **date_context, l10n_it_account_journal_ids=other_journals.ids
            ),
            [
                {
                    "base_balance": 0,
                    "balance": 0,
                    "deductible_balance": 0,
                    "undeductible_balance": 0,
                }
            ],
        )
