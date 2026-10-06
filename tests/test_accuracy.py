"""accuracy_data.py must match eval/results_fresh_dev.md; wilson_interval sanity; pages enabled."""
import re
from pathlib import Path

import pytest

import accuracy_data as ad
from pages_.registry import PAGES

MD = (Path(__file__).parent.parent / "eval" / "results_fresh_dev.md").read_text(encoding="utf-8")
NAMES = {"rules-only": "rules", "model-only": "model", "hybrid": "hybrid"}


def _table_rows():
    rows = {}
    for m in re.finditer(r"^\| (rules-only|model-only|hybrid) \| (\d+)% \| (\d+)% \| (\d+)% \| ([\d.]+) \| (\d+) \|", MD, re.M):
        rows[NAMES[m[1]]] = tuple(float(x) if "." in x else int(x) for x in m.groups()[1:])
    return rows


def _matrices():
    out = {}
    for name in NAMES:
        sec = MD.split(f"## {name}")[1]
        nums = re.findall(r"\*\*Actually (?:scam|legit)\*\* \| (\d+) \| (\d+)", sec)[:2]
        out[NAMES[name]] = tuple(int(n) for pair in nums for n in pair)
    return out


@pytest.mark.parametrize("key", ["rules", "model", "hybrid"])
def test_numbers_match_results_file(key):
    acc, prec, rec, f1, errs = _table_rows()[key]
    d = ad.RESULTS[key]
    assert (d["accuracy"], d["precision"], d["recall"], d["f1"], d["errors"]) == (acc, prec, rec, f1, errs)
    assert (d["tp"], d["fn"], d["fp"], d["tn"]) == _matrices()[key]


def test_dev_header_counts():
    assert "50 messages (22 scam, 28 legitimate)" in MD
    assert (ad.N_MESSAGES, ad.N_SCAM, ad.N_LEGIT) == (50, 22, 28)


def test_before_tuning_row():
    b = ad.BEFORE_TUNING
    assert (b["model"]["fp"], b["model"]["tp"], b["model"]["accuracy"]) == (10, 20, 75)
    assert (b["hybrid"]["fp"], b["hybrid"]["tp"], b["hybrid"]["accuracy"]) == (13, 20, 68)


def test_wilson_known_values():
    lo, hi = ad.wilson_interval(19, 22)
    assert lo == pytest.approx(0.6666, abs=1e-3) and hi == pytest.approx(0.9526, abs=1e-3)
    lo, hi = ad.wilson_interval(0, 10)
    assert lo == 0 and 0.25 < hi < 0.3
    lo, hi = ad.wilson_interval(10, 10)
    assert hi == 1 and 0.7 < lo < 0.75


def test_wilson_edge_cases():
    assert ad.wilson_interval(0, 0) == (0.0, 1.0)
    with pytest.raises(ValueError):
        ad.wilson_interval(5, 3)


def test_pages_enabled_no_coming_soon():
    assert all(p.enabled for p in PAGES)
    for p in PAGES:
        assert Path(__file__).parent.parent.joinpath(p.path).exists()


def test_pages_no_banned_claims():
    root = Path(__file__).parent.parent / "pages_"
    text = (root / "accuracy.py").read_text(encoding="utf-8") + (root / "about.py").read_text(encoding="utf-8")
    for word in ("state of the art", "state-of-the-art", "cookie", "encrypt", "GDPR", "compliant"):
        assert word.lower() not in text.lower()
