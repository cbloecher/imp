# IMP – Integrated Management Plane

IMP bündelt Aufgaben, Ideen, Vorgänge und Prioritäten über mehrere Organisationen, Funktionen, Themen und bestehende Systeme hinweg.

IMP ersetzt Jira, Outlook, Teams, Kalender, GitHub oder andere operative Systeme **nicht**. Es bildet die persönliche Steuerungsebene darüber.

## Problem

Arbeit entsteht heute verteilt:

- auf dem klassischen Schreibtischzettel,
- in E-Mails und Kalendern,
- in Jira, Teams, Planner oder anderen Fachsystemen,
- in Git-Repositories und YAML/Markdown-Dateien,
- in Datenbanken,
- aus Gesprächen, Recherchen und spontanen Ideen.

Dabei vermischen sich Ideen, unverbindliche nächste Schritte und harte Verpflichtungen. Gleichzeitig gehören Themen zu unterschiedlichen Organisationen, Funktionen und fachlichen Bereichen.

IMP soll diese Arbeit **erfassen, zusammenführen, strukturieren, zerlegen, bündeln, filtern und priorisieren**, ohne bestehende Source-of-Truth-Systeme unnötig zu ersetzen.

## Architekturgrundsatz: föderierte Quellen

IMP benötigt nicht eine einzige globale Source of Truth.

Stattdessen kann jedes Objekt dort fachlich führend bleiben, wo es entsteht:

- Jira-Ticket → Jira
- Outlook-Termin → Outlook / Kalender
- GitHub-Issue → GitHub
- YAML-/Markdown-Item → entsprechendes Data-Repository
- natives IMP-Item → IMP-PostgreSQL

IMP normalisiert diese Quellen in ein gemeinsames Modell und führt sie in einem lokalen, materialisierten Arbeitsgraphen zusammen.

```text
Jira ---------\
Outlook -------\
GitHub ---------+--> Source Adapter --> IMP Arbeitsgraph --> Views / Sprint / Suche
YAML / Git -----/
SQL / DB -------/
IMP PostgreSQL -/
```

PostgreSQL ist dabei:

- operative Heimat nativer IMP-Objekte,
- lokaler Index und materialisierte Projektion externer Quellen,
- Speicher für IMP-eigene Overlays wie Priorität, Sprint, Tags oder persönliche Zuordnungen.

Externe Quellen behalten ihre jeweilige fachliche Autorität.

## Leitgedanken

1. **Capture first** – neue Gedanken dürfen zunächst ungeordnet in einer Inbox landen.
2. **Idee ist nicht Aufgabe** – unterschiedliche Verbindlichkeitsgrade bleiben sichtbar.
3. **Föderierte Sources of Truth** – jedes Objekt kann in seiner Ursprungquelle führend bleiben.
4. **IMP als Overlay** – persönliche Steuerungsdaten können externe Objekte ergänzen, ohne sie vollständig zu kopieren.
5. **Arbeitsgraph statt starrer Baum** – Vorgänge, Beziehungen und Kontextknoten bilden einen Graphen.
6. **Mehrfachzuordnung** – ein Item kann mehreren Organisationen, Funktionen, Themen und Tags angehören.
7. **Materialisierte lokale Sicht** – PostgreSQL führt Quellen für Suche, Filter, Graph und Sprint zusammen.
8. **Drift sichtbar machen** – fehlende, veraltete oder gelöschte Quellobjekte werden erkannt und nicht stillschweigend entfernt.
9. **Reparierbarkeit** – verwaiste Referenzen können neu zugeordnet, übernommen oder bewusst entfernt werden.
10. **Offene Integrationsarchitektur** – neue Source Adapter sollen ohne Änderung des Kernmodells ergänzt werden können.

## Begriffe

- **Item** – generisches Objekt in IMP.
- **Idee** – interessant, aber noch keine Verpflichtung.
- **Next Action** – konkret ausführbarer nächster Schritt ohne zwingenden Termin.
- **Commitment** – verbindliche Aufgabe mit Termin, Zusage oder anderer harter Verpflichtung.
- **Vorgang / Paket** – übergeordnetes Arbeitsthema, das weitere Items bündeln kann.
- **Organisation** – organisatorischer Kontext, z. B. FKM, Giesserei Blöcher, Familie, Selbst.
- **Funktion** – Rolle, in der ein Item bearbeitet wird, z. B. GF, IT, Personal.
- **Thema** – relativ stabile fachliche Zuordnung.
- **Tag** – frei verwendbarer, zentral verwalteter Marker.
- **Source Object** – Objekt in einem externen oder internen führenden System.
- **IMP Overlay** – persönliche Steuerungsinformationen, die IMP zu einem Source Object ergänzt.
- **Materialisierte Projektion** – lokale PostgreSQL-Repräsentation für Suche, Filter, Graph und Views.

## Dokumente

- [Konzept](docs/concept.md)
- [Datenmodell](docs/data-model.md)
- [Storage und Quellen](docs/storage.md)
- [Beispiele](examples/)

## Technische Arbeitsannahme

Für den ersten PoC:

- PostgreSQL
- FastAPI
- SQLAlchemy / Alembic
- Vue 3
- Bootstrap 5

Authentifizierung, Graph-Darstellung, konkrete Source Adapter und Detail-Schema bleiben noch offen.
