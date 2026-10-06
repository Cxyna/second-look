from itertools import product

import pytest

import warn
from tests.test_simplify import RESULT, client_replying

GOOD = "Watch out for messages asking for gift cards. Don't click, don't reply, don't send money or codes. Keep it as evidence."
WHO, LEN = "a friend", "text message"


def draft(reply, who=WHO, length=LEN, result=RESULT):
    return warn.draft_warning(result, who, length, client_replying(reply))


def test_good_reply_is_shown() -> None:
    assert draft(GOOD) == GOOD


@pytest.mark.parametrize("bad", [
    "Do not open http://x.com", "Avoid bank-help.co.uk", "Write to me@mail.com", "Call 0123456789 now",
    "Call 555 123 4567", "Code 12-345", "Please delete it", "Erase it", "Just ignore it", "",
    None, "word " * 100, "<b>Careful</b>", "**Careful**", "# Careful",
])
def test_bad_reply_falls_back(bad) -> None:
    assert draft(bad) == warn.fallback("gift card", WHO, LEN)


def test_long_note_limit() -> None:
    assert draft("a" * 901, length="longer note") == warn.fallback("gift card", WHO, "longer note")
    ok = ("Be careful. " * 70).strip()
    assert draft(ok, length="longer note") == ok


def test_timeout_falls_back() -> None:
    out = warn.draft_warning(RESULT, WHO, LEN, client_replying(error=TimeoutError()))
    assert out == warn.fallback("gift card", WHO, LEN)


def test_final_text_is_redacted() -> None:
    assert "@" not in draft("Be careful with 123-45-6789 ok")


def test_prompt_has_only_result_fields() -> None:
    result = {**RESULT, "evidence_phrases": ["a", "b", "c", "d"], "original": "SECRET ORIGINAL"}
    prompt = warn.build_prompt(result, WHO, LEN)
    assert "SECRET ORIGINAL" not in prompt
    assert "likely scam" in prompt and "It asks for gift cards." in prompt
    assert "a" in prompt and "\nd\n" not in prompt  # max 3 phrases
    assert "untrusted" in prompt and "300" in prompt


@pytest.mark.parametrize("who, length", list(product(warn.WHO, warn.LIMITS)))
def test_every_fallback_exists_and_passes(who: str, length: str) -> None:
    for category in warn.CATEGORIES:
        text = warn.fallback(category, who, length)
        assert warn.is_safe(text, length), (category, who, length)
        assert "don't click" in text.lower() and "evidence" in text.lower()


@pytest.mark.parametrize("scam_type, category", [
    ("parcel delivery fee", "parcel fee"), ("bank impersonation", "bank impersonation"),
    ("gift card", "gift card"), ("boss request", "gift card"), ("romance scam", "romance"),
    ("wrong number", "romance"), ("crypto investment", "investment"), ("tax refund", "tax"),
    ("unknown", "generic"),
])
def test_scam_type_mapping(scam_type: str, category: str) -> None:
    assert warn.fallback(scam_type, WHO, LEN) == warn.fallback(category, WHO, LEN)
