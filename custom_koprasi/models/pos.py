# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta
from itertools import groupby

from odoo import api, fields, models, _, Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare
from odoo.osv.expression import AND, OR
from odoo.service.common import exp_version





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
                    'default_code', 'digital','to_weight', 'uom_id', 'description_sale', 'description', 'product_tmpl_id', 'tracking',
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



class PosPayment(models.Model):
    _inherit = 'pos.payment'

    # def create(self,vals):
    #     limit = self.env['pos.order'].sudo().search([('id','=',vals['pos_order_id'])]).partner_id.limit
    #     total_utang = self.env['pos.order'].sudo().search([('id','=',vals['pos_order_id'])]).partner_id.credit_limit
    #     print(vals)
    #     if total_utang + vals['amount'] > limit:
    #         raise ValidationError(_("LIMIT BOS"))

    #     else:
    #         result = super(PosPayment, self).create(vals)

    #     return result
    

    