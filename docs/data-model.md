# Datenmodell

## 1. Grundprinzip: Arbeitsgraph

IMP modelliert Arbeit als **Graph aus Items, Kontextknoten und externen Source Objects**.

Ein Item kann gleichzeitig:

- zu einer oder mehreren Organisationen gehören,
- in mehreren Funktionen bearbeitet werden,
- mehrere Themen betreffen,
- mehrere Tags tragen,
- Teil eines oder mehrerer Vorgänge/Pakete sein,
- andere Items voraussetzen oder referenzieren,
- auf externe Source Objects verweisen.

Parent/Child bleibt möglich, ist aber nur eine spezielle Relation im Graphen.

## 2. Keine globale Source of Truth

IMP unterscheidet zwischen:

1. **nativen IMP-Objekten** – fachlich in IMP geführt,
2. **externen Source Objects** – fachlich in einem anderen System geführt,
3. **IMP Overlays** – persönliche Steuerungsdaten zu nativen oder externen Objekten.

Damit kann PostgreSQL alle Objekte lokal zusammenführen, ohne externe Systeme fachlich zu ersetzen.

## 3. Identität

Jedes IMP-Item erhält eine stabile interne ID.

Zusätzlich kann ein Source Object eine externe Identität besitzen.

Beispiel:

```yaml
imp_id: 7fbb...
source:
  type: github
  external_id: issue:123
  locator: cbloecher/imp
```

Die interne IMP-ID darf nicht von Dateipfad, Titel oder externer ID abhängen.

## 4. Kernobjekte

Mindestens vorgesehen:

```text
items
source_objects
sources
organisations
functions
topics
tags
relations
sprints
sprint_items
```

sowie n:m-Zuordnungen:

```text
item_organisations
item_functions
item_topics
item_tags
```

## 5. Item

Ein Item ist die lokale Arbeitsrepräsentation.

Beispielhafte Felder:

```text
id
title
description
type
state
due_at
review_after
created_at
updated_at
source_object_id?
```

Initiale Typen:

- `idea`
- `action`
- `commitment`
- `process`
- `waiting`
- `reference`

Primärer Bearbeitungsstatus bleibt getrennt von horizontalen Merkmalen wie Delegation, Warten auf Antwort, Wiedervorlage oder Sprint-Zugehörigkeit.

## 6. Source

Eine Source beschreibt ein angebundenes Quellsystem bzw. eine konkrete Quelle.

Beispiele:

- Jira-Instanz
- GitHub-Repository
- Outlook-/Graph-Connector
- YAML-/Git-Repository
- SQL-Datenquelle
- IMP selbst

Mögliche Felder:

```text
id
type
name
config_reference
writable
enabled
last_sync_at
last_success_at
```

Geheimnisse oder Credentials gehören nicht direkt in diese Tabelle, sondern in eine geeignete Secret-/Konfigurationsverwaltung.

## 7. Source Object

Ein Source Object repräsentiert ein Objekt in einer externen Quelle.

Beispielhafte Felder:

```text
id
source_id
external_id
external_url
external_type
source_state
last_seen_at
last_sync_at
source_hash
raw_snapshot?
```

Die Kombination aus `source_id + external_id` muss eindeutig sein.

## 8. Source State / Drift

Mögliche Zustände:

- `active`
- `missing`
- `stale`
- `error`
- `detached`
- `deleted`

Regeln:

- Ein einmal fehlendes Objekt wird nicht sofort gelöscht.
- `missing` darf nur nach erfolgreicher Abfrage der Quelle gesetzt werden.
- Ein Connector-Fehler führt zu `error` oder `stale`, nicht zu `missing`.
- `deleted` setzt eine hinreichend sichere Bestätigung voraus.
- Lokale IMP-Overlays bleiben erhalten, solange sie nicht bewusst entfernt werden.

## 9. IMP Overlay

IMP-eigene Steuerungsdaten werden lokal geführt, auch wenn das Basisobjekt extern ist.

Typische Overlay-Daten:

- Organisation
- Funktion
- Thema
- Tag
- persönliche Priorität
- Sprint-Zugehörigkeit
- Wiedervorlage
- persönliche Notiz
- Delegationsinformation
- lokale Beziehungen

Damit kann z. B. ein Jira-Ticket fachlich in Jira geführt werden, während IMP zusätzliche persönliche Metadaten ergänzt.

## 10. Kontextknoten

### Organisation

Beispiele:

- FKM
- Giesserei Blöcher
- Familie
- Selbst

### Funktion

Beispiele:

- GF
- IT
- Personal
- Strategie
- Technik
- Privat

### Thema

Relativ stabile fachliche Zuordnung.

### Tag

Freier situativer Marker, aber als referenziertes Lookup-Objekt mit stabiler ID.

Tags können damit zentral umbenannt werden, ohne alle Items ändern zu müssen.

Alle vier Dimensionen sind n:m.

## 11. Relationen

Relationen werden explizit modelliert.

Beispiele:

- `part_of`
- `depends_on`
- `related`
- `blocks`
- `follows`
- `derived_from`

Ein Vorgang/Paket ist selbst ein Item bzw. Graphknoten.

## 12. Tages-/Sprint-Auswahl

Ein Sprint ist eine gespeicherte Auswahl von Items.

Beispielhafte Felder:

```text
sprints:
  id
  owner_person_id
  date
  state

sprint_items:
  sprint_id
  item_id
  position
  kind   # focus | optional
```

Nicht ausgewählte Items bleiben im Pool erhalten.

## 13. Synchronisation

Jeder Source Adapter normalisiert externe Objekte auf ein gemeinsames Minimalmodell.

Ein Adapter sollte konzeptionell mindestens unterstützen:

```text
list / scan
get
sync metadata
(optional) create
(optional) update
(optional) delete
```

Schreibfähigkeit ist pro Source ausdrücklich zu deklarieren.

## 14. Reparatur verwaister Einträge

IMP soll mindestens folgende Operationen unterstützen:

- Source erneut prüfen
- External ID / Locator korrigieren
- Source Object auf ein anderes externes Objekt umhängen
- Source-Verknüpfung lösen
- Item als natives IMP-Item weiterführen
- lokalen Eintrag bewusst entfernen

Diese Operationen müssen nachvollziehbar sein und dürfen vorhandene Overlays nicht unbeabsichtigt vernichten.

## 15. PostgreSQL als materialisierter Arbeitsgraph

PostgreSQL ist die zentrale lokale Laufzeitbasis von IMP.

Es speichert:

- native IMP-Objekte,
- Projektionen externer Source Objects,
- Kontextknoten,
- Relationen,
- Overlays,
- Sync-/Drift-Zustände,
- Sprints und Views.

Es ist jedoch **nicht automatisch fachliche Source of Truth aller externen Objekte**.

Eine echte Graphdatenbank ist für den PoC nicht erforderlich.
