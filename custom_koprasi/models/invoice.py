from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError
import math
import logging
import math
import numpy_financial 
from datetime import datetime

from dateutil.relativedelta import relativedelta



class company(models.Model):
    _inherit = 'account.move'

    # company = fields.Char('Company')
    company = fields.Char('Company', related='partner_id.commercial_company_name')
    # partner_id = fields.Char('partner id', related='loan_id.partner_id.name')
    cust = fields.Char('Customer', related='partner_id.name')
    # self.partner_id = self.loan_id.partner_id.name
    # partner_id = fields.Many2one(compute='_compute_partner_id')
    
    # @api.onchange("partner_id")
    # def _compute_partner_id(self):
    #     if self.loan_id:
    #         partner = self.line_ids.filtered(lambda p: p.partner_id.id != False)
    #         self.partner_id  = self.line_ids.partner_id
                        
        # if self.partner_id:
        #     for line in self.partner_id:
        #         line.partner_id = self.partner_id


     
 

class AccountLoanPost(models.TransientModel):
    _inherit = "account.loan.post"

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
            return (self.rate * self.loan_id.loan_amount / self.loan_id.periods / 100)
        
        return self.pending_principal_amount * self.loan_id._loan_rate() / 100

# class accountloan(models.Model):
#     _inherit = 'account.loan'
#     rate_type = fields.Selection(
#         [("napr", "Nominal APR"), ("ear", "EAR"), ("real", "Real rate"), ("fix", "Fixed Rate")],
#         required=True,
#         help="Method of computation of the applied rate",
#         default="napr",
#         readonly=True,
#         states={"draft": [("readonly", False)]},
#     )


#     @api.model
#     def _compute_rate(self, rate, rate_type, method_period, loan_amount):
#         """
#         Returns the real rate
#         :param rate: Rate
#         :param rate_type: Computation rate
#         :param method_period: Number of months between payments
#         :return:
#         """
#         if rate_type == "napr":
#             return rate / 12 * method_period
#         if rate_type == "fix":
#             return loan_amount * rate / method_period
#         if rate_type == "ear":
#             return math.pow(1 + rate, method_period / 12) - 1
#         return rate
    
#     @api.depends("rate", "method_period", "rate_type", "loan_amount")
#     def _compute_rate_period(self):
#         for record in self:
#             record.rate_period = record._loan_rate()

#     def _loan_rate(self):
#         return self._compute_rate(self.rate, self.rate_type, self.method_period, self.loan_amount)




    

    # @api.onchange ("partner_id")
    # def _onchange_partner_id(self):
    #     if self.partner_id:
    #     #  self.barcode  = self.partner_id.barcode
    #         self.partner_id = self.loan_id.partner_id.name

    # @api.depends('partner_id')
    # def _compute_partner_id(self):
        # moves_to_update = self.search([('partner_id', '=', False)])

        # for move in moves_to_update:
        #         # Perform your operations on each move here
        #         # For example, you might want to update a field or perform some calculations
        #         move.write({
        #             self.partner_id: self.line_ids.partner_id.name
        #             # Add other fields you want to update
        #         })

        # # return False
        # print(self)
        # # if self.line_ids.partner_id[0]:
            # self.partner_id  = self[0].line_ids.partner_id.name
        # for record in self:
        #     record.partner_id = record.line_ids.partner_id.name
    
    
    
    # pseudocode
    # 1. loop account move
    # 2. if parter false and account move have loan
    # 3. filtered move line where parner not false
    # 4. set partner id in account move 
    # 5. done, happy coding :) 

    # @api.depends('partner_id')
    # def _compute_partner_id(self):
    #     for move in self:
            
    #         if move.partner_id.id == False and move.loan_id.name != False: 
    #             partner = move.line_ids.filtered(lambda p: p.partner_id.id != False)
    #             move.partner_id = partner[0].partner_id
    #         elif move.loan_id.name == False:
    #             move.partner_id = move.partner_id
    #     return  


    # tr
    #    @api.depends('partner_id')
    # def _compute_partner_id(self):
    #     for move in self:
    #         # if move.partner_id == None:
    #         #     move.partner_id = move.line_ids.partner_id
    #         # moves_to_update = move.search([('loan_id', '=', True)])
            
    #         if move.partner_id.id == False and move.loan_line_id.name != False: 
    #             partner = move.line_ids.filtered(lambda p: p.partner_id.id != False)
    #             move.partner_id = partner.partner_id

    #         # elif move.partner_id.id == True and move.loan_line_id.name != True:
    #         #     # partner = move.line_ids.filtered(lambda p: p.partner_id.id != False)
    #         #     move.partner_id = self.partner_id.id

    #     return 


    

    



# class company(models.Model):
#     _inherit = 'account.move.line'
    
#     partner_id = fields.Char('partner id', related='partner_id.name')