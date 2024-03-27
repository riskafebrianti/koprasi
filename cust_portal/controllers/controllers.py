from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict

from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class PortalAccount(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        
        if 'loan_count' in counters:
            loan_count = request.env['account.loan'].search_count(self._get_invoices_domainn(partner)) \
                if request.env['account.loan'].check_access_rights('read', raise_exception=False) else 0
            values['loan_count'] = loan_count
        return values       
    
    def _get_invoices_domainn(self, partner):
        
        return [
            ('state', 'in', ('posted', 'draft')),
            ('partner_id', '=', [partner.id])
            ]

# my home
    
    # def _invoice_get_page_view_values(self, invoice, access_token, **kwargs):
    #     values = {
    #         'page_name': 'loan',
    #         'loan': invoice,
    #     }   
    #     return self._get_page_view_values(invoice, access_token, values, 'my_invoices_history', False, **kwargs)

    # def _prepare_quotations_domainn(self, partner):
    #     return [
    #         ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
    #         ('state', 'in', ['sent', 'cancel'])
    #     ]

    @http.route(['/my/loan'], type='http', auth="user", website=True)
    def portal_my_loan(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        partner = request.env.user.partner_id
        values = self._prepare_my_invoices_valuess(page, date_begin, date_end, sortby, filterby, partner)

        # pager
        # pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        # loan = values['invoices'](pager['offset'])
        # request.session['my_invoices_history'] = loan.ids[:100]

        # loan.update({
        #     'invoices': values,
        #     'pager': pager,
        # })
        # return request.render("'my_invoices_history',cust_portal.loanTes", {"invoicess":values,
        #                                               'page_name' : 'loan'})
        return request.render("cust_portal.loanTes", {"invoicess":values,              
                                                      'page_name' : 'loan'})
        # return http.request.render('cust_portal.loanTes',
        #                             {'payslip_ids': payslip_ids,
        #                                 'page_name':'loan'})
        
    def _prepare_my_invoices_valuess(self, date_begin, date_end, sortby, filterby, domain=None, url="/my/loan"):
        
        partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values()
        AccountInvoices = request.env['account.loan'].search([])

        domain = expression.AND([
            domain or [],

            self._get_invoices_domainn(partner)
        ])

        # searchbar_sortings = self._get_account_searchbar_sortings()
        # # default sort by order
        # if not sortby:
        #     sortby = 'date'
        # order = searchbar_sortings[sortby]['order']

        # searchbar_filters = self._get_account_searchbar_filters()
        # # default filter by value
        # if not filterby:
        #     filterby = 'all'
        # domain += searchbar_filters[filterby]['domain']

        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        values.update({
            'date': date_begin,
            # content according to pager and archive selected
            # lambda function to get the invoices recordset when the pager will be defined in the main method of a route
            'invoices': lambda pager_offset: AccountInvoices.search(domain, limit=self._items_per_page, offset=pager_offset),
            'page_name': 'invoice',
            # 'pager': {  # vals to define the pager.
            #     "url": url,
            #     "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            #     "total": AccountInvoices.search_count(domain),
            #     "page": page,
            #     "step": self._items_per_page,
            # },
            # 'default_url': url,
            # 'searchbar_sortings': searchbar_sortings,
            # 'sortby': sortby,
            # 'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            # 'filterby': filterby
        })
        return values

