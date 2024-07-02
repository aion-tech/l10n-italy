#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo import Command
from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestGenerateFile(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        company = cls.env.company
        company.initiating_party_identifier = "CUC Code"
        company.initiating_party_issuer = "CBI"

        company_bank_account_form = Form(cls.env["res.partner.bank"])
        company_bank_account_form.acc_number = "IT89O0300203280429513916296"
        company_bank_account_form.partner_id = company.partner_id
        cls.company_bank_account = company_bank_account_form.save()

        cls.bank_journal = cls.company_data["default_journal_bank"]
        cls.bank_journal.bank_account_id = cls.company_bank_account

        cls.supplier_bank = cls.env["res.bank"].create(
            {
                "name": "Test supplier bank",
                "bic": "TESTBICA",
            }
        )

        cls.supplier = cls.env["res.partner"].create(
            {
                "name": "Test supplier",
                "bank_ids": [
                    Command.create(
                        {
                            "acc_number": "IT48N0300203280543765183341",
                            "bank_id": cls.supplier_bank.id,
                        }
                    ),
                ],
            }
        )

        cls.payment_method = cls.env.ref("l10n_it_sct_cbi.sepa_cbi_credit_transfer")

        payment_mode_form = Form(cls.env["account.payment.mode"])
        payment_mode_form.name = "Test SEPA CBI payment mode"
        payment_mode_form.bank_account_link = "fixed"
        payment_mode_form.fixed_journal_id = cls.bank_journal
        payment_mode_form.payment_method_id = cls.payment_method
        cls.payment_mode = payment_mode_form.save()

    def _get_record_from_action(self, action):
        record_id = action["res_id"]
        record_model = action["res_model"]
        return self.env[record_model].browse(record_id)

    def _get_payment_order(self, invoices):
        payment_order_action = invoices.create_account_payment_line()
        return self._get_record_from_action(payment_order_action)

    def _get_payment_attachment(self, invoices):
        payment_order = self._get_payment_order(invoices)
        payment_order.draft2open()
        payment_file_action = payment_order.open2generated()
        return self._get_record_from_action(payment_file_action)

    def test_generate_2_bills(self):
        """Generate a payment file for 2 vendor bills."""
        payment_mode = self.payment_mode
        supplier = self.supplier

        bill_1 = self.init_invoice(
            "in_invoice",
            partner=supplier,
            amounts=[
                100,
            ],
            post=True,
        )
        bill_1.ref = "Test invoice 1"
        bill_2 = self.init_invoice(
            "in_invoice",
            partner=supplier,
            amounts=[
                200,
            ],
            post=True,
        )
        bill_2.ref = "Test invoice 2"
        bills = bill_1 | bill_2
        bills.payment_mode_id = payment_mode

        payment_att = self._get_payment_attachment(bills)
        payment_att_content = base64.b64decode(payment_att.datas).decode()
        self.assertIn(bill_1.ref, payment_att_content)
        self.assertIn(bill_2.ref, payment_att_content)
