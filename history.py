import json
from datetime import datetime
from pathlib import Path


HISTORY_FILE = Path("data/history.json")


def load_history():
    """Load verification history."""

    if not HISTORY_FILE.exists():
        return []

    if HISTORY_FILE.stat().st_size == 0:
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def record_verification(file_path, result):
    """Store a verification result in the history."""

    history = load_history()

    record = {
        "file": str(Path(file_path).resolve()),
        "status": result["status"],
        "message": result["message"],
        "timestamp": datetime.now().isoformat()
    }

    if "baseline_hash" in result:
        record["baseline_hash"] = result["baseline_hash"]

    if "current_hash" in result:
        record["current_hash"] = result["current_hash"]

    history.append(record)

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

    return record
