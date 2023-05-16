{
    'name': "First_Demo",
    'version': '1.0',
    'depends': ['base', 'website'],
    'author': "Ritik Jariya",
    'category': 'Real Estate/Brokerage',
    'description': "",
    # data files always loaded at installation
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
        'wizard/estate_wizard_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type.xml',
        'views/res_users.xml',
        'views/estate_menus.xml',
        'controllers/estate_template.xml',
    ],
    # data files containing optionally loaded demonstration data

    "demo": [
        "demo/estate_demo.xml",
    ],

    'application': True,
}
