# Datenmodell

## 1. Grundprinzip: Arbeitsgraph

IMP modelliert Arbeit nicht primär als Baum, sondern als **Graph aus Items und Kontextknoten**.

Ein Item kann gleichzeitig:

- zu einer oder mehreren Organisationen gehören,
- in mehreren Funktionen/Rollen bearbeitet werden,
- mehrere Themen betreffen,
- freie Tags tragen,
- Teil eines oder mehrerer Vorgänge/Pakete sein,
- andere Items voraussetzen oder referenzieren,
- auf externe Systeme wie Jira, Outlook oder Git verweisen.

Parent/Child bleibt möglich, ist aber nur **eine spezielle Relation** im Graphen.

```text
[Item]
  ├─ organisation → [Organisation]
  ├─ function     → [Funktion]
  ├─ topic        → [Thema]
  ├─ tag          → [Tag]
  ├─ part_of      → [Vorgang/Paket]
  ├─ depends_on   → [Item]
  └─ source       → [Jira/Outlook/Git/...]
```

Die führenden Daten bleiben dateibasiert in Markdown/YAML. Eine Datenbank darf für Suche, Aggregation und Views als **abgeleiteter Index** dienen.

## 2. Identität

Jedes Item benötigt eine stabile ID.

Der Dateiname bzw. Slug darf sich ändern, ohne Referenzen zu brechen.

```yaml
id: FKM-IT-0042
slug: ai-infrastruktur-produktionsreif
```

Anforderungen:

- stabil
- eindeutig
- kurz genug für manuelle Referenzen
- unabhängig vom Dateipfad
- maschinell validierbar

Das endgültige globale ID-Schema über mehrere Data-Repositories hinweg ist noch festzulegen.

## 3. Minimales Item-Schema

```yaml
---
id: FKM-IT-0042
slug: ai-infrastruktur-produktionsreif
title: AI-Infrastruktur produktionsreif machen

type: process
status: active

organisations:
  - fkm

functions:
  - it
  - strategy

topics:
  - ai
  - infrastructure
  - security

tags:
  - review

relations:
  - type: part_of
    target: FKM-AI-0001

due:
review_after:

source:
links: []
---
```

## 4. Item-Typen

Initial vorgesehene Typen:

- `idea` – interessant, aber unverbindlich
- `action` – konkret ausführbarer nächster Schritt
- `commitment` – verbindliche Aufgabe
- `process` – Vorgang / übergeordnetes Thema
- `waiting` – wartet auf externe Person, Ereignis oder System
- `reference` – primär Verweis auf externen Sachverhalt

Die Typen bleiben bewusst klein. Zusätzliche Bedeutung entsteht durch Relationen und Metadaten.

## 5. Kontextknoten

### Organisation

Organisatorischer Kontext, z. B.:

- FKM
- Giesserei Blöcher
- Familie
- Selbst

### Funktion

In welcher Funktion/Rolle wird ein Item bearbeitet?

Beispiele:

- GF
- IT
- Personal
- Strategie
- Technik
- Privat

### Thema

Stabile fachliche Zuordnung.

Beispiele:

- KI
- Infrastruktur
- VPN
- idPlan
- Personal
- Website

Themen sollen gepflegt und wiederverwendet werden.

### Tag

Freier, situativer Marker.

Beispiele:

- mit-ds-besprechen
- kurz
- lesen
- delegierbar
- später

Tags dürfen deutlich lockerer entstehen als Themen.

Alle vier Dimensionen sind **n:m**.

## 6. Relationen zwischen Items

Hierarchische und nicht-hierarchische Beziehungen werden einheitlich als Relationen gedacht.

Beispiele:

```yaml
relations:
  - type: part_of
    target: FKM-AI-0001

  - type: depends_on
    target: FKM-SEC-0011

  - type: related
    target: FKM-IT-0038
```

Mögliche Relationstypen:

- `part_of`
- `depends_on`
- `related`
- `blocks`
- `follows`
- `derived_from`

Für einfache Zerlegung kann `parent` zunächst als Kurzform von `part_of` unterstützt werden. Langfristig soll die Relation das kanonische Modell bilden.

## 7. Graph auch zwischen Kontextknoten

Nicht nur Items können miteinander verbunden sein. Auch Kontextknoten dürfen Beziehungen besitzen.

Beispiel:

```text
[FKM]
  └─ function → [IT]
                  └─ topic → [Infrastruktur]
                                ├─ topic → [VPN]
                                └─ topic → [KI]
```

Diese Beziehungen dienen Navigation, Vorschlägen und Filterung. Sie erzwingen keine Exklusivität: Das Thema `KI` kann gleichzeitig in mehreren Organisationen oder Funktionen relevant sein.

## 8. Pakete und Vorgänge

Ein Paket/Vorgang ist kein Ordnerzwang, sondern selbst ein Item bzw. Knoten im Arbeitsgraphen.

Lose Items können später zusammengeführt werden:

```text
[VPN-Doku] ───────┐
[Kamera Serverraum] ├─ part_of → [IT-Infrastruktur verbessern]
[DNS-Doku] ───────┘
```

Ebenso kann ein Vorgang in Teilvorgänge und Actions zerlegt werden.

Damit unterstützt IMP beide Richtungen:

- **Decompose** – Vorgang in ausführbare Schritte zerlegen
- **Consolidate** – lose Gedanken/Aufgaben zu einem Vorgang bündeln

## 9. Tages-/Sprint-Auswahl als View

Der nächste persönliche Sprint ist **kein eigener Datensilo**.

Er ist eine bewusste Auswahl von Items aus dem Arbeitsgraphen.

Beispiel:

```yaml
sprint:
  date: 2026-09-28
  focus:
    - FKM-IT-0042
    - FKM-HR-0017
  optional:
    - SELF-0011
```

Nicht gewählte Items bleiben im Pool erhalten und werden lediglich aus der aktuellen Tagesansicht ausgeblendet.

## 10. Termine und Wiedervorlage

Ein Fälligkeitsdatum wird nur verwendet, wenn tatsächlich eine zeitliche Verbindlichkeit besteht.

```yaml
due: 2026-10-02
```

Ideen oder unverbindliche Punkte erhalten keine künstlichen Deadlines.

Für Wiedervorlage:

```yaml
review_after: 2026-11-01
```

## 11. Source of Truth

Externe operative Systeme bleiben führend.

```yaml
source:
  system: jira
  ref: IDP-471
  url: https://...
```

IMP speichert nur die Informationen, die für persönliche Steuerung notwendig sind.

## 12. Dateiformat und Markdown-Body

Ein Item liegt primär als Markdown-Datei mit YAML-Frontmatter vor.

Für maschinell gepflegte Abschnitte werden stabile Marker vorgesehen:

```md
# AI-Infrastruktur produktionsreif machen

## Kontext

Freier Text.

<!-- IMP:BEGIN next -->
- Traefik prüfen
- Monitoring vervollständigen
<!-- IMP:END next -->

## Notizen

Freier Text.
```

Damit können einfache Werkzeuge per `sed`, `awk`, Python oder Agent Inhalte gezielt zwischen Markern ändern.

## 13. Dateien statt Ordner pro Item

Standardfall:

```text
items/ai-infrastruktur-produktionsreif.md
```

Ein eigener Ordner pro Item ist nur nötig, wenn lokale Artefakte dazugehören.

Fachliche Struktur wird durch den Graphen erzeugt, nicht durch den Dateipfad.

## 14. Datenbank als abgeleiteter Index

Eine interne IMP-Anwendung darf den Arbeitsgraphen in SQLite oder PostgreSQL materialisieren.

Beispiel:

```text
items
organisations
functions
topics
tags
relations

item_organisations
item_functions
item_topics
item_tags
```

Die Datenbank dient:

- Filterung
- Volltextsuche
- Graph-Navigation
- Aggregation mehrerer Data-Repositories
- Tages-/Sprint-Views
- berechneten Hinweisen

Sie ist zunächst **nicht Source of Truth**. Der Index muss aus den Data-Repositories neu aufgebaut werden können.

Eine echte Graphdatenbank ist für den PoC nicht erforderlich.
