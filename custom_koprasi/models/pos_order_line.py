from odoo import models, fields, api, _
from odoo.exceptions import UserError

class linePOS(models.Model):
    _inherit = 'pos.order.line'

    toko = fields.Char(string='Toko', related='order_id.config_id.name',store=True)
    payment_method = fields.Char(string='Payment Method', related='order_id.payment_ids.payment_method_id.name',store=True)
    partner_ids = fields.Char(string='Customer',related='order_id.partner_id.name',)
    date_orders = fields.Date(string='Date Order', compute='compute_relate',)
    refund = fields.Char(string='Keterangan',compute='compute_relate')

    # @api.depends('order_id.state')
    def compute_relate(self):
        for rec in self:
            rec.date_orders = rec.order_id.date_order
            if rec.order_id.name.split(" ")[-1] == 'REFUND':
                rec.refund = 'REFUND'
            else:
                rec.refund = ''


    def action_refresh_compute(self):
    # for record in self:
        self.compute_relate()
    