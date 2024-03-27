from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict

from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from datetime import datetime, timedelta
import pandas as pd
from odoo.tools import date_utils

class PortalAccount(portal.CustomerPortal):

    @http.route(['/rekap/'], type='http', auth="user", website=True)    
    def portal_my_loan(self, **kw):
        partner = request.env.user.partner_id
        today = datetime.now().strftime('%Y-%m-%d')
        # bulan lalu
        date_begin = datetime.now().replace(datetime.now().year, datetime.now().month-1, day=22).strftime('%Y-%m-%d') if datetime.now().month != 1 else (12, datetime.now().year-1)
        # 2 bulan lalu
        date_pas = datetime.now().replace(datetime.now().year, datetime.now().month-2, day=22).strftime('%Y- %m- %d') if datetime.now().month != 1 else (12, datetime.now().year-1)

        # date_begin = today - timedelta(days=1).strftime('%Y-%m-%d')
        # values = self._prepare_my_rekap(page, date_begin, date_end, sortby, filterby, partner)
        loan = request.env['account.move'].search([
            ('state', '=', ('posted')),
            ('partner_id', '=', [partner.id]),
            ('journal_id', '=', (10)),
            ('date', '>', date_begin)
            
            ])
        if not loan : 
            loan = 0
        else:
            loan = loan[-1].amount_total_signed
        # invtotal= (sum(record.amount_untaxed for record in inv))
        
        inv = request.env['account.move'].search([
            ('state', 'in', ('posted','draft')),
            ('partner_id', '=', [partner.id]),
            ('journal_id', '=', (1)),
            ('date', '>', date_begin)
            ])
        if not inv : 
            inv = 0
            invtotal = 0
        else:
            
            invtotal= (sum(record.amount_untaxed for record in inv))

        simpok = request.env['account.move.line'].search([
            ('account_id', '=', (116)),
            ('partner_id', '=', [partner.id]),
            ('parent_state', '=', 'posted'),
            ('date', '>', date_begin)
            ])
        if not simpok: 
            simpok = 0
            simpoktotal = 0
        else:
            simpoktotal = sum(record.move_id.amount_total_signed for record in simpok)
            simpok = simpok[-1].move_id.amount_total_signed

        
        # if not simpoktotal :
        #     simpok = 0
        # return simpok
            

        simwab = request.env['account.move.line'].search([
            ('account_id', '=', (117)),
            ('partner_id', '=', [partner.id]),
            ('date', '>', date_begin)
            ])
        if not simwab: 
            simwab = 0
            simwabtotal = 0
        else:
            simwabtotal = sum(record.move_id.amount_total_signed for record in simwab)
            simwab = simwab[-1].move_id.amount_total_signed

        simsuk = request.env['account.move.line'].search([
            ('account_id', '=', (118)),
            ('partner_id', '=', [partner.id]),
            ('date', '>', date_begin)
            ])
        if not simsuk : 
            simsuk = 0
            simsuktotal = 0
        else:
            simsuktotal = sum(record.move_id.amount_total_signed for record in simsuk)            
            simsuk = simsuk[-1].move_id.amount_total_signed
            
               
        return request.render("cust_portal.rekap", {"invoicess":inv, 
                                                    "totalinv":invtotal, 
                                                    "simpok":simpok, 
                                                    "loan":loan,
                                                    "simwab":simwab, 
                                                    "simsuk":simsuk,
                                                    "today":today,
                                                    "simpoktotal":simpoktotal, 
                                                    "simwabtotal":simwabtotal, 
                                                    "simsuktotal":simsuktotal,
                                                        'page_name' : 'rekap'})
    
   

    # Example usage:
    # numbers_list = [10, 20, 30, 40, 50]
    # result_sum = calculate_sum(numbers_list)
    # print("Sum of numbers:", result_sum)

    # def _prepare_my_rekap(self, date_begin, date_end, sortby, filterby, domain=None, url="/rekap/"):
    #     partner = request.env.user.partner_id
    #     values = self._prepare_portal_layout_values()
    #     rekap = request.env['account.move'].search([])

    #     domain = expression.AND([
    #         domain or [],

    #         self._get_invoices_domainn(partner)
    #     ])

    #     values.update({
    #         'date': date_begin,
    #         # content according to pager and archive selected
    #         # lambda function to get the invoices recordset when the pager will be defined in the main method of a route
    #         'invoices': lambda pager_offset: rekap.search(domain, limit=self._items_per_page, offset=pager_offset),
    #         'page_name': 'rekap',

    #     })
    #     return values
