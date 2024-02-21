# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalCustom(http.Controller):
    # super(SaleOrder, self).action_cancel()

    
    # @http.route('/portal_custom/portal_custom', auth='public')
    # def index(self, **kw):
    #     return "Hello, world"

    # @http.route('/portal_custom/portal_custom/objects', auth='public')
    # def list(self, **kw):
    #     return http.request.render('portal_custom.listing', {
    #         'root': '/portal_custom/portal_custom',
    #         'objects': http.request.env['portal_custom.portal_custom'].search([]),
    #     })

    # @http.route('/portal_custom/portal_custom/objects/<model("portal_custom.portal_custom"):obj>', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('portal_custom.object', {
    #         'object': obj
    #     })

# class pinjamanCustomerPortal(CustomerPortal):
#     def _prepare_home_portal_values(self):
#         values = super(CustomerPortal, self)._prepare_home_portal_values()
#         return values
        
    @http.route(['/my/orderss', '/my/orderss/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_orders(self, **kwargs):
        values = self._prepare_sale_portal_rendering_values(quotation_page=False, **kwargs)
        request.session['my_orders_history'] = values['orders'].ids[:100]
        return request.render("sale.portal_my_orders", values)

    @http.route(['/my/orderss/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')