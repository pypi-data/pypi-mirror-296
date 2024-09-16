# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Helpdesk Split and Merge',
    'summary': 'Split and Merge Helpdesk Tickets',
    'description': """This module allows users to split and merge helpdesk tickets.""",
    'version': '12.0.1.0.2',
    'category': 'Tools',
    "license": "AGPL-3",
    'author': 'Som It Cooperatiu SCCL',
    'website': 'https://gitlab.com/somitcoop/erp-research/odoo-helpdesk',
    'depends': [
        "base",
        "mail",
        "helpdesk_mgmt",
    ],
    'data': [
        'views/helpdesk_ticket_split_view.xml',
        'views/helpdesk_ticket_merge_view.xml',
        'views/res_config_settings.xml',
        'wizards/split_ticket_wizard.xml',
        'wizards/merge_ticket_wizard.xml',
        # 'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': False,
}
