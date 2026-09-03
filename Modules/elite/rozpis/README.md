# Rozpis služeb

Odoo 18 modul. Přidává aplikaci **Rozpis služeb** a veřejnou stránku
**`/rozpis-lekaru`** s měsíčním kalendářem.

## Jak se rozpis vyplňuje

Odoo → **Rozpis služeb** → **Rozpis** → tlačítko **Nové**.

Vyplní se tři věci a je hotovo:

| Pole | Hodnota |
|---|---|
| **Datum** | den služby |
| **Lékařka** | výběr ze seznamu |
| **Směna** | Ranní / Odpolední / Noční / Víkendová / Zavřeno |

Časy se nezadávají — jsou dané typem směny:

| Směna | Čas | Barva na webu |
|---|---|---|
| Ranní | 8:00–14:00 | zelená |
| Odpolední | 14:00–20:00 | oranžová |
| Noční | 20:00–8:00 | fialová |
| Víkendová | 10:00–18:00 | růžová |

Seznam se dá psát rovnou v tabulce (klik do řádku, vyplnit, Enter na další),
nebo přepnout vpravo nahoře na **kalendář** a klikat do dní.

**Zavřeno / svátek:** směna `Zavřeno`, lékařka se nevyplňuje, do **Poznámky**
se napíše text (například `Státní svátek`). Na webu se vypíše červeně.

**Lékařky** se spravují v druhé položce menu. Jméno a nic víc.

## Co se objeví na webu

Stránka ukazuje **aktuální a následující měsíc**. Přelomem měsíce se posunou
samy. Čísla dnů, prázdné buňky i názvy měsíců se počítají samy, nic se nepřepisuje.

Po najetí na jméno vyskočí bublina s typem služby a časem.

## Navigace

Odkazy v horní liště i v mobilním menu se berou z **menu webu**, ne z kódu
stránky. Mění se v Odoo: **Web → Upravit → Menu**. Modul si při instalaci
založí položku *Rozpis služeb* mířící na `/rozpis-lekaru`; jde přejmenovat,
přesunout i smazat.

## Pro správce

* Modely: `elite.vet.shift` (řádek rozpisu), `elite.vet.doctor` (lékařka).
* Ukládá se **datum**, ne čas — odpadá tím přepočet časových zón.
* Šablona má pojistku `'elite.vet.shift' in request.env`; kdyby model chyběl,
  stránka se vykreslí prázdná místo chyby 500.
* Záznam stránky `website.page` je publikovaný rovnou modulem.
* Multi-website: `website_id` není nastavené, stránka je na všech webech
  v databázi. Pro omezení jen na Elite Vet doplňte pole do záznamu `website.page`.

Nasazení přes Docker: [../../../DOCKER.md](../../../DOCKER.md).
