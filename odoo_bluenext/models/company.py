import json

from odoo import _, api, fields, models

from ..api.bluenext import Bluenext


class ResCompany(models.Model):
    _inherit = "res.company"

    bluenext_base_url = fields.Char(
        string="Bluenext Base URL",
        help="Bluenext API Base URL",
    )
    bluenext_username = fields.Char(
        string="Bluenext Username",
        help="Bluenext Username",
    )
    bluenext_password = fields.Char(
        string="Bluenext Password",
        help="Bluenext Password",
    )
    bluenext_access_token = fields.Char(
        string="Bluenext Access Token",
        help="Bluenext Access Token",
        readonly=True,
    )
    bluenext_access_token_expiration = fields.Datetime(
        string="Bluenext Access Token Expiration",
        help="Bluenext Access Token Expiration",
        readonly=True,
    )
    bluenext_last_download_date = fields.Datetime(
        string="Bluenext Last eBill Download Date",
        help="Bluenext Last eBill Download Date",
    )
    bluenext_state_map_ids = fields.Many2many(
        comodel_name="bluenext.state.map",
        relation="bluenext_state_map_res_company_rel",
        column1="company_id",
        column2="bluenext_state_map_id",
        string="Bluenext States Map",
        help="Bluenext States Map",
    )

    @api.onchange("bluenext_base_url")
    def onchange_bluenext_base_url(self):
        if self.bluenext_base_url:
            if not self.bluenext_base_url.endswith("/"):
                self.bluenext_base_url += "/"

    def _get_bluenext_access_token(self):
        if (
            not self.bluenext_access_token
            or not self.bluenext_access_token_expiration
            or fields.Datetime.now() > self.bluenext_access_token_expiration
        ):
            # need new access token
            return "", None
        else:
            return self.bluenext_access_token, self.bluenext_access_token_expiration

    def _init_bluenext(self):
        self.ensure_one()
        token, expiration = self._get_bluenext_access_token()
        bluenext = Bluenext(
            url=self.bluenext_base_url,
            username=self.bluenext_username,
            password=self.bluenext_password,
            access_token=token,
            access_token_expiration=expiration,
        )
        self.write(
            dict(
                bluenext_access_token=bluenext.access_token,
                bluenext_access_token_expiration=bluenext.access_token_expiration,
            )
        )
        self.env.cr.commit()
        return bluenext

    def btn_bluenext_regen_access_token(self):
        # not really needed, useful for debugging
        self.ensure_one()
        bluenext = Bluenext(
            url=self.bluenext_base_url,
            username=self.bluenext_username,
            password=self.bluenext_password,
            access_token="",
            access_token_expiration=None,
        )
        self.write(
            dict(
                bluenext_access_token=bluenext.access_token,
                bluenext_access_token_expiration=bluenext.access_token_expiration,
            )
        )
        return True
