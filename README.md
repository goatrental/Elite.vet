# Elite Vet — Rozpis služeb

Odoo 18 modul. Přidává veřejnou stránku **`/rozpis-lekaru`** s měsíčním kalendářem
služeb lékařů. Stránka se plní z aplikace **Kalendář**, ne ručně v HTML.

## Instalace

1. **Nejdřív smazat stávající ručně vytvořenou stránku**, jinak se URL srazí:
   Web → Stránky → `/rozpis-lekaru` → smazat.
   (Smaže se i její pohled. Na téhle stránce nejsou žádné překlady, takže se nic neztratí.)
2. Složku `elite_vet_rozpis` zkopírovat do addons path.
3. Restartovat Odoo.
4. Aplikace → **Aktualizovat seznam aplikací** → najít `Elite Vet - Rozpis sluzeb` → **Instalovat**.

Aktualizace po změně kódu: `-u elite_vet_rozpis`.

> Modul jde nasadit na **Odoo.sh** nebo na **vlastní server**. Na Odoo Online (SaaS)
> se vlastní moduly instalovat nedají.

## Co modul obsahuje

| Soubor | Obsah |
|---|---|
| `data/calendar_event_type.xml` | štítek `Rozpis služeb` (`noupdate="1"`, upgrade ho nepřepíše) |
| `views/rozpis_lekaru_page.xml` | QWeb šablona stránky + záznam `website.page` (rovnou publikovaná) |

Závislosti: `website`, `calendar`. Žádný Python kód.

## Jak se rozpis vyplňuje

V aplikaci **Kalendář** se založí událost:

| Pole | Hodnota |
|---|---|
| Téma schůzky | jméno lékařky, přesně jak má být v buňce |
| Začít | datum a čas začátku směny |
| Trvání | délka směny |
| Štítky | **`Rozpis služeb`** — bez něj se událost na web nedostane |
| Opakovaný | zapnout u pravidelných směn |

Čas začátku určuje barvu:

| Začátek | Směna | Barva |
|---|---|---|
| do 10:00 | Ranní | zelená |
| do 17:00 | Odpolední | oranžová |
| později | Noční | fialová |
| sobota / neděle | Víkend | růžová |

**Zavřeno / státní svátek:** zapnout **Celý den**, text napsat do Tématu schůzky.
Vypíše se červeně přes celou buňku.

## Poznámky pro správce

* Vykresluje se **aktuální a následující měsíc**. Přelomem měsíce se posunou samy,
  nic se nepřepisuje.
* Časy se ve website QWebu čtou v UTC (`context_timestamp` tam není k dispozici),
  proto se typ směny určuje z UTC hodiny s prahy 10 a 17 — sedí pro zimní i letní čas.
  V bublině se čas zobrazuje přes `t-field` s `tz_name='Europe/Prague'`, návštěvník
  tedy vidí správný místní čas bez ohledu na to, odkud se dívá.
* Šablona má pojistku `'calendar.event' in request.env`. Kdyby aplikace Kalendář
  chyběla, stránka se vykreslí prázdná místo chyby 500.
* Multi-website: `website_id` není nastavené, stránka je tedy na všech webech
  v databázi. Pro omezení jen na Elite Vet doplnit pole do záznamu `website.page`.

## Nasazení přes Docker

Podrobný postup pro Odoo v Dockeru (addons volume, práva, instalace přes
`docker compose exec`, řešení potíží) je v [`DOCKER.md`](DOCKER.md).
