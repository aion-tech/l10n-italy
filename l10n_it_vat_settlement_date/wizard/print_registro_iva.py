# Copyright (c) 2021 Marco Colombo <https://github/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class WizardRegistroIva(models.TransientModel):
    _inherit = "wizard.registro.iva"

    def _get_move_ids_domain(self):
        domain = super()._get_move_ids_domain()
        domain = self.env["account.tax"]._inject_vat_settlement_date_domain(domain)
        return domain
