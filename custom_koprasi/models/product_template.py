from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
from odoo import modules

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    available_in_pos = fields.Boolean(string='Available in POS', help='Check if you want this product to appear in the Point of Sale.', default=True)
    
    
    digital = fields.Boolean('Digital', tracking=1, help="Check this, if you want this product quantity not to be printed!",default=False,store=True)
    digital_inv = fields.Boolean('Invisible', tracking=1, help="Check this, if you want this product quantity not to be printed!",default=False,store=True)
    



# def get_default_img():
#     with open(modules.get_module_resource('my_module', 'static/img', 'my_image.png'),
#               'rb') as f:
#         return base64.b64encode(f.read())



# class MyModel(models.Model):
#     _name = 'my.model'

#     field_binary = fields.Binary(default=get_default_img())