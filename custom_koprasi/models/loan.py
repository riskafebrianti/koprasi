from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError,ValidationError
import math
import logging
import math
import numpy_financial 
from datetime import datetime
from dateutil.relativedelta import relativedelta
class AccountLoanPost(models.TransientModel):

    _inherit = "account.loan.post"

    date = fields.Date(
        string='Date',
        default=fields.Date.context_today,
    )
    

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
            "date": self.date.strftime("%Y-%m-%d"),
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
        self.journal_id=self.env['account.journal'].search([('code','=','LOAN')], limit=1).id
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