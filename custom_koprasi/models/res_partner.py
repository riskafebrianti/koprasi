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
    
    # def default_tgl_buka(self):
    #     def_tgl_buka = datetime.now().replace(day=22,)
    #     if datetime.now().day >= 22: #bila tgl hari ini lebih besar dari 22
    #         def_tgl_buka = datetime.now().replace(day=22,)
    #         return def_tgl_buka
    #     if datetime.now().day < 22: #bila tgl hari ini lebih besar dari 22
    #         def_tgl_buka = datetime.now().replace(day=22, month =datetime.now().month-1)
            
    #         return def_tgl_buka
   
    def _default_tgl_tutup(self):
        # data = fields.datetime.now()
        return fields.datetime.now()
        # if datetime.now().day >= 22: #bila tgl hari ini lebih besar dari 22
        #     def_tgl_tutup = datetime.now().replace(day=22, month =datetime.now().month+1)
        #     return def_tgl_tutup

        # if datetime.now().day < 22: #bila tgl hari ini lebih besar dari 22
        #     def_tgl_tutup = datetime.now().replace(day=22,)
 
        #     return def_tgl_tutup
    option_date = fields.Selection([("def","Default (Otomatis)"),("manual","Setting")], string='Metode Tanggal Periode')
    tgl_buka = fields.Date(string='Tanggal Buka Buku',)
    tgl_tutup = fields.Date(string='Tanggal Tutup Buku',)

    approval = fields.Selection([("manager","Manager")], string='Approval')
    today = datetime.now()
    # date_begin = datetime.now().replace(datetime.now().year, datetime.now().month-1, day=22).strftime('%Y-%m-%d') if datetime.now().month != 1 else (12, datetime.now().year-1) 
    date_begin = datetime.now().replace(datetime.now().year, datetime.now().month-1, day=22) if datetime.now().month != 1 else datetime.now().replace(year=datetime.now().year - 1, month=12, day=1)

    simla_anggota = fields.One2many("account.move.line",'partner_id') 
    no_anggota = fields.Integer('Nomor Anggota',tracking=1)
    anggota_koprasi = fields.Boolean(string='Anggota Koprasi',tracking=1, default=False)
    # company_partner = fields.Char(string='Perusahaan Anggota',tracking=1, store=True,)
    company_partner_id = fields.Many2one('res.partner', string='Perusahaan Anggota',tracking=1, store=True,)
    

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
    badan_hukum = fields.Selection(
        string='Badan Hukum', store=True,
        selection=[('PT', 'PT'), ('UD', 'UD'), ('CV', 'CV'), ('KOPERASI', 'KOPRASI'), ('YAYASAN', 'YAYASAN'), ('TOKO', 'TOKO'), ('APOTIK', 'APOTIK')]
    )
    credit_limit = fields.Integer(
        string='Amount Spent this Month ', 
        compute='compute_amount',
        store=True,
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

    # @api.depends('quantity', 'price')

                # data.tgl_tutup = datetime.now().replace(day=22)
    

     
    @api.depends('simla_anggota.credit','simla_anggota.debit','simla_anggota.parent_state') 
    def _compute_simla(self):
            
        for order in self:
            simsu_account = order.env['account.move.line'].sudo().search([('account_id.simsu','=','true'),('partner_id','=', order.id),('parent_state','=', 'posted')])
            order.credit =  (sum(simsu_account.filtered(lambda d: d.credit > 0).mapped('credit'))) 
            order.debit =  (sum(simsu_account.filtered(lambda d: d.debit > 0).mapped('debit'))) 
            order.tabungan = order.credit - order.debit
            print(order)
    
    # def date_periode(self):
    #     for data in self:
    #         if not self.tgl_buka or not self.tgl_tutup:
    #             if datetime.now().day >= 22: #bila tgl hari ini lebih besar dari 22
    #                 data.tgl_buka = datetime.now().replace(day=22,)
    #                 data.tgl_tutup = datetime.now().replace(day=22, month =datetime.now().month+1)

    #             if datetime.now().day < 22: #bila tgl hari ini lebih besar dari 22
    #                 data.tgl_buka = datetime.now().replace(day=22, month =datetime.now().month-1)
    #                 data.tgl_tutup = datetime.now().replace(day=22,)


    @api.depends('pos_order_ids.partner_id','invoice_ids','tgl_buka','tgl_tutup')
    def compute_amount(self):
        for record in self:
            today = datetime(2025, 4, 29).date()
            # today = datetime.now()
            if record.tgl_tutup and today > record.tgl_tutup:
                record.option_date = 'def'
                if today.day > 21: #bila tgl hari ini lebih besar dari 22
                    record.tgl_buka = today.replace(day=22,)
                    record.tgl_tutup = today.replace(day=21, month =today.month+1)

                    amount_pos = self.env['account.move'].sudo().search([('partner_id','=',record.id),
                                                                        ('payment_state','=', 'not_paid'),
                                                                        ('pos_order_ids.payment_ids.payment_method_id.name','=','Customer Account'),
                                                                        ('create_date','>',record.tgl_buka),
                                                                        ('create_date','<=',record.tgl_tutup)
                                                                        ])
                    record.credit_limit = sum(amount_pos.mapped('amount_total'))
                    
                if today.day < 22: #bila tgl hari ini lebih besar dari 22
                    record.tgl_buka = today.replace(day=22, month =today.month-1)
                    record.tgl_tutup = today.replace(day=21,)

                    amount_pos = self.env['account.move'].sudo().search([('partner_id','=',record.id),
                                                                        ('payment_state','=', 'not_paid'),
                                                                        ('pos_order_ids.payment_ids.payment_method_id.name','=','Customer Account'),
                                                                        ('create_date','>',record.tgl_buka),
                                                                        ('create_date','<=',record.tgl_tutup)
                                                                        ])
                    record.credit_limit = sum(amount_pos.mapped('amount_total'))
            else:
                amount_pos = self.env['account.move'].sudo().search([('partner_id','=',record.id),
                                                                    ('payment_state','=', 'not_paid'),
                                                                    ('pos_order_ids.payment_ids.payment_method_id.name','=','Customer Account'),
                                                                    ('create_date','>',record.tgl_buka),
                                                                    ('create_date','<=',record.tgl_tutup)
                                                                    ])
                record.credit_limit = sum(amount_pos.mapped('amount_total'))
            
    # def open_wizard(self):
    #     return {
    #         'name': 'Wizard',
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         "view_type": "form",
    #         'res_model': 'product.generation.wizard',
    #         'target': 'new',
    #         'view_id': self.env.ref
    #         ('product_generation.product_generation_wizard_form').id,
    #         'context': {'active_id': self.id},
    #     }
    
    def open_wizard(self):
        return {
            'name': 'Popup',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'partner.wizard',
            'target': 'new',
            'view_id': self.env.ref,
        }
    
            
    

    

class Res__Users(models.Model):
    _inherit = 'res.users'

    # approval = fields.Selection([("cash","Cash"),("card","Card")], string='Approval')
    # approval = fields.Char(string='Product name')
    # change_payment = fields.Boolean(string='Apakah User ini bisa update change payment?',store=True,)

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
  
    class hr(models.AbstractModel):
        _inherit = 'hr.employee.base'
    # class HrEmployeeBase(models.AbstractModel):
    # """The inherited class HrEmployee to add new fields to 'hr.employee' """
    # _inherit = "hr.employee.base"

        change_pay = fields.Boolean(string="POS order Ubah Pembayaran", help="Sembunyikn button Change Payment")
        
        