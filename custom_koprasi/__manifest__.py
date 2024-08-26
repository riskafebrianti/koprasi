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
    'depends': ['base','sale','point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/followup.xml',
        'views/report_tagihan.xml',
        'views/res.xml',
        'views/invoice.xml',
        'views/res_users.xml'
        # 'static/src/xml/uom.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'custom_koprasi/static/src/js/PaymentScreen.js',
            # 'custom_koprasi/static/src/js/producrscreen.js'
            'custom_koprasi/static/src/xml/pos.xml',
            # 'custom_koprasi/static/src/xml/productconfig.xml',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
