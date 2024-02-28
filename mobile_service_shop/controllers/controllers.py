# -*- coding: utf-8 -*-
# from odoo import http
# from odoo.http import request

# class MobileShopController(http.Controller):

#     @http.route('/path/to/route', type='http', auth='user')
#     def some_controller_method(self, **kwargs):
#         docs = request.env['mobile.service.shop'].search([])
#         return http.request.render('mobile_service_shop.report_customer_details', {'docs': docs})







# class MobileServiceShop(http.Controller):
#     @http.route('/mobile_service_shop/mobile_service_shop/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mobile_service_shop/mobile_service_shop/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mobile_service_shop.listing', {
#             'root': '/mobile_service_shop/mobile_service_shop',
#             'objects': http.request.env['mobile_service_shop.mobile_service_shop'].search([]),
#         })

#     @http.route('/mobile_service_shop/mobile_service_shop/objects/<model("mobile_service_shop.mobile_service_shop"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mobile_service_shop.object', {
#             'object': obj
#         })
