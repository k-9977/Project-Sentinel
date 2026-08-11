
import json
from datetime import datetime
from pathlib import Path

from hash_utils import calculate_file_hash


BASELINE_FILE = Path("data/baselines.json")


def load_baselines():
    """Load existing file integrity baselines from storage."""

    if not BASELINE_FILE.exists():
        return {}

    if BASELINE_FILE.stat().st_size == 0:
        return {}

    with open(BASELINE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_baseline(file_path):
    """Calculate and save the current SHA-256 hash of a file."""

    baselines = load_baselines()

    file_path = str(Path(file_path).resolve())
    file_hash = calculate_file_hash(file_path)

    baselines[file_path] = {
        "hash": file_hash,
        "created_at": datetime.now().isoformat()
    }

    BASELINE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(BASELINE_FILE, "w", encoding="utf-8") as file:
        json.dump(baselines, file, indent=4)

    return file_hash
