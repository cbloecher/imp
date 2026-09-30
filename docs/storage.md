# Storage und Berechtigungen

## 1. PostgreSQL als führende IMP-Datenbasis

Der PoC startet mit PostgreSQL und FastAPI. IMP-eigene Items, Kontextknoten,
Zuordnungen, Beziehungen und Source-Verweise liegen dauerhaft in PostgreSQL.
Die Datenbank ist kein rekonstruierbarer Index hinter Markdown/YAML.

Externe Systeme bleiben Source of Truth für ihre operativen Inhalte. IMP ist
führend nur für den eigenen persönlichen Steuerungskontext.

## 2. Anwendung, Daten und Integrationen

Das Repository `imp` enthält Anwendungscode, Schemaentwürfe und Dokumentation.
Laufende Nutzdaten und Zugangsdaten gehören nicht ins Code-Repository.
FastAPI kapselt Datenzugriff und Anwendungsregeln. Integrationen werden als
separate Adapter entwickelt; der erste PoC enthält keine Integrationen.
Vue/Bootstrap ist die bevorzugte, noch nicht implementierte Frontend-Richtung.

## 3. Berechtigungsräume bleiben offen

Die bisherige Data-Repo-Grenze wird nicht als Datenbank-Berechtigungsmodell übernommen.
Organisation, Funktion, Thema und Tag bleiben fachliche n:m-Zuordnungen und sind
nicht automatisch Zugriffsrechte.

Offen sind Authentifizierung (z. B. Keycloak/AD), Autorisierung, persönliche und
geteilte Räume, Mandanten sowie Sichtbarkeit von Beziehungen über Raumgrenzen.
Der PoC ist ein lokaler Einzelbenutzertest ohne Authentifizierung und wird nur
an Loopback gebunden. Er darf nicht mit vertraulichen Produktionsdaten betrieben werden.

## 4. Identität und Schreibmodell

Knoten behalten eine stabile technische Identität beim Umbenennen. Der PoC nutzt UUIDs.
Schreibzugriffe erfolgen über FastAPI in PostgreSQL-Transaktionen. Fremdschlüssel
verhindern Beziehungen zu nicht existierenden Knoten; doppelte identische Kanten
werden zurückgewiesen. Konkurrenzregeln, Audit und Versionskontrolle sind offen.

Ein Item hat eine führende IMP-Identität und wird über Beziehungen mehrfach zugeordnet,
nicht pro Kontext dupliziert. Wechsel von Berechtigungsräumen ist erst nach deren
Definition zu spezifizieren; ein Git-Repo-Wechsel ist kein aktuelles Schreibmodell.

## 5. Sicherung, Austausch und Wiederherstellung

Die führende Datenbank erfordert Backups und geprüfte Wiederherstellung.
Der PoC nutzt ein persistentes Docker-Volume; es ist kein Backup.
Backup-/Restore-Prozess, Aufbewahrung und Betrieb sind vor einem produktiven Einsatz zu klären.

Markdown/YAML-Import und -Export sind spätere Optionen. Exportdateien sind keine
parallele Schreibquelle. Ein möglicher Suchindex bleibt abgeleitet; die PostgreSQL-
Primärdaten lassen sich nicht allein aus dem Anwendungscode rekonstruieren.

## 6. PoC und Ausbaugrenze

[PoC-Umfang](poc.md) und [Start-/Testanleitung](../backend/README.md) beschreiben den
kleinen vertikalen Schnitt. Migrationen, Frontend, Rechteverwaltung, Synchronisation,
Volltextsuche und Agentenunterstützung folgen erst nach gesonderter Entscheidung.
