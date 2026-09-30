import os
from uuid import uuid4

import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo

from imp_api.db import initialize
from imp_api.main import app


@pytest.fixture
def client(monkeypatch):
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.fail("Set TEST_DATABASE_URL to a disposable PostgreSQL database")
    schema = "imp_test_" + uuid4().hex
    with psycopg.connect(url) as conn:
        conn.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    config = conninfo_to_dict(url)
    config["options"] = config.get("options", "") + f" -csearch_path={schema}"
    monkeypatch.setenv("DATABASE_URL", make_conninfo(**config))
    try:
        initialize()
        with TestClient(app) as test_client:
            yield test_client
    finally:
        with psycopg.connect(url) as conn:
            conn.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


def node(client, title, kind="item"):
    result = client.post("/nodes", json={"title": title, "kind": kind})
    assert result.status_code == 201
    return result.json()["id"]


def test_persistence(client):
    assert client.get("/health").json() == {"status": "ok"}
    item = node(client, "Eintrag")
    with TestClient(app) as reader:
        assert reader.get(f"/nodes/{item}").json()["title"] == "Eintrag"
    assert client.get("/nodes").json()[0]["id"] == item


def test_many_to_many_and_rename(client):
    first, second = node(client, "A"), node(client, "B")
    tag, topic = node(client, "Lesen", "tag"), node(client, "KI", "topic")
    for source, target in [(first, tag), (second, tag), (first, topic)]:
        assert (
            client.post(
                "/edges", json={"source_id": source, "target_id": target, "relation": "context"}
            ).status_code
            == 201
        )
    before = client.get("/edges", params={"node_id": tag}).json()
    result = client.patch(f"/nodes/{tag}", json={"title": "Prüfen"})
    assert result.status_code == 200
    assert result.json()["id"] == tag
    assert client.get("/edges", params={"node_id": tag}).json() == before
    assert len(before) == 2
    assert client.get("/nodes", params={"kind": "tag"}).json()[0]["title"] == "Prüfen"


def test_item_and_context_relations(client):
    child, parent = node(client, "Action"), node(client, "Vorgang")
    org, topic = node(client, "FKM", "organisation"), node(client, "KI", "topic")
    for source, target, relation in [(child, parent, "part_of"), (org, topic, "topic")]:
        assert (
            client.post(
                "/edges", json={"source_id": source, "target_id": target, "relation": relation}
            ).status_code
            == 201
        )
    assert client.get("/edges", params={"node_id": parent}).json()[0]["source_id"] == child


def test_integrity_and_rollback(client):
    first, second = node(client, "A"), node(client, "B")
    edge = {"source_id": first, "target_id": str(uuid4()), "relation": "related"}
    assert client.post("/edges", json=edge).status_code == 404
    edge["target_id"] = second
    assert client.post("/edges", json=edge).status_code == 201
    assert client.post("/edges", json=edge).status_code == 409
    assert len(client.get("/edges", params={"node_id": first}).json()) == 1
    missing = str(uuid4())
    assert client.get(f"/nodes/{missing}").status_code == 404
    assert client.patch(f"/nodes/{missing}", json={"title": "Neu"}).status_code == 404


def test_source_reference(client):
    item = node(client, "Persönlicher Kontext")
    source = {"system": "jira", "external_ref": "IDP-471", "url": "https://jira.example/IDP-471"}
    assert client.post(f"/nodes/{item}/sources", json=source).status_code == 201
    assert client.post(f"/nodes/{item}/sources", json=source).status_code == 409
    assert client.get(f"/nodes/{item}/sources").json()[0]["external_ref"] == "IDP-471"
    assert client.post(f"/nodes/{uuid4()}/sources", json=source).status_code == 404


def test_validation():
    with TestClient(app) as client:
        for payload in [
            {"title": " "},
            {"title": "A", "kind": "unknown"},
            {"title": "A", "unexpected": True},
        ]:
            assert client.post("/nodes", json=payload).status_code == 422
        assert client.get("/nodes", params={"limit": 501}).status_code == 422
        assert client.get("/nodes/not-a-uuid").status_code == 422
        assert (
            client.post(
                f"/nodes/{uuid4()}/sources",
                json={"system": "jira", "external_ref": "X", "url": "not-a-url"},
            ).status_code
            == 422
        )
