from __future__ import annotations

import os
import sqlite3
from typing import Tuple, Any, List


def get_connection(db_path: str) -> sqlite3.Connection:
    """
    Open a SQLite connection with a Row factory so results can be accessed
    like dictionaries (e.g., row['name']).
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def run_query(conn: sqlite3.Connection, sql: str, params: Tuple[Any, ...] = ()) -> List[sqlite3.Row]:
    """
    Execute a SELECT query and return all rows.
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()
    except sqlite3.Error as e:
        raise RuntimeError(f"Database query failed: {e}\nSQL: {sql}\nParams: {params}") from e


def run_execute(conn: sqlite3.Connection, sql: str, params: Tuple[Any, ...] = ()) -> int:
    """
    Execute an INSERT/UPDATE/DELETE statement and return number of rows affected.
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Database write failed: {e}\nSQL: {sql}\nParams: {params}") from e
