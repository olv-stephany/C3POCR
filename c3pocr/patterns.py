import re
from typing import Any

FIELD_PATTERNS = {
    "valor_total": re.compile(r"^valor\s*total$", re.IGNORECASE),
    "data": re.compile(r"^(dia|data)$", re.IGNORECASE),
}
VALUE_PATTERNS = {
    "valor": re.compile(r"^R?\$?\s*\d+(?:[.,]\d{2})$"),
    "data": re.compile(r"^\d{1,2}/\d{1,2}(?:/\d{2,4})?$"),
}


def parse_lines(text: str) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    for line in text.splitlines():
        clean_line = re.sub(r"\s+", " ", line).strip()
        parts = re.split(r"\s*(?:\.{2,}|:)\s*", clean_line, maxsplit=1)
        if len(parts) != 2:
            continue
        label, raw_value = (part.strip() for part in parts)
        for field_name, label_pattern in FIELD_PATTERNS.items():
            if not label_pattern.fullmatch(label):
                continue
            if field_name == "valor_total" and VALUE_PATTERNS["valor"].fullmatch(raw_value):
                number = raw_value.replace("R$", "").replace("$", "").strip()
                fields[field_name] = {"value": float(number.replace(".", "").replace(",", ".")), "raw_value": raw_value}
            elif field_name == "data" and VALUE_PATTERNS["data"].fullmatch(raw_value):
                fields[field_name] = {"value": raw_value, "raw_value": raw_value}
    return fields
