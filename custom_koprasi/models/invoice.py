from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError,ValidationError
import math
import logging
import math
import numpy_financial 
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Accountnya(models.Model):
    _inherit = 'account.account'
    simpok = fields.Boolean('Simpok', tracking=1)
    simwab = fields.Boolean('Simwab', tracking=1)
    simsu = fields.Boolean('Simsu', tracking=1)
    amount = fields.Float(string='Amount', tracking=1)
    counter_account = fields.Many2one(comodel_name='account.account', string='Counter Account', tracking=1)
    other_account = fields.Many2one(comodel_name='account.account', string='Other Account', tracking=1)
    
class ubah(models.Model):
    _inherit = 'account.move'

    custtt = fields.Char('Customer', related='line_ids.partner_id.display_name',)
    cust = fields.Char('Customer', related='partner_id.name')
    company = fields.Char('Company', related='partner_id.commercial_company_name')
    pos_payment = fields.Char('POS Payment Method', related='pos_order_ids.payment_ids.payment_method_id.name',)
    entri = fields.Selection([
        ('simwa', 'Simpanan Wajib'),
        ('simsu', 'Simpanan Sukarela'),
    ], string='Simpanan')
    
    # partneram = fields.Many2one('res.partner', string='Karyawan')
    partneram = fields.Many2many('res.partner',
                                            string="Karyawan",
                                           )
    # simla_anggota = fields.One2many("account.move.line",'partner_id') 

    simwab = fields.Boolean(string='Entries Simwab')
    # partner = fields.Many2many('res.partner', 'res_partner_wizard_template_rel', string='Karyawan')
    amount_simsu = fields.Float(string='Amount Sukarela', store=True)
    
    pos_count = fields.Integer(compute='_compute_pos_count',
                                string="Invoice "
                                        "Count",
                                help="The number of invoices created")
    
    pos_refund_count = fields.Integer(compute='_compute_pos_count',
                                string="Invoice "
                                        "Count",
                                help="The number of invoices created")
    
    def _compute_pos_count(self):
        """Compute the invoice count"""
        for record in self:
            
            record.pos_count = self.env['pos.order'].search_count(
                [('name', '=', self.ref)])
            if record.pos_count:
                record.pos_refund_count = self.env['pos.order'].search_count(
                    [('name', '=', self.ref+' REFUND')])
            else:
                record.pos_refund_count = 0
            # if record.pos_refund_count

    def action_view_pos(self):
        # """Method for Returning invoice View"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Point Of Sale Order',
            'view_mode': 'list,form',
            'view_type': 'list,form',
            'res_model': 'pos.order',
            'domain': [('name', '=', self.ref)],
            'context': {'create': False},
            'target': 'current',
        }
    
    def action_view_pos_refund(self):
        # """Method for Returning invoice View"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Point Of Sale Order',
            'view_mode': 'list,form',
            'view_type': 'list,form',
            'res_model': 'pos.order',
            'domain': [('name', '=', self.ref+' REFUND')],
            'context': {'create': False},
            'target': 'current',
        }
    
    
    def load_simsu(self):
        print(self)
        journal = self.env['account.account'].sudo().search([('simsu','=',True)]).allowed_journal_ids
        if journal :
             self.journal_id = journal
        line_ids =[]
        simsu_account = self.env['account.account'].sudo().search([('simsu','=',True)])
        for record in self.partneram:
            line_data_simsu = ((0,0,{
                'partner_id': record.id,
                'info': record.tabungan,
                'account_id': simsu_account.counter_account.id,
                'name': 'Simpanan Sukarela '+datetime.today().strftime('%Y-%m'),
                'debit': self.amount_simsu,
                'credit':0,
            }))
            line_ids.append(line_data_simsu)
            line_data_simsu = ((0,0,{
                'partner_id': record.id,
                'account_id': simsu_account.id,
                'name': 'Simpanan Sukarela '+datetime.today().strftime('%Y-%m'),
                'debit': 0,
                'credit':self.amount_simsu,
            }))
            line_ids.append(line_data_simsu)
        if line_ids:
            self.write({'line_ids': line_ids})

    def pay_simla(self):
        print(self)
        journal = self.env['account.account'].sudo().search([('simsu','=',True)]).allowed_journal_ids
        if journal :
             self.journal_id = journal
        line_ids =[]
        simsu_account = self.env['account.account'].sudo().search([('simsu','=',True)])
        if not simsu_account:
            raise ValidationError(_("Simwab Account tidak ditemukan"))
        for data in self.partneram:
            if self.amount_simsu > data.tabungan:
                raise ValidationError(_(f"Saldo {data.name} Tidak Terpenuhi"))
        for record in self.partneram:
            line_data_simsu = ((0,0,{
                'partner_id': record.id,
                'info': record.tabungan,
                'account_id': simsu_account.id,
                'name': 'Simpanan Sukarela '+datetime.today().strftime('%Y-%m'),
                'debit': self.amount_simsu,
                'credit':0,
            }))
            line_ids.append(line_data_simsu)
            line_data_simsu = ((0,0,{
                'partner_id': record.id,
                'account_id': simsu_account.counter_account.id,
                'name': 'Simpanan Sukarela '+datetime.today().strftime('%Y-%m'),
                'debit': 0,
                'credit':self.amount_simsu,
            }))
            line_ids.append(line_data_simsu)
        if line_ids:
            self.write({'line_ids': line_ids})  
    
    def load_simwab(self):
        print(self)
        journal = self.env['account.account'].sudo().search([('simwab','=',True)]).allowed_journal_ids
        if journal :
             self.journal_id = journal
        if not journal:
             raise ValidationError(_("jurnal di CoA tidak ditemukan"))

        # partners = self.env['res.partner'].sudo().search([('is_company','=',False),('active','=',True),('anggota_koprasi','=',True),('no_anggota','>',0)])
        partners = self.env['res.partner'].sudo().search([('active','=',True),('anggota_koprasi','=',True)])
        line_ids = []
        simwab_account = self.env['account.account'].sudo().search([('simwab','=',True)])
        if not simwab_account:
            raise ValidationError(_("Simwab Account tidak ditemukan"))
        if not simwab_account.counter_account:
            raise ValidationError(_("lawan Simwab Tidak ditemukan"))
        for partner in partners:
            line_data = ((0,0,{
                'partner_id': partner.id,
                # 'info': partner.tabungan,
                'account_id': simwab_account.id,
                'name': 'Simpanan Wajib '+datetime.today().strftime('%Y-%m'),
                'debit': 0,
                'credit':simwab_account.amount,
            }))
            line_ids.append(line_data)
            line_dataa = ((0,0,{
                'partner_id': partner.id,

                'account_id': simwab_account.counter_account.id,
                'name': 'Simpanan Wajib '+datetime.today().strftime('%Y-%m'),
                'debit': simwab_account.amount,
                'credit':0,
            }))
            line_ids.append(line_dataa)
        if line_ids:
            self.write({'line_ids': line_ids})
        print("aww")

    def fee_simla(self):
        partners = self.env['res.partner'].sudo().search([('tabungan','>','0')])
        journal = self.env['account.account'].sudo().search([('simsu','=',True)]).allowed_journal_ids
        if journal :
             self.journal_id = journal
        line_ids = []
        simwab_account = self.env['account.account'].sudo().search([('simsu','=',True)])
        if not simwab_account:
            raise ValidationError(_("Simwab Account tidak ditemukan"))
        
        for partner in partners:
            total_bunga = round((partner.tabungan * 0.2) /100)
            simla_line_data = ((0,0,{
                'partner_id': partner.id,
                'info': partner.tabungan,
                'account_id': simwab_account.other_account.id,
                'name': 'Bunga Anggota '+datetime.today().strftime('%Y-%m'),
                'debit': total_bunga,
                'credit':0,
            }))
            line_ids.append(simla_line_data)
            simla_line_data = ((0,0,{
                'partner_id': partner.id, 
                'account_id': simwab_account.id,
                'name': 'Bunga Anggota '+datetime.today().strftime('%Y-%m'),
                'debit': 0,
                'credit': total_bunga,
            }))
            line_ids.append(simla_line_data)

        if line_ids:
            self.write({'line_ids': line_ids})
    
 
    # @api.onchange('partneram')
    # def amountauto(self):
    #     if self.partneram:
    #         self.amount_simsu = self.partneram.tabungan
            
class MoveLine(models.Model):
    _inherit = 'account.move.line'
    
    info = fields.Float(string= 'Simla Partner', store=True,)
    info_simwa = fields.Float(string= 'Simwab')
    pelunasan = fields.Boolean(string='Check ?')
    company = fields.Char(string='Perusahaan', compute='company_partner', store=True)
    # company = fields.Many2one('res.partner', string='company Partner',related='partner_id.company_partner_id')

    @api.depends('move_id','move_id.partner_id')
    def company_partner(self):
        for data in self:
            data.company = data.move_id.partner_id.company_partner_id.name
    

    

    def new_entry(self):
       
        selected_records = self.browse(self.env.context['active_ids'])
        
        invoice_vals = {
            'invoice_date': fields.Date.today(),
            # 'move_type': 'out_invoice',
            'invoice_line_ids': []
            
        }
        company_totals = {}
        print(selected_records)

        for rec in selected_records:
            if rec.partner_id.company_partner_id:
                line_vals = (0, 0, {
                    'account_id': rec.account_id.id,
                    'partner_id': rec.partner_id.id,
                    'name': 'PELUNASAN ANGGOTA '+rec.name,
                    'debit':  rec.credit, 
                    'credit': rec.debit,
                })
                invoice_vals['invoice_line_ids'].append(line_vals)
                
              
                company_partner = rec.partner_id.company_partner_id
                if company_partner:
                    if company_partner not in company_totals:
                        company_totals[company_partner] = {'debit': 0, 'credit': 0, 'account_id': rec.account_id.id}

                    
                    company_totals[company_partner]['debit'] += rec.debit
                    company_totals[company_partner]['credit'] += rec.credit
                    
                    for move in rec.move_id:
                        if move.payment_state == 'paid':
                            raise UserError(_('Invoice sudah dibayar.'))
            
                else:
                    raise UserError(rec.partner_id.name +'Tidak ada Nama Perusahaan')
        
        for company_partner, totals in company_totals.items():
            
            line_val_company = (0, 0, {
                'account_id': totals['account_id'],  # Sesuaikan akun
                'partner_id': company_partner.id,
                'name': 'PELUNASAN ANGGOTA ' + rec.partner_id.company_partner_id.name,
                'debit': totals['debit'],
                'credit': totals['credit'],  
            })

            if company_partner:
                invoice_vals['invoice_line_ids'].append(line_val_company)
            else:
                raise UserError(rec.partner_id.name +'Tidak ada Nama Perusahaan')
                
       
            rec.pelunasan = True
        invoice = self.env['account.move'].create(invoice_vals)


        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }

       

    @api.onchange('partner_id')
    def infomasiSimpanan(self):
        for record in self:
            if record.partner_id:
                record.info = record.partner_id.tabungan
    
    



