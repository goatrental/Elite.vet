{
    "name": "Elite Vet - Rozpis sluzeb",
    "version": "18.0.2.0.0",
    "category": "Website",
    "summary": "Rozpis sluzeb lekaru: jednoducha aplikace v Odoo a mesicni kalendar na webu.",
    "description": """
Elite Vet - Rozpis sluzeb
=========================

Prida vlastni aplikaci **Rozpis sluzeb** a verejnou stranku **/rozpis-lekaru**.

Zadavani je zamerne co nejjednodussi. Jeden radek rozpisu ma tri udaje:

* **Datum**
* **Lekarka** (vyber ze seznamu lekarek kliniky)
* **Smena** (Ranni / Odpoledni / Nocni / Vikendova / Zavreno)

Casy se nezadavaji, jsou dane typem smeny. Zadna dalsi pole, zadni ucastnici,
zadne upominky.

Na webu se z toho vykresli mesicni kalendar na aktualni a nasledujici mesic.
Cisla dnu, prazdne bunky i nazvy mesicu se pocitaji samy.

Navigace stranky se bere z menu webu, takze odkazy jdou menit v Odoo
(Web -> Upravit -> Menu) a nemusi se sahat do kodu.
""",
    "author": "Michal Varys",
    "website": "https://www.michalvarys.eu",
    "license": "LGPL-3",
    "depends": ["website"],
    "data": [
        "security/ir.model.access.csv",
        "data/vet_doctor_data.xml",
        "data/website_menu.xml",
        "views/vet_shift_views.xml",
        "views/vet_doctor_views.xml",
        "views/menus.xml",
        "views/rozpis_lekaru_page.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
