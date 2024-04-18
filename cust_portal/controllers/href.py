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


from odoo.http import request, Response
from odoo.tools import image_process
from odoo.tools.translate import _
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
class PortalAccount(portal.CustomerPortal):

    @http.route(['/rekap/'], type='http', auth="public", website=True ) 
    def portal_my_loan(self, **kw):
        
        partner = request.env.user.partner_id
        today = datetime.now().strftime('%Y-%m-%d')
        # bulan lalu
        date_begin = datetime.now().replace(datetime.now().year, datetime.now().month-1, day=22).strftime('%Y-%m-%d') if datetime.now().month != 1 else (12, datetime.now().year-1)
        # 2 bulan lalu
        date_pas = datetime.now().replace(datetime.now().year, datetime.now().month-2, day=22).strftime('%Y-%m-%d') if datetime.now().month != 1 else (12, datetime.now().year-1)
        # filter = values.search([('date', '>', date_begin)])
       
        
        # date_begin = today - timedelta(days=1).strftime('%Y-%m-%d')
        # values = self._prepare_my_rekap(page, date_begin, date_end, sortby, filterby, partner)
        loann = request.env['account.move.line'].search([
            ('parent_state', '=', ('posted')),
            ('partner_id', '=', [partner.id]),
            ('account_id', '=', (29))
            # ('date', '<', date_begin) 
            ])
        
        if not loann : 
            loann = 0
            loan = 0
        else:
            loan = loann[-1].credit
            # loan 
        # invtotal= (sum(record.amount_untaxed for record in inv))
        
        inv = request.env['account.move'].search([
            ('state', '=', ('posted')),
            ('partner_id', '=', [partner.id]),
            ('journal_id', '=', (1))
            # ('date', '<', date_begin)
            ])
        if not inv : 
            inv = 0
            invtotal = 0
        else:
            values = {"invoicess":inv}
            # invtotal= (sum(inv.amount_untaxed for inv in values.get('invoicess')))
            invtotal= sum(values.get('invoicess').mapped('amount_untaxed'))

        simpok = request.env['account.move.line'].search([
            ('account_id', '=', (116)),
            ('partner_id', '=', [partner.id]),
            ('parent_state', '=', 'posted')
            # ('date', '>', date_begin)
            ])
        if not simpok: 
            simpok = 0
            simpoktotal = 0
        else:
            simpoktotal = sum(record.move_id.amount_total_signed for record in simpok)
            simpok = simpok[-1].move_id.amount_total_signed
            

        simwab = request.env['account.move.line'].search([
            ('account_id', '=', (117)),
            ('partner_id', '=', [partner.id])
            # ('date', '>', date_begin)
            ])
        if not simwab: 
            simwab = 0
            simwabtotal = 0
        else:
            simwabtotal = sum(record.move_id.amount_total_signed for record in simwab)
            simwab = simwab[-1].move_id.amount_total_signed

        simsuk = request.env['account.move.line'].search([
            ('account_id', '=', (118)),
            ('partner_id', '=', [partner.id])
            # ('date', '>', date_begin)
            ])
        if not simsuk : 
            simsuk = 0
            simsuktotal = 0
        else:
            simsuktotal = sum(record.move_id.amount_total_signed for record in simsuk)            
            simsuk = simsuk[-1].move_id.amount_total_signed

        totalpotongan = simpok+simsuk+simwab+invtotal+loan
        values = {
                    "invoicess":inv,  
                    "simpok":simpok, 
                    "loann":loann,
                    "simwab":simwab, 
                    "simsuk":simsuk,
                    "totalinv":invtotal,
                    "loan":loan,
                    "totalpotongan" : totalpotongan,
                    "simpoktotal":simpoktotal, 
                    "simwabtotal":simwabtotal, 
                    "simsuktotal":simsuktotal,
                    "today":today,
                     'page_name' : 'rekap'
                    
                    
        }
        

        filter  = {
                    "loann" : loann.search([('date', '<', date_begin)]).credit, 
                    "invoicess" : inv.search([('date', '<', date_begin)]),
                    # "totalinv" : sum(values.get('invoicess').mapped('amount_untaxed'))
                    }
        # invtotal= sum(values.get('invoicess').mapped('amount_untaxed'))
        
        if kw.get('filterr') == 'bulan_lalu':
            values.update(filter)
            itung={
                "totalinv" : sum(values.get('invoicess').mapped('amount_untaxed'))
            }
            values.update(itung)
            totalpotongan = simpok+simsuk+simwab+values.get('totalinv')+values.get('loann')
            jumlah={
                "totalpotongan" : totalpotongan
            }
            values.update(jumlah)
            # invtotal= sum(record.amount_untaxed for record in values.get('invoicess'))


        
        # values.update({"filter" :filter})
    
        # "x.invoice_list.filtered(lambda r: r.to_check == True)"
        # {key: value for key, value in data.items() if value > 2}

        # hitung = {
        #     "totalinv":invtotal,
        #     "loan":loan,
        #     "simpoktotal":simpoktotal, 
        #     "simwabtotal":simwabtotal, 
        #     "simsuktotal":simsuktotal,
        #     'page_name' : 'rekap'
        # }
        

        return request.render("cust_portal.rekap",
                              values,{
                                  "filter":filter,
                                  "totalinv":invtotal
                              }
                              )
        # return request.render("cust_portal.rekap", {"invoicess":inv, 
        #                                             "totalinv":invtotal, 
        #                                             "simpok":simpok, 
        #                                             "loan":loan,
        #                                             "loann":loann,
        #                                             "simwab":simwab, 
        #                                             "simsuk":simsuk,
        #                                             "today":today,
        #                                             "simpoktotal":simpoktotal, 
        #                                             "simwabtotal":simwabtotal, 
        #                                             "simsuktotal":simsuktotal,
        #                                             "filter":filter,
        #                                                 'page_name' : 'rekap'})
                              
                            # 'search' : all
                              
        # return request.render("cust_portal.rekap", 
        #                       values,
        #                       )

# def _render_portal(self, template, page, date_begin, date_end, sortby, filterby, domain, searchbar_filters, default_filter, url, history, page_name, key):
#             values.update{(
                 
#             )}
#     return




   
    
   

