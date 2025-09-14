import sqlite3
import pathlib

DB_PATH = pathlib.Path("data/cricket.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_db_ready():
    if not DB_PATH.exists():
        from utils.init_db import main as init_main
        init_main()
