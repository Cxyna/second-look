"""Eval numbers copied from eval/results_fresh_dev.md (tests/test_accuracy.py checks they match)."""
from math import sqrt

N_MESSAGES, N_SCAM, N_LEGIT = 50, 22, 28

# tp/fn = actual scams caught/missed; fp/tn = actual legit flagged/passed. Percentages are whole numbers.
RESULTS: dict[str, dict] = {
    "rules": {"label": "Rules only", "accuracy": 58, "precision": 100, "recall": 5, "f1": 0.09,
              "tp": 1, "fn": 21, "fp": 0, "tn": 28, "errors": 0},
    "model": {"label": "AI model only", "accuracy": 94, "precision": 95, "recall": 90, "f1": 0.92,
              "tp": 18, "fn": 2, "fp": 1, "tn": 26, "errors": 3},
    "hybrid": {"label": "Full app (rules + AI)", "accuracy": 92, "precision": 95, "recall": 86, "f1": 0.90,
               "tp": 19, "fn": 3, "fp": 1, "tn": 27, "errors": 0},
}

# Development history, given by the team; NOT an unseen test (the prompt was improved using this run).
# VERIFY: 20 scam + 20 legit = 40 messages is implied by the counts, not stated in any eval file.
BEFORE_TUNING: dict[str, dict] = {
    "model": {"label": "AI model only", "fp": 10, "tn": 10, "tp": 20, "fn": 0, "accuracy": 75},
    "hybrid": {"label": "Full app (rules + AI)", "fp": 13, "tn": 7, "tp": 20, "fn": 0, "accuracy": 68},
}


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a proportion. No data means the widest range."""
    if total == 0:
        return 0.0, 1.0
    if not 0 <= successes <= total:
        raise ValueError("successes must be between 0 and total")
    p = successes / total
    d = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / d
    half = z * sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / d
    return max(0.0, centre - half), min(1.0, centre + half)
