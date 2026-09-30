"""PostgreSQL access; connections are scoped to a request/transaction."""

import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row


def connect():
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)


def initialize():
    # Explicit one-time initialization, never implicitly during API startup.
    with connect() as conn:
        conn.execute(Path(__file__).with_name("schema.sql").read_text())


if __name__ == "__main__":
    initialize()
