# Konzept

## 1. IMP als persönliche Steuerungsebene

IMP ist zuerst der **digitale Ersatz für den klassischen Schmierzettel** – mit der Fähigkeit, Einträge später zu ordnen, zu filtern, zu bündeln und zu priorisieren.

IMP liegt über bestehenden operativen Systemen.

```text
schnell erfassen
      ↓
   Arbeitsgraph
      ↓
ordnen / filtern / bündeln
      ↓
Tages- oder Sprint-Auswahl
      ↓
bei Bedarf Übergabe/Verweis
      ↓
Jira / Outlook / Teams / Kalender / GitHub / SQL / YAML
```

Die operative Arbeit bleibt dort, wo sie hingehört. IMP bildet die persönliche Steuerungsebene.

## 2. Der digitale Schreibtischzettel

Die Stärke des Papierzettels bleibt erhalten: extrem niedrige Erfassungshürde.

Eine Inbox darf zunächst heterogen sein.

Beim Review wird ein Eintrag geklärt:

```text
Inbox
  |
  +--> Idee
  +--> Next Action
  +--> Commitment
  +--> Warten auf
  +--> externer Verweis
  +--> Vorgang / Paket
  +--> weiter ungeklärt
```

Nichts muss verschwinden, nur weil es heute nicht bearbeitet wird.

## 3. Pool statt ewiger Tagesliste

IMP trennt drei Ebenen:

```text
INBOX
neu und ungeklärt

POOL
alles weiterhin Relevante
├─ Ideen
├─ offene Actions
├─ Vorgänge
├─ Warten auf
└─ Commitments

SPRINT
bewusste Auswahl für heute / den nächsten Arbeitstag
```

Nicht erledigte Items bleiben im Pool. Sie werden nicht automatisch als Altlasten auf jede neue Tagesliste kopiert.

## 4. Ideenmanagement und Arbeitsmanagement

IMP ist beides:

1. persönliches Arbeitsmanagement
2. Ideen-/Opportunity-Management

Eine Idee ist keine schwache Aufgabe.

```text
Idee
  ↓
konkretisieren
  ↓
mit anderen Items bündeln
  ↓
Vorgang / Paket
  ↓
Action / Commitment
```

Sie darf aber ebenso dauerhaft Idee bleiben.

## 5. Arbeitsgraph

IMP modelliert seine Inhalte als Graph.

```text
[Item]
  ├─ Organisation → FKM
  ├─ Funktion     → IT
  ├─ Thema        → KI
  ├─ Tag          → mit-ds-besprechen
  ├─ part_of      → AI-Infrastruktur
  ├─ depends_on   → anderes Item
  └─ source       → Jira / Outlook / GitHub / SQL / YAML
```

Eine Baumstruktur ist lediglich eine mögliche Sicht auf diesen Graphen.

## 6. Kontextdimensionen

### Organisation

Wo gehört das Thema organisatorisch hin?

Beispiele:

- FKM
- Giesserei Blöcher
- Familie
- Selbst

### Funktion

In welcher Funktion wird daran gearbeitet?

Beispiele:

- GF
- IT
- Personal
- Strategie
- Technik
- Privat

### Thema

Worum geht es fachlich?

Beispiele:

- KI
- Infrastruktur
- VPN
- Website
- idPlan
- Personal

Themen sind relativ stabil und gepflegt.

### Tags

Freie situative Marker, die dennoch als Lookup-Objekte mit stabiler ID geführt werden.

Beispiele:

- mit-ds-besprechen
- kurz
- lesen
- delegierbar
- später

Alle Dimensionen sind n:m.

## 7. Zerlegen und Pakete schnüren

IMP strukturiert in beide Richtungen.

### Decompose

```text
Vorgang
  -> Teilvorgang
      -> Next Action
      -> Next Action
  -> Commitment
```

### Consolidate

```text
lose Idee
lose Aufgabe
offene Frage
      \
       -> gemeinsamer Vorgang / Paket
```

Das Paket ist selbst ein Knoten im Arbeitsgraphen und kein bloßer Ordner.

## 8. Tagesplanung als persönlicher Sprint

Abends oder morgens wird aus dem Pool bewusst der nächste Sprint zusammengestellt.

Dabei sollen sichtbar sein:

- harte Commitments und Termine,
- offene Vorgänge ohne Next Action,
- Wiedervorlagen,
- aktuelle Fokusthemen,
- bewusst ausgewählte Ideen oder kleine Actions.

Der Sprint bleibt klein. Nicht ausgewählte Items bleiben erhalten.

```text
Arbeitsgraph / Pool
        ↓
Review
        ↓
1–3 Hauptthemen
+ wenige weitere Actions
        ↓
nächster Sprint
```

## 9. Föderierte Quellen statt einer globalen Wahrheit

IMP erzwingt **keine einzige Source of Truth für alle Objekte**.

Stattdessen bleibt die jeweilige Ursprungquelle fachlich führend:

```text
Jira-Ticket       -> Jira
Outlook-Termin    -> Outlook / Kalender
GitHub-Issue      -> GitHub
YAML-Item         -> Data-Repository
SQL-Datensatz     -> jeweilige SQL-Quelle
natives IMP-Item  -> IMP PostgreSQL
```

IMP führt diese Quellen über Adapter zusammen.

```text
Sources
  ↓
Source Adapter
  ↓
Canonical IMP Model
  ↓
lokaler materialisierter Arbeitsgraph
  ↓
Tree / Filter / Sprint / Suche / Details
```

## 10. Source Object + IMP Overlay

Ein externes Objekt besteht in IMP logisch aus zwei Schichten:

```text
Source Object
      +
IMP Overlay
      =
IMP Item View
```

Beispiel:

```text
Jira:
Titel, Jira-Status, Due Date

IMP ergänzt:
Organisation, Funktion, Thema, Tags,
persönliche Priorität, Sprint,
Wiedervorlage, Notizen
```

Dadurch kann IMP persönliche Steuerungsinformationen ergänzen, ohne das externe System zu duplizieren oder dessen fachliche Autorität zu übernehmen.

## 11. Drift, Löschung und verwaiste Einträge

Quellen können sich ändern, nicht erreichbar sein oder Objekte löschen.

IMP muss dies explizit sichtbar machen.

Mögliche Source-Zustände:

- `active` – Objekt wurde erfolgreich gefunden
- `missing` – Objekt wurde bei erfolgreicher Synchronisation nicht gefunden
- `stale` – Quelle wurde längere Zeit nicht erfolgreich geprüft
- `error` – Quelle konnte nicht gelesen werden
- `detached` – Verbindung wurde bewusst getrennt
- `deleted` – Löschung an der Quelle wurde bestätigt

Ein einmal fehlendes Objekt wird **nicht sofort gelöscht**.

Mögliche Reparaturaktionen:

- Quelle erneut prüfen
- Referenz / External ID korrigieren
- auf ein neues Source Object umhängen
- als natives IMP-Item übernehmen
- lokalen Eintrag bewusst entfernen

Damit können IMP-Overlays, Notizen und Beziehungen erhalten bleiben, auch wenn ein externes Source Object verschwindet.

## 12. Bestehende Systeme

```text
Source-Systeme -> Was existiert?
IMP            -> Was ist jetzt relevant?
Kalender       -> Wann wird es getan?
```

IMP ersetzt Jira, Outlook, Teams, Kalender, GitHub oder andere Quellsysteme nicht.

## 13. Methoden als Bausteine

IMP übernimmt keine Selbstmanagementmethode vollständig.

Nützliche Mechanismen:

- **GTD:** Capture, Next Action, Review
- **Kanban:** Work-in-Progress begrenzen
- **MIT / Ivy Lee:** wenige bewusste Tagesprioritäten
- **Time Blocking:** Ausführung im Kalender
- **Weekly Review:** Pool und Fokus regelmäßig neu bewerten

## 14. Speicherung und Anwendung

PostgreSQL dient als:

- Heimat nativer IMP-Objekte,
- lokaler materialisierter Index externer Quellen,
- Arbeitsgraph für Beziehungen,
- Speicher für IMP-Overlays,
- Basis für Suche, Filter und Views.

```text
Jira ---------\
Outlook -------\
GitHub ---------+--> Adapter / Sync --> PostgreSQL --> FastAPI --> Vue
YAML / Git -----/
SQL ------------/
IMP native -----/
```

PostgreSQL ist damit nicht automatisch fachliche Source of Truth externer Objekte, sondern deren lokale Projektion innerhalb von IMP.

## 15. Nicht-Ziele

IMP soll zunächst ausdrücklich nicht werden:

- Jira-Ersatz
- Team-Projektmanagement-Suite
- Kalender
- Dokumentenmanagement
- Wissenswiki
- universelle Workflow-Engine
- weitere isolierte To-do-App

Der Wert liegt in der persönlichen Steuerungs-, Aggregations- und Strukturierungsschicht über einem heterogenen Arbeitsvorrat.
