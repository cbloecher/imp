# Beispiele

Die Beispiele zeigen bewusst unterschiedliche Verbindlichkeitsgrade und Beziehungen.
YAML ist hier eine fachliche Illustration, keine führende Speicherung und kein
PoC-API-Vertrag. PostgreSQL speichert IMP-eigene Daten.

## Idee

```yaml
---
id: EX-0001
slug: gitdiagram-fuer-idplan
title: GitDiagram für idPlan prüfen
type: idea
status: open

organisations: [fkm]
functions: [strategy]
topics: [digitalisation, software-modernisation]

due:
review_after: 2026-10-15
---
```

Noch keine Verpflichtung. Beim Review kann daraus ein Vorgang oder eine Action werden.

## Next Action

```yaml
---
id: EX-0002
slug: traefik-konfiguration-pruefen
title: Traefik-Konfiguration des AI-Gatekeepers prüfen
type: action
status: active

organisations: [fkm]
functions: [it]
topics: [ai, infrastructure, security]

relations:
  - type: part_of
    target: EX-0003
due:
---
```

## Vorgang

```yaml
---
id: EX-0003
slug: ai-infrastruktur-produktionsreif
title: AI-Infrastruktur produktionsreif machen
type: process
status: active

organisations: [fkm]
functions: [it, strategy]
topics: [ai, infrastructure, security]

---
```

`EX-0002` ist über `part_of` diesem Vorgang zugeordnet.

## Harte Verpflichtung

```yaml
---
id: EX-0004
slug: mitarbeitergespraech-vorbereiten
title: Mitarbeitergespräch vorbereiten
type: commitment
status: active

organisations: [fkm]
functions: [hr]
topics: [personnel]

due: 2026-10-02
---
```

Das Datum bedeutet eine reale zeitliche Verpflichtung und nicht bloß eine gewünschte Wiedervorlage.

## Externer Vorgang

```yaml
---
id: EX-0005
slug: idplan-dokumentmodul
title: Architektur des idPlan-Dokumentmoduls verstehen
type: action
status: active

organisations: [fkm]
functions: [strategy]
topics: [software-modernisation]

source:
  system: jira
  ref: IDP-471
  url: https://jira.example/IDP-471
---
```

Jira bleibt Source of Truth. IMP hält nur den persönlichen Steuerungskontext.

## Bottom-up Consolidation

Aus zunächst losen Items:

```text
Zertifikat prüfen
LiteLLM Provider ergänzen
GPU-Auslastung prüfen
DNS-Dokumentation ergänzen
```

kann beim Review ein gemeinsamer Vorgang entstehen:

```text
AI-Infrastruktur produktionsreif machen
```

Die Einzelitems erhalten anschließend eine `part_of`-Relation zu diesem Vorgang.
