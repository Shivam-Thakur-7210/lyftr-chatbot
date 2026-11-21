import os
import sqlite3
from contextlib import closing
from pathlib import Path


backend_directory = Path(__file__).resolve().parent
database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///./data/app.db",
)

if not database_url.startswith("sqlite:///"):
    raise ValueError("DATABASE_URL must be a SQLite URL")

database_path = Path(database_url.removeprefix("sqlite:///"))

if not database_path.is_absolute():
    database_path = backend_directory / database_path


def get_connection():
    return sqlite3.connect(database_path)


def initialize_database():
    database_path.parent.mkdir(parents=True, exist_ok=True)

    with closing(get_connection()) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TEXT NOT NULL
            )
        """)
        connection.commit()