{
    "name": "Elite Vet - Rozpis sluzeb",
    "version": "18.0.1.0.0",
    "category": "Website",
    "summary": "Stranka /rozpis-lekaru: mesicni kalendar sluzeb lekaru generovany z Odoo Kalendare.",
    "description": """
Elite Vet - Rozpis sluzeb
=========================

Pridava verejnou stranku **/rozpis-lekaru** s mesicni mrizkou sluzeb.

Mrizka se nevyplnuje rucne v HTML. Cte udalosti z aplikace Kalendar, ktere maji
stitek **Rozpis sluzeb**, a vykresli aktualni a nasledujici mesic. Cisla dnu,
prazdne bunky i nazvy mesicu se pocitaji samy.

Jak se udalost cte
------------------
* nazev udalosti  -> jmeno lekarky zobrazene v bunce
* cas zacatku     -> typ sluzby (rano / odpoledne / noc)
* sobota a nedele -> vikendova sluzba bez ohledu na cas
* celodenni udalost -> cervena poznamka pres celou bunku (Zavreno, statni svatek)

Modul nema zadny Python kod ani zavislosti mimo standardni Odoo.
""",
    "author": "Michal Varys",
    "website": "https://www.michalvarys.eu",
    "license": "LGPL-3",
    "depends": ["website", "calendar"],
    "data": [
        "data/calendar_event_type.xml",
        "views/rozpis_lekaru_page.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
