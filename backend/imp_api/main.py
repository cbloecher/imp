"""Local graph persistence PoC. Authentication and domain edge rules are intentionally open."""

from typing import Annotated, Literal
from uuid import UUID, uuid4

import psycopg
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StringConstraints

from .db import connect

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
Kind = Literal["item", "organisation", "function", "topic", "tag"]


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NodeCreate(Input):
    kind: Kind = "item"
    title: Text
    body: str = Field(default="", max_length=10000)


class NodeRename(Input):
    title: Text


class Node(NodeCreate):
    id: UUID


class Edge(Input):
    source_id: UUID
    target_id: UUID
    relation: Text


class SourceCreate(Input):
    system: Text
    external_ref: Text
    url: HttpUrl


class Source(SourceCreate):
    id: UUID
    node_id: UUID


app = FastAPI(title="IMP graph PoC", version="0.1.0")


def require_node(conn, node_id):
    row = conn.execute("SELECT * FROM nodes WHERE id = %s", (node_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "Node not found")
    return row


@app.get("/health")
def health():
    try:
        with connect() as conn:
            conn.execute("SELECT 1")
    except psycopg.OperationalError:
        raise HTTPException(503, "Database unavailable") from None
    return {"status": "ok"}


@app.post("/nodes", response_model=Node, status_code=201)
def create_node(node: NodeCreate):
    with connect() as conn:
        return conn.execute(
            "INSERT INTO nodes (id, kind, title, body) VALUES (%s, %s, %s, %s) RETURNING *",
            (uuid4(), node.kind, node.title, node.body),
        ).fetchone()


@app.get("/nodes", response_model=list[Node])
def list_nodes(kind: Kind | None = None, limit: int = Query(100, ge=1, le=500)):
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM nodes WHERE (%s::text IS NULL OR kind = %s) ORDER BY id LIMIT %s",
            (kind, kind, limit),
        ).fetchall()


@app.get("/nodes/{node_id}", response_model=Node)
def get_node(node_id: UUID):
    with connect() as conn:
        return require_node(conn, node_id)


@app.patch("/nodes/{node_id}", response_model=Node)
def rename_node(node_id: UUID, change: NodeRename):
    with connect() as conn:
        row = conn.execute(
            "UPDATE nodes SET title = %s WHERE id = %s RETURNING *", (change.title, node_id)
        ).fetchone()
        if row is None:
            raise HTTPException(404, "Node not found")
        return row


@app.post("/edges", response_model=Edge, status_code=201)
def create_edge(edge: Edge):
    try:
        with connect() as conn:
            return conn.execute(
                "INSERT INTO edges VALUES (%s, %s, %s) RETURNING *",
                (edge.source_id, edge.target_id, edge.relation),
            ).fetchone()
    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(404, "Edge endpoint not found") from None
    except psycopg.errors.UniqueViolation:
        raise HTTPException(409, "Edge already exists") from None


@app.get("/edges", response_model=list[Edge])
def list_edges(node_id: UUID, limit: int = Query(100, ge=1, le=500)):
    with connect() as conn:
        require_node(conn, node_id)
        return conn.execute(
            "SELECT * FROM edges WHERE source_id = %s OR target_id = %s "
            "ORDER BY source_id, target_id, relation LIMIT %s",
            (node_id, node_id, limit),
        ).fetchall()


@app.post("/nodes/{node_id}/sources", response_model=Source, status_code=201)
def create_source(node_id: UUID, source: SourceCreate):
    try:
        with connect() as conn:
            require_node(conn, node_id)
            return conn.execute(
                "INSERT INTO source_refs VALUES (%s, %s, %s, %s, %s) RETURNING *",
                (uuid4(), node_id, source.system, source.external_ref, str(source.url)),
            ).fetchone()
    except psycopg.errors.UniqueViolation:
        raise HTTPException(409, "Source reference already exists") from None


@app.get("/nodes/{node_id}/sources", response_model=list[Source])
def list_sources(node_id: UUID, limit: int = Query(100, ge=1, le=500)):
    with connect() as conn:
        require_node(conn, node_id)
        return conn.execute(
            "SELECT * FROM source_refs WHERE node_id = %s ORDER BY id LIMIT %s", (node_id, limit)
        ).fetchall()
