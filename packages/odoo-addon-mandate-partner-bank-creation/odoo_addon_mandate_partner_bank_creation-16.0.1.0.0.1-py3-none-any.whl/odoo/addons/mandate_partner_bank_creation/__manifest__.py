# Copyright 2021-Coopdevs Treball SCCL (<https://coopdevs.org>)
# - César López Ramírez - <cesar.lopez@coopdevs.org>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Banking Mandate creation with Res Partner Bank",
    "version": "16.0.1.0.0",
    "depends": [
        "base", "component_event", "account_banking_mandate",
        "account_banking_sepa_direct_debit"
    ],
    "author": "Coopdevs Treball SCCL",
    "category": "Accounting & Finance",
    "website": "https://coopdevs.org",
    "license": "AGPL-3",
    "summary": """
        When a Res Partner Bank is created, a Account Banking Mandate is created too
    """,
    "data": [],
    "demo": [
        "demo/partner.xml",
    ],
    "installable": True,
}
