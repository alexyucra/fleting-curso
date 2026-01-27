

import sqlite3
# import mysql.connector  
from configs.database import DATABASE
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
_connection = None

def get_connection():
    global _connection

    if _connection is not None:
        return _connection

    engine = DATABASE.get("ENGINE", "sqlite").lower()

    if engine == "sqlite":
        _connection = _connect_sqlite()
    elif engine == "mysql":
        _connection = _connect_mysql()
    else:
        raise RuntimeError(f"Unsupported database engine: {engine}")

    return _connection

# =========================
# SQLITE
# =========================
def _connect_sqlite():
    cfg = DATABASE.get("SQLITE", {})
    path_cfg = cfg.get("PATH", "data/fleting.db")

    db_path = BASE_DIR / Path(path_cfg)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(db_path)

# =========================
# MYSQL
# =========================
def _connect_mysql():
    pass
    # try:
    #     import mysql.connector
    # except ImportError:
    #     raise RuntimeError(
    #         "MySQL support requires `mysql-connector-python` :"
    #         "pip install mysql-connector-python"
    #     )

    # cfg = DATABASE.get("MYSQL", {})

    # return mysql.connector.connect(
    #     host=cfg.get("HOST", "localhost"),
    #     port=cfg.get("PORT", 3306),
    #     user=cfg.get("USER"),
    #     password=cfg.get("PASSWORD"),
    #     database=cfg.get("NAME"),
    #     charset=cfg.get("OPTIONS", {}).get("charset", "utf8mb4"),
    # )

