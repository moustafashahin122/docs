# -*- coding: utf-8 -*-
{
    'name': "Chatter RTL",

    'summary': " this module handles rtl in the chatter ",
    'description': """
    this module handles rtl in the chatter 
    """,
    'author': "Metrics",
    'website': "https://www.metrics.com.eg/",
    'category': 'other',
    'version': '17.0.1.0.0',
    'installable': True,
    'application': False,
    'depends' : ['base', 'web'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],



 'assets': {
        'web.assets_backend': [
            'chatter_rtl/static/src/components/*/*.js',
            'chatter_rtl/static/src/components/*/*.xml',
            'chatter_rtl/static/src/components/*/*.scss',
        ],
    },
}

