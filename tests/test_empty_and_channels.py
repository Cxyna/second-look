from streamlit.testing.v1 import AppTest

import analyzer
from report_channels import REPORT_CHANNELS


def test_uk_reports_to_report_fraud_not_action_fraud() -> None:
    uk = " ".join(REPORT_CHANNELS["UK"])
    assert "reportfraud.police.uk" in uk
    assert "0300 123 2040" in uk
    assert "Police Scotland on 101" in uk
    assert "Action Fraud" not in uk


def test_blank_message_shows_notice_and_skips_model(monkeypatch) -> None:
    calls: list[str] = []
    monkeypatch.setattr(analyzer, "analyze", lambda m: calls.append(m))
    at = AppTest.from_file("../pages_/check.py").run()
    at.text_area(key="message").set_value("   ").run()
    at.button[-1].click().run()  # the Analyze button is the last button
    assert [w.value for w in at.warning] == ["Paste a message first."]
    assert calls == []
