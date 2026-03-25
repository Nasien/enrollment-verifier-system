from rapidfuzz import fuzz


def score_name(a: str, b: str) -> int:
    return int(fuzz.ratio(a, b))
