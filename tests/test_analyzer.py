from unittest.mock import MagicMock

import analyzer


def _timeout_client() -> MagicMock:
    client = MagicMock()
    create = client.with_options.return_value.chat.completions.create
    create.side_effect = TimeoutError("timed out")
    return client


def test_timeout_falls_back_to_rules_only() -> None:
    result = analyzer.analyze("URGENT: verify your account now", _timeout_client())

    assert result["notice"] and "TimeoutError" in result["notice"]
    assert result["verdict"] in analyzer.VERDICTS
    assert result["evidence_phrases"] == []


def test_call_model_sets_timeout_and_one_retry() -> None:
    client = MagicMock()
    client.with_options.return_value.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="ok"))
    ]

    assert analyzer.call_model(client, "hi") == "ok"
    client.with_options.assert_called_once_with(
        timeout=analyzer.TIMEOUT_SECONDS, max_retries=analyzer.MAX_RETRIES
    )
