import pathlib
import sqlite3

# Get project root (one level above utils/)
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent  

# Point to schema.sql inside data/
SCHEMA_FILE = BASE_DIR / "data" / "schema.sql"

# Debugging tip: check the path being used
print("Loading schema from:", SCHEMA_FILE)

# Read the schema
SCHEMA = SCHEMA_FILE.read_text(encoding="utf-8")
SAMPLE_FILE = BASE_DIR / "data" / "sample_data.sql"
SAMPLE = SAMPLE_FILE.read_text(encoding="utf-8")

def main():
    db_path = pathlib.Path("data/cricket.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    cur.executescript(SAMPLE)
    conn.commit()
    conn.close()
    print("Initialized DB at", db_path)

if __name__ == "__main__":
    main()
