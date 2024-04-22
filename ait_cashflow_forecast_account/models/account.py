from typing import Any, Dict, List

from odoo import api, fields, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ["account.move", "cashflow.mixin"]

    def _split_cashflow_record_vals(self, vals: dict) -> List[Dict[str, Any]]:
        self.ensure_one()
        terms = self.needed_terms
        if not terms:
            return [vals]
        split_vals: List[Dict[str, Any]] = list()
        for k, v in terms.items():
            new_vals = vals.copy()
            new_vals.update(
                {
                    "date": k["date_maturity"],
                    "amount": v["amount_currency"],
                }
            )
            split_vals.append(new_vals)

        return split_vals
