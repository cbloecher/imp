# Storage, Quellen und Berechtigungen

## 1. Grundsatz

IMP benötigt nicht eine einzige globale Datenquelle.

Stattdessen können mehrere fachlich führende Quellen parallel existieren.

Beispiele:

- PostgreSQL / native IMP-Objekte
- Jira
- Outlook / Microsoft Graph
- GitHub
- YAML / Markdown in Git-Repositories
- weitere SQL-Datenbanken
- zukünftige Fachsysteme

IMP führt diese Quellen lokal in PostgreSQL zu einem gemeinsamen Arbeitsgraphen zusammen.

## 2. PostgreSQL

PostgreSQL ist die zentrale Laufzeitdatenbank der IMP-Anwendung.

Sie enthält:

- native IMP-Items,
- normalisierte Projektionen externer Objekte,
- Organisationen, Funktionen, Themen und Tags,
- Relationen,
- Sprints,
- IMP-Overlays,
- Source- und Sync-Metadaten.

PostgreSQL ist für native IMP-Objekte führend.

Für externe Objekte ist PostgreSQL dagegen die lokale Projektion und nicht automatisch deren fachliche Source of Truth.

## 3. Source Adapter

Jede externe Quelle wird über einen Adapter angebunden.

```text
GitHub -------\
Jira ----------\
Outlook --------+--> Adapter --> Canonical Model --> PostgreSQL
YAML / Git -----/
SQL -----------/
```

Adapter kapseln quellspezifische Details und liefern ein gemeinsames Minimalmodell.

## 4. YAML / Git als vollwertige Quelle

Die frühere Idee mehrerer Data-Repositories bleibt möglich, ist aber nun **eine mögliche Source-Art unter mehreren**.

Ein Git-/YAML-Repo kann weiterhin:

- gemeinsam bearbeitet werden,
- Berechtigungsraum sein,
- versionierte Items bereitstellen,
- für Agenten gut lesbar sein.

Es ist aber nicht mehr zwingend das globale Primärformat von IMP.

## 5. Berechtigungsräume

Berechtigungen können auf unterschiedlichen Ebenen entstehen:

- Quellsystem selbst, z. B. GitHub/Jira
- konkreter Connector bzw. dessen Service Account
- IMP-interne Sichtbarkeit
- Organisation/Funktion
- zukünftige feinere ACLs

IMP darf keine Objekte sichtbar machen, die der jeweilige Benutzer über die vorgesehene Berechtigungslogik nicht sehen darf.

Das konkrete Autorisierungsmodell bleibt für den PoC noch offen.

## 6. Provenance

Jedes externe Objekt benötigt nachvollziehbare Herkunftsinformationen.

Mindestens:

```text
source_id
external_id
external_url / locator
last_seen_at
last_sync_at
source_state
source_hash (optional)
```

Damit kann IMP erkennen, ob ein Eintrag:

- aktuell,
- länger nicht geprüft,
- verschwunden,
- fehlerhaft,
- bewusst getrennt oder
- an der Quelle gelöscht wurde.

## 7. Kein automatisches Löschen bei Abweichungen

Ein Quellobjekt darf nicht gelöscht werden, nur weil es bei einem Sync-Lauf fehlt.

Zuerst wird der Zustand markiert.

```text
active
  ↓
missing
  ↓ erneute erfolgreiche Prüfung
deleted / orphaned
```

Connector-Ausfälle werden als `error` oder `stale` behandelt.

## 8. Reparatur

Für verwaiste oder fehlerhafte Source-Verknüpfungen sind explizite Operationen vorgesehen:

- erneut prüfen
- External ID korrigieren
- neue Quelle zuordnen
- Source-Verknüpfung lösen
- als natives IMP-Item übernehmen
- lokalen Eintrag entfernen

IMP-eigene Overlays und Beziehungen sollen dabei möglichst erhalten bleiben.

## 9. Schreibmodell

Quellen können unterschiedliche Schreibfähigkeiten besitzen.

Beispiele:

```text
GitHub Issue Connector  -> read/write
Jira Connector          -> read/write oder read-only
Outlook Calendar        -> read-only im ersten PoC
YAML/Git                -> read/write
SQL Reporting Source    -> read-only
```

Der Adapter deklariert seine Fähigkeiten.

IMP darf nur dort zurückschreiben, wo dies fachlich gewollt und technisch erlaubt ist.

## 10. Zielarchitektur

```text
             externe / interne Quellen
      ┌────────┬────────┬────────┬────────┐
      │ Jira   │ GitHub │ YAML   │ SQL    │
      └────┬───┴───┬────┴───┬────┴───┬────┘
           │       Source Adapter      │
           └───────────┬───────────────┘
                       ↓
                  PostgreSQL
             materialisierter Graph
                       ↓
                    FastAPI
                       ↓
               Vue 3 + Bootstrap
```

Damit bleibt IMP offen für unterschiedliche Datenhaltungsmodelle, ohne auf eine einheitliche Benutzeroberfläche und ein gemeinsames Arbeitsmodell zu verzichten.
