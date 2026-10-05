import csv
from pathlib import Path


def normalize_columns(row):
    return {k.strip().lower().replace(" ", "_"): v for k, v in row.items()}


def extract_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [normalize_columns(row) for row in csv.DictReader(f)]
