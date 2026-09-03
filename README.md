# Elite Vet — Odoo moduly

Repozitář s moduly pro Odoo 18 kliniky Elite Vet a s Docker sestavou, která je
používá.

```
Elite.vet/
├── docker-compose.yml     Odoo 18 + PostgreSQL, ./modules jako addons
├── config/odoo.conf       addons_path, připojení k databázi
└── modules/
    └── rozpis/            Rozpis služeb lékařů
```

Nový modul = nová podsložka v `modules/`. Nic dalšího se nenastavuje, Docker
tu složku už má namountovanou jako addons.

## Spuštění

```bash
git clone https://github.com/goatrental/Elite.vet.git
cd Elite.vet
docker compose up -d
```

Odoo běží na `http://localhost:8069`. Podrobnosti a nasazení na existující
server jsou v [DOCKER.md](DOCKER.md).

## Moduly

### `rozpis` — Rozpis služeb

Přidává aplikaci **Rozpis služeb** a veřejnou stránku `/rozpis-lekaru`
s měsíčním kalendářem.

Zadávání je záměrně co nejjednodušší — jeden řádek má tři údaje:

| Pole | Hodnota |
|---|---|
| Datum | den služby |
| Lékařka | výběr ze seznamu lékařek kliniky |
| Směna | Ranní / Odpolední / Noční / Víkendová / Zavřeno |

Časy se u směny nezadávají, nese je její typ. V položce **Typy směn** jde
změnit čas i barvu a projeví se to na webu:

| Směna | Čas | Barva na webu |
|---|---|---|
| Ranní | 8:00–14:00 | zelená |
| Odpolední | 14:00–20:00 | oranžová |
| Noční | 20:00–8:00 | fialová |
| Víkendová | 10:00–18:00 | růžová |
| Zavřeno | — | červený text z poznámky |

Detaily v [modules/rozpis/README.md](modules/rozpis/README.md).
