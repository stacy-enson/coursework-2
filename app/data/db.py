import sqlite3
from pathlib import Path 

#Define paths
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

#Create DATA folder if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    return sqlite3.connect(str(db_path))



