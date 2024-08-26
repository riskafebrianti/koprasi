from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError,ValidationError
import math
import logging
import math
import numpy_financial 
from datetime import datetime
from dateutil.relativedelta import relativedelta


class PosConfig(models.Model):
    _inherit = 'pos.config'

    invoice_auto_check = fields.Boolean()
class PosConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_auto_check = fields.Boolean(
        related="pos_config_id.invoice_auto_check",
        help='Check to enable the invoice button',
        readonly=False, store=True,
        config_parameter='pos_invoice_automate.invoice_auto_check')
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
            simsu_account = order.env['account.move.line'].sudo().search([('account_id.simsu','=','true'),('partner_id','=', order.id),('parent_state','!=', 'draft')])
            order.credit =  (sum(simsu_account.filtered(lambda d: d.credit > 0).mapped('credit'))) 
            order.debit =  (sum(simsu_account.filtered(lambda d: d.debit > 0).mapped('debit'))) 
            order.tabungan = order.credit - order.debit
class Account(models.Model):
    _inherit = 'account.account'
    simpok = fields.Boolean('Simpok', tracking=1)
    simwab = fields.Boolean('Simwab', tracking=1)
    simsu = fields.Boolean('Simsu', tracking=1)
    amount = fields.Float(string='Amount', tracking=1)
    counter_account = fields.Many2one(comodel_name='account.account', string='Counter Account', tracking=1)
    other_account = fields.Many2one(comodel_name='account.account', string='Other Account', tracking=1)
class AccountMove(models.Model):
    _inherit = 'account.move'

    custtt = fields.Char('Customer', related='line_ids.partner_id.display_name',)
    cust = fields.Char('Customer', related='partner_id.name')
    company = fields.Char('Company', related='partner_id.commercial_company_name')
    entri = fields.Selection([
        ('simwa', 'Simpanan Wajib'),
        ('simsu', 'Simpanan Sukarela'),
    ], string='Simpanan')
    
    partneram = fields.Many2one('res.partner', string='Karyawan')
    # simla_anggota = fields.One2many("account.move.line",'partner_id') 

    simwab = fields.Boolean(string='Entries Simwab')
    # partner = fields.Many2many('res.partner', 'res_partner_wizard_template_rel', string='Karyawan')
    amount_simsu = fields.Float(string='Amount Sukarela', store=True)
    
    def load_simsu(self):
        print(self)
        line_ids =[]
        simsu_account = self.env['account.account'].sudo().search([('simsu','=',True)])
        for record in self:
            line_data_simsu = ((0,0,{
                'partner_id': record.partneram.id,
                'account_id': simsu_account.counter_account.id,
                'name': 'Simpanan Sukarela '+datetime.today().strftime('%Y-%m'),
                'debit': self.amount_simsu,
                'credit':0,
            }))
            line_ids.append(line_data_simsu)
            line_data_simsu = ((0,0,{
                'partner_id': record.partneram.id,
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
        line_ids =[]
        simsu_account = self.env['account.account'].sudo().search([('simsu','=',True)])
        if not simsu_account:
            raise ValidationError(_("Simwab Account tidak ditemukan"))
        if self.amount_simsu > self.partneram.tabungan:
            raise ValidationError(_("Saldo Tidak Terpenuhi"))
        for record in self:
            line_data_simsu = ((0,0,{
                'partner_id': record.partneram.id,
                'account_id': simsu_account.id,
                'name': 'Simpanan Sukarela '+datetime.today().strftime('%Y-%m'),
                'debit': self.amount_simsu,
                'credit':0,
            }))
            line_ids.append(line_data_simsu)
            line_data_simsu = ((0,0,{
                'partner_id': record.partneram.id,
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
        # partners = self.env['res.partner'].sudo().search([('is_company','=',False),('active','=',True),('anggota_koprasi','=',True),('no_anggota','>',0)])
        partners = self.env['res.partner'].sudo().search([('is_company','=',False),('active','=',True),('anggota_koprasi','=',True)])
        line_ids = []
        simwab_account = self.env['account.account'].sudo().search([('simwab','=',True)])
        if not simwab_account:
            raise ValidationError(_("Simwab Account tidak ditemukan"))
        for partner in partners:
            line_data = ((0,0,{
                'partner_id': partner.id,
                'account_id': simwab_account.id,
                'name': 'Simpanan Wajib '+datetime.today().strftime('%Y-%m'),
                'debit': simwab_account.amount,
                'credit':0,
            }))
            line_ids.append(line_data)
            line_data = ((0,0,{
                'partner_id': partner.id,
                'account_id': simwab_account.counter_account.id,
                'name': 'Simpanan Wajib '+datetime.today().strftime('%Y-%m'),
                'debit': 0,
                'credit':simwab_account.amount,
            }))
            line_ids.append(line_data)
        if line_ids:
            self.write({'line_ids': line_ids})
        print("aww")

    def fee_simla(self):


        print(self)
        # partners = self.env['res.partner'].sudo().search([('is_company','=',False),('active','=',True),('anggota_koprasi','=',True),('no_anggota','>',0)])
        partners = self.env['res.partner'].sudo().search([('tabungan','>','0')])
        
        line_ids = []
        # for bunga in partners:
        #     total_bunga = (bunga.tabungan * 0.2) /100
           
        simwab_account = self.env['account.account'].sudo().search([('simsu','=',True)])
        if not simwab_account:
            raise ValidationError(_("Simwab Account tidak ditemukan"))
        
        for partner in partners:
            total_bunga = (partner.tabungan * 0.2) /100
            simla_line_data = ((0,0,{
                'partner_id': partner.id,
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

    @api.onchange('partneram')
    def amountauto(self):
        if self.partneram:
            self.amount_simsu = self.partneram.tabungan

class AccountLoanPost(models.TransientModel):
    _inherit = "account.loan.post"

    def move_line_vals(self):
        res = list()
        partner = self.loan_id.partner_id.with_company(self.loan_id.company_id)
        line = self.loan_id.line_ids.filtered(lambda r: r.sequence == 1)
        res.append(
            {
                "account_id": self.account_id.id,
                "partner_id": partner.id,
                "credit": 0,
                "debit": line.pending_principal_amount + sum(self.loan_id.line_ids.mapped('interests_amount')),
            }
        )
        if line.pending_principal_amount - line.long_term_pending_principal_amount > 0:
            res.append(
                {
                    "account_id": self.loan_id.interest_expenses_account_id.id,
                    "partner_id": partner.id,
                    "credit": sum(self.loan_id.line_ids.mapped('interests_amount')),
                    "debit": 0,
                }
            )
            res.append(
                {
                    "account_id": self.loan_id.long_term_loan_account_id.id,
                    "partner_id": partner.id,
                    "credit": (
                        line.pending_principal_amount
                        - line.long_term_pending_principal_amount
                    ),
                    "debit": 0,
                }
            )
        if (
            line.long_term_pending_principal_amount > 0
            and self.loan_id.long_term_loan_account_id
        ):
            res.append(
                {
                    "account_id": self.loan_id.long_term_loan_account_id.id,
                    "credit": line.long_term_pending_principal_amount,
                    "debit": 0,
                }
            )

        return res
    
    
    def move_vals(self):
        return {
            "loan_id": self.loan_id.id,
            "date": self.loan_id.start_date,
            "ref": self.loan_id.name,
            "journal_id": self.journal_id.id,
            "partner_id": self.loan_id.partner_id.id,
            "line_ids": [Command.create(vals) for vals in self.move_line_vals()],
        }
class accountloan(models.Model):
    _inherit = 'account.loan'

    loan_date = fields.Date('Loan Date')
  
    
    name = fields.Char(
        copy=False,
        required=True,
        readonly=True,
        default="/",
        states={"draft": [("readonly", True)]},
    )

    loan_type = fields.Selection(
        [
            ("fixed-annuity", "Fixed Annuity"),
            ("fixed-annuity-begin", "Fixed Annuity Begin"),
            ("fixed-principal", "Fixed Principal"),
            ("interest", "Only interest"),
        ],
        required=True,
        help="Method of computation of the period annuity",
        readonly=True,
        states={"draft": [("readonly", False)]},
        default="fixed-principal",
    )
    rate_type = fields.Selection(
        [("napr", "Nominal APR"), ("ear", "EAR"), ("real", "Real rate")],
        required=True,
        help="Method of computation of the applied rate",
        default="real",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )


    short_term_loan_account_id = fields.Many2one(
        "account.account",
        domain="[('company_id', '=', company_id)]",
        string="Short term account",
        help="Account that will contain the pending amount on short term",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    long_term_loan_account_id = fields.Many2one(
        "account.account",
        string="Bank account",
        help="Account that will contain the pending amount on Long term",
        domain="[('company_id', '=', company_id)]",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    interest_expenses_account_id = fields.Many2one(
        "account.account",
        domain="[('company_id', '=', company_id)]",
        string="Interests account",
        help="Account where the interests will be assigned to",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.onchange('partner_id','name')
    def get_price(self):
        if not self.long_term_loan_account_id:
            self.long_term_loan_account_id = self.env['account.account'].search([('code','=','22110010')], limit=1).id
        else:
            self.long_term_loan_account_id 
        if not self.short_term_loan_account_id:
            self.short_term_loan_account_id= self.env['account.account'].search([('code','=','81100040')], limit=1).id
        else :
            self.short_term_loan_account_id
        if not self.interest_expenses_account_id:
            self.interest_expenses_account_id= self.env['account.account'].search([('code','=','81100010')], limit=1).id
        else:
            self.interest_expenses_account_id
        
    def _compute_draft_lines(self):
        self.ensure_one()
        self.fixed_periods = self.periods
        self.fixed_loan_amount = self.loan_amount
        self.line_ids.unlink()
        amount = self.loan_amount
        if self.start_date:
            date = self.start_date
        else:
            date = datetime.today().date()
        delta = relativedelta(months=self.method_period)
        if not self.payment_on_first_period:
            date += delta
        for i in range(1, self.periods + 1):
            line = self.env["account.loan.line"].create(
                self._new_line_vals(i, date, amount)
            )
            line._check_amount()
            date += delta
            amount -= line.payment_amount - line.interests_amount
        if self.long_term_loan_account_id:
            self._check_long_term_principal_amount()

class loanline(models.Model):
    _inherit = 'account.loan.line'

    def _compute_interest(self):
        if self.loan_type == "fixed-annuity-begin":
            return -numpy_financial.ipmt(
                self.loan_id._loan_rate() / 100,
                2,
                self.loan_id.periods - self.sequence + 1,
                self.pending_principal_amount,
                -self.loan_id.residual_amount,
                when="begin",
            )
        if self.loan_type == "fixed-principal":
            # return (self.rate * self.loan_id.loan_amount / self.loan_id.periods / 100)
            return (self.rate * self.loan_id.periods * 1000)
        
        return self.pending_principal_amount * self.loan_id._loan_rate() / 100
    
    def _generate_move(self, journal=False, account=False):
        """
        Computes and post the moves of loans
        :return: list of account.move generated
        """
        res = []
        for record in self:
            if not record.move_ids:
                if record.loan_id.line_ids.filtered(
                    lambda r: r.date < record.date and not r.move_ids
                ):
                    raise UserError(_("Some moves must be created first"))
                move = self.env["account.move"].create(
                    record._move_vals(journal=journal, account=account)
                )
                move.action_post()
                res.append(move.id)
        return res
    
    
        
    
    

    
    

    def _long_term_move_vals(self):
        return {
            "loan_line_id": self.id,
            "loan_id": self.loan_id.id,
            "date": self.date,
            "ref": self.name,
            "journal_id": self.loan_id.journal_id.id,
            "line_ids": [
                Command.create(vals) for vals in self._get_long_term_move_line_vals()
            ],
        }

    def _generate_invoice(self):
        """
        Computes invoices of leases
        :return: list of account.move generated
        """
        res = []
        for record in self:
            if not record.move_ids:
                if record.loan_id.line_ids.filtered(
                    lambda r: r.date < record.date and not r.move_ids
                ):
                    raise UserError(_("Some invoices must be created first"))
                invoice = self.env["account.move"].create(record._invoice_vals())
                res.append(invoice.id)
                for line in invoice.invoice_line_ids:
                    line.tax_ids = line._get_computed_taxes()
                invoice.flush_recordset()
                invoice.filtered(
                    lambda m: m.currency_id.round(m.amount_total) < 0
                ).action_switch_invoice_into_refund_credit_note()
                if record.loan_id.post_invoice:
                    invoice.action_post()
                if (
                    record.long_term_loan_account_id
                    and record.long_term_principal_amount != 0
                ):
                    move = self.env["account.move"].create(
                        record._long_term_move_vals()
                    )
                    if record.loan_id.post_invoice:
                        move.action_post()
                    res.append(move.id)
        return res

    def _get_long_term_move_line_vals(self):
        return [
            {
                "account_id": self.loan_id.short_term_loan_account_id.id,
                "credit": 0,
                "debit": self.long_term_principal_amount,
            },
            {
                "account_id": self.long_term_loan_account_id.id,
                "credit": 0,
                "debit": self.long_term_principal_amount,
            },
        ]

    def view_account_values(self):
        """Shows the invoice if it is a leasing or the move if it is a loan"""
        self.ensure_one()
        if self.is_leasing:
            return self.view_account_invoices()
        return self.view_account_moves()




    def _move_line_vals(self, account=False):
        vals = []
        partner = self.loan_id.partner_id.with_company(self.loan_id.company_id)
        vals.append(
            {
                "account_id": self.long_term_loan_account_id.id,
                "partner_id": partner.id,
                "credit": 0,
                "debit": self.payment_amount,
            }
        )
        vals.append(
            {
                "account_id": self.loan_id.move_ids[-1].line_ids.account_id[0].id,
                "partner_id": partner.id,
                "credit": self.payment_amount,
                "debit": 0,
            }
        )
        if self.interests_amount:
            vals.append(
                {
                    "account_id": self.loan_id.interest_expenses_account_id.id,
                    "partner_id": partner.id,
                    "credit": 0,
                    "debit": self.interests_amount,
                }
            )
        vals.append(
            {
                "account_id": self.loan_id.short_term_loan_account_id.id,
                "partner_id": partner.id,
                "credit": self.interests_amount,
                "debit": 0,
            }
        )
        if self.long_term_loan_account_id and self.long_term_principal_amount:
            vals.append(
                {
                    "account_id": self.loan_id.short_term_loan_account_id.id,
                    "credit": self.long_term_principal_amount,
                    "debit": 0,
                }
            )
            vals.append(
                {
                    "account_id": self.long_term_loan_account_id.id,
                    "credit": 0,
                    "debit": self.long_term_principal_amount,
                }
            )
        return vals
class MoveLine(models.Model):
    _inherit = 'account.move.line'
    
    info = fields.Float(string= 'Simsuk')
    info_simwa = fields.Float(string= 'Simwab')

    @api.onchange('partner_id')
    def infomasiSimpanan(self):
        for record in self:
            if record.partner_id:
                record.info = record.partner_id.tabungan
    
    @api.onchange('partner_id')
    def infomasiSimpanan(self):
        for record in self:
            if record.move_id.amount_simsu == 0.0:
                record.move_id.amount_simsu = record.partner_id.tabungan[0]
        
                
            # info= {
            #     'simwa': simwa,
            #     'sukarela': simsu
            # }
            # self.info_simwa = info  
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
    # @api.model
    # def create(self, vals):
    #     print(vals)
        # partners = self.env['res.partner'].sudo().search([('no_anggota','!=',''),('is_company','=',False)],order='no_anggota desc',limit=1)
        # if vals['is_company'] == False and vals['anggota_koprasi'] == True:
        #     vals['no_anggota'] = partners.no_anggota + 1
        # return super(ResPartner, self).create(vals)
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    available_in_pos = fields.Boolean(string='Available in POS', help='Check if you want this product to appear in the Point of Sale.', default=True)

class PosConfig(models.Model):
	_inherit = "pos.config"

	restrict_zero_qty = fields.Boolean(string='Restrict Zero Quantity')


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	pos_restrict_zero_qty = fields.Boolean(related="pos_config_id.restrict_zero_qty",readonly=False)


class PosSession(models.Model):
	_inherit = 'pos.session'

	def _loader_params_product_product(self):
		result = super()._loader_params_product_product()
		result['search_params']['fields'].extend(['qty_available','type'])
		return result




