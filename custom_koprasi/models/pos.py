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

# class PosPayment(models.Model):
#     _inherit = 'pos.payment'
#     note = fields.Char(string='Note Order',store=True)
#     # def create(self,vals):
#     #     limit = self.env['pos.order'].sudo().search([('id','=',vals['pos_order_id'])]).partner_id.limit
#     #     total_utang = self.env['pos.order'].sudo().search([('id','=',vals['pos_order_id'])]).partner_id.credit_limit
#     #     print(vals)
#     #     if total_utang + vals['amount'] > limit:
#     #         raise ValidationError(_("LIMIT BOS"))

#     #     else:
#     #         result = super(PosPayment, self).create(vals)

#     #     return result
#     @api.model
    # def _order_fields(self, ui_order):
    #     # Panggil super untuk mendapatkan fields default
    #     fields = super(PosSession, self)._order_fields(ui_order)

    #     # Tambahkan atau modifikasi value dari frontend POS
    #     fields['note'] = ui_order.get('note', '') + ' - Processed from POS'
    #     # fields['custom_field'] = 'Value from Frontend'
    #     return fields
    



# class PosOrder(models.Model):
#     _inherit = "pos.order"

#     employee_id = fields.Many2one('hr.employee', help="Person who uses the cash register. It can be a reliever, a student or an interim employee.", states={'done': [('readonly', True)], 'invoiced': [('readonly', True)]})
#     cashier = fields.Char(string="Cashier", compute="_compute_cashier", store=True)
#     note = fields.Char(string='Note Order',store=True, compute="_order_fields")

    # @api.model
    # def _order_fields(self, CustomDemoButtons):
    #     print(CustomDemoButtons)
        # order_fields = super(PosOrder, self)._export_for_ui()
        # order_fields['employee_id'] 

        # return order_fields

#     @api.depends('note')
#     def _compute_cashierrr(self):
#         for order in self:
#             # if order.employee_id:
#             order.note = order.note
#                 # order.cashier = order.user_id.name

#     def _export_for_ui(self, order):
#         result = super(PosOrder, self)._export_for_ui(order)
#         result.update({
#             'note': order.note,
#         })
#         return result
    
#     @api.model
#     def _order_fields(self, ui_order):
#         # Panggil super untuk mendapatkan fields default
#         fields = super(PosOrder, self)._order_fields(ui_order)

#         # Tambahkan atau modifikasi value dari frontend POS
#         fields['note'] = ui_order.get('note', '') + ' - Processed from POS'
#         # fields['custom_field'] = 'Value from Frontend'
#         return fields


    
    # class PosOrderss(models.Model):
    #     _inherit = 'pos.order'

    #     note = fields.Text('Customer Note',)  # Kolom catatan

        

    #     def _export_for_ui(self, order):
    #         timezone = pytz.timezone(self._context.get('tz') or self.env.user.tz or 'UTC')
    #         return {
    #             'lines': [[0, 0, line] for line in order.lines.export_for_ui()],
    #             'statement_ids': [[0, 0, payment] for payment in order.payment_ids.export_for_ui()],
    #             'name': order.pos_reference,
    #             'uid': re.search('([0-9-]){14}', order.pos_reference).group(0),
    #             'amount_paid': order.amount_paid,
    #             'amount_total': order.amount_total,
    #             'amount_tax': order.amount_tax,
    #             'amount_return': order.amount_return,
    #             'pos_session_id': order.session_id.id,
    #             'note': order.note,
    #             'pricelist_id': order.pricelist_id.id,
    #             'partner_id': order.partner_id.id,
    #             'user_id': order.user_id.id,
    #             'sequence_number': order.sequence_number,
    #             'creation_date': str(order.date_order.astimezone(timezone)),
    #             'fiscal_position_id': order.fiscal_position_id.id,
    #             'to_invoice': order.to_invoice,
    #             'to_ship': order.to_ship,
    #             'state': order.state,
    #             'account_move': order.account_move.id,
    #             'id': order.id,
    #             'is_tipped': order.is_tipped,
    #             'tip_amount': order.tip_amount,
    #             'access_token': order.access_token,
    #         }    
    #         print(self)  

    #     @api.model
    #     def set_order_note(self, CustomDemoButtons):
    #         # _logger.info(f"Menyiapkan catatan untuk order {order_id} dengan note: {note}")
    #         order = self.browse(CustomDemoButtons)  # Mencari order berdasarkan ID
    #         if order:
    #             order.note  =  CustomDemoButtons# Menyimpan catatan pada order
    #             # return True
    #     #     return True

    # -*- coding: utf-8 -*-


# class PosOrder(models.Model):
#     _inherit = "pos.order"

#     note = fields.Text('Customer Note',compute="get_order_details", store=True) 

#     @api.model
#     def get_order_details(self, CustomDemoButtons):
#         order = self.env['pos.order'].browse(CustomDemoButtons)
#         if order:
#             return {
#                 'name': order.name,
#                 'note': order.note,
#                 'lines': [{
#                     'product': line.product_id.name,
#                     'qty': line.qty,
#                     'price': line.price_unit,
#                 } for line in order.lines],
#             }
#         return {}

    
        

    