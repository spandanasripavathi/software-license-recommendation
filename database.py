import sqlite3
from pathlib import Path
from flask import g

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "licenses.db"

def get_db():
    if "db" not in g:
        DATABASE_DIR.mkdir(exist_ok=True)
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    DATABASE_DIR.mkdir(exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            requirements_json TEXT NOT NULL,
            recommended_key TEXT NOT NULL,
            explanation TEXT NOT NULL,
            alternatives TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS licenses (
            license_key TEXT PRIMARY KEY,
            license_name TEXT NOT NULL,
            reference_url TEXT NOT NULL
        );
    """)
    license_rows = [
        ("MIT", "MIT License", "https://opensource.org/license/mit"),
        ("GPL", "GNU General Public License", "https://www.gnu.org/licenses/gpl-3.0.en.html"),
        ("Apache", "Apache License 2.0", "https://www.apache.org/licenses/LICENSE-2.0"),
        ("BSD", "BSD 3-Clause License", "https://opensource.org/license/bsd-3-clause")
    ]
    connection.executemany("INSERT OR IGNORE INTO licenses VALUES (?,?,?)", license_rows)
    connection.commit()
    connection.close()
