# Elite Vet — Odoo moduly

Repozitář s moduly pro Odoo 18 kliniky Elite Vet a s Docker sestavou, která je
používá.

```
Elite.vet/
├── docker-compose.yml     Odoo 18 + PostgreSQL, ./Modules jako addons
├── config/odoo.conf       addons_path, připojení k databázi
└── Modules/
    └── elite/             moduly kliniky Elite Vet
        └── rozpis/        Rozpis služeb lékařů
```

Nový modul = nová podsložka v `Modules/elite/`. Nic dalšího se nenastavuje,
Docker tu složku už má namountovanou jako addons.

Moduly jiného klienta patří do vlastní podsložky vedle `elite/`. Pak se do
`addons_path` v `config/odoo.conf` přidá i ta cesta.

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

Časy se nezadávají, jsou dané typem směny:

| Směna | Čas | Barva na webu |
|---|---|---|
| Ranní | 8:00–14:00 | zelená |
| Odpolední | 14:00–20:00 | oranžová |
| Noční | 20:00–8:00 | fialová |
| Víkendová | 10:00–18:00 | růžová |
| Zavřeno | — | červený text z poznámky |

Detaily v [Modules/elite/rozpis/README.md](Modules/elite/rozpis/README.md).
