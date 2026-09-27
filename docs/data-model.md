# Datenmodell

## 1. Grundprinzip

Ein fachliches Objekt wird als **Item** modelliert.

Ein Item liegt primär als Markdown-Datei mit YAML-Frontmatter vor. Die Datei ist zugleich menschenlesbare Dokumentation und maschinenlesbare Datenquelle.

Ordner sind nur eine grobe Ablagestruktur. Fachliche Zuordnungen werden über Metadaten modelliert.

## 2. Identität

Jedes Item benötigt eine **stabile ID**.

Der Dateiname bzw. Slug darf sich ändern, ohne Referenzen zu brechen.

Beispiel:

```yaml
id: FKM-IT-0042
slug: ai-infrastruktur-produktionsreif
```

Das endgültige ID-Schema über mehrere Data-Repositories hinweg ist noch festzulegen.

Anforderungen:

- stabil
- eindeutig
- kurz genug für manuelle Referenzen
- unabhängig vom Dateipfad
- maschinell validierbar

## 3. Minimales Schema

```yaml
---
id: FKM-IT-0042
slug: ai-infrastruktur-produktionsreif
title: AI-Infrastruktur produktionsreif machen

type: process
status: active

organisations:
  - fkm

roles:
  - it
  - strategy

areas:
  - ai
  - infrastructure
  - security

parent:
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

Die Typen sollen klein bleiben. Zusätzliche Differenzierung erfolgt bevorzugt über Metadaten statt über viele Spezialtypen.

## 5. Beziehungen

### Parent / Child

Für Zerlegung:

```yaml
parent: FKM-IT-0042
```

Die kanonische Beziehung sollte möglichst nur auf **einer Seite** gepflegt werden und die Gegenseite daraus berechnet werden.

Empfehlung für den PoC: `parent` ist kanonisch; `children` wird bei Bedarf erzeugt.

### Weitere Links

Nicht-hierarchische Beziehungen:

```yaml
links:
  - type: related
    target: FKM-SEC-0011
  - type: external
    system: jira
    ref: IDP-471
```

## 6. Organisationen, Rollen und Bereiche

Alle drei Dimensionen sind Listen.

```yaml
organisations:
  - fkm

roles:
  - it
  - strategy

areas:
  - ai
  - infrastructure
  - security
```

Dadurch kann dasselbe Item mehreren fachlichen oder funktionalen Kontexten angehören.

Eine spätere Registry kann erlaubte Codes und deren Anzeigenamen definieren.

## 7. Termine

Ein Fälligkeitsdatum darf nur verwendet werden, wenn tatsächlich eine zeitliche Verbindlichkeit besteht.

```yaml
due: 2026-10-02
```

Ideen oder bloße Wiedervorlagen sollen nicht durch künstliche Deadlines zu Commitments werden.

Für Wiedervorlage sollte deshalb ein eigenes Feld verwendet werden:

```yaml
review_after: 2026-11-01
```

## 8. Source of Truth

Externe operative Systeme bleiben führend.

```yaml
source:
  system: jira
  ref: IDP-471
  url: https://...
```

IMP speichert nur die Informationen, die für persönliche Steuerung notwendig sind.

## 9. Markdown-Body

Der Body darf frei lesbar bleiben.

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

Die Marker sind **kein Ersatz für strukturierte YAML-Metadaten**. Sie dienen für gezielt pflegbare Body-Sektionen.

## 10. Dateien statt Ordner pro Item

Standardfall:

```text
items/fkm/ai-infrastruktur-produktionsreif.md
```

Ein eigener Ordner pro Item ist nur nötig, wenn das Item weitere lokale Artefakte benötigt.

So bleibt der Dateibaum flach und gut mit Git, grep und einfachen CLI-Werkzeugen nutzbar.
