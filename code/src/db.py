import sqlite3
from pathlib import Path
import os

DB_FILE = Path(__file__).parent / "nl2sql.db"

def init_db(force=False):
    # If force=True → delete existing DB
    if force and DB_FILE.exists():
        try:
            os.remove(DB_FILE)
        except PermissionError:
            # Windows file lock workaround
            conn = sqlite3.connect(str(DB_FILE))
            conn.close()
            os.remove(DB_FILE)

    # ⬇️ NEW CHECK (prevents re-running schema if DB already exists)
    if DB_FILE.exists() and not force:
        return

    conn = sqlite3.connect(str(DB_FILE))
    cursor = conn.cursor()

    # ⬇️ Runs only when DB is being created fresh (or force=True)
    schema_file = Path(__file__).parent / "data" / "banking_schema_sqlite.sql"
    with open(schema_file, "r") as f:
        cursor.executescript(f.read())

    data_file = Path(__file__).parent / "data" / "banking_data.sql"
    with open(data_file, "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()


def run_query(sql: str):
    conn = sqlite3.connect(DB_FILE, check_same_thread=False, timeout=5)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows
