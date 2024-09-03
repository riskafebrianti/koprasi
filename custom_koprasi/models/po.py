from odoo import models, fields, api, _
from odoo.exceptions import UserError

class namePurchase(models.Model):
    _inherit = 'purchase.order.line'
    
    total = fields.Float(string='Top Up Price',store=True,)

    @api.onchange('price_unit','total')
    def bagi(self):
        for record in self:
            if record.total == 0 :
                record.price_unit 

            else:
                record.price_unit = record.total / record.product_qty
    