from odoo import _, api, fields, models

from ..api.bluenext import Bluenext


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    bluenext_base_url = fields.Char(
        related="company_id.bluenext_base_url",
        readonly=False,
    )
    bluenext_username = fields.Char(
        related="company_id.bluenext_username",
        readonly=False,
    )
    bluenext_password = fields.Char(
        related="company_id.bluenext_password",
        readonly=False,
    )
    bluenext_state_map_ids = fields.Many2many(
        related="company_id.bluenext_state_map_ids",
        readonly=False,
    )
    bluenext_last_download_date = fields.Datetime(
        related="company_id.bluenext_last_download_date",
        readonly=False,
    )

    @api.onchange("bluenext_base_url")
    def onchange_bluenext_base_url(self):
        if self.bluenext_base_url:
            if not self.bluenext_base_url.endswith("/"):
                self.bluenext_base_url += "/"
