from unittest.mock import MagicMock

import pytest

import analyzer

GOOD = '{"verdict": "likely safe", "scam_type": "none", "evidence_phrases": [], "reasoning": "ok", "actions": []}'
LEAKY = "SECRET-REPLY-TEXT no json here"


def _reply(content: str, finish_reason: str = "stop") -> MagicMock:
    return MagicMock(choices=[MagicMock(message=MagicMock(content=content), finish_reason=finish_reason)])


def _client(*outcomes: object) -> MagicMock:
    client = MagicMock()
    client.with_options.return_value.chat.completions.create.side_effect = list(outcomes)
    return client


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(analyzer.time, "sleep", lambda _s: None)


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
    client.with_options.return_value.chat.completions.create.return_value = _reply("ok")

    assert analyzer.call_model(client, "hi") == ("ok", "stop")
    client.with_options.assert_called_once_with(
        timeout=analyzer.TIMEOUT_SECONDS, max_retries=analyzer.MAX_RETRIES
    )


def test_succeeds_on_third_attempt() -> None:
    client = _client(TimeoutError("x"), _reply(""), _reply(GOOD))

    result = analyzer.analyze("hello", client)

    assert result["notice"] is None and result["verdict"] == "likely safe"
    assert client.with_options.return_value.chat.completions.create.call_count == 3


def test_three_failures_fall_back_with_category_notice() -> None:
    client = _client(_reply(LEAKY), _reply(LEAKY), _reply("", "stop"))

    result = analyzer.analyze("hello", client)

    assert "3 attempts" in result["notice"]
    assert "empty reply (finish_reason=stop)" in result["notice"]
    assert "SECRET-REPLY-TEXT" not in result["notice"]
    assert result["scam_type"] == "unknown"


def test_debug_off_by_default(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.delenv("SECOND_LOOK_DEBUG", raising=False)

    analyzer.analyze("hello", _client(*[_reply(LEAKY)] * 3))

    captured = capsys.readouterr()
    assert "SECRET-REPLY-TEXT" not in captured.out + captured.err


def test_debug_on_prints_truncated_reply_to_stderr(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("SECOND_LOOK_DEBUG", "1")

    analyzer.analyze("hello", _client(*[_reply("x" * 500)] * 3))

    captured = capsys.readouterr()
    assert captured.out == "" and "x" * 300 in captured.err and "x" * 301 not in captured.err
