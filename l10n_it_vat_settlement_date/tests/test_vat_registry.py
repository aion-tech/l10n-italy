#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from odoo import Command
from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestVATRegistry(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.supplier_bill = cls.init_invoice(
            "in_invoice",
            amounts=[
                100,
            ],
            post=True,
        )
        cls.supplier_journal = cls.company_data["default_journal_purchase"]
        cls.supplier_tax_registry = cls.env["account.tax.registry"].create(
            {
                "name": "Sales",
                "layout_type": "customer",
                "journal_ids": [
                    Command.set(cls.supplier_journal.ids),
                ],
            }
        )

    def _get_wizard(self, from_date, to_date, tax_registry):
        """Create the wizard to print the VAT Registry."""
        wizard_form = Form(self.env["wizard.registro.iva"])
        wizard_form.from_date = from_date
        wizard_form.to_date = to_date
        wizard_form.tax_registry_id = tax_registry
        wizard = wizard_form.save()
        return wizard

    def _get_report(self, from_date, to_date, tax_registry):
        """Print the VAT Registry."""
        wizard = self._get_wizard(from_date, to_date, tax_registry)

        report_action = wizard.with_context(discard_logo_check=True).print_registro()
        report_name = report_action["report_name"]
        report_context = report_action["context"]
        report_data = report_action["data"]
        html, _report_type = (
            self.env["ir.actions.report"]
            .with_context(**report_context)
            ._render_qweb_html(report_name, wizard.ids, data=report_data)
        )
        return html

    def test_report(self):
        """The settlement date decides whether a move is in the report."""
        # Arrange: a date range and a bill out of that range
        bill = self.supplier_bill
        settlement_date = bill.l10n_it_vat_settlement_date
        tax_registry = self.supplier_tax_registry
        from_date = datetime.date(2020, 1, 1)
        to_date = datetime.date(2020, 12, 31)
        # pre-condition: the report does not contain the bill
        self.assertFalse(from_date <= settlement_date <= to_date)
        html = self._get_report(
            from_date,
            to_date,
            tax_registry,
        )
        self.assertNotIn(bill.name, html.decode())

        # Act: move the settlement date in the report date range
        bill.l10n_it_vat_settlement_date = from_date

        # Assert: the report now contains the bill
        html = self._get_report(
            from_date,
            to_date,
            tax_registry,
        )
        self.assertIn(bill.name, html.decode())
