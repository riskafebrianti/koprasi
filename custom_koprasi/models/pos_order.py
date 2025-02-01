from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Pos_orderan(models.Model):
    _inherit = 'pos.order'

    method_pay = fields.Char(string='Payment Method', compute='method_payy',store=True)
    # payment = fields.One2many('pos.payment', 'order_id', string='Riwayat Jual')
    # payment_ids = fields.One2many('pos.payment', 'pos_order_id', string='Payments', readonly=True)
    # payment_method = fields.Many2one('pos.payment', string='Kasir')

    # @api.depends('')
    # def method_payy(self):
    #     for data in self:
    #         if data.payment_ids:
    #             for loop in data.payment_ids.payment_method_id:
    #                 data.method_pay = loop.name
    @api.depends('payment_ids')
    def method_payy(self):
        dataa = self.env['pos.order'].sudo().search([('method_pay','=', False)])
        if dataa:
            for data_pos in dataa:
                data_pos.method_pay = data_pos.payment_ids.payment_method_id.name
        else:
            for data in self:
                if data.payment_ids:
                    data.method_pay = data.payment_ids[0].payment_method_id.name
        

