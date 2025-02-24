# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta
from itertools import groupby

from odoo import api, fields, models, _, Command
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
# from odoo.tools import float_is_zero, float_compare
from odoo.osv.expression import AND, OR
from odoo.service.common import exp_version
from functools import partial
import logging
from datetime import timedelta
from functools import partial
from itertools import groupby
from collections import defaultdict

import psycopg2
import pytz
import re

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero, float_round, float_repr, float_compare
# from odoo.exceptions import ValidationError, UserError
# from odoo.osv.expression import AND
import base64


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        domain = [
            '&', '&', ('sale_ok', '=', True), ('available_in_pos', '=', True), '|',
            ('company_id', '=', self.config_id.company_id.id), ('company_id', '=', False)
        ]
        if self.config_id.limit_categories and self.config_id.iface_available_categ_ids:
            domain = AND([domain, [('pos_categ_id', 'in', self.config_id.iface_available_categ_ids.ids)]])
        if self.config_id.iface_tipproduct:
            domain = OR([domain, [('id', '=', self.config_id.tip_product_id.id)]])

        return {
            'search_params': {
                'domain': domain,
                'fields': [
                    'display_name', 'lst_price', 'standard_price', 'categ_id', 'pos_categ_id', 'taxes_id', 'barcode',
                    'default_code', 'digital','digital_inv','to_weight', 'uom_id', 'description_sale', 'description', 'product_tmpl_id', 'tracking',
                    'available_in_pos', 'attribute_line_ids', 'active', '__last_update', 'image_128'
                ],
                'order': 'sequence,default_code,name',
            },
            'context': {'display_default_code': False},
        }
    
    def _loader_params_res_partner(self):
        return {
            'search_params': {
                'domain': self._get_partners_domain(),
                'fields': [
                    'name', 'street', 'city', 'state_id', 'country_id', 'vat', 'lang', 'phone', 'zip', 'mobile', 'email',
                    'barcode', 'write_date', 'property_account_position_id', 'property_product_pricelist', 'parent_name','limit','credit_limit'
                ],
            },
        }



class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _order_fields(self, ui_order):
        result = super(PosOrder, self)._order_fields(ui_order)
        if ui_order.get('note'):
            result['note'] = ui_order['note']
        return result

class PosPaymentt(models.Model):

    _inherit = 'pos.payment'
   

    def _create_payment_moves(self):
        result = self.env['account.move']
        for payment in self:
            order = payment.pos_order_id
            payment_method = payment.payment_method_id
            if payment_method.type == 'pay_later' or float_is_zero(payment.amount, precision_rounding=order.currency_id.rounding):
                continue
            accounting_partner = self.env["res.partner"]._find_accounting_partner(payment.partner_id)
            pos_session = order.session_id
            journal = pos_session.config_id.journal_id
            payment_move = self.env['account.move'].with_context(default_journal_id=journal.id).create({
                'journal_id': journal.id,
                'date': fields.Date.context_today(payment),
                'ref': _('Invoice payment for %s (%s) using %s') % (order.name, order.account_move.name, payment_method.name),
                'pos_payment_ids': payment.ids,
            })
            result |= payment_move
            payment.write({'account_move_id': payment_move.id})
            amounts = pos_session._update_amounts({'amount': 0, 'amount_converted': 0}, {'amount': payment.amount}, payment.payment_date)
            credit_line_vals = pos_session._credit_amounts({
                'account_id': accounting_partner.with_company(order.company_id).property_account_receivable_id.id,  # The field being company dependant, we need to make sure the right value is received.
                'partner_id': accounting_partner.id,
                'move_id': payment_move.id,
            }, amounts['amount'], amounts['amount_converted'])
            debit_line_vals = pos_session._debit_amounts({
                'account_id': pos_session.company_id.account_default_pos_receivable_account_id.id,
                'move_id': payment_move.id,
            }, amounts['amount'], amounts['amount_converted'])
            self.env['account.move.line'].with_context(check_move_validity=False).create([credit_line_vals, debit_line_vals])
            payment_move._post()
        return result

    

    