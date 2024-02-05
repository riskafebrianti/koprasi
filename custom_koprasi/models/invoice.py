from odoo import models, fields, api, _
from odoo.exceptions import UserError

class company(models.Model):
    _inherit = 'account.move'

    # company = fields.Char('Company')
    company = fields.Char('Company', related='partner_id.commercial_company_name')
    cust = fields.Char('Customer', related='partner_id.name')
