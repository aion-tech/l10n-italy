# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import api, fields, models

from .stock_delivery_note import DOMAIN_DELIVERY_NOTE_STATES, DOMAIN_INVOICE_STATUSES


class SaleOrder(models.Model):
    _inherit = "sale.order"

    default_transport_condition_id = fields.Many2one(
        "stock.picking.transport.condition",
        string="Condition of transport",
        default=False,
    )
    default_goods_appearance_id = fields.Many2one(
        "stock.picking.goods.appearance", string="Appearance of goods", default=False
    )
    default_transport_reason_id = fields.Many2one(
        "stock.picking.transport.reason", string="Reason of transport", default=False
    )
    default_transport_method_id = fields.Many2one(
        "stock.picking.transport.method", string="Method of transport", default=False
    )

    @api.onchange("partner_id")
    def onchange_partner_id_shipping_info(self):
        if self.partner_id:
            values = {
                "default_transport_condition_id": (
                    self.partner_id.default_transport_condition_id
                ),
                "default_goods_appearance_id": (
                    self.partner_id.default_goods_appearance_id
                ),
                "default_transport_reason_id": (
                    self.partner_id.default_transport_reason_id
                ),
                "default_transport_method_id": (
                    self.partner_id.default_transport_method_id
                ),
            }

        else:
            values = {
                "default_transport_condition_id": False,
                "default_goods_appearance_id": False,
                "default_transport_reason_id": False,
                "default_transport_method_id": False,
            }

        self.update(values)

    def _assign_delivery_notes_invoices(self, invoice_ids):
        order_lines = self.mapped("order_line").filtered(
            lambda l: l.is_invoiced and l.delivery_note_line_ids
        )

        delivery_note_lines = order_lines.mapped("delivery_note_line_ids").filtered(
            lambda l: l.is_invoiceable
        )
        delivery_notes = delivery_note_lines.mapped("delivery_note_id")

        ready_delivery_notes = delivery_notes.filtered(
            lambda n: n.state != DOMAIN_DELIVERY_NOTE_STATES[0]
        )

        draft_delivery_notes = delivery_notes - ready_delivery_notes
        draft_delivery_note_lines = (
            draft_delivery_notes.mapped("line_ids") & delivery_note_lines
        )

        ready_delivery_note_lines = delivery_note_lines - draft_delivery_note_lines

        #
        # TODO: È necessario gestire il caso di fatturazione splittata
        #        di una stessa riga d'ordine associata ad una sola
        #        picking (e di conseguenza, ad un solo DdT)?
        #       Può essere, invece, un caso "borderline"
        #        da lasciar gestire all'operatore?
        #       Personalmente, non lo gestirei e delegherei
        #        all'operatore questa responsabilità...
        #

        draft_delivery_note_lines.write(
            {"invoice_status": DOMAIN_INVOICE_STATUSES[0], "sale_line_id": None}
        )

        ready_delivery_note_lines.write({"invoice_status": DOMAIN_INVOICE_STATUSES[2]})
        for ready_delivery_note in ready_delivery_notes:
            ready_invoice_ids = [
                invoice_id
                for invoice_id in ready_delivery_note.sale_ids.mapped("invoice_ids").ids
                if invoice_id in invoice_ids
            ]
            ready_delivery_note.write(
                {"invoice_ids": [(4, invoice_id) for invoice_id in ready_invoice_ids]}
            )

        ready_delivery_notes._compute_invoice_status()

    def _generate_delivery_note_lines(self, invoice_ids):
        invoices = self.env["account.move"].browse(invoice_ids)
        invoices.update_delivery_note_lines()

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoice_ids = super()._create_invoices(grouped=grouped, final=final, date=date)

        self._assign_delivery_notes_invoices(invoice_ids.ids)
        self._generate_delivery_note_lines(invoice_ids.ids)

        return invoice_ids


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    delivery_note_line_ids = fields.One2many(
        "stock.delivery.note.line", "sale_line_id", readonly=True
    )
    delivery_picking_id = fields.Many2one("stock.picking", readonly=True, copy=False)

    @property
    def has_picking(self):
        return self.move_ids or (self.is_delivery and self.delivery_picking_id)

    @property
    def is_invoiceable(self):
        return (
            self.invoice_status == DOMAIN_INVOICE_STATUSES[1]
            and self.qty_to_invoice != 0
        )

    @property
    def is_invoiced(self):
        return (
            self.invoice_status != DOMAIN_INVOICE_STATUSES[1] and self.qty_invoiced != 0
        )

    @property
    def need_to_be_invoiced(self):
        return self.product_uom_qty != (self.qty_to_invoice + self.qty_invoiced)

    def fix_qty_to_invoice(self, new_qty_to_invoice=0):
        self.ensure_one()

        cache = {
            "invoice_status": self.invoice_status,
            "qty_to_invoice": self.qty_to_invoice,
        }

        self.write(
            {
                "invoice_status": "to invoice" if new_qty_to_invoice else "no",
                "qty_to_invoice": new_qty_to_invoice,
            }
        )

        return cache

    def is_pickings_related(self, picking_ids):
        if self.is_delivery:
            return self.delivery_picking_id in picking_ids

        return bool(self.move_ids & picking_ids.mapped("move_lines"))

    def retrieve_pickings_lines(self, picking_ids):
        return self.filtered(lambda l: l.has_picking).filtered(
            lambda l: l.is_pickings_related(picking_ids)
        )
