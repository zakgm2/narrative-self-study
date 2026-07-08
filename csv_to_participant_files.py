"""
csv_to_participant_files.py
----------------------------
Converts a SplitForms CSV export (Dashboard -> Submissions -> Export CSV)
into one P-XXXX.json file per row, matching the format PhysicsLibrary's
text-field-study pipeline expects.

Usage:
    python csv_to_participant_files.py submissions.csv output_folder
"""

import csv
import json
import sys
from pathlib import Path

FIELDS = [
    "participant_id", "timestamp", "age_range", "character_name",
    "character_backstory", "character_evolution", "ideal_home",
    "background", "current_challenges", "ten_year_outlook",
]


def convert(csv_path, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    written, skipped = 0, 0
    with open(csv_path, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            participant_id = row.get("participant_id", "").strip()
            if not participant_id:
                skipped += 1
                continue

            dest = out_dir / f"{participant_id}.json"
            if dest.exists():
                skipped += 1
                continue

            record = {field: row.get(field, "") for field in FIELDS}
            dest.write_text(json.dumps(record, indent=2), encoding="utf-8")
            written += 1

    print(f"Wrote {written} file(s) to {out_dir}, skipped {skipped} (missing ID or already present).")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_participant_files.py <submissions.csv> <output_folder>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
