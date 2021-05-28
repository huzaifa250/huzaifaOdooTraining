# -*- coding: utf-8 -*-
{
    'name': "cinema",

    'summary': "Cinema Erp System Management",

    'description': """
       An Erp System to Manage Cinema
        Manage audience and halls
       Mange ticket and events
    """,

    'author': "Huzaifa",
    'website': "huz.dark1@gmail.com",
    'category': 'Marketing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/cinema.xml',
        'views/film.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
