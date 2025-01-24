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
    'depends': ['base','point_of_sale','sale','purchase','website',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/followup.xml',
        'views/report_tagihan.xml',
        'views/res.xml',
        'views/invoice.xml',
        'views/res_users.xml',
        'views/website.xml',
        'views/pos_order_line.xml',
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
            'custom_koprasi/static/src/js/payment.js',
            # 'custom_koprasi/static/src/xml/button.xml',
            # 'custom_koprasi/static/src/js/producrscreen.js'
            'custom_koprasi/static/src/xml/pos.xml',
            # 'custom_koprasi/static/src/js/button.js',
            # 'custom_koprasi/static/src/js/order_extension.js',
            'custom_koprasi/static/src/xml/disablee.xml',
            # 'custom_koprasi/static/src/xml/productconfig.xml',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
