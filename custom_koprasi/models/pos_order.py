from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Pos_orderan(models.Model):
    _inherit = 'pos.order'

    method_pay = fields.Char(string='Product name', compute='method_payy',)
    # payment = fields.One2many('pos.payment', 'order_id', string='Riwayat Jual')
    # payment_ids = fields.One2many('pos.payment', 'pos_order_id', string='Payments', readonly=True)
    # payment_method = fields.Many2one('pos.payment', string='Kasir')

    # @api.depends('')
    def method_payy(self):
        for data in self:
            if self.payment_ids:
                data.method_pay = data.payment_ids.payment_method_id.name
