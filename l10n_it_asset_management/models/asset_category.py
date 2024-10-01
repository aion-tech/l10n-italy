# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Command


class AssetCategory(models.Model):
    _name = "asset.category"
    _description = "Asset Category"
    _order = "name"

    @api.model
    def get_default_company_id(self):
        return self.env.company

    @api.model
    def get_default_type_ids(self):
        mode_obj = self.env["asset.depreciation.mode"]
        dom = [("company_id", "=", self.get_default_company_id().id)]
        mode = mode_obj.search(dom + [("default", "=", True)], limit=1)
        # Field ``mode_id`` is required for asset.category.depreciation.type;
        # if no default mode is found, retry by getting the first one found.
        if not mode:
            mode = mode_obj.search(dom, limit=1)

        types = self.env["asset.depreciation.type"].search(dom)

        # Raise error if configuration has not been completed.
        if not (mode and types):
            raise UserError(
                _(
                    "Before creating new categories, please complete the"
                    " assets' configuration for both depreciation types"
                    " and modes."
                )
            )

        return [
            Command.create(
                {"base_coeff": 1, "depreciation_type_id": t.id, "mode_id": mode.id}
            )
            for t in types
        ]

    asset_account_id = fields.Many2one(
        "account.account",
        required=True,
        string="Asset Account",
    )

    comment = fields.Text()

    company_id = fields.Many2one(
        "res.company", default=get_default_company_id, string="Company"
    )

    depreciation_account_id = fields.Many2one(
        "account.account",
        required=True,
        string="Depreciation Account",
    )

    fund_account_id = fields.Many2one(
        "account.account",
        required=True,
        string="Fund Account",
    )

    gain_account_id = fields.Many2one(
        "account.account",
        required=True,
        string="Capital Gain Account",
    )

    journal_id = fields.Many2one("account.journal", required=True, string="Journal")

    loss_account_id = fields.Many2one(
        "account.account",
        required=True,
        string="Capital Loss Account",
    )

    name = fields.Char(
        required=True,
    )

    print_by_default = fields.Boolean(
        default=True,
        help="Defines whether a category should be added by default when"
        " printing assets' reports.",
    )

    tag_ids = fields.Many2many(
        "asset.tag",
        string="Tag",
    )

    type_ids = fields.One2many(
        "asset.category.depreciation.type",
        "category_id",
        default=get_default_type_ids,
        string="Depreciation Types",
    )

    def copy(self, default=None):
        default = dict(default or [])
        default.update(
            {
                "tag_ids": [Command.set(self.tag_ids.ids)],
                "type_ids": [
                    Command.create(t.copy_data({"category_id": False})[0])
                    for t in self.type_ids
                ],
            }
        )
        return super().copy(default)

    @api.ondelete(
        at_uninstall=False,
    )
    def _unlink_except_in_asset(self):
        if self.env["asset.asset"].sudo().search([("category_id", "in", self.ids)]):
            raise UserError(
                _("Cannot delete categories while they're still linked" " to an asset.")
            )

    def get_depreciation_vals(self, amount_depreciable=0):
        return [t.get_depreciation_vals(amount_depreciable) for t in self.type_ids]
