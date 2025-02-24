# -*- coding: utf-8 -*-
{
    'name': "Mantenimodoo",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """
Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail'],
    'data': [
        'data/ir_cron.xml',
        'reports/paperformat_custom.xml',
        'reports/mantenimiento_invoice_report_view.xml',
        'reports/dates_external_layout.xml',  # Asegúrate de incluirlo
        'security/mantenimiento_segurity.xml',
        'security/ir.model.access.csv',
        'views/equipo_sequence.xml',
        'views/menu_root.xml',
        'views/equipo_view.xml',
        'views/mantenimiento_view.xml',
        'views/user_inherit_view.xml',
        'views/views.xml',
        'views/templates.xml',
        'wizard/date_report.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
