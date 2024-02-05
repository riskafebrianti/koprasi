# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class custom_koprasi(models.Model):
#     _name = 'custom_koprasi.custom_koprasi'
#     _description = 'custom_koprasi.custom_koprasi'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
