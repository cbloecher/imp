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
Jira / Outlook / Teams / Kalender / Git
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
  └─ source       → Jira / Outlook / Git
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

Freie situative Marker.

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

## 9. Bestehende Systeme

```text
Source-Systeme -> Was existiert?
IMP            -> Was ist jetzt relevant?
Kalender       -> Wann wird es getan?
```

IMP ersetzt Jira, Outlook, Teams, Kalender oder Git nicht.

Externe Systeme bleiben Source of Truth und werden referenziert statt vollständig dupliziert.

## 10. Methoden als Bausteine

IMP übernimmt keine Selbstmanagementmethode vollständig.

Nützliche Mechanismen:

- **GTD:** Capture, Next Action, Review
- **Kanban:** Work-in-Progress begrenzen
- **MIT / Ivy Lee:** wenige bewusste Tagesprioritäten
- **Time Blocking:** Ausführung im Kalender
- **Weekly Review:** Pool und Fokus regelmäßig neu bewerten

## 11. Speicherung und Anwendung

PostgreSQL speichert den IMP-eigenen Arbeitsgraphen dauerhaft. FastAPI bildet den
Anwendungskern mit Validierung und transaktionalen Schreibzugriffen. Vue/Bootstrap
ist die bevorzugte Frontend-Richtung; Darstellung und Komponenten bleiben offen.

Externe Systeme bleiben für ihre operativen Daten führend. IMP speichert den
persönlichen Steuerungskontext und Source-Verweise. Das ist kein vollständiger Spiegel.

Connectoren für Jira, Outlook, Teams oder Git sind getrennte Integrationsadapter.
Sie sollen über definierte Anwendungsgrenzen arbeiten und nicht direkt Tabellen verändern.
Der erste PoC enthält keine Connectoren, Synchronisation oder externen Schreibzugriffe.

Markdown/YAML kann später dem Import/Export dienen. Ein Export ist kein Ersatz für
Datenbankbackup und keine zweite gleichberechtigte Schreibquelle.

Authentifizierung, Autorisierung, Berechtigungsräume, Detail-Schema und Graph-Darstellung
sind ausdrücklich offen. Der [erste PoC](poc.md) nimmt sie nicht vorweg.

## 12. Nicht-Ziele

IMP soll zunächst ausdrücklich nicht werden:

- Jira-Ersatz
- Team-Projektmanagement-Suite
- Kalender
- Dokumentenmanagement
- Wissenswiki
- universelle Workflow-Engine
- weitere isolierte To-do-App

Der Wert liegt in der dünnen persönlichen Steuerungs- und Strukturierungsschicht über einem heterogenen Arbeitsvorrat.
