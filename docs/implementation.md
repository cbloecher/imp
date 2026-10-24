# Umsetzung

## Referenzstack

Der erste PoC wird direkt mit dem vorgesehenen Zielstack umgesetzt:

- Vue 3 + TypeScript
- Bootstrap 5
- FastAPI
- SQLAlchemy 2
- Alembic
- PostgreSQL 17
- Docker Compose

## Lokaler Start

```bash
cp .env.example .env
docker compose up --build
```

Danach:

- Frontend: http://localhost:5173
- FastAPI/OpenAPI: http://localhost:8000/docs
- Healthcheck: http://localhost:8000/health

## Erster Vertical Slice

Der erste Slice bildet den Schmierzettel-Workflow ab:

1. Item über eine einzelne Texteingabe erfassen.
2. Ungeordnete Items landen in `Inbox / ungeordnet`.
3. Navigation über `Ich → Organisation → Funktion → Thema`.
4. Klick auf einen Knoten filtert die Item-Liste.
5. Klick auf ein Item öffnet die Detailansicht.
6. Dort können Typ, Bearbeitungsstatus, Organisation, Funktion, Thema und Tags gepflegt werden.
7. Horizontale Arbeitsmerkmale: Delegation, Warten auf, Wiedervorlage.
8. Item kann in den aktuellen persönlichen Sprint aufgenommen werden.
9. Tags sind Lookup-Objekte und zentral umbenennbar.

Der Baum ist eine Projektion des Arbeitsgraphen, nicht die Datenstruktur selbst.

## Föderierte Quellen

Das Datenbankschema enthält bereits `sources` und `source_objects`.

Externe Connectoren sind im ersten Slice noch nicht implementiert. Der erwartete Fluss ist:

```text
Quelle → Adapter → Source Object → IMP Item + Overlay → UI
```

Damit kann der PoC zunächst mit nativen IMP-Items arbeiten, ohne später die Architektur für GitHub, YAML, SQL, Jira oder Outlook umzubauen.

## Nächste Schritte

- Kontextknoten unabhängig von vorhandenen Items miteinander verbinden
- Drag & Drop vom Item auf Baumknoten
- Vorgänge/Pakete und Item-Relationen in der UI
- Sprint-Reihenfolge und Fokus/Optional
- Source-Adapter-Interface
- erster Adapter: YAML/JSON oder GitHub
- Authentifizierung über Keycloak/OIDC
- Tests und CI
