# CSV Data Pipeline

## 1. Overview

The CSV Pipeline is responsible for processing student data received
from a CSV file.

This pipeline is independent from the other data source pipelines.

---

## 2. Pipeline Flow

```text
CSV File
   ↓
Extract
   ↓
Source Validation
   ↓
Clean / Transform
   ↓
Prepared Dataset
```

---

## 3. Source

The input file is:

```text
data/raw/students.csv
```

The CSV extraction is handled by:

```text
app/sources/csv_source.py
```

The function used for extraction is:

```python
extract_csv()
```

---

## 4. Source Validation

After extraction, each CSV record is validated using:

```text
validate_source_rows()
```

The validation checks the required fields for CSV records.

Invalid records are separated from valid records.

---

## 5. Transformation

Valid CSV records are cleaned using:

```text
clean_student_row()
```

The cleaning process includes text normalization and city normalization.

---

## 6. Pipeline Implementation

The CSV-specific pipeline is implemented in:

```text
app/pipelines/csv_pipeline.py
```

The main function is:

```python
run_csv_pipeline()
```

Its responsibilities are:

1. Extract CSV records
2. Validate source records
3. Clean valid records
4. Return valid and rejected records

---

## 7. Result

The pipeline returns a `PipelineResult` containing:

```text
valid
rejected
```

This allows the integration stage to consume the prepared data later.

---

## 8. Testing

The existing project tests continue to pass after introducing the
CSV-specific pipeline.

The CSV pipeline was also executed independently.

Example result:

```text
Valid: 5
Rejected: 2
```

The existing test suite result was:

```text
10 passed
```

---

## 9. Design Principle

The CSV source is processed independently from the other data sources.

This allows the CSV pipeline to be tested, maintained, and extended
without coupling its extraction and preparation logic to the API,
PostgreSQL, MongoDB, or Web Scraping pipelines.