# -*- coding: utf-8 -*-
{
    'name': "maintenodoo",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'data/ir_cron.xml',
        'reports/paperformat_custom.xml',
        'reports/mantenimiento_invoice_report_view.xml',
        'security/mantenimiento_segurity.xml',
        'security/ir.model.access.csv',
        'views/equipo_sequence.xml',
        'views/menu_root.xml',
        'views/equipo_view.xml',
        'views/mantenimiento_view.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
