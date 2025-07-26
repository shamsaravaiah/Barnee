import json, os
from threading import Lock

DB_FILE = "data/companies.json"
_lock = Lock()

# Load existing data or empty dict
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        db = json.load(f)
else:
    db = {}

def save_db():
    with _lock:
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=2)
