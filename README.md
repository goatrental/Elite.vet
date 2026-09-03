# Modules

Odoo 18 moduly a Docker sestava, která je používá. Moduly jsou seřazené
po projektech.

```
Modules/
├── docker-compose.yml     Odoo 18 + PostgreSQL
├── config/odoo.conf       addons_path, připojení k databázi
└── vet/                   Elite Vet
    └── rozpis/            Rozpis služeb lékařů
```

Celý repozitář je v kontejneru namountovaný do `/mnt/modules`.

**Nový modul stejného projektu** = nová podsložka v `vet/`. Nic se nenastavuje.

**Nový projekt** = nová složka vedle `vet/` a jeden záznam navíc
v `addons_path` v [config/odoo.conf](config/odoo.conf):

```ini
addons_path = /mnt/modules/vet,/mnt/modules/dalsi-projekt,/usr/lib/python3/dist-packages/odoo/addons
```

## Spuštění

```bash
git clone https://github.com/goatrental/Modules.git
cd Modules
docker compose up -d
```

Odoo běží na `http://localhost:8069`. Nasazení na existující server je
v [DOCKER.md](DOCKER.md).

## vet — Elite Vet

### `rozpis` — Rozpis služeb

Aplikace **Rozpis služeb** a veřejná stránka `/rozpis-lekaru` s měsíčním
kalendářem. Aplikace má tři položky a nic víc.

**Rozpis** — jeden řádek má tři údaje:

| Pole | Hodnota |
|---|---|
| Datum | den služby |
| Lékařka | výběr ze seznamu |
| Směna | výběr z typů směn |

**Lékařky** — jméno a konec.

**Typy směn** — tady se mění čas i barva směny. Změna se hned promítne na web,
do vysvětlivek i do bublin u jmen.

| Název | Od | Do | Barva |
|---|---|---|---|
| Ranní služba | 8:00 | 14:00 | zelená |
| Odpolední služba | 14:00 | 20:00 | oranžová |
| Noční služba | 20:00 | 8:00 | fialová |
| Víkendová služba | 10:00 | 18:00 | růžová |
| Zavřeno | — | — | červená |

Detaily v [vet/rozpis/README.md](vet/rozpis/README.md).
