# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Helpdesk Ticket to Lead',
    'summary': 'Create CRM Leads from Helpdesk Tickets',
    'description': """This module allows users to convert CRM Leads from a Helpdesk Ticket.""",
    'version': '12.0.1.1.0',
    'category': 'Tools',
    "license": "AGPL-3",
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    'website': 'https://gitlab.com/somitcoop/erp-research/odoo-helpdesk',
    'depends': [
        "base",
        "helpdesk_mgmt",
        "crm",
    ],
    'data': [
        'views/helpdesk_ticket_to_lead.xml',
        'views/crm_lead_form_view.xml',
    ],
    'installable': True,
    'application': False,
}
