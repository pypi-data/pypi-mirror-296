# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "version": "12.0.0.1.1",
    "name": "Helpdesk with CC and TO text fields",
    "depends": [
        "helpdesk_mgmt",
        "mail_cc_and_to_text",
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
        Helpdesk with CC and TO text fields without res_partner model dependency".
    """,
    "data": ["views/helpdesk_ticket_view.xml"],
    "demo": [],
    "application": False,
    "installable": True,
}
