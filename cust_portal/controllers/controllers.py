# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class CustomKoprasi(http.Controller):
    # @http.route('/JumlahTagihan', type='http', auth="public", website=True)
    # def display(self, **kw):
    #     # return "Hello, world"
    #     return http.request.render('cust_portal.sub', {

    #     })

    # @http.route('/custom_koprasi/custom_koprasi/objects', auth='public')
    # def list(self, **kw):
    #     return http.request.render('custom_koprasi.listing', {
    #         'root': '/custom_koprasi/custom_koprasi',
    #         'objects': http.request.env['custom_koprasi.custom_koprasi'].search([]),
    #     })

    @http.route('/JumlahTagihan', auth='public')
    def object(self, **kw):
        return http.request.render('custom_koprasi.object', {
            'object': 
                ['testing','testing2'],
        })
