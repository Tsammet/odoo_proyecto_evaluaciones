# -*- coding: utf-8 -*-
{
    'name': 'Evaluaciones',
    'version': '1.0',
    'website': 'https://www.driverp.com',
    'author': 'DrivErp',
    'category': 'Extra Tools',
    'sequence': 50,
    'summary': 'Modulo de Evaluaciones',
    'depends': ['base'],
    'description': '''
        Descripcion blablablablablabla Evaluations
    ''',
    'data': [
        'views/tsm_evaluations_menu.xml',
        'views/tsm_employee_views.xml',
        'views/tsm_department_views.xml',
        'views/tsm_position_view.xml',
        'views/tsm_evaluate_template.xml',
        'views/tsm_evaluation.xml',
        'security/ir.model.access.csv'

    ],
    'demo': [],
    'test': [],
    'application': True,
}
