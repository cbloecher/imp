# Beispiele

Die Beispiele zeigen bewusst unterschiedliche Verbindlichkeitsgrade und Beziehungen.

## Idee

```yaml
---
id: EX-0001
slug: gitdiagram-fuer-idplan
title: GitDiagram für idPlan prüfen
type: idea
status: open

organisations: [fkm]
roles: [strategy]
areas: [digitalisation, software-modernisation]

parent:
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
roles: [it]
areas: [ai, infrastructure, security]

parent: EX-0003
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
roles: [it, strategy]
areas: [ai, infrastructure, security]

parent:
---
```

`EX-0002` ist über `parent` diesem Vorgang zugeordnet.

## Harte Verpflichtung

```yaml
---
id: EX-0004
slug: mitarbeitergespraech-vorbereiten
title: Mitarbeitergespräch vorbereiten
type: commitment
status: active

organisations: [fkm]
roles: [hr]
areas: [personnel]

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
roles: [strategy]
areas: [software-modernisation]

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

Die Einzelitems erhalten anschließend dessen ID als `parent`.
