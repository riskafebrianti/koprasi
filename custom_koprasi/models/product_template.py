from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    available_in_pos = fields.Boolean(string='Available in POS', help='Check if you want this product to appear in the Point of Sale.', default=True)
    
    
    digital = fields.Boolean('digital', tracking=1, help="Check this, if you want this product quantity not to be printed!")
    
    
    