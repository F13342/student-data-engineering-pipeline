# Data Engineering Pipeline Architecture

## 1. Project Overview

This project is a Python-based Data Engineering Pipeline.

The goal is to collect data from multiple sources, process and validate
the data, integrate the results, and store the final dataset.

The project is developed incrementally using Git and GitHub.

---

## 2. Pipeline Strategy

When the data source is different, each source has its own pipeline.

Each source pipeline is responsible for:

1. Extract
2. Transform
3. Validate
4. Store / Prepare for Integration

After the individual pipelines complete, the processed datasets are
integrated into a unified dataset.

---

## 3. Data Sources

The target project architecture includes different data sources:

- CSV files
- REST API
- Web Scraping
- Relational Database
- MongoDB

The relational database source will use PostgreSQL.

SQLite will be used as the final storage database for the processed data.

---

## 4. High-Level Architecture

```text
                    DATA SOURCES
                         |
       +-----------------+-----------------+
       |                 |                 |
      CSV               API         WEB SCRAPING
       |                 |                 |
       +-----------------+-----------------+
                         |
                  POSTGRESQL / MONGODB
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
                       SQLITE
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
PASS ─────→ Load
   │
   └──────→ Reject / Quarantine
```

Invalid records should be separated from valid records whenever the
error is recoverable.

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
LOAD
```

Keeping raw data supports:

- Reprocessing
- Debugging
- Auditing
- Reproducibility

---

## 9. Final Storage

SQLite will be used as the final storage database for the training
project.

The final flow is:

```text
Source Pipelines
       ↓
Integration
       ↓
Final Validation
       ↓
SQLite
```

---

## 10. Logging and Error Handling

The pipeline will include logging for important operations.

Examples:

- Pipeline started
- Source extraction completed
- Transformation completed
- Validation completed
- Records rejected
- Database errors
- Pipeline completed successfully

Errors will be classified as recoverable or fatal when appropriate.

---

## 11. Reproducibility

The pipeline should be executable repeatedly using the same process
and rules.

The project should avoid unintended duplicate data when the same
pipeline is executed multiple times.

---

## 12. Git and GitHub

Git is used for version control.

The project will be developed using feature branches and meaningful
commits.

Example commit messages:

- `chore: initialize project baseline`
- `feat: add csv pipeline`
- `feat: add api pipeline`
- `feat: add web scraping pipeline`
- `feat: add postgresql pipeline`
- `feat: add mongodb pipeline`
- `feat: add integration pipeline`
- `feat: add validation layer`
- `docs: document pipeline architecture`

The GitHub repository is public so that the project history and
documentation can be reviewed.

---

## 13. Development Principle

The project will be developed incrementally.

Each major change will be:

1. Implemented
2. Tested
3. Documented
4. Committed to Git
5. Pushed to GitHub

The `main` branch is kept stable while development is performed in
feature branches.