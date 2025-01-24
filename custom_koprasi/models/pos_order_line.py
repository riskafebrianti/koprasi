from odoo import models, fields, api, _
from odoo.exceptions import UserError

class linePOS(models.Model):
    _inherit = 'pos.order.line'

    toko = fields.Char(string='Toko', related='order_id.config_id.name',store=True)
    payment_method = fields.Char(string='Paymen Method', related='order_id.payment_ids.payment_method_id.name',store=True)

    