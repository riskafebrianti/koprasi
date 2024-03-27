# from odoo import models, fields, api, _
# from odoo.exceptions import UserError
# from openerp import SUPERUSER_ID
# from openerp.osv import osv, fields
# from openerp import SUPERUSER_ID


# class saleportal(osv.Model):
#     _inherit = 'sale.order'

#     def _get_invoices_domain(self):
#         return [('state', 'not in', ('cancel', 'draft')), ('move_type', 'in', ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt','entry')), ('sequence_prefix','or',('loan'))]
from odoo import http, _
from odoo.osv import expression
from odoo.addons.account.controllers.portal import CustomerPortal, PortalAccount
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request
from odoo import models, fields, api, _
from odoo.exceptions import UserError

    

class PortalAccount(CustomerPortal):

    def _get_invoices_domain(self):
        # return [('state', 'not in', ('cancel', 'draft')), ('move_type', 'in', ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt','entry')), ('journal_id.code', 'in', ('LN','INV'))]
        return [('state', 'not in', ('cancel', 'draft')), ('move_type', 'in', ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt'))]


