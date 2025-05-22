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
from odoo.exceptions import ValidationError, UserError
from odoo.osv.expression import AND
import base64

_logger = logging.getLogger(__name__)
 

    

    

class Pos_orderan(models.Model):
    _inherit = ['pos.order','portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _name = 'pos.order'


    method_pay = fields.Char(string='Payment Method', compute='method_payy',tracking=True, store=True)
    date_order = fields.Datetime(string='Date', readonly=True, index=True, default=lambda self: fields.Datetime.context_timestamp(self, fields.Datetime.now()))
    state_invc = fields.Char(string='Status Invoice', store=True)
    retur_track = fields.Boolean(string='POS Order ini ada Transaksi Retur',tracking=True)

    def refund(self):
        """Create a copy of order  for refund order"""
        refund_orders = self.env['pos.order']
        for order in self:
            # When a refund is performed, we are creating it in a session having the same config as the original
            # order. It can be the same session, or if it has been closed the new one that has been opened.
            current_session = order.session_id.config_id.current_session_id
            if not current_session:
                raise UserError(_('To return product(s), you need to open a session in the POS %s', order.session_id.config_id.display_name))
            refund_order = order.copy(
                order._prepare_refund_values(current_session)
            )
            for line in order.lines:
                PosOrderLineLot = self.env['pos.pack.operation.lot']
                for pack_lot in line.pack_lot_ids:
                    PosOrderLineLot += pack_lot.copy()
                line.copy(line._prepare_refund_data(refund_order, PosOrderLineLot))
            refund_orders |= refund_order
        self.retur_track = True

        return {
            'name': _('Return Products'),
            'view_mode': 'form',
            'res_model': 'pos.order',
            'res_id': refund_orders.ids[0],
            'view_id': False,
            'context': self.env.context,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }



    def write(self, vals):
        result = super().write(vals)

        
      
        for order in self:
            if order.payment_ids:
                
                payment_names = set(order.payment_ids.mapped('payment_method_id.name'))

        
                for name in payment_names:
                    message_text = f"Metode Pembayaran yang dipilih: {name}"
            
                    if not order.message_ids.filtered(lambda m: str(message_text) in m.body):    
                        order.message_post(
                            body=message_text,
                            message_type='comment',
                            subtype_xmlid='mail.mt_note'
                        )

        return result

    @api.depends('state')
    def get_state(self):
        for rec in self:
            data = rec.account_move
            if data.payment_state == 'not_paid':
                rec.state_invc = 'Belum Lunas'
            elif data.payment_state == 'paid':
                rec.state_invc = 'Lunas'
            if not data:
                rec.state_invc = 'Tidak ada Invoice'
    

    @api.depends('payment_ids')
    def method_payy(self):
        dataa = self.env['pos.order'].sudo().search([('method_pay','=', False)])
        if dataa:
            for data_pos in dataa:
                if  len(data_pos.payment_ids) == 1:
                    data_pos.method_pay = data_pos.payment_ids.payment_method_id.name

                if len(data_pos.payment_ids) > 1:
                    data_pos.method_pay = data_pos.payment_ids[0].payment_method_id.name
                    if not data_pos.method_pay:
                        data_pos.method_pay = ""
        else:
            for data in self:
                if data.payment_ids:
                    data.method_pay = data.payment_ids[0].payment_method_id.name

    # def _apply_invoice_payments(self):
    #     receivable_account = self.env["res.partner"]._find_accounting_partner(self.partner_id).with_company(self.company_id).property_account_receivable_id
    #     payment_moves = self.payment_ids.sudo().with_company(self.company_id)._create_payment_moves()
    #     if receivable_account.reconcile:
    #         invoice_receivables = self.account_move.line_ids.filtered(lambda line: line.account_id == receivable_account and not line.reconciled)
    #         if invoice_receivables:
    #             payment_receivables = payment_moves.mapped('line_ids').filtered(lambda line: line.account_id == receivable_account and line.partner_id)
    #             (invoice_receivables | payment_receivables).sudo().with_company(self.company_id).reconcile()
    #     return payment_moves

    # def _p                     repare_invoice_vals(self):
    #     self.ensure_one()
    #     timezone = pytz.timezone(self._context.get('tz') or self.env.user.tz or 'UTC')
    #     invoice_date = fields.Datetime.context_timestamp(self, fields.Datetime.now()).replace(tzinfo=None)
    #     vals = {
    #         'invoice_origin': self.name,
    #         'journal_id': self.session_id.config_id.invoice_journal_id.id,
    #         'move_type': 'out_invoice' if self.amount_total >= 0 else 'out_refund',
    #         'ref': self.name,
    #         'partner_id': self.partner_id.id,
    #         'partner_bank_id': self._get_partner_bank_id(),
    #         # considering partner's sale pricelist's currency
    #         'currency_id': self.pricelist_id.currency_id.id,
    #         'invoice_user_id': self.user_id.id,
    #         'invoice_date': invoice_date.astimezone(timezone).date(),
    #         'fiscal_position_id': self.fiscal_position_id.id,
    #         'invoice_line_ids': self._prepare_invoice_lines(),
    #         'invoice_payment_term_id': self.partner_id.property_payment_term_id.id or False,
    #         'invoice_cash_rounding_id': self.config_id.rounding_method.id
    #         if self.config_id.cash_rounding and (not self.config_id.only_round_cash_method or any(p.payment_method_id.is_cash_count for p in self.payment_ids))
    #         else False
    #     }
    #     if self.refunded_order_ids.account_move:
    #         vals['ref'] = _('Reversal of: %s', self.refunded_order_ids.account_move.name)
    #         vals['reversed_entry_id'] = self.refunded_order_ids.account_move.id
    #     if self.note:
    #         vals.update({'narration': self.note})
    #     return vals


  
    