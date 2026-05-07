"""
conftest.py — shared pytest fixtures for Resume + Portfolio Builder tests.

Provides a single in-memory SQLite connection that is shared across both
test modules (test_database.py and test_app.py).

Why a shared connection?
  SQLite ":memory:" databases are per-connection — a new connect() call
  creates a completely separate empty database. Since database.py opens and
  closes a connection on every function call, we replace get_connection()
  with a factory that always returns the same wrapped connection.

Why _NoCloseConn?
  database.py calls conn.close() in every finally block. Closing the shared
  in-memory connection would destroy the database. _NoCloseConn makes
  close() a no-op while delegating everything else to the real connection.
"""

import sqlite3
import pytest
import sys
import os

# Make sure the project root is on the path so database and app can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import database

# ---------------------------------------------------------------------------
# Shared in-memory connection
# ---------------------------------------------------------------------------

_real_conn = sqlite3.connect(":memory:", check_same_thread=False)
_real_conn.row_factory = sqlite3.Row


class _NoCloseConn:
    """Proxy that delegates all sqlite3 operations but ignores close()."""

    def __init__(self, conn):
        self._conn = conn

    def execute(self, *args, **kwargs):
        return self._conn.execute(*args, **kwargs)

    def commit(self):
        return self._conn.commit()

    def close(self):
        pass  # intentional no-op — keeps the in-memory DB alive

    @property
    def row_factory(self):
        return self._conn.row_factory

    @row_factory.setter
    def row_factory(self, value):
        self._conn.row_factory = value


_wrapped_conn = _NoCloseConn(_real_conn)

# Patch database module once at import time
database.DB_PATH = ":memory:"
database.get_connection = lambda: _wrapped_conn


# ---------------------------------------------------------------------------
# Session-scoped: create table once
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_schema():
    """Create the profile table once for the entire test session."""
    database.init_db()
    yield


# ---------------------------------------------------------------------------
# Function-scoped: wipe rows before each test
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clean_db():
    """Delete all rows from profile before each test for a clean slate."""
    _real_conn.execute("DELETE FROM profile")
    _real_conn.commit()
    yield
    _real_conn.execute("DELETE FROM profile")
    _real_conn.commit()
