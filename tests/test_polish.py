from pathlib import Path

import accuracy_data as ad
from pages_.registry import PAGES
from ui.theme import VERDICT_ICONS, accuracy_tile_html

ROOT = Path(__file__).resolve().parent.parent


def test_verdict_icons_are_distinct_static_svg():
    assert set(VERDICT_ICONS) == {"scam", "warn", "safe"}
    assert len(set(VERDICT_ICONS.values())) == 3
    for svg in VERDICT_ICONS.values():
        assert svg.startswith("<svg") and 'aria-hidden="true"' in svg and "currentColor" in svg
        assert all(ord(c) < 0x2190 for c in svg)  # no emoji


def test_accuracy_tile_matches_accuracy_data():
    tile = accuracy_tile_html()
    r = ad.RESULTS["hybrid"]["accuracy"]
    assert f"{r}% accuracy on {ad.N_MESSAGES} unseen test messages" in tile
    page = next(p for p in PAGES if p.title == "How accurate is it?")
    assert f'st.page_link("{page.path}"' in (ROOT / "pages_" / "home.py").read_text(encoding="utf-8")


def test_check_page_wording():
    src = (ROOT / "pages_" / "check.py").read_text(encoding="utf-8")
    assert "Rule score" not in src
    assert "Rule-based checks (links and phrases):" in src
    assert "The verdict combines these rule checks with the AI model's reading of the message." in src
    assert "Please don't type names or addresses." in src
    for emoji in ("🚫", "⚠", "✅"):
        assert emoji not in src


def test_home_has_no_todo_or_typed_number():
    src = (ROOT / "pages_" / "home.py").read_text(encoding="utf-8")
    assert "TODO" not in src and "92" not in src


def test_highlight_escapes_html() -> None:
    from ui.theme import highlight
    msg = "<script>alert(1)</script> pay </mark> now"
    out = highlight(msg, ["</mark>", "<script>"])
    assert "<script>" not in out and "&lt;script&gt;" in out
    assert out.count("</mark>") == 2 and "&lt;/mark&gt;" in out


SAFE_BADGE = "No warning signs found by our checks"


def _render_check(monkeypatch, verdict: str, **rule_overrides) -> str:
    from streamlit.testing.v1 import AppTest
    import analyzer

    rules = {"score": 0, "shorteners": [], "lookalikes": {}, "patterns": [], **rule_overrides}
    result = {
        "verdict": verdict, "scam_type": "unknown", "notice": "", "reasoning": "r",
        "actions": [], "evidence_phrases": [], "rules": rules,
    }
    monkeypatch.setattr(analyzer, "analyze", lambda _text: result)
    at = AppTest.from_file(str(ROOT / "pages_" / "check.py"), default_timeout=30)
    at.run()
    at.text_area(key="message").set_value("hello").run()
    next(b for b in at.button if b.label == "Analyze").click().run()
    assert not at.exception
    return "".join(str(e.value) for e in at.get("html"))


def test_safe_badge_wording_and_verdict_restriction(monkeypatch) -> None:
    src = (ROOT / "pages_" / "check.py").read_text(encoding="utf-8")
    assert "No Suspicious Links or Requests" not in src

    assert SAFE_BADGE in _render_check(monkeypatch, "likely safe")
    for verdict in ("likely scam", "suspicious", "unknown"):
        assert SAFE_BADGE not in _render_check(monkeypatch, verdict)
    # a clean "likely safe" with a rule signal must not claim "no warning signs"
    assert SAFE_BADGE not in _render_check(monkeypatch, "likely safe", patterns=["urgency"])
