from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REJECTED_DIR = DATA_DIR / "rejected"
DB_FILE = ROOT / "database" / "students.db"
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"
