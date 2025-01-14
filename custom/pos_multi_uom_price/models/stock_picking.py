# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from itertools import groupby

_logger = logging.getLogger(__name__)
    
class StockPicking(models.Model):
    _inherit='stock.picking'

    def _prepare_stock_move_vals(self, first_line, order_lines):
        res = super()._prepare_stock_move_vals(first_line, order_lines)
        res.update({'product_uom': first_line.product_uom_id.id})
        return res

    def _create_move_from_pos_order_lines(self, lines):
        self.ensure_one()
        lines_by_product = groupby(sorted(lines, key=lambda l: (l.product_id.id,l.product_uom_id.id)), key=lambda l: (l.product_id.id,l.product_uom_id.id))
        for product, olines in lines_by_product:
            order_lines = self.env['pos.order.line'].concat(*olines)
            current_move = self.env['stock.move'].create(
                self._prepare_stock_move_vals(order_lines[0], order_lines)
            )
            confirmed_moves = current_move._action_confirm()
            confirmed_moves._add_mls_related_to_order(order_lines)
        self._link_owner_on_return_picking(lines)