import re
import unicodedata


def normalize_name(value: str) -> str:
    text = str(value or "").lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\b(jr|sr|ii|iii|iv)\b", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def title_case_name(value: str) -> str:
    return " ".join(word.capitalize() for word in str(value or "").split())
