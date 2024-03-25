#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AssetComputeDepreciableAmount(models.AbstractModel):
    _name = "l10n_it_asset_management.compute.depreciable_amount"
    _description = "Compute depreciable amount"

    base_computation = fields.Selection(
        selection=[
            ("coeff", "Coefficient"),
            ("max_amount", "Maximum amount"),
        ],
        default="coeff",
        required=True,
        string="Depreciable amount computation",
        help="How to compute the depreciable amount based on the purchase amount.",
    )
    base_coeff = fields.Float(
        default=1,
        help="Coeff to compute depreciable amount from purchase amount",
        string="Dep Base Coeff",
    )
    base_max_amount = fields.Float(
        string="Maximum depreciable amount",
    )

    def _get_depreciable_amount(self, base_amount):
        self.ensure_one()
        computation_method = self.base_computation
        if computation_method == "coeff":
            depreciable_amount = base_amount * self.base_coeff
        elif computation_method == "max_amount":
            depreciable_amount = min(base_amount, self.base_max_amount)
        else:
            depreciable_amount = base_amount
        return depreciable_amount
