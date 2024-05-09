import datetime
import logging
from functools import wraps
from typing import Any, Callable, Dict, List, Tuple, Union

from odoo import Command, _, api, fields, models
from odoo.tools.safe_eval import safe_eval
from typing_extensions import Literal

_logger = logging.getLogger(__name__)

FIELD_NAMES: List[str] = [
    "name",
    "date",
    "partner",
    "amount",
    "account",
    "journal",
    "bank",
    "pt",
]

CASHFLOW_FIELDS_MAP: Dict[str, str] = {
    "name": "name",
    "date": "date",
    "partner": "partner_id",
    "amount": "amount",
    "account": "account_id",
    "journal": "journal_id",
    "bank": "bank_id",
    "pt": "pt_id",
}


class CashflowMixin(models.AbstractModel):
    _name = "cashflow.mixin"
    _description = "Cashfow Mixin"

    cashflow_record_ids = fields.Many2many(
        "cashflow.record",
        string="Cashflow Records",
        copy=False,
    )
    cashflow_records_count = fields.Integer(
        compute="_compute_cashflow_records_count",
        string="Cashflow Records",
    )
    cashflow_config_id = fields.Many2one("cashflow.config", "Source")

    def _compute_cashflow_records_count(self):
        for record in self:
            record.cashflow_records_count = len(record.cashflow_record_ids)

    def open_cashflow_records(self):
        ctx = self.env.context.copy()
        model_id = self.env["ir.model"].search([("model", "=", self._name)])
        ctx.update(
            {
                "default_res_id": self.id,
                "default_model_id": model_id.id,
                # @TODO ? more defaults
            }
        )
        return {
            "name": "Cashflow Records",
            "view_mode": "tree,form",
            "res_model": "cashflow.record",
            "type": "ir.actions.act_window",
            "domain": [("id", "in", self.cashflow_record_ids.ids)],
            "context": ctx,
        }

    def _get_cashflow_amount_sign(self, formula):
        results = {
            "self": self,
            "result": False,
            "timedelta": datetime.timedelta,
        }
        safe_eval(formula, results, mode="exec", nocopy=True)
        return results["result"]

    def _get_type_cast_fn(self, field_name) -> Callable:
        """
        Return a type casting function based on the field type
        """
        CashflowRecord = self.env["cashflow.record"]
        ttype = CashflowRecord._fields[field_name].type
        type_cast_fn = dict(
            char=str,
            text=str,
            many2one=int,
            float=float,
            integer=int,
            date=fields.Date.from_string,
            datetime=fields.Datetime.from_string,
        )[ttype]
        return type_cast_fn

    def _get_cashflow_field_value(
        self,
        field_name: str,
        config,
    ):
        field_id = config[f"field_{field_name}_id"]
        formula = config[f"field_{field_name}_formula"]

        type_cast_fn = self._get_type_cast_fn(CASHFLOW_FIELDS_MAP[field_name])
        if field_id:
            field_value = type_cast_fn(self[field_id.name])
            # signed amount
            if field_name == "amount":
                sign = self._get_cashflow_amount_sign(config.amount_sign_formula)
                return sign * field_value

            return field_value
        else:
            results = {
                "self": self,
                "result": False,
                "timedelta": datetime.timedelta,
            }
            safe_eval(formula, results, mode="exec", nocopy=True)
            # cast safe_eval result to the correct type
            # based on cashflow.record field types
            return type_cast_fn(results["result"])

    def _split_cashflow_record_vals(self, vals: dict) -> List[Dict[str, Any]]:
        """
        Split a single cashflow.record values into multiple values.
        Useful e.g. when dealing with payment terms or any other scenario where
        cashflow records should be split into multiple dates/amounts.

        :param vals: original record vals
        :return: list of vals
        """
        raise NotImplementedError(
            _(
                "_split_cashflow_record_vals not implemented on model %s.",
                self._name,
            )
        )

    def _create_cashflow_record(self, delete_existing=True):
        """
        create one or more new cashflow record(s) with values
        taken from singleton `self`

        :param delete_existing bool: whether to delete existing cashflow
                                     records after creating the new ones
        """
        self.ensure_one()
        self = self.with_context(skip_cashflow_rule_write=True)
        IrModel = self.env["ir.model"]
        CashflowRecord = self.env["cashflow.record"]
        if not self.cashflow_config_id:
            # No config set on record `self`
            return CashflowRecord

        config = self.cashflow_config_id
        res_model = self.__class__.__name__
        res_id = self.id
        model_id = IrModel.search([("model", "=", res_model)])

        vals = dict(
            config_id=config.id,
            model_id=model_id.id,
            model_name=model_id.name,
            res_id=res_id,
        )
        split_vals = []

        for field_name in FIELD_NAMES:
            field_val = self._get_cashflow_field_value(
                field_name,
                config,
            )
            cashflow_record_field = CASHFLOW_FIELDS_MAP[field_name]
            vals[cashflow_record_field] = field_val

        if vals["pt_id"]:
            split_vals = self._split_cashflow_record_vals(vals)

        cashflow_record_ids = CashflowRecord.create(split_vals or vals)

        if cashflow_record_ids:
            if delete_existing:
                self.cashflow_record_ids = [
                    Command.unlink(i) for i in self.cashflow_record_ids.ids
                ]
            self.cashflow_record_ids |= cashflow_record_ids
        return cashflow_record_ids

    def _get_cashflow_config_id(self):
        """
        Return cashflow.config records that apply to singleton `self`,
        based on `self.model_id` and `self.domain`.
        Configurations with non empty domains are prioritized.
        If more than one cashflow.config is found, return the first one
        and warn the user. @TODO ? should raise instead?
        """
        self.ensure_one()
        IrModel = self.env["ir.model"]
        CashflowConfig = applicable_config_ids = self.env["cashflow.config"]

        res_model = self.__class__.__name__
        model_id = IrModel.search([("model", "=", res_model)])

        config_ids = CashflowConfig.search([("model_id", "=", model_id.id)])

        domains = [
            ("domain", "not in", (False, "", "[]")),
            ("domain", "=", "[]"),  # empty domains last
        ]
        for domain in domains:
            for config_id in config_ids.filtered_domain([domain]):
                # apply domain found in config to record in `self`
                config_domain = safe_eval(config_id.domain)
                filtered_record = self.filtered_domain(config_domain)
                if filtered_record:
                    applicable_config_ids |= config_id

        if len(applicable_config_ids) > 1:
            _logger.warning(
                "Multiple cashflow.config found:\nmodel: %s\nconfig_ids: %s\ndomains:\n%s\nReturning the first one (id: %s, domain %s)",
                self.__class__.__name__,
                applicable_config_ids,
                ("    \n").join(applicable_config_ids.mapped("domain")),
                applicable_config_ids[0].id,
                applicable_config_ids[0].domain,
            )

        return applicable_config_ids[0] if applicable_config_ids else CashflowConfig

    def _apply_cashflow_rules(
        self,
        trigger: Literal["create", "write", "unlink"],
    ):
        """
        apply cashflow rules to record `self`

        :param trigger: filter rules to apply by current crud method
        """
        self.ensure_one()
        if self.cashflow_config_id:
            rule_ids = self.cashflow_config_id.rule_ids.filtered(
                lambda rule: rule.trigger == trigger
            )
            rule_ids.apply(self)

    def _set_cashflow_config_id(self, config_id: int):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update({"skip_cashflow_rule_write": True})
        self = self.with_context(ctx)
        self.cashflow_config_id = config_id

    @api.model_create_multi
    def create(self, vals_list):
        res_ids = super().create(vals_list)
        if self.env.context.get("skip_cashflow_rule_create"):
            return res_ids

        for res in res_ids:
            # set config_id
            config_id = res._get_cashflow_config_id()
            if config_id:
                res._set_cashflow_config_id(config_id.id)
                res._create_cashflow_record()
                res._apply_cashflow_rules("create")

        return res_ids

    def unlink(self):
        if self.env.context.get("skip_cashflow_rule_unlink"):
            return super().unlink()
        for rec in self:
            rec._apply_cashflow_rules("unlink")

        return super().unlink()

    def write(self, vals):
        res = super().write(vals)

        if not self.env.context.get("skip_cashflow_rule_write"):
            for rec in self:
                rec._apply_cashflow_rules("write")

        return res

    def unlink_cashflow_records(self) -> None:
        self = self.with_context(
            skip_cashflow_rule_write=True,
        )
        # self.cashflow_record_ids.unlink()
        self.cashflow_record_ids = [
            Command.delete(i) for i in self.cashflow_record_ids.ids
        ]
        return
