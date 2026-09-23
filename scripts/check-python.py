"""Check the locked Python environment and load local configuration without printing it."""
from pathlib import Path
import sqlite3
import ssl

from dotenv import load_dotenv

PROJECT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT / ".env", override=False)

if __name__ == "__main__":
    with sqlite3.connect(":memory:") as connection:
        assert connection.execute("SELECT 1").fetchone() == (1,)
    assert ssl.OPENSSL_VERSION
    print("Python dependencies, SQLite, TLS and local .env loading are ready.")
