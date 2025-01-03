from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError,ValidationError
import math
import logging
import math
import numpy_financial 
from datetime import datetime
from dateutil.relativedelta import relativedelta
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    today = datetime.now().strftime('%Y-%m-%d')
    date_begin = datetime.now().replace(datetime.now().year, datetime.now().month-1, day=22).strftime('%Y-%m-%d') if datetime.now().month != 1 else (12, datetime.now().year-1)
    simla_anggota = fields.One2many("account.move.line",'partner_id') 
    no_anggota = fields.Integer('Nomor Anggota',tracking=1)
    anggota_koprasi = fields.Boolean(string='Anggota Koprasi',tracking=1, default=False)
    
    tabungan = fields.Integer(
        string='Tabungan Simpanan Sukarela', 
        compute='_compute_simla',
        # default=0,
        store=True,
    )
    limit = fields.Integer(
        string='Limit Partner', 
        default=1500000,
        store=True,
    )
    credit_limit = fields.Integer(
        string='Amount Spent this Month ', 
        compute='compute_amount',
    )
    
    invoice_list = fields.One2many('account.move', 'commercial_partner_id',
                                string="Invoice Details",
                                readonly=True,
                                domain=(
                                [('payment_state', '=', 'not_paid'),
                                ('move_type', '=', ('out_invoice')),
                                ('date', '>', date_begin),
                                ('date', '<=', today)
                                ]))
    
    _sql_constraints = [
        ("noga_check", "unique(no_anggota)", "Nomor Anggota already exists"),
    ]

       
    @api.depends('simla_anggota.credit','simla_anggota.debit','simla_anggota.parent_state') 
    def _compute_simla(self):
            
        for order in self:
            simsu_account = order.env['account.move.line'].sudo().search([('account_id.simsu','=','true'),('partner_id','=', order.id),('parent_state','=', 'posted')])
            order.credit =  (sum(simsu_account.filtered(lambda d: d.credit > 0).mapped('credit'))) 
            order.debit =  (sum(simsu_account.filtered(lambda d: d.debit > 0).mapped('debit'))) 
            order.tabungan = order.credit - order.debit
            print(order)
    
    @api.depends('pos_order_ids.partner_id')
    def compute_amount(self):
        date_buka = datetime.now().replace(datetime.now().year, datetime.now().month-1, day=22).strftime('%Y-%m-%d') if datetime.now().month != 1 else (12, datetime.now().year-1)
        date_tutup = datetime.now().replace(datetime.now().year, datetime.now().month, day=22).strftime('%Y-%m-%d') if datetime.now().month != 1 else (12, datetime.now().year-1)
        for record in self:
            amount_pos = record.env['pos.payment'].sudo().search([('pos_order_id.partner_id','=',record.id),('payment_method_id','=',3),('payment_date','>',date_buka), ('payment_date','<=',date_tutup)])
            record.credit_limit = sum(amount_pos.mapped('amount'))
            
    

    

class ResUsers(models.Model):
    _inherit = 'res.users'

    def generate_no_anggota(self):
        print(self)
        # self.groups_id.filtered(lambda x: x.category_id.name == 'User types')
        partners = self.env['res.partner'].sudo().search([('no_anggota','!=',''),('is_company','=',False)],order='no_anggota desc',limit=1)
        no_anggota = partners.no_anggota + 1
        # if vals['is_company'] == False and vals['anggota_koprasi'] == True:
        #     vals['no_anggota'] = partners.no_anggota + 1
        # if self.groups_id.filtered(lambda x: x.category_id.name == 'User types').name == 'Portal':
        if self.partner_id.no_anggota > 0:
            raise ValidationError(_("he has a member number"))
        else:
            return self.partner_id.write({
                'anggota_koprasi': True,
                'no_anggota': no_anggota
            })