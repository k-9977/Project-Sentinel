import json
from datetime import datetime
from pathlib import Path

from hash_utils import calculate_file_hash


BASELINE_FILE = Path("data/baselines.json")


def load_baselines():
    """Load all trusted file baselines."""

    if not BASELINE_FILE.exists():
        return {}

    if BASELINE_FILE.stat().st_size == 0:
        return {}

    try:
        with open(BASELINE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def save_baseline(file_path):
    """Create or update the trusted baseline for a file."""

    file_path = str(Path(file_path).resolve())

    if not Path(file_path).is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    baselines = load_baselines()
    file_hash = calculate_file_hash(file_path)

    baselines[file_path] = {
        "hash": file_hash,
        "created_at": datetime.now().isoformat()
    }

    BASELINE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(BASELINE_FILE, "w", encoding="utf-8") as file:
        json.dump(baselines, file, indent=4)

    return file_hash


def verify_file(file_path):
    """Compare the current file hash against its trusted baseline."""

    file_path = str(Path(file_path).resolve())

    if not Path(file_path).is_file():
        return {
            "status": "missing",
            "message": "The selected file does not exist."
        }

    baselines = load_baselines()

    if file_path not in baselines:
        return {
            "status": "not_baselined",
            "message": "No trusted baseline exists for this file."
        }

    current_hash = calculate_file_hash(file_path)
    baseline_hash = baselines[file_path]["hash"]

    if current_hash == baseline_hash:
        return {
            "status": "verified",
            "message": "File integrity verified. No changes detected.",
            "baseline_hash": baseline_hash,
            "current_hash": current_hash
        }

    return {
        "status": "modified",
        "message": "File has been modified.",
        "baseline_hash": baseline_hash,
        "current_hash": current_hash
    }
