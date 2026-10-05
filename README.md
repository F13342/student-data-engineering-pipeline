# Student Data Engineering Pipeline

## Project Overview

A Python-based multi-source Data Engineering Pipeline that extracts,
transforms, validates, integrates, and stores student data.

The project is developed incrementally using Git and GitHub.

---

## Data Sources

The project uses five independent data sources:

1. CSV
2. REST API
3. Web Scraping
4. PostgreSQL
5. MongoDB

Each different source has its own pipeline.

---

## Architecture

```text
CSV ────────────────┐
REST API ───────────┤
Web Scraping ───────┤
PostgreSQL ─────────┤
MongoDB ────────────┘
        ↓
Source-Specific Pipelines
        ↓
Raw / Prepared Data
        ↓
Integration
        ↓
Final Validation
        ↓
MongoDB
   ├── SQLite Export
   └── CSV Export
```

---

## Pipeline Stages

Each source pipeline follows the appropriate processing stages:

```text
Extract
   ↓
Transform
   ↓
Validate
   ↓
Prepare for Integration
```

The integration stage combines the prepared datasets.

The final validated dataset is loaded into MongoDB.

---

## Project Structure

```text
student_data_engineering_app/
│
├── app/
│   ├── database/
│   │   ├── mongodb.py
│   │   └── postgresql.py
│   │
│   ├── pipelines/
│   │   ├── csv_pipeline.py
│   │   ├── api_pipeline.py
│   │   ├── web_scraping_pipeline.py
│   │   ├── postgresql_pipeline.py
│   │   ├── mongodb_pipeline.py
│   │   └── integration_pipeline.py
│   │
│   ├── sources/
│   │   ├── csv_source.py
│   │   ├── api_source.py
│   │   ├── web_scraping_source.py
│   │   ├── postgresql_source.py
│   │   └── mongodb_source.py
│   │
│   ├── transformation/
│   ├── validation/
│   ├── output/
│   └── utils/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── rejected/
│   └── exports/
│
├── database/
│   ├── schema.sql
│   └── postgresql_schema.sql
│
├── docs/
│   ├── architecture.md
│   └── csv-pipeline.md
│
├── mock_api/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

---

## Technologies

- Python
- PyMongo
- PostgreSQL
- SQLite
- REST API
- Web Scraping
- CSV
- Git
- GitHub

---

## Requirements

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Running the Project

Make sure MongoDB and PostgreSQL are running.

Then execute:

```bash
python main.py
```

The pipeline performs:

```text
Extract
↓
Transform
↓
Validate
↓
Integration
↓
Final Validation
↓
MongoDB Load
↓
SQLite Export
↓
CSV Export
```

---

## Validation Result

The current test dataset demonstrates both accepted and rejected
records.

Example:

```text
Final valid: 5
Total rejected: 2
MongoDB final records: 5
```

Rejected records demonstrate the validation layer, including cases such
as duplicate records and invalid data.

---

## Testing

Run the complete test suite:

```bash
python -m pytest -q
```

Current result:

```text
10 passed
```

---

## Output

The final validated dataset is stored in MongoDB.

Additional exports are generated as:

```text
data/exports/final_dataset.db
data/exports/final_dataset.csv
```

Generated outputs are excluded from Git using `.gitignore`.

---

## Logging

Pipeline execution is logged for important operations, including:

- Pipeline start
- Extraction
- Transformation
- Validation
- Integration
- Rejections
- Database operations
- Export operations
- Pipeline completion

---

## Git Workflow

The project uses Git feature branches.

Current development branch:

```text
feature/multi-source-pipelines
```

Examples of meaningful commits:

```text
chore: initialize project baseline
docs: update pipeline architecture and storage
feat: add csv pipeline
feat: add mongodb source pipeline
feat: add web scraping pipeline
feat: add postgresql source pipeline
feat: add api pipeline
feat: add multi-source integration pipeline
feat: add final mongodb storage and exports
```

The `main` branch is kept stable.

---

## Documentation

Detailed documentation is available in:

```text
docs/architecture.md
docs/csv-pipeline.md
```

---

## Development Principle

Each major change is:

```text
Implement
↓
Test
↓
Document
↓
Commit
↓
Push
```

This keeps the project reproducible, traceable, and reviewable through
GitHub history.