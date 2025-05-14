# -*- coding: utf-8 -*-
{
    'name': 'Language Center Management',
    'version': '1.0',
    'summary': 'Quản lý trung tâm ngoại ngữ và hệ thống câu hỏi',
    'description': """
        Module quản lý trung tâm ngoại ngữ bao gồm:
        - Quản lý học viên
        - Quản lý khóa học
        - Quản lý lịch học
        - Quản lý câu hỏi trắc nghiệm
    """,
    'author': 'DEVTHINH',
    'website': 'https://example.com',
    'license': 'LGPL-3',
    'category': 'Education',
    'depends': ['base', 'mail', 'polling'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/course_views.xml',
        'views/class_schedule_views.xml',
        'views/menu.xml',
        'wizard/import_questions_wizard_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
} 