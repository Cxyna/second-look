import re

import pytest

from recovery import ACTIONS, STEPS, URGENCY_ORDER, build_plan
from report_channels import REPORT_CHANNELS

BANNED = re.compile(r"\b(legal|law|rights?|refund\w*|reimburs\w*|compensat\w*)\b", re.I)


@pytest.mark.parametrize("action", ACTIONS)
def test_every_action_returns_at_least_one_specific_step(action: str) -> None:
    always = {s.text for s in STEPS if not s.actions}
    specific = [s for s in build_plan([action], "UK") if s.text not in always]
    assert specific


def test_urgent_steps_come_before_later_ones() -> None:
    plan = build_plan(list(ACTIONS), "US")
    ranks = [URGENCY_ORDER.index(s.urgency) for s in plan]
    assert ranks == sorted(ranks)
    assert plan[0].urgency == "Do this now"


def test_duplicates_are_merged_across_actions() -> None:
    plan = build_plan(list(ACTIONS), "UK")
    texts = [s.text for s in plan]
    assert len(texts) == len(set(texts))


def test_always_included_steps_present() -> None:
    text = " ".join(s.text.lower() for s in build_plan(["clicked a link"], "UK"))
    assert "stop replying" in text
    assert "screenshot" in text


def test_empty_selection_gives_no_plan() -> None:
    assert build_plan([], "UK") == []


def test_uk_and_us_reporting_steps_differ() -> None:
    uk = {s.text for s in build_plan(["clicked a link"], "UK")}
    us = {s.text for s in build_plan(["clicked a link"], "US")}
    assert uk != us
    for country, plan in (("UK", uk), ("US", us)):
        for line in REPORT_CHANNELS[country]:
            assert line in plan


def test_gift_card_company_step_only_for_gift_cards() -> None:
    text = "Contact the gift card company straight away."
    assert text in {s.text for s in build_plan(["bought gift cards"], "UK")}
    others = [a for a in ACTIONS if a != "bought gift cards"]
    assert text not in {s.text for s in build_plan(others, "UK")}


def test_no_legal_or_refund_claims() -> None:
    texts = [s.text for s in STEPS] + [l for lines in REPORT_CHANNELS.values() for l in lines]
    assert not [t for t in texts if BANNED.search(t)]


def test_unknown_country_raises_clear_error() -> None:
    with pytest.raises(ValueError, match="country"):
        build_plan(["clicked a link"], "FR")
