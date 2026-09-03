# Nasazení přes Docker

Repozitář obsahuje hotovou sestavu. Složka `modules/` je namountovaná jako
addons, takže se moduly nikam nekopírují — stačí je mít v repozitáři.

---

## A) Nová instalace na čistém stroji

```bash
git clone https://github.com/goatrental/Elite.vet.git
cd Elite.vet
docker compose up -d
```

Odoo naběhne na `http://localhost:8069`, založí se databáze a v seznamu
aplikací je **Rozpis služeb**.

Instalace modulu z příkazové řádky:

```bash
docker compose exec odoo odoo -d NAZEV_DATABAZE -i rozpis --stop-after-init
docker compose restart odoo
```

> Před ostrým provozem změňte `admin_passwd` v `config/odoo.conf` a hesla
> databáze v `docker-compose.yml`.

---

## B) Nasazení do už běžícího Odoo v Dockeru

### Krok 0 — smazat stávající ruční stránku

**Nepřeskakovat.** Stránka `/rozpis-lekaru` je teď v databázi vložená ručně.
Kdyby tam zůstala, modul narazí na stejnou URL a instalace spadne.

Web → Stránky → `/rozpis-lekaru` → smazat.

Na téhle stránce nejsou žádné překlady, takže se smazáním nic neztratí.

### Krok 1 — zjistit addons path

```bash
docker compose exec odoo cat /etc/odoo/odoo.conf | grep addons_path
```

Odpovídající složku na hostiteli najdete v `docker-compose.yml` v sekci
`volumes`, typicky `./addons:/mnt/extra-addons`.

### Krok 2 — naklonovat repozitář do addons složky

```bash
cd /cesta/k/addons
git clone https://github.com/goatrental/Elite.vet.git elitevet
```

Vznikne `/cesta/k/addons/elitevet/modules/rozpis/`. Do `addons_path` se pak
přidá cesta k `modules`:

```ini
addons_path = /mnt/extra-addons/elitevet/modules,/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
```

Aktualizace později:

```bash
cd /cesta/k/addons/elitevet
git pull
```

### Krok 3 — práva

Odoo v oficiálním image běží pod UID 101. Pokud se modul v seznamu aplikací
neobjeví, bývá to právy:

```bash
sudo chown -R 101:101 /cesta/k/addons/elitevet
```

### Krok 4 — instalace

```bash
docker compose restart odoo
docker compose exec odoo odoo -d NAZEV_DATABAZE -i rozpis --stop-after-init
docker compose restart odoo
```

Aktualizace po změně kódu — místo `-i` použít `-u`:

```bash
docker compose exec odoo odoo -d NAZEV_DATABAZE -u rozpis --stop-after-init
docker compose restart odoo
```

Nebo přes rozhraní: zapnout vývojářský režim → Aplikace → **Aktualizovat
seznam aplikací** → hledat `Rozpis` → Instalovat.

### Krok 5 — kontrola

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://elite-vet.cz/rozpis-lekaru
```

Očekávaná odpověď `200`. Stránka je publikovaná rovnou modulem.

Mřížka bude po instalaci prázdná — naplní se v Odoo v aplikaci
**Rozpis služeb**.

---

## Když se modul neobjeví v seznamu

| příznak | příčina |
|---|---|
| není v Aplikacích ani po *Aktualizovat seznam aplikací* | složka `modules` není v `addons_path` |
| v logu `Skipped unreadable module` | práva, viz krok 3 |
| instalace spadne na duplicitní URL | nesmazaná ruční stránka `/rozpis-lekaru`, viz krok 0 |
| aplikace je vidět, ale stránka hlásí 404 | modul nainstalovaný, ale web není publikovaný — Web → Stránky |

Log kontejneru:

```bash
docker compose logs -f --tail=100 odoo
```
