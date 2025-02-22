# -*- coding: utf-8 -*-
# from odoo import http


# class Maintenodoo(http.Controller):
#     @http.route('/maintenodoo/maintenodoo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/maintenodoo/maintenodoo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('maintenodoo.listing', {
#             'root': '/maintenodoo/maintenodoo',
#             'objects': http.request.env['maintenodoo.maintenodoo'].search([]),
#         })

#     @http.route('/maintenodoo/maintenodoo/objects/<model("maintenodoo.maintenodoo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('maintenodoo.object', {
#             'object': obj
#         })

