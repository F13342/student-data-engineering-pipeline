# Data Engineering Pipeline Architecture

## 1. Project Overview

This project is a Python-based Data Engineering Pipeline.

The goal is to collect data from multiple sources, process and validate
the data, integrate the results, store the final dataset in MongoDB,
and provide additional exports for SQLite and CSV.

The project is developed incrementally using Git and GitHub.

---

## 2. Pipeline Strategy

When the data source is different, each source has its own pipeline.

Each source pipeline is responsible for:

1. Extract
2. Transform
3. Validate
4. Prepare data for Integration

After the individual pipelines complete, the processed datasets are
integrated into a unified dataset.

The final validated dataset is loaded into MongoDB and can also be
exported to SQLite and CSV.

---

## 3. Data Sources

The project includes the following data sources:

- CSV files
- REST API
- Web Scraping
- PostgreSQL
- MongoDB

The relational database source uses PostgreSQL.

MongoDB is also used as a separate source through the PyMongo library.

---

## 4. High-Level Architecture

```text
                         DATA SOURCES
                              |
        +---------------------+---------------------+
        |           |         |         |           |
       CSV         API    WEB SCRAPING PostgreSQL MongoDB
        |           |         |         |           |
        +-----------+---------+---------+-----------+
                              |
                  SOURCE-SPECIFIC PIPELINES
                              |
                         RAW STORAGE
                              |
                          TRANSFORM
                              |
                          VALIDATE
                              |
                         INTEGRATE
                              |
                      FINAL VALIDATION
                              |
                              v
                          MongoDB
                     PRIMARY FINAL STORAGE
                              |
                 +------------+------------+
                 |                         |
                 v                         v
          SQLite Export              CSV Export
```

---

## 5. Source-Specific Pipelines

Each different source is processed independently.

### CSV Pipeline

```text
CSV
 ↓
Extract
 ↓
Transform
 ↓
Validate
 ↓
Prepared Dataset
```

### REST API Pipeline

```text
REST API
 ↓
Extract
 ↓
Transform
 ↓
Validate
 ↓
Prepared Dataset
```

### Web Scraping Pipeline

```text
Web
 ↓
Scrape
 ↓
Transform
 ↓
Validate
 ↓
Prepared Dataset
```

### PostgreSQL Pipeline

```text
PostgreSQL
 ↓
Extract
 ↓
Transform
 ↓
Validate
 ↓
Prepared Dataset
```

### MongoDB Pipeline

```text
MongoDB
 ↓
PyMongo
 ↓
Extract
 ↓
Transform
 ↓
Validate
 ↓
Prepared Dataset
```

---

## 6. Integration Pipeline

After the source-specific pipelines finish, the processed datasets
are integrated using the appropriate common fields.

```text
CSV Dataset
      \
API Dataset
       \
Web Dataset ----> Integration ----> Unified Dataset
       /
PostgreSQL
     /
MongoDB
```

The integration stage must preserve data quality and avoid unintended
duplicate records.

---

## 7. Validation

Validation is a gate before final loading.

```text
Extract
   ↓
Transform
   ↓
Validate
   ↓
PASS ─────────→ Load
   │
   └───────────→ Reject / Quarantine
```

Invalid records should be separated from valid records whenever the
error is recoverable.

Final validation is performed before loading the unified dataset into
MongoDB.

---

## 8. Raw Data

The original extracted data should be retained before transformation.

```text
SOURCE
  ↓
RAW COPY
  ↓
TRANSFORM
  ↓
VALIDATE
  ↓
INTEGRATE
  ↓
FINAL VALIDATION
  ↓
LOAD
```

Keeping raw data supports:

- Reprocessing
- Debugging
- Auditing
- Reproducibility

The project follows the principle of retaining an original copy before
processing.

---

## 9. Final Storage

MongoDB is the primary final storage database.

The final validated dataset is loaded into MongoDB using PyMongo.

```text
Source Pipelines
       ↓
Integration
       ↓
Final Validation
       ↓
MongoDB
```

---

## 10. Export Layer

The final dataset stored in MongoDB can also be exported into other
formats for analysis, testing, or portability.

### SQLite Export

```text
MongoDB
   ↓
SQLite Export
```

SQLite is used as an export/snapshot of the final validated dataset.

### CSV Export

```text
MongoDB
   ↓
CSV Export
```

CSV is used as an additional portable representation of the final
dataset.

---

## 11. Logging and Error Handling

The pipeline will include logging for important operations.

Examples:

- Pipeline started
- Source extraction completed
- Transformation completed
- Validation completed
- Integration completed
- Records rejected
- MongoDB connection errors
- Export errors
- Pipeline completed successfully

Errors will be classified as recoverable or fatal when appropriate.

---

## 12. Reproducibility

The pipeline should be executable repeatedly using the same process
and rules.

The project should avoid unintended duplicate data when the same
pipeline is executed multiple times.

MongoDB loading should use appropriate uniqueness and upsert strategies
where required.

---

## 13. Git and GitHub

Git is used for version control.

The project is developed using feature branches and meaningful commits.

Example commit messages:

- `chore: initialize project baseline`
- `docs: document pipeline architecture`
- `feat: add csv pipeline`
- `feat: add api pipeline`
- `feat: add web scraping pipeline`
- `feat: add postgresql pipeline`
- `feat: add mongodb pipeline`
- `feat: add integration pipeline`
- `feat: add validation layer`
- `feat: add mongodb loader`
- `feat: add sqlite export`
- `feat: add csv export`
- `test: add pipeline tests`

The GitHub repository is public so that the project history,
documentation, and implementation can be reviewed.

---

## 14. Development Principle

The project will be developed incrementally.

Each major change will be:

1. Implemented
2. Tested
3. Documented
4. Committed to Git
5. Pushed to GitHub

The `main` branch is kept stable while development is performed in
feature branches.

---

## 15. Final Pipeline

The complete project workflow is:

```text
                    CSV
                     |
                 CSV Pipeline
                     |
                    RAW
                     |
                     v

                    API
                     |
                 API Pipeline
                     |
                    RAW
                     |
                     v

               WEB SCRAPING
                     |
              Scraping Pipeline
                     |
                    RAW
                     |
                     v

                PostgreSQL
                     |
            PostgreSQL Pipeline
                     |
                    RAW
                     |
                     v

                  MongoDB
                     |
            MongoDB Source Pipeline
                     |
                    RAW
                     |
                     v

              +----------------+
              |   INTEGRATION  |
              +----------------+
                       |
                       v
                 FINAL VALIDATION
                       |
                       v
                  +---------+
                  | MongoDB |
                  +---------+
                       |
                +------+------+
                |             |
                v             v
            SQLite          CSV
            Export         Export
```

---

## 16. Architecture Goal

The final architecture separates data extraction from transformation,
validation, integration, loading, and exporting.

This separation makes the project easier to:

- Maintain
- Test
- Debug
- Extend
- Reuse
- Document

Each source can evolve independently without requiring all other source
pipelines to be rewritten.