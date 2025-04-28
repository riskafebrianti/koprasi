from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError,ValidationError
import math
import logging
import math
import numpy_financial 
from datetime import datetime
from dateutil.relativedelta import relativedelta

class periode_wizard(models.TransientModel):

    _name = 'partner.wizard'

    
    manual = fields.Boolean(string='Ubah Tanggal Periode')
    tgl_buka = fields.Date(string='Tanggal Buka Buku',default=lambda self: self._compute_default_tgl_buka())
    tgl_tutup = fields.Date(string='Tanggal Tutup Buku', default=lambda self: self._compute_default_tgl_tutup())

    @api.model
    def _compute_default_tgl_buka(self):
        if datetime.now().day >= 22: #bila tgl hari ini lebih besar dari 22
            tgl_buka = datetime.now().replace(day=22,)
            
        if datetime.now().day < 22: #bila tgl hari ini lebih besar dari 22
            tgl_buka = datetime.now().replace(day=22, month =datetime.now().month-1)
            
            
         
        return tgl_buka
    
    @api.model
    def _compute_default_tgl_tutup(self):
        if datetime.now().day > 21: #bila tgl hari ini lebih besar dari 22
            tgl_tutup = datetime.now().replace(day=21, month =datetime.now().month+1)
        if datetime.now().day < 21: #bila tgl hari ini lebih besar dari 22
            tgl_tutup = datetime.now().replace(day=21,)
 
        return tgl_tutup
    
    def action_confirm(self):
        data = self.env['res.partner'].sudo().search([])
        tgl_hari_ini = datetime(2025, 4, 26).date()
        for record in data:
            # if tgl_hari_ini
            record.tgl_buka = self.tgl_buka
            record.tgl_tutup = self.tgl_tutup
            record.option_date = 'manual'

        print(self)
    


   