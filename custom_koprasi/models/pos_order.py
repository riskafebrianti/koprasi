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
    _inherit = 'pos.order'

    method_pay = fields.Char(string='Payment Method', compute='method_payy',store=True)
    # date_order = fields.Datetime(string='Date', readonly=True, index=True, default=lambda self: fields.Datetime.context_timestamp(self, fields.Datetime.now()))
   
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
    
    