#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_values = super()._prepare_invoice()
        invoice_values.update(
            {
                "delivery_transport_condition_id": self.default_transport_condition_id.id,
                "delivery_goods_appearance_id": self.default_goods_appearance_id.id,
                "delivery_transport_reason_id": self.default_transport_reason_id.id,
                "delivery_transport_method_id": self.default_transport_method_id.id,
            }
        )
        return invoice_values
