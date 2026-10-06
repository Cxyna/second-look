"""Tests for impersonation.py scenario data.

Rules enforced:
- Every required scenario key is present.
- check_steps always includes "use a number/account you already had".
- No statistics, refund or legal wording.
- No bare phone numbers or http URLs in scenario content.
- SAFE_WORD_ADVICE and IDENTITY_NOTE are non-empty strings.
"""
import re

import pytest

import impersonation
from impersonation import SCENARIOS, SAFE_WORD_ADVICE, IDENTITY_NOTE

REQUIRED_KEYS = {"how_it_works", "warning_signs", "check_steps", "questions", "never"}

EXPECTED_SCENARIOS = {
    "relative",
    "boss-colleague",
    "bank-tax-company",
    "wrong-number",
    "online-contact",
    "marketplace",
}

FORBIDDEN_WORDS = re.compile(
    r"\bstatistic|\bpercent|\brefund|\blegal right|\byour rights|\b\d+%",
    re.IGNORECASE,
)
BARE_PHONE = re.compile(r"\b\d{3}[\s\-]\d{3,4}\b")
BARE_URL = re.compile(r"https?://", re.IGNORECASE)

ALREADY_HAD_STEP = re.compile(
    r"(number|account)\s+you\s+already\s+had", re.IGNORECASE
)


def all_text(scenario: dict) -> str:
    """Flatten all string content in a scenario dict for bulk checks."""
    parts = [scenario.get("how_it_works", "")]
    for key in ("warning_signs", "check_steps", "questions", "never"):
        parts.extend(scenario.get(key, []))
    return " ".join(parts)


@pytest.mark.parametrize("key", sorted(EXPECTED_SCENARIOS))
def test_scenario_exists(key):
    assert key in SCENARIOS, f"Missing scenario: {key}"


@pytest.mark.parametrize("key", sorted(EXPECTED_SCENARIOS))
def test_scenario_has_required_keys(key):
    scenario = SCENARIOS[key]
    missing = REQUIRED_KEYS - scenario.keys()
    assert not missing, f"{key} missing keys: {missing}"


@pytest.mark.parametrize("key", sorted(EXPECTED_SCENARIOS))
def test_how_it_works_is_two_sentences(key):
    text = SCENARIOS[key]["how_it_works"].strip()
    # Rough check: at least one full stop, exclamation or question mark mid-text
    assert text.count(".") + text.count("!") + text.count("?") >= 2, (
        f"{key}: how_it_works should be 2 sentences"
    )


@pytest.mark.parametrize("key", sorted(EXPECTED_SCENARIOS))
def test_check_steps_count(key):
    steps = SCENARIOS[key]["check_steps"]
    assert 3 <= len(steps) <= 5, f"{key}: expected 3–5 check_steps, got {len(steps)}"


@pytest.mark.parametrize("key", sorted(EXPECTED_SCENARIOS))
def test_check_steps_includes_already_had_contact(key):
    steps = SCENARIOS[key]["check_steps"]
    combined = " ".join(steps)
    assert ALREADY_HAD_STEP.search(combined), (
        f"{key}: check_steps must include 'number/account you already had'"
    )


@pytest.mark.parametrize("key", sorted(EXPECTED_SCENARIOS))
def test_no_forbidden_words(key):
    text = all_text(SCENARIOS[key])
    match = FORBIDDEN_WORDS.search(text)
    assert not match, f"{key}: forbidden word found: {match.group()!r}"


@pytest.mark.parametrize("key", sorted(EXPECTED_SCENARIOS))
def test_no_bare_phone_numbers(key):
    text = all_text(SCENARIOS[key])
    match = BARE_PHONE.search(text)
    assert not match, f"{key}: bare phone number found: {match.group()!r}"


@pytest.mark.parametrize("key", sorted(EXPECTED_SCENARIOS))
def test_no_http_urls_in_scenarios(key):
    text = all_text(SCENARIOS[key])
    match = BARE_URL.search(text)
    assert not match, f"{key}: URL found in scenario text: {match.group()!r}"


@pytest.mark.parametrize("key", sorted(EXPECTED_SCENARIOS))
def test_questions_not_findable_on_social_media(key):
    questions = SCENARIOS[key]["questions"]
    assert len(questions) >= 2, f"{key}: should have at least 2 verification questions"
    # Spot-check: none should ask for name, birthday, city — all public info
    social_media_info = re.compile(
        r"\b(your name|date of birth|birthday|home town|hometown|city you live)\b",
        re.IGNORECASE,
    )
    for q in questions:
        assert not social_media_info.search(q), (
            f"{key}: question may be findable on social media: {q!r}"
        )


def test_safe_word_advice_exists():
    assert isinstance(SAFE_WORD_ADVICE, str) and SAFE_WORD_ADVICE.strip()


def test_identity_note_exists():
    assert isinstance(IDENTITY_NOTE, str) and IDENTITY_NOTE.strip()


def test_identity_note_does_not_claim_detection():
    # Must not claim to detect fake voices or video
    detection_claim = re.compile(
        r"\b(detect|identify|verify|confirm)\b.{0,40}\b(voice|video|fake|AI)\b",
        re.IGNORECASE,
    )
    assert not detection_claim.search(IDENTITY_NOTE), (
        "IDENTITY_NOTE must not claim to detect fake voices or video"
    )


def test_no_unexpected_scenarios():
    """Guard against scenario keys that don't have tests."""
    assert set(SCENARIOS.keys()) == EXPECTED_SCENARIOS, (
        f"Unexpected scenario keys: {set(SCENARIOS.keys()) ^ EXPECTED_SCENARIOS}"
    )
