import csv
from pathlib import Path


def export_to_csv(
    file_path: Path,
    rows: list[dict],
) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        file_path.write_text("", encoding="utf-8")
        return

    columns = list(rows[0].keys())

    with file_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=columns,
        )

        writer.writeheader()
        writer.writerows(rows)