from odoo import api, fields, models


class MisCashFlowForecastLine(models.Model):
    _inherit = "mis.cash_flow.forecast_line"

    cf_record_id = fields.Many2one(
        "cashflow.record", "Cashflow Record", ondelete="cascade"
    )


class CashflowRecord(models.Model):
    _inherit = "cashflow.record"

    mis_cf_line = fields.One2many(
        "mis.cash_flow.forecast_line",
        "cf_record_id",
        string="MIS Cash Flow Forecast Line",
        ondelete="cascade",
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        mis_cf_data = {}
        mis_cf_data["partner_id"] = vals.get("partner_id", False)
        mis_cf_data["date"] = vals.get("date", False)
        mis_cf_data["account_id"] = vals.get("account_id", False)
        mis_cf_data["name"] = vals.get("name", False)
        mis_cf_data["balance"] = vals.get("amount", False)
        mis_cf_data["cf_record_id"] = res.id
        self.env["mis.cash_flow.forecast_line"].create(mis_cf_data)

        return res
