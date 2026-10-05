"""Check the locked Python environment and load local configuration without printing it."""
from importlib import import_module
from pathlib import Path
import sqlite3
import ssl

from dotenv import load_dotenv

PROJECT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT / ".env", override=False)

# Shared libraries every participant installs before the day (see pyproject.toml).
SHARED = {"pypdf": "PDFs", "openpyxl": "Excel workbooks", "docx": "Word documents",
          "httpx": "web requests", "feedparser": "news feeds"}

if __name__ == "__main__":
    with sqlite3.connect(":memory:") as connection:
        assert connection.execute("SELECT 1").fetchone() == (1,)
    assert ssl.OPENSSL_VERSION
    for module in SHARED:
        import_module(module)
    print("Python dependencies, SQLite, TLS and local .env loading are ready.")
    print("Shared libraries ready for " + ", ".join(SHARED.values()) + ".")
