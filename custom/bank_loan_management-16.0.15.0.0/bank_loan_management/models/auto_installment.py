from odoo import api, fields, models
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class AutoInstallment(models.Model):
    _name = "auto.installment"

    @api.model
    def generate_installments(self):
        today = date.today()
        loans = self.env['loan.management'].search([('state', '=', 'disbursement')])
        for loan in loans:
            if loan.next_installment_date and loan.next_installment_date.month == today.month:
                installment_date = loan.next_installment_date
            else:
                installment_date = today
            installment_vals = {
                'loan_ref_no': loan.id,
                'installment_date': installment_date,
            }
            self.env['loan.installment'].create(installment_vals)
            loan.update_next_installment_date()