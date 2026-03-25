from io import BytesIO
import pandas as pd
from app.utils.normalizer import normalize_name, title_case_name


NAME_PRIORITIES = [
    "full name",
    "fullname",
    "student name",
    "grantee name",
    "beneficiary name",
    "name",
]


def _detect_name_column(columns: list[str]):
    lowered = [str(c).strip().lower() for c in columns]
    for key in NAME_PRIORITIES:
        for idx, col in enumerate(lowered):
            if col == key or key in col:
                return columns[idx]
    return None


def _build_name_from_parts(row: dict, columns: list[str]):
    lowered_map = {str(c).strip().lower(): c for c in columns}
    last = next((lowered_map[c] for c in lowered_map if "last" in c), None)
    first = next((lowered_map[c] for c in lowered_map if "first" in c), None)
    middle = next((lowered_map[c] for c in lowered_map if "middle" in c), None)
    suffix = next((lowered_map[c] for c in lowered_map if "suffix" in c or "extension" in c), None)
    parts = [row.get(last, ""), row.get(first, ""), row.get(middle, ""), row.get(suffix, "")]
    return " ".join(str(p).strip() for p in parts if str(p).strip())


def parse_excel(file_bytes: bytes):
    df = pd.read_excel(BytesIO(file_bytes), dtype=str).fillna("")
    rows = df.to_dict(orient="records")
    columns = list(df.columns)
    detected_name_col = _detect_name_column(columns)
    parsed = []
    for row in rows:
        if detected_name_col:
            full_name = row.get(detected_name_col, "")
        else:
            full_name = _build_name_from_parts(row, columns)
        normalized_name = normalize_name(full_name)
        if not normalized_name:
            continue
        parsed.append(
            {
                "full_name": title_case_name(full_name),
                "normalized_name": normalized_name,
                "source_row": row,
            }
        )
    return parsed, columns
