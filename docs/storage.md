# Storage und Berechtigungen

## 1. Keine zentrale Datenbank

IMP soll zunächst ohne zentrale Datenbank funktionieren.

Daten liegen als Markdown/YAML in Git-Repositories.

Vorteile:

- menschenlesbar
- diffbar
- versioniert
- offline nutzbar
- mit einfachen Unix-Werkzeugen bearbeitbar
- gut für Agenten und Code-Assistenten zugänglich
- keine zusätzliche Datenbankadministration

## 2. Mehrere Data-Repositories

IMP unterscheidet zwischen Anwendung und Daten.

Beispiel:

```text
imp                 # Anwendung, Schema, CLI, Views

imp-data-private    # nur persönlich
imp-data-fkm-it     # Zusammenarbeit IT
imp-data-fkm-hr     # kleiner Berechtigtenkreis
imp-data-fkm-strat  # Strategie / GF
imp-data-bloecher   # Giesserei
imp-data-family     # Familie
```

Die konkrete Aufteilung ist nicht vorgeschrieben.

## 3. Repo-Grenze als Vertrauensraum

Ein Data-Repo bildet primär einen **Berechtigungs- und Kollaborationsraum**.

Damit entscheidet nicht die Fachhierarchie über das Repository, sondern:

- wer darf lesen?
- wer darf schreiben?
- mit wem wird gemeinsam gearbeitet?
- welche Inhalte dürfen gemeinsam versioniert werden?

Organisation, Rolle und Bereich bleiben trotzdem Metadaten auf Item-Ebene.

## 4. Eindeutiger Owner eines Items

Ein Item hat genau **ein führendes Data-Repository**.

Dasselbe fachliche Item wird nicht in mehreren Repositories dupliziert.

Andere Repositories referenzieren es lediglich.

Beispiel:

```yaml
links:
  - type: imp
    repo: imp-data-fkm-it
    id: FKM-IT-0042
```

Damit werden Synchronisationskonflikte vermieden.

## 5. Verschieben zwischen Repositories

Das Verschieben muss ein expliziter Anwendungsfall sein.

Beispiel:

```text
private Idee
    |
    v
offizieller FKM-IT-Vorgang
```

Dabei sollen erhalten bleiben:

- stabile Identität oder nachvollziehbare Alias-Beziehung
- Historie soweit sinnvoll
- Links aus anderen Items
- Herkunft

Offen ist, ob die globale ID beim Repo-Wechsel unverändert bleibt oder über Alias/Redirect abgebildet wird.

## 6. Persönliche Aggregation

Die persönliche IMP-Instanz darf mehrere Data-Repositories lesen und daraus lokale Views erzeugen.

```text
imp-data-private ----\
imp-data-fkm-it ------+
imp-data-bloecher ----+--> persönlicher Index / Views
imp-data-family ------+
externe Systeme -----/
```

Der aggregierte Index ist **abgeleitet** und kann jederzeit neu aufgebaut werden.

Er ist nicht Source of Truth.

## 7. Schreibmodell

Für den PoC gelten einfache Git-Semantiken:

- Änderungen an Items sind normale Commits.
- Gemeinsame Data-Repositories können Branch/PR-Workflows verwenden.
- Persönliche Repositories können direkt geschrieben werden.
- Konflikte werden über Git sichtbar statt durch versteckte Last-write-wins-Logik.

## 8. Spätere Optionen

Ohne Änderung am Grundmodell können später ergänzt werden:

- lokaler Suchindex
- SQLite als Cache, nicht als Source of Truth
- Web-UI
- REST/API
- Hintergrund-Synchronisation
- Connectoren für Jira, Outlook, Teams
- Volltext- oder semantische Suche
- Agenten, die Items klassifizieren, zerlegen oder konsolidieren
