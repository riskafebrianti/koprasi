# -*- coding: utf-8 -*-
# from odoo import http


# class CustomKoprasi(http.Controller):
#     @http.route('/custom_koprasi/custom_koprasi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_koprasi/custom_koprasi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_koprasi.listing', {
#             'root': '/custom_koprasi/custom_koprasi',
#             'objects': http.request.env['custom_koprasi.custom_koprasi'].search([]),
#         })

#     @http.route('/custom_koprasi/custom_koprasi/objects/<model("custom_koprasi.custom_koprasi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_koprasi.object', {
#             'object': obj
#         })
