# Student Data Integration & ETL Pipeline

مشروع Python يطبق التكليف الأساسي: جمع بيانات الطلاب من **CSV + REST API + SQLite** ثم تنفيذ:

**Extract → Validate → Clean → Integrate → Transform → Final Validation → Load**

## Structure
```text
student_data_engineering_app/
├── app/
│   ├── sources/
│   │   ├── csv_source.py
│   │   ├── api_source.py
│   │   └── database_source.py
│   ├── transformation/
│   │   ├── cleaner.py
│   │   ├── integration.py
│   │   └── transformer.py
│   ├── validation/
│   │   └── quality.py
│   ├── output/
│   │   └── csv_writer.py
│   └── utils/
├── data/
│   ├── raw/students.csv
│   ├── processed/final_dataset.csv
│   └── rejected/rejected_records.csv
├── database/students.db
├── mock_api/server.py
├── logs/pipeline.log
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## Sources
- CSV: student_id, student_name, age, major, city
- REST API: student_id, gpa, attendance, status
- SQLite: courses + enrollments linked by student_id

## Data Quality
- Validate student_id, age, GPA, attendance, score.
- Detect missing values and invalid values.
- Remove duplicate records.
- Normalize whitespace and city casing (`Sanaa / sanaa / SANAA`).
- Reject invalid records with a `reason` field.

## Integration & Transformation
All sources are integrated by `student_id`. The final dataset contains the derived columns:
- `performance_level`
- `attendance_status`

## Run
```bash
python main.py
```

The command creates/refreshes the SQLite demo data, starts the local REST API, and runs the complete ETL pipeline in the required order: Extract → Validate → Clean → Integrate → Transform → Final Validation → Load.
```text
data/processed/final_dataset.csv
data/rejected/rejected_records.csv
logs/pipeline.log
```

## Tests
```bash
python -m unittest discover -s tests -v
```

There are 10 tests covering the three sources, duplicates, missing values, invalid data, integration, output creation, cleaning, and derived columns.

## Scope
The project intentionally focuses on the **required assignment scope**. Features such as `config.yaml`, incremental processing, data lineage, and pipeline metrics are not included because they are enhancement items rather than core requirements.
