# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "version": "12.0.0.1.0",
    "name": "Mass Parent Ticket Generation",
    "depends": [
        "helpdesk_mgmt",
        "helpdesk_ticket_massive_creation",
        "contract",
        "queue_job",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Auth",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        Create helpdesk tickets massively, from multiple preselected partners.
    """,
    "data": [
        "views/helpdesk_ticket_view.xml",
        "wizards/helpdesk_ticket_massive_creation/helpdesk_ticket_massive_creation_view.xml",  # noqa
        "wizards/helpdesk_ticket_massive_creation/helpdesk_ticket_massive_creation_parents_view.xml",  # noqa
        "wizards/send_global_email/helpdesk_ticket_parent_global_send.xml",
        "wizards/helpdesk_set_child_ticket/helpdesk_ticket_massive_creation_parents_view.xml",
    ],
    "demo": [],
    "application": True,
    "installable": True,
}
