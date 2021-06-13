# -*- coding: utf-8 -*-
{
    'name': "cinema",

    'summary': "Cinema Erp System Management",

    'description': """
       An Erp System to Manage Cinema
        Manage audience and halls
       Manage tickets and events
    """,

    'author': "Huzaifa",
    'website': "huz.dark1@gmail.com",
    'category': 'Marketing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/create_show_wizard.xml',
        'data/data.xml',
        'views/cinema.xml',
        'views/film.xml',
        'views/cinema_reservation.xml',
        'data/sequence.xml',
        'reports/report.xml',
        'reports/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
