from typing import Any, Dict, List

from odoo import api, fields, models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "cashflow.mixin"]

    def _split_cashflow_record_vals(self, vals: dict) -> List[Dict[str, Any]]:
        self.ensure_one()
        if not self.payment_term_id:
            return [vals]

        terms = self.payment_term_id._compute_terms(
            self.commitment_date or self.expected_date,
            self.currency_id,
            self.company_id,
            self.amount_tax,
            # tax_amount_currency, TODO
            self.amount_tax,
            1,
            self.amount_untaxed,
            # untaxed_amount_currency, TODO
            self.amount_untaxed,
        )
        split_vals: List[Dict[str, Any]] = list()
        sign = self._get_cashflow_amount_sign(
            self.cashflow_config_id.amount_sign_formula
        )
        for term in terms:
            new_vals = vals.copy()
            new_vals.update(
                {
                    "date": term["date"],
                    "amount": sign * term["company_amount"],
                }
            )
            split_vals.append(new_vals)

        return split_vals
