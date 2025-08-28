
import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent / 'nl2sql.db'
SCHEMA_SQL = Path(__file__).parent / 'sample_data.sql'

def init_db(force=False):
    """Initialize the SQLite database using sample_data.sql.
    If force=True, the existing DB will be removed and recreated."""
    if force and DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_SQL, 'r') as f:
        sql = f.read()
    conn.executescript(sql)
    conn.commit()
    conn.close()
    print(f"Initialized database at {DB_PATH}")

def run_query(query, params=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query) if not params else cur.execute(query, params)
    rows = cur.fetchall()
    cols = [c[0] for c in cur.description] if cur.description else []
    conn.close()
    results = [dict(zip(cols, r)) for r in rows]
    return results

if __name__ == '__main__':
    init_db(force=False)
