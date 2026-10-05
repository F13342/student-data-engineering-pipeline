import csv
import unittest
from pathlib import Path
from app.database.connection import get_connection, initialize_database
from app.etl.pipeline import run_pipeline
from app.validation.quality import validate_record
from app.transformation.cleaner import clean_city
from app.transformation.transformer import performance_level, attendance_status
from app.sources.csv_source import extract_csv
from app.sources.database_source import extract_database
from mock_api.server import create_server
from threading import Thread

ROOT = Path(__file__).resolve().parents[1]

class TestPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(); cls.thread = Thread(target=cls.server.serve_forever, daemon=True); cls.thread.start()
        cls.conn = get_connection(); initialize_database(cls.conn)
    @classmethod
    def tearDownClass(cls):
        cls.conn.close(); cls.server.shutdown()
    def test_csv_source_works(self):
        rows = extract_csv(ROOT / "data/raw/students.csv"); self.assertGreaterEqual(len(rows), 5)
    def test_api_source_works(self):
        from app.sources.api_source import extract_api
        rows = extract_api("http://127.0.0.1:8765/students"); self.assertGreaterEqual(len(rows), 5)
    def test_sqlite_source_works(self):
        rows = extract_database(self.conn); self.assertEqual(len(rows), 5)
    def test_duplicate_rejected(self):
        from app.validation.quality import validate_and_split
        row = {"student_id":"S1","student_name":"A","age":20,"major":"CS","city":"Sanaa","gpa":3,"attendance":90,"score":80,"course_code":"CS","course_name":"X"}
        valid, rejected = validate_and_split([row, row]); self.assertEqual(len(valid),1); self.assertEqual(rejected[0]["reason"],"duplicate student_id")
    def test_missing_values_rejected(self):
        row = {"student_id":"S1","student_name":"","age":20,"major":"CS","city":"Sanaa","gpa":3,"attendance":90,"score":80,"course_code":"CS","course_name":"X"}
        self.assertIn("missing student_name", validate_record(row))
    def test_invalid_data_rejected(self):
        row = {"student_id":"S1","student_name":"A","age":12,"major":"CS","city":"Sanaa","gpa":3,"attendance":90,"score":80,"course_code":"CS","course_name":"X"}
        self.assertIn("invalid age", validate_record(row))
    def test_integration_pipeline(self):
        result = run_pipeline(self.conn, "http://127.0.0.1:8765/students"); self.assertGreater(len(result.valid),0); self.assertGreater(len(result.rejected),0)
    def test_final_dataset_created(self):
        run_pipeline(self.conn, "http://127.0.0.1:8765/students")
        path=ROOT/"data/processed/final_dataset.csv"; self.assertTrue(path.exists())
        with path.open(encoding="utf-8-sig") as f: self.assertIn("performance_level", next(csv.DictReader(f)))
    def test_clean_city(self): self.assertEqual(clean_city("  sANAA  "), "Sanaa")
    def test_derived_columns(self): self.assertEqual(performance_level(3.7,90),"Excellent"); self.assertEqual(attendance_status(70),"Low")

if __name__ == "__main__": unittest.main()
