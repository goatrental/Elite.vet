# Nasazení modulu `elite_vet_rozpis` do Odoo v Dockeru

Modul je čistě datový (QWeb šablona + záznam stránky + štítek), nemá Python kód
a nepotřebuje žádné build kroky ani další balíčky. Stačí ho dostat do addons
složky, kterou má kontejner namountovanou, a nainstalovat.

---

## Krok 0 — nejdřív smazat stávající ruční stránku

**Tohle nepřeskakovat.** Stránka `/rozpis-lekaru` je teď v databázi vložená ručně.
Kdyby tam zůstala, modul narazí na stejnou URL a instalace spadne.

Web → Stránky → `/rozpis-lekaru` → smazat.

Na téhle stránce nejsou žádné překlady, takže se smazáním nic neztratí.

---

## Krok 1 — zjistit, kam kontejner kouká pro addons

```bash
docker compose exec odoo cat /etc/odoo/odoo.conf | grep addons_path
```

Typicky je to `/mnt/extra-addons`. Odpovídající složku na hostiteli najdete
v `docker-compose.yml` v sekci `volumes`, například:

```yaml
volumes:
  - ./addons:/mnt/extra-addons
```

Tady by hostitelská složka byla `./addons`.

---

## Krok 2 — dostat modul do té složky

### Varianta A — klonovat z gitu (doporučeno, jde snadno aktualizovat)

```bash
cd /cesta/k/addons
git clone https://github.com/goatrental/Elite.vet.git elite_vet_rozpis
```

Vznikne `/cesta/k/addons/elite_vet_rozpis/__manifest__.py`, což je přesně to,
co Odoo potřebuje. Nic se nekopíruje ani nepřesouvá.

> Ten `elite_vet_rozpis` na konci příkazu je povinný. Repozitář se jmenuje
> `Elite.vet`, ale složka modulu se musí jmenovat `elite_vet_rozpis` — název
> složky je pro Odoo zároveň názvem modulu a tečku v něm mít nesmí.

Aktualizace později:

```bash
cd /cesta/k/addons/elite_vet_rozpis
git pull
```

pak `-u elite_vet_rozpis` (viz krok 4).

### Varianta B — rozbalit ZIP

GitHub → **Code → Download ZIP**. Rozbalit a nakopírovat tak, aby vznikla cesta
`/cesta/k/addons/elite_vet_rozpis/__manifest__.py`.

> Pozor na jednu častou chybu: `__manifest__.py` musí ležet **přímo** ve složce
> `elite_vet_rozpis`. Když se rozbalením vytvoří o úroveň víc
> (`elite_vet_rozpis/Elite.vet-main/__manifest__.py`), Odoo modul neuvidí.
> ZIP z GitHubu se rozbalí jako `Elite.vet-main`, je potřeba tu složku
> přejmenovat na `elite_vet_rozpis`.

---

## Krok 3 — práva

Odoo v oficiálním image běží pod uživatelem `odoo` (UID 101). Pokud se modul
v seznamu aplikací neobjeví, bývá to právy:

```bash
sudo chown -R 101:101 /cesta/k/addons/elite_vet_rozpis
```

---

## Krok 4 — instalace

### Z příkazové řádky (spolehlivější než klikání)

```bash
docker compose exec odoo odoo \
    -d NAZEV_DATABAZE \
    -i elite_vet_rozpis \
    --stop-after-init

docker compose restart odoo
```

Aktualizace po změně kódu — stejný příkaz, jen `-i` nahradit za `-u`:

```bash
docker compose exec odoo odoo -d NAZEV_DATABAZE -u elite_vet_rozpis --stop-after-init
docker compose restart odoo
```

### Nebo přes rozhraní

1. `docker compose restart odoo`
2. Zapnout vývojářský režim (Nastavení → dole *Aktivovat vývojářský režim*)
3. Aplikace → **Aktualizovat seznam aplikací**
4. Vymazat filtr *Aplikace*, hledat `Elite Vet` → **Instalovat**

---

## Krok 5 — kontrola

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://elite-vet.cz/rozpis-lekaru
```

Očekávaná odpověď `200`. Stránka je publikovaná rovnou modulem, nic se
nemusí zapínat ručně.

Mřížka bude po instalaci prázdná — naplní se až událostmi v aplikaci
**Kalendář** se štítkem **`Rozpis služeb`**. Postup je v
[`README.md`](README.md).

---

## Když se modul neobjeví v seznamu

| příznak | příčina |
|---|---|
| není v Aplikacích ani po *Aktualizovat seznam aplikací* | složka není v `addons_path`, nebo je o úroveň zanořená navíc |
| v logu `Skipped unreadable module` | práva, viz krok 3 |
| v Aplikacích nic, filtr *Aplikace* aktivní | modul má `application: False`, filtr je potřeba smazat |
| instalace spadne na duplicitní URL | nesmazaná ruční stránka `/rozpis-lekaru`, viz krok 0 |

Log kontejneru:

```bash
docker compose logs -f --tail=100 odoo
```

---

## Ukázkový docker-compose.yml

Pro srovnání, kdyby se addons volume teprve doplňoval. **Existující nasazení
tímhle nepřepisujte**, důležitý je jen řádek s `extra-addons`.

```yaml
services:
  odoo:
    image: odoo:18
    depends_on:
      - db
    ports:
      - "8069:8069"
    volumes:
      - odoo-data:/var/lib/odoo
      - ./addons:/mnt/extra-addons      # sem patri slozka elite_vet_rozpis
      - ./config:/etc/odoo
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    volumes:
      - db-data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  odoo-data:
  db-data:
```

A odpovídající `config/odoo.conf`:

```ini
[options]
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
db_host = db
db_user = odoo
db_password = odoo
```
