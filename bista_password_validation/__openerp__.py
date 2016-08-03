# -*- coding: utf-8 -*-
# This module is developed for the Odoo v9 

{
    "name": "Password Validation",
    'version': '9.0.1.0',
    'category': 'tools',
    'description': """Password Validation
    """,
    'author': 'Bista Solutions Pvt. Ltd.',
    'website': 'http://www.bistasolutions.com',
    'depends': ['auth_signup'],
    'price': '446.09',
    'currency': 'EUR',
    'data': [
        'security/ir.model.access.csv',
        'views/change_password_views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        'static/src/xml/password_validation.xml',
    ],
    'installable': True,
    'auto_install': False,
}
