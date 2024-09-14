{
    'name': "Odoo customizations for Agresta",
    'version': '16.0.0.0.1',
    'depends': ["project"],
    'author': "Coopdevs Treball SCCL",
    'website': 'https://coopdevs.org',
    'category': "Project",
    'summary': """
    Odoo customizations for Agresta
    """,
    "license": "AGPL-3",
    'data': [ 'data/security_groups.xml',
              'data/scheduled_action.xml',
              'security/ir.model.access.csv',
              'wizards/project_recalculate_execution.xml',
              'views/project_task.xml',
              'views/project.xml',

    ],
}
