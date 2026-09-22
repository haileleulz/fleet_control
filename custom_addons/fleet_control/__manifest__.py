{
    'name': 'Fleet Control',
    'version': '1.0',
    'author': 'Haile',
    'category': 'Sales',
    'website': 'https://www.haile.com',
    'summary': 'Bus',
    'description': """
    Bus Deployment and Route control System
    """,
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/bus_deployment.xml',
        'views/bus_route.xml',
        'views/bus_information.xml',
        'views/bus_stations.xml',
        'views/bus_depot.xml',
        'views/menu.xml',
        'report/report_template.xml',
        'report/deployment_report.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
