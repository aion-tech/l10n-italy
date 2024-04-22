from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class CashflowRecord(models.Model):
    _name = "cashflow.record"
    _description = "Cashflow Record"
    _order = "date desc"

    config_id = fields.Many2one(
        "cashflow.config",
        "Cashflow Config",
    )
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
    )
    model_name = fields.Char(
        "Resource Model",
    )
    name = fields.Char(
        "Name",
        default="/",
    )
    res_id = fields.Integer(
        "Resource ID",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
    )
    amount = fields.Float(
        "Amount",
    )
    journal_id = fields.Many2one(
        "account.journal",
        "Account Journal",
    )
    bank_id = fields.Many2one(
        "res.partner.bank",
        "Bank Account",
    )
    account_id = fields.Many2one(
        "account.account",
        "Account",
    )
    pt_id = fields.Many2one(
        "account.payment.term",
        "Payment Terms",
    )
    date = fields.Date("Date")
    cum_sum = fields.Float(
        "Cumulative Sum",
        compute="_compute_cum_sum",
        store=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        to_remove_idxs = [
            vals_list.index(val) for val in vals_list if not val.get("amount")
        ]
        # do not create records with amount = 0
        for idx in to_remove_idxs:
            vals_list.pop(idx)

        return super().create(vals_list)

    def open_source_record(self):
        self.ensure_one()
        return {
            "name": self.name,
            "type": "ir.actions.act_window",
            "res_model": self.model_id.model,
            "view_mode": "form",
            "res_id": self.res_id,
        }

    @api.depends("date", "amount", "model_id")
    def _compute_cum_sum(self):
        query = """
            SELECT id, SUM(amount) OVER (PARTITION BY model_id ORDER BY date,create_date,id) AS cum_sum
            FROM cashflow_record
        """
        self.env.cr.execute(
            query,
            (tuple(self.ids),),
        )
        results = self.env.cr.fetchall()
        cum_sum_map = {result[0]: result[1] for result in results}
        for record in self:
            record.cum_sum = cum_sum_map.get(record.id, 0.0)


class CashflowConfig(models.Model):
    _name = "cashflow.config"
    _description = "Cashflow Configuration"

    name = fields.Char(
        "Description",
        required=True,
    )
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        ondelete="cascade",
        required=True,
    )
    model_name = fields.Char(
        "Model Name",
        related="model_id.model",
        store=True,
    )
    field_name_id = fields.Many2one(
        "ir.model.fields",
        "Name Field",
    )
    field_name_formula = fields.Text(
        "Name Formula",
        default="result = False",
    )
    field_partner_id = fields.Many2one(
        "ir.model.fields",
        string="Partner Field",
    )
    field_partner_formula = fields.Text(
        "Partner Formula",
        default="result = False",
    )
    field_amount_id = fields.Many2one(
        "ir.model.fields",
        string="Amount Field",
    )
    amount_sign_formula = fields.Text(
        "Amount Sign Formula",
        help="Return 1 or -1. Only used if Amount Field is set.",
        default="result = 1",
    )
    field_amount_formula = fields.Text(
        "Amount Formula",
        default="result = False",
    )
    field_date_id = fields.Many2one(
        "ir.model.fields",
        string="Date Field",
    )
    field_date_formula = fields.Text(
        "Date Formula",
        default="result = False",
    )
    field_account_id = fields.Many2one(
        "ir.model.fields",
        "Account Field",
    )
    field_account_formula = fields.Text(
        "Account Formula",
        default="result = False",
    )
    field_journal_id = fields.Many2one(
        "ir.model.fields",
        "Account Journal Field",
    )
    field_journal_formula = fields.Text(
        "Account Journal Formula",
        default="result = False",
    )
    field_bank_id = fields.Many2one(
        "ir.model.fields",
        "Bank Account Field",
    )
    field_bank_formula = fields.Text(
        "Bank Account Formula",
        default="result = False",
    )
    field_pt_id = fields.Many2one(
        "ir.model.fields",
        "Payment Terms Field",
    )
    field_pt_formula = fields.Text(
        "Payment Terms Formula",
        default="result = False",
    )
    rule_ids = fields.One2many(
        "cashflow.config.update.rule",
        "config_id",
        string="Update Rules",
    )
    domain = fields.Char(
        string="Domain",
        default=[],
    )


class CashflowConfigUpdateRule(models.Model):
    _name = "cashflow.config.update.rule"
    _description = "Cashflow Update Rule"

    config_id = fields.Many2one("cashflow.config")
    trigger = fields.Selection(
        [("create", "Create"), ("write", "Write"), ("unlink", "Unlink")],
        string="Trigger",
    )
    rule = fields.Text("Rule")
    server_action_id = fields.Many2one(
        "ir.actions.server",
        "Server Action",
    )

    def apply(self, record):
        """
        execute the rule(s) in `self` on singleton `record`

        :param record: singleton recordset
        """
        record.ensure_one()
        for rule in self:
            formula = rule.rule
            results = {
                "self": record,
                "cashflow_record_ids": record.cashflow_record_ids,
                "result": False,
            }
            safe_eval(formula, results, mode="exec", nocopy=True)
