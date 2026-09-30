# FastAPI/PostgreSQL-PoC

Lokaler vertikaler Schnitt für den Arbeitsgraphen. Keine Authentifizierung, kein
Frontend und keine Connectoren. Tabellen und UUIDs sind vorläufig; siehe [Umfang](../docs/poc.md).

## Start

Voraussetzungen: Python 3.12, uv 0.12.18, Docker mit Compose und freier Port 5432.
Alle Befehle in `backend/` ausführen:

```sh
uv sync --locked --python 3.12
docker compose up -d --wait
export DATABASE_URL='postgresql://imp:imp-local-poc@127.0.0.1:5432/imp'
uv run --locked python -m imp_api.db
uv run --locked uvicorn imp_api.main:app --host 127.0.0.1 --port 8000
```

Schema-Initialisierung einmalig für eine leere Datenbank. Wiederholung auf bestehenden
Tabellen schlägt bewusst fehl. Sie ersetzt keine Migrationen und erfolgt nicht beim API-Start.
Unter PowerShell statt `export`: `$env:DATABASE_URL = 'postgresql://...'`.

OpenAPI/Swagger: <http://127.0.0.1:8000/docs>. PostgreSQL und API sind nur lokal
gebunden. Compose-Zugangsdaten gelten ausschließlich für diesen lokalen PoC.
`DATABASE_URL` und Nutzdaten werden nicht ins Repository geschrieben.

```sh
curl -f http://127.0.0.1:8000/health
curl -f http://127.0.0.1:8000/nodes \
  -H 'Content-Type: application/json' \
  -d '{"kind":"item","title":"Ersten nächsten Schritt erfassen"}'
curl -f http://127.0.0.1:8000/nodes
```

## API-Schnitt

| Endpoint | Verhalten |
| --- | --- |
| `POST /nodes` | Item oder Kontextknoten mit stabiler UUID anlegen |
| `GET /nodes?kind=tag` | Knoten lesen; optional nach Art filtern |
| `GET /nodes/{id}` | Einzelnen Knoten lesen |
| `PATCH /nodes/{id}` | Titel umbenennen; ID und Kanten bleiben erhalten |
| `POST /edges` | Beziehung mit `source_id`, `target_id`, `relation` |
| `GET /edges?node_id={id}` | Eingehende und ausgehende Beziehungen lesen |
| `POST /nodes/{id}/sources` | Verweis mit `system`, `external_ref`, `url` speichern |
| `GET /nodes/{id}/sources` | Externe Verweise lesen |
| `GET /health` | Datenbankverbindung prüfen |

Knotenarten: `item`, `organisation`, `function`, `topic`, `tag`.
Item-Typen, Termine und Status gehören zum fachlichen Entwurf, sind aber noch nicht
Teil dieses technischen Schemas. Relationen sind vorläufig freie, nicht leere Namen.
Fachliche Endpunkt-/Zyklenregeln bleiben offen. Fehlende Endpunkte liefern 404,
Duplikate 409, ungültige Eingaben 422. Listen sind auf 100 Einträge begrenzt
(`limit` bis 500); Pagination ist noch nicht umgesetzt.
Source-URLs werden nur gespeichert; es erfolgt kein Aufruf externer Systeme.

## Reproduzierbare Prüfung

Mit laufender Compose-Datenbank:

```sh
export TEST_DATABASE_URL='postgresql://imp:imp-local-poc@127.0.0.1:5432/imp'
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest -q
```

Tests benötigen PostgreSQL und die Berechtigung, Schemas anzulegen. Jeder Test
legt ein eigenes zufälliges Schema an und entfernt es anschließend. Bestehende
Anwendungstabellen werden nicht geleert. Nur eine lokale/Test-Datenbank nutzen.
Ohne `TEST_DATABASE_URL` scheitern die Integrationstests statt zu überspringen.

GitHub Actions prüft dieselben Tests mit PostgreSQL 17 und dem Python-Lockfile.
PostgreSQL `17` ist ein beweglicher Patch-Tag; der Container ist nicht per Digest fixiert.
Ein grüner CI-Lauf bestätigt keinen produktiven Betrieb.

Lokal am 30.09.2026: sechs Tests gegen PostgreSQL 16.2 bestanden, Ruff bestanden.
Compose/PostgreSQL 17 und GitHub Actions wurden dabei noch nicht ausgeführt.
Der TestClient meldet eine upstream Deprecation-Warnung zur httpx-Anbindung;
die sechs Tests laufen durch.

## Stoppen

`docker compose down` stoppt PostgreSQL und behält das Datenvolume.
Das Volume ist kein Backup. Kein automatisches Löschen oder Zurücksetzen von Daten.
