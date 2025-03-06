"""Initialize SQLite database"""

import os
from pathlib import Path
from sqlite3 import connect, Connection, Cursor, IntegrityError

conn: Connection | None = None
curs: Cursor | None = None


def get_db(name: str | None = None, reset: bool = False):
    """Connect to SQLite database file"""
    global conn, curs
    if conn:
        if not reset:
            return
        conn = None
    if not name:
        name = os.getenv("CRYPTID_SQLITE_DB")
        top_dir = Path(__file__).resolve().parents[1]  # repo top
        # print(f"This is the top {top_dir}")
        db_dir = top_dir / "db"
        db_name = "cryptid.sqlite3"
        db_path = str(db_dir / db_name)
        name = os.getenv("CRYPTID_SQLITE_DB", db_path)
        print(f"this is the name {name}")
    conn = connect(name, check_same_thread=False)
    curs = conn.cursor()


get_db()
