# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    shipping_info_on_invoice = fields.Boolean(string="Show shipping info on invoice reports", readonly=False, default=False, config_parameter='ait_report_invoice.shipping_info_on_invoice')