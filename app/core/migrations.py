
from pathlib import Path
from core.database import get_connection

MIGRATIONS_TABLE = "_fleting_migrations"

def ensure_migrations_table():
    db = get_connection()
    db.execute(f'''
        CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    db.commit()

def applied_migrations():
    db = get_connection()
    ensure_migrations_table()
    rows = db.execute(
        f"SELECT name FROM {MIGRATIONS_TABLE} ORDER BY id"
    ).fetchall()
    return [r[0] for r in rows]

def apply_migration(name, up):
    db = get_connection()
    up(db)
    db.execute(
        f"INSERT INTO {MIGRATIONS_TABLE} (name) VALUES (?)",
        (name,)
    )
    db.commit()

def rollback_migration(name, down):
    db = get_connection()
    down(db)
    db.execute(
        f"DELETE FROM {MIGRATIONS_TABLE} WHERE name = ?",
        (name,)
    )
    db.commit()
