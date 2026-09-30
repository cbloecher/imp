-- Vorläufiges PoC-Schema. Kein finales Domänenschema und kein Migrationstool.
CREATE TABLE nodes (
    id uuid PRIMARY KEY,
    kind text NOT NULL CHECK (kind IN ('item', 'organisation', 'function', 'topic', 'tag')),
    title text NOT NULL CHECK (length(trim(title)) > 0),
    body text NOT NULL DEFAULT ''
);
CREATE TABLE edges (
    source_id uuid NOT NULL REFERENCES nodes(id),
    target_id uuid NOT NULL REFERENCES nodes(id),
    relation text NOT NULL CHECK (length(trim(relation)) > 0),
    PRIMARY KEY (source_id, target_id, relation)
);
CREATE TABLE source_refs (
    id uuid PRIMARY KEY,
    node_id uuid NOT NULL REFERENCES nodes(id),
    system text NOT NULL CHECK (length(trim(system)) > 0),
    external_ref text NOT NULL CHECK (length(trim(external_ref)) > 0),
    url text NOT NULL,
    UNIQUE (node_id, system, external_ref)
);
