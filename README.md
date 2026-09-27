# IMP – Integrated Management Plane

IMP bündelt Aufgaben, Ideen, Vorgänge und Prioritäten über mehrere Organisationen, Rollen und bestehende Systeme hinweg.

IMP ersetzt Jira, Outlook, Teams, Kalender oder andere operative Systeme **nicht**. Es bildet die persönliche Steuerungsebene darüber.

## Problem

Arbeit entsteht heute verteilt:

- auf dem klassischen Schreibtischzettel,
- in E-Mails und Kalendern,
- in Jira, Teams, Planner oder anderen Fachsystemen,
- in Git-Repositories,
- aus Gesprächen, Recherchen und spontanen Ideen.

Dabei vermischen sich Ideen, unverbindliche nächste Schritte und harte Verpflichtungen. Gleichzeitig gehören Themen zu unterschiedlichen Organisationen, Funktionen und fachlichen Bereichen.

IMP soll diese Arbeit **erfassen, strukturieren, zerlegen, zusammenführen und priorisieren**, ohne die jeweiligen Source-of-Truth-Systeme zu duplizieren.

## Leitgedanken

1. **Capture first** – neue Gedanken dürfen zunächst ungeordnet in einer Inbox landen.
2. **Idee ist nicht Aufgabe** – unterschiedliche Verbindlichkeitsgrade bleiben sichtbar.
3. **Source of Truth bleibt extern** – Jira-Tickets, Termine oder Team-Aufgaben werden referenziert, nicht kopiert.
4. **Hierarchie und Graph** – Vorgänge können zerlegt und lose Items zu übergeordneten Vorgängen zusammengeführt werden.
5. **Mehrfachzuordnung** – ein Item kann mehreren Bereichen, Rollen oder Kontexten angehören.
6. **Dateibasiert statt Datenbank** – Markdown/YAML in Git bleibt lesbar, versionierbar und agentenfähig.
7. **Repos sind Berechtigungsräume** – mehrere Data-Repositories erlauben unterschiedliche Mitwirkende und Sichtbarkeiten.
8. **Persönliche Gesamtsicht** – IMP kann mehrere Repositories und externe Systeme zu einer persönlichen Steuerungsebene aggregieren.

## Begriffe

- **Item** – generisches Objekt in IMP.
- **Idee** – interessant, aber noch keine Verpflichtung.
- **Next Action** – konkret ausführbarer nächster Schritt ohne zwingenden Termin.
- **Commitment** – verbindliche Aufgabe mit Termin, Zusage oder anderer harter Verpflichtung.
- **Vorgang** – übergeordnetes Arbeitsthema, das weitere Items enthalten kann.
- **Bereich** – fachliche/domänenspezifische Zuordnung, n:m.
- **Rolle** – Funktion, in der ein Item bearbeitet wird, z. B. GF, IT, Personal.
- **Organisation** – organisatorischer Kontext, z. B. FKM, Giesserei Blöcher, Familie, Selbst.

## Erste Dokumente

- [Konzept](docs/concept.md)
- [Datenmodell](docs/data-model.md)
- [Storage und Berechtigungen](docs/storage.md)
- [Beispiele](examples/)

## Noch bewusst offen

- konkrete CLI-Syntax
- Rendering/Views
- Synchronisation mit externen Systemen
- Priorisierungsalgorithmus
- Agentenunterstützung
- ID-Schema über mehrere Data-Repositories hinweg

Diese Punkte sollen aus dem Datenmodell abgeleitet werden, nicht umgekehrt.
