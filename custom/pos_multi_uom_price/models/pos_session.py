# -*- coding: utf-8 -*-

# ehuerta _at_ ixer.mx

from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        new_model = 'product.multi.uom.price'
        if new_model not in result:
            result.append(new_model)
        return result


    def _loader_params_product_multi_uom_price(self):
        return {'search_params': {'domain': [], 'fields': ['product_id', 'uom_id', 'price'],},}

    def _get_pos_ui_product_multi_uom_price(self, params):
        products_uom_price = self.env['product.multi.uom.price'].search_read(**params['search_params'])
        product_uom_price = {}
        if products_uom_price:
            for unit in products_uom_price:
                if not unit['product_id'][0] in product_uom_price:
                    product_uom_price[unit['product_id'][0]] = {}
                    product_uom_price[unit['product_id'][0]]['uom_id'] = {}
                product_uom_price[unit['product_id'][0]]['uom_id'][unit['uom_id'][0]] = {
                        'id'    : unit['uom_id'][0],
                        'name'  : unit['uom_id'][1],
                        'price' : unit['price'],}
        return product_uom_price
