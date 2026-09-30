# Erster PoC: Arbeitsgraph über FastAPI und PostgreSQL

## Entscheidung und Ziel

PostgreSQL ist die führende Datenbasis für IMP-eigene Inhalte, FastAPI das Backend.
Vue/Bootstrap ist die bevorzugte Frontend-Richtung. Der erste Schnitt prüft nur,
ob Erfassen und Verknüpfen über eine API dauerhaft in PostgreSQL funktionieren.
Die vorhandenen fachlichen Konzepte bleiben erhalten; die Tabellen sind vorläufig.

## Enthalten

- Einträge mit Titel, optionalem Markdown-Text und stabiler UUID erfassen und lesen
- Kontextknoten für Organisation, Funktion, Thema und Tag erfassen
- Mehrere Kontexte pro Item und mehrere Items pro Kontext verknüpfen
- Tags umbenennen, ohne deren Identität und Zuordnungen zu ändern
- `part_of` und andere gerichtete Item- sowie Kontextbeziehungen speichern
- Externe Source-of-Truth-Verweise speichern, ohne operative Daten zu kopieren
- PostgreSQL-Transaktionen, Fremdschlüssel, Validierung und Duplikatschutz prüfen
- Startanleitung, Python-Lockfile und PostgreSQL-basierte CI-Prüfung bereitstellen

## Abnahme

1. Ein API-erfasstes Item ist über einen neuen Client/DB-Zugriff lesbar.
2. Zwei Items teilen einen Tag; ein Item besitzt gleichzeitig mehrere Kontexte.
3. Umbenennen des Tags lässt IDs und Beziehungen unverändert.
4. Item- und Kontextbeziehungen sind über beide Endpunkte abrufbar.
5. Fehlende Endpunkte und doppelte Kanten werden abgewiesen; danach sind weitere Writes möglich.
6. Ein Jira-Verweis wird gespeichert und zurückgelesen; Jira wird nicht aufgerufen.

Tests stehen in `backend/tests/test_api.py`, Anleitung in [backend/README.md](../backend/README.md).
Die Persistenzprüfung bestätigt Commits über getrennte Verbindungen, noch keinen
Backup/Restore oder Server-Neustart.

## Ausdrücklich offen

| Entscheidung | Noch zu klären |
| --- | --- |
| Authentifizierung | Keycloak/AD oder anderer Ansatz; Login-/Tokenfluss |
| Autorisierung | Persönliche/geteilte Räume, Rollen, Mandanten, Beziehungen über Grenzen |
| Graph-Darstellung | Baum-/Graph-/Listenansichten und Vue-Komponenten; keine Bibliothek festgelegt |
| Detail-Schema | Typen, Status, Termine, Quellen, n:m-Tabellen, Kantenregeln, IDs und Historie |
| Schemaentwicklung | Migrationstool und Upgrade-/Rollback-Verfahren |
| Betrieb | Deployment, Backup/Restore, Secrets, Mehrbenutzer-Konkurrenz |
| Frontend | Vue/Bootstrap ist Richtung, keine endgültige Komponenten-/Versionswahl |

UUIDs, generische Knoten/Kanten, psycopg und ein explizites initiales SQL-Skript sind
reversible PoC-Implementierungsentscheidungen. Sie legen das Zielschema nicht fest.

## Ausbaugrenze

Der PoC implementiert noch keine Inbox-Klärung, Verbindlichkeitsgrade, Sprint-Auswahl,
Priorisierung, Synchronisation, Agenten, Import/Export oder UI. Diese bleiben
fachliche Ziele, aber sind keine Voraussetzung für diesen Persistenztest.

Integrationen sollen als getrennte Adapter über definierte Anwendungsgrenzen
hinzukommen. Ein Connector darf keine direkte zweite Schreibquelle in PostgreSQL
werden. Externe operative Daten bleiben in ihren jeweiligen Source-Systemen.
