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
        # today = datetime.now().strftime('%Y-%m-%d')
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d").date()
        # bulan lalu
        date_begin = datetime.now().replace(datetime.now().year, datetime.now().month-1, day=22).strftime('%Y-%m-%d') if datetime.now().month != 1 else (12, datetime.now().year-1)
        date_beginn = datetime.strptime(date_begin, "%Y-%m-%d").date()
        # 2 bulan lalu
        date_pas = datetime.now().replace(datetime.now().year, datetime.now().month-2, day=22).strftime('%Y-%m-%d') if datetime.now().month != 1 else (12, datetime.now().year-1)
        date_pass = datetime.strptime(date_pas, "%Y-%m-%d").date()
        # filter = values.search([('date', '>', date_begin)])
       
        
        # date_begin = today - timedelta(days=1).strftime('%Y-%m-%d')
        # values = self._prepare_my_rekap(page, date_begin, date_end, sortby, filterby, partner)
        # pinjam = request.env['account.move.line'].search([
        #     ('move_id.state', '=', ('posted')),
        #     ('partner_id', '=', [partner.id]),
        #     ('journal_id', '=', (10)),
        #     # ('account_id', '=', (29))
        #     # ('date', '<', date_begin) 
        #     ])
        
        # if not pinjam : 
        #     # pinjam = 0
            
        #     pinjaman = 0
        # else:
        #     # for x in loan:
        #     pinjaman = pinjam.line_ids[0].payment_amount
        
        loann = request.env['account.loan.line'].sudo().search([
            ('loan_state', '=', ('posted')),
            ('partner_id', '=', [partner.id]),
            ('date', '<=', today),
            ('date', '>=', date_begin)
            ])
  
        
        if not loann : 
            loann = 0
            loantotal = 0
            loop = []
        # else:
        #     loop = []
            
        # for lon in loann: 
        #     loop.append(lon.payment_amount)
        #     loantotal = sum(loop)
        #     print(lon)

                # for tes in values.get('loann'): 
                #     print(tes)
                #     loantotal = tes.line_ids[0].payment_amount
                # loan
            # loan 
        
<<<<<<< HEAD
        inv = request.env['account.move'].search([
            ('state', '=', ('posted')),
            ('partner_id', '=', [partner.id]),
            ('journal_id', '=', (1)),
            ('payment_state', '=', ('not_paid'))

            # ('date', '<', date_begin)
            ])
=======
        values = {"loann":loann}
        # inv = request.env['account.move'].search([
        #     ('state', '=', ('posted')),
        #     ('partner_id', '=', [partner.id]),
        #     ('journal_id', '=', (1)),
        #     ('payment_state', '=', ('not_paid'))

        #     # ('date', '<', date_begin)
        #     ])
# invoice POS
        inv = request.env['pos.order'].sudo().search([
                                                ('partner_id', '=', [partner.id]),
                                                ('date_order', '<=', today),
                                                ('date_order', '>=', date_begin), 
                                                ('state','!=', ('paid')),
                                                ('account_move.payment_state','!=', False),
                                                
                                                ])
>>>>>>> ce02dfa4dbba93fd0289fdcc1b1bf0fb476e82b4
        if not inv : 
            invtotal = 0
        else:
            values["invoicess"] = inv
            invtotal= sum(values.get('invoicess').mapped('amount_total'))

<<<<<<< HEAD
        simpokdaftar = request.env['account.move.line'].search([
            ('account_id.name', 'like', ('%Pokok')),
            ('partner_id', '=', [partner.id])
            ])
        simpok = request.env['account.move.line'].search([
            ('account_id.name', 'like', ('%Pokok')),
            ('partner_id', '=', [partner.id]),
            ('date', '<=', today),
            ('date', '>=', date_begin)
            ])
        
        if not values.get('simpokdaftar') : 
            simpokdaftar : 0
            # simpok = 0
            simpokk = 0
=======

# simpanan pokok
        simpokdaftar = request.env['account.move.line'].sudo().search([
            ('account_id.name', 'like', ('%Pokok')),
            ('partner_id', '=', [partner.id])
            ])
        simpok = sum(simpokdaftar.filtered(lambda d: d.date <= today and d.date >= date_beginn).mapped('amount_currency'))  

        if not simpokdaftar :
            simpok = 0
>>>>>>> ce02dfa4dbba93fd0289fdcc1b1bf0fb476e82b4
            simpoktotal = 0

        else:
<<<<<<< HEAD
            values = {"invoicess":inv, "simwab":simwab, "simwabdaftar" :simwabdaftar, "simpokdaftar":simpokdaftar, "simpok":simpok, "simsukdaftar":simsukdaftar, "simsuk":simsuk}
            
            simpokk = simpok.amount_currency
            simpoktotal = sum(values.get('simpokdaftar').mapped('amount_currency'))
            # simsuk = simsuk[-1].move_id.amount_total_signed

            

        simwab = request.env['account.move.line'].search([
            ('account_id.name', 'like', ('%Wajib')),
            ('partner_id', '=', [partner.id]),
            ('date', '<', today),
            ('date', '>=', date_begin)
            
            ])
        simwabdaftar = request.env['account.move.line'].search([
            ('account_id.name', 'like', ('%Wajib')),
            ('partner_id', '=', [partner.id])
            
            ])
        if not simwabdaftar: 
            simwabdaftar = 0
            simwab = 0
            simwabb = 0
            simwabtotal = 0
        else:
            values = {"invoicess":inv, "simwab":simwab, "simwabdaftar" :simwabdaftar,}
            simwabb = simwab.amount_currency
            simwabtotal= sum(values.get('simwabdaftar').mapped('amount_currency'))
            # values = {"invoicess":inv, "simwab":simwab, "simwabb":simwabb, "simwabtotal" : simwabtotal, "simwabdaftar" :simwabdaftar,}


        simsukdaftar = request.env['account.move.line'].search([
            ('account_id.name', 'like', ('%Sukarela')),
            ('partner_id', '=', [partner.id])
            ])
        simsuk = request.env['account.move.line'].search([
            ('account_id.name', 'like', ('%Sukarela')),
            ('partner_id', '=', [partner.id]),
            ('date', '<=', today),
            ('date', '>=', date_begin)
            ])
        
        if not simsukdaftar : 
            simsukdaftar : 0
=======
            values["simpokdaftar"] = simpokdaftar
            simpoktotal = sum(values.get('simpokdaftar').mapped('amount_currency'))

            
# simpanan Wajib
        simwabdaftar = request.env['account.move.line'].sudo().search([
            ('account_id.name', 'like', ('%Wajib')),
            ('partner_id', '=', [partner.id])
            ])    
        simwab = sum(simwabdaftar.filtered(lambda d: d.date <= today and d.date >= date_beginn).mapped('amount_currency'))  
        if not simwabdaftar: 
            simwab= 0
            simwabtotal = 0
        else:
            values["simwabdaftar"] = simwabdaftar
            simwabtotal= sum(values.get('simwabdaftar').mapped('amount_currency'))
            

# simpanan Sukarela
        simsukdaftar = request.env['account.move.line'].sudo().search([
            ('account_id.name', 'like', ('%Sukarela')),
            ('partner_id', '=', [partner.id])
            ])
        simsuk = sum(simsukdaftar.filtered(lambda d: d.date <= today and d.date >= date_beginn).mapped('amount_currency'))  
        
        if not simsukdaftar : 
>>>>>>> ce02dfa4dbba93fd0289fdcc1b1bf0fb476e82b4
            simsuk = 0
            simsukk = 0
            simsuktotal = 0
<<<<<<< HEAD

        else:
            values = {"invoicess":inv, "simwab":simwab, "simwabdaftar" :simwabdaftar, "simsukdaftar":simsukdaftar, "simsuk":simsuk}
            
            simsukk = simsuk.amount_currency
            simsuktotal = sum(values.get('simsukdaftar').mapped('amount_currency'))
            # simsuk = simsuk[-1].move_id.amount_total_signed

        totalpotongan = simpokk+simsukk+simwabb+invtotal+loan
        values = {
                    "invoicess":inv,  
                    "simpok":simpok, 
                    "loann":loann,
                    "simwabb":simwabb, 
                    "simwab":simwab, 
                    "simsuk":simsuk,
                    "simsukk":simsukk,
                    "totalinv":invtotal,
                    "loan":loan,
                    "totalpotongan" : totalpotongan,
                    "simpoktotal":simpoktotal, 
                    "simwabtotal":simwabtotal, 
                    "simsuktotal":simsuktotal,
                    "simwabdaftar" :simwabdaftar,
                    "simpokdaftar" :simpokdaftar,
                    "simsukdaftar" :simsukdaftar,
                    "today":today,
                     'page_name' : 'rekap'
                    
                    
        }
        # simwabupdate = 

        filter  = {
                    "loann" : loann.search([('date', '<', date_begin),('date', '>', date_pas)]).credit, 
                    "invoicess" : inv.search([('date', '<', date_begin),('date', '>', date_pas)]),
                    "simwab" : simwab.search([('date', '<', date_begin),('date', '>', date_pas)]),
                    "simsuk" : simsuk.search([('account_id', '=', (118)),('partner_id', '=', [partner.id]),('date', '<', date_begin),('date', '>', date_pas)]),
                    "simsukdaftar" : simsukdaftar.search([('account_id', '=', (118)),('partner_id', '=', [partner.id]),('date', '<', date_begin)]),
                    "simpok" : simpok.search([('account_id', '=', (116)),('partner_id', '=', [partner.id]),('date', '<', date_begin),('date', '>', date_pas)]),
                    "simpokdaftar" : simpokdaftar.search([('account_id', '=', (116)),('partner_id', '=', [partner.id]),('date', '<', date_begin)]),
                    "simwabdaftar" : simwabdaftar.search([('date', '<=', date_begin)]),
                    # "simsukdaftar" : simsukdaftar.search([('date', '<=', date_begin),('date', '>=', date_pas)]),
                    # "simsukdaftar" : simsukdaftar.search([('date', '<=', date_begin)])
                    # "totalinv" : sum(values.get('invoicess').mapped('amount_untaxed'))
=======
        else:
            values["simsukdaftar"] = simsukdaftar
            simsuktotal = partner.tabungan
            

        totalpotongan = simpok+simsuk+simwab+invtotal+loantotal

        values.update({"simpok": simpok, 
                       "simwab": simwab,
                       "simsuk": simsuk,
                       "totalinv": invtotal,
                       "loop": loop,
                       "loantotal": loantotal,
                       "totalpotongan": totalpotongan,
                       "simwabtotal": simwabtotal,
                       "simsuktotal": simsuktotal,
                       "simpoktotal": simpoktotal,
                       "today":today,
                        'page_name' : 'rekap'
                    })
        # values = {
        #             "invoicess":inv,  
        #             "simpok":simpok, 
        #             "loann":loann,
        #             "simwab":simwab, 
        #             "simsuk":simsuk,
        #             "totalinv":invtotal,
        #             "loop":loop, 
        #             "loantotal":loantotal,
        #             "totalpotongan" : totalpotongan,
        #             "simpoktotal":simpoktotal, 
        #             "simwabtotal":simwabtotal, 
        #             "simsuktotal":simsuktotal,
        #             "simwabdaftar" :simwabdaftar,
        #             "simpokdaftar" :simpokdaftar,
        #             "simsukdaftar" :simsukdaftar,
        #             # "loannn" :loannn,
        #             "today":today,
        #             'page_name' : 'rekap'      
        # }
        
        loan_bulan = request.env['account.loan.line'].sudo().search([
                                                                    # ('loan_state', '=', ('posted')),
                                                                    ('partner_id', '=', [partner.id]),
                                                                    ('date', '<=', date_beginn),
                                                                    ('date', '>=', date_pass)
                                                                    ])
        if not loan_bulan : 
            loan_bulan_tot = 0
            loan = []
        else:

            loan = []
            
            # for lon in loann:
                
            #     loan.append(lon.payment_amount)
            loan_bulan_tot = sum(loan)
            #     print(lon)

            # loan_bulan_tot= sum(loan_bulan.mapped('payment_amount'))
            # loan = [loan_bulan.payment_amount]


        filter  = {
                    "loop" : loan, 
                    # "loop" : 
                    "loantotal" : loan_bulan_tot,
                    "invoicess" : request.env['pos.order'].sudo().search([('account_move.date', '<', date_begin),('account_move.date', '>', date_pas),('partner_id', '=', [partner.id])]),
                    # "invoicess" : inv.filtered(lambda d: d.account_move.date < date_beginn and d.account_move.date > date_pass),
                    # "simwab" : simwabdaftar.filtered(lambda a: a.date < date_beginn and a.date > date_pass),
                    "simwab" : sum(simwabdaftar.filtered(lambda a: a.date < date_beginn and a.date > date_pass).mapped('amount_currency'))  ,
                    "simsuk" : simsukdaftar.filtered(lambda b: b.date < date_beginn and b.date > date_pass),
                    "simsukdaftar" : simsukdaftar.filtered(lambda c: c.date < date_beginn and c.date > date_pass),
                    "simpok" : simpokdaftar.filtered(lambda e: e.date < date_beginn and e.date > date_pass),
                    "simpokdaftar" : simpokdaftar.filtered(lambda g: g.date < date_beginn and g.date > date_pass),
                    "simwabdaftar" : simwabdaftar.filtered(lambda f: f.date <= date_beginn),
>>>>>>> ce02dfa4dbba93fd0289fdcc1b1bf0fb476e82b4
                    }
        
        
        if kw.get('filterr') == 'bulan_lalu':
            
            values.update(filter)

            itung={
<<<<<<< HEAD
                "totalinv" : sum(values.get('invoicess').mapped('amount_untaxed')),
                "simwabb" : values.get('simwab').amount_currency,
=======
                "totalinv" : sum(values.get('invoicess').mapped('amount_total')),
                # "loantotal" : values.get('loann').amount_total,
                # "simwab" : values.get('simwab').amount_currency,
>>>>>>> ce02dfa4dbba93fd0289fdcc1b1bf0fb476e82b4
                "simwabtotal" : sum(values.get('simwabdaftar').mapped('amount_currency')),
                "simpoktotal" : sum(values.get('simpokdaftar').mapped('amount_currency')),
                "simsuktotal" : sum(values.get('simsukdaftar').mapped('amount_currency'))


            }
            values.update(itung)
<<<<<<< HEAD
            totalpotongan = values.get('simpok').amount_currency+values.get('simsuk').amount_currency+values.get('simwab').amount_currency+values.get('totalinv')+values.get('loann')
=======
            totalpotongan = values.get('simpok').amount_currency+values.get('simsuk').amount_currency+values.get('simwab')+values.get('totalinv')+values.get('loantotal')
>>>>>>> ce02dfa4dbba93fd0289fdcc1b1bf0fb476e82b4
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




   
    
   

