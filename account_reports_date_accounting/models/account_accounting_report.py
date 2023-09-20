from odoo import _, api, fields, models, tools


class AccountReport(models.AbstractModel):
    _inherit = 'account.report'

    filter_accounting_date = False


    def _get_options_date_domain(self, options, date_scope):
        if options.get('accounting_date', False):
            #TODO implement logic
            # date_from, date_to, allow_include_initial_balance = self._get_date_bounds_info(options, date_scope)

            # scope_domain = [('date', '<=', date_to)]
            # if date_from:
            #     if allow_include_initial_balance:
            #         scope_domain += [
            #             '|',
            #             ('date', '>=', date_from),
            #             ('account_id.include_initial_balance', '=', True),
            #         ]
            #     else:
            #         scope_domain += [('date', '>=', date_from)]
            # import ipdb; ipdb.set_trace()
            # return scope_domain
            #TODO remove following line
            return super()._get_options_date_domain(options, date_scope)
        else:
            return super()._get_options_date_domain(options, date_scope)

    #old method taken from v12/v14
    # @api.model
    # def _get_options_date_domain_OLD(self, options):
    #     import ipdb; ipdb.set_trace()
    #     options_date = options['date']
    #     date_from = options_date.get('date_from', False)
    #     date_to = options_date.get('date_to', False)
    #     if options.get('accounting_date', False):
    #         options_date['date_field'] = 'date_accounting'
    #         domain = [
    #             '|',
    #             '&',
    #             ('date_accounting', '<=', date_to),
    #             ('date_accounting', '!=', False),
    #             '&',
    #             ('date', '<=', date_to),
    #             ('date_accounting', '=', False),
    #         ]
    #         if options_date['mode'] == 'range' and options_date['date_from']:
    #             strict_range = options_date.get('strict_range')
    #             if not strict_range:
    #                 domain += [
    #                     '|',
    #                     ('account_id.user_type_id.include_initial_balance', '=', True),
    #                     '|',
    #                     '&',
    #                     ('date_accounting', '>=', date_from),
    #                     ('date_accounting', '!=', False),
    #                     '&',
    #                     ('date', '>=', date_from),
    #                     ('date_accounting', '=', False),
    #                 ]
    #             else:
    #                 domain += [
    #                     '|',
    #                     '&',
    #                     ('date_accounting', '>=', date_from),
    #                     ('date_accounting', '!=', False),
    #                     '&',
    #                     ('date', '>=', date_from),
    #                     ('date_accounting', '=', False),
    #                 ]
    #         return domain
    #     else:
    #         import ipdb; ipdb.set_trace()

    #         return super()._get_options_date_domain(options)
