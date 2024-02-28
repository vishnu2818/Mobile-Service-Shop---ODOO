# -*- coding: utf-8 -*-
{
    'name': "Mobile Service Shop",
    'sequence': -200,
    'summary': """All Types of Mobile's Service Here!!""",
    'description': """Mobile Service Shop""",
    'author': " >inu",
    'website': "https://github.com/vishnu2818",
    'category': 'Service',
    'version': '14.0.0.0.0',
    'depends': ['base','sale','product'],
    'data': [
            'security/ir.model.access.csv',
            'report/reports.xml',
            'report/mobile_shop_template.xml',
            'data/shop_sequence.xml',
            'views/app_view.xml',
            'views/sale_order.xml'
            ],
    'images': [
            'static/description/icon.png',
            'static/description/logo.png'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}

# Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml --->category