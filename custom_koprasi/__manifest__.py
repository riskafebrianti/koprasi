# -*- coding: utf-8 -*-
{
    'name': "custom_koprasi",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.',

    # any module necessary for this one to work correctly
    'depends': ['base','account','purchase','point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/followup.xml',
        'views/report_tagihan.xml',
        'views/res.xml',
        'views/invoice.xml',
        # 'views/config.xml',
        'views/res_users.xml',
        'views/res_wizard.xml',
        # 'views/website.xml',
        'views/pos_order_line.xml',
        'views/pos_order.xml',
        # 'views/stock_move.xml',
        # 'views/sale.xml',
        'report/template.xml',
        'report/report.xml',
        'report/pos_order.xml',
        'report/report_kwitansi.xml',
        'report/pos_order_lap.xml',
        # 'views/loan.xml',

        # 'views/note_pos.xml'
        # 'security/product_approval_management_groups.xml',
        # 'security/ir.model.access.csv',
        # 'views/assets.xml',
        # 'views/pos.xml'
        # ' stazstic/src/xml/uom.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            # 'custom_koprasi/static/src/js/PaymentScreen.js',
            'custom_koprasi/static/src/js/OrderReceipt.js',
            # 'custom_koprasi/static/src/js/payment.js',
            'custom_koprasi/static/src/js/method.js',
            'custom_koprasi/static/src/xml/button.xml',
            'custom_koprasi/static/src/js/producrscreen.js',
            'custom_koprasi/static/src/xml/pos.xml',
             'custom_koprasi/static/src/xml/order.xml',
            'custom_koprasi/static/src/js/button.js',
            'custom_koprasi/static/src/js/note.js',
            'custom_koprasi/static/src/js/hitung.js',
            'custom_koprasi/static/src/js/hitung_model.js',
            # 'custom_koprasi/static/src/js/disablee.js',
            # 'custom_koprasi/static/src/xml/productconfig.xml',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
