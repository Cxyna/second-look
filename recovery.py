"""Recovery checklist. Hardcoded on purpose: nothing here comes from the model."""
from collections.abc import Iterable
from typing import NamedTuple

from report_channels import REPORT_CHANNELS

LINK = "clicked a link"
LOGIN = "entered a password or login"
CODE = "shared a one-time code"
CARD_DETAILS = "entered card details"
BANK = "paid by bank transfer"
CARD_PAID = "paid by card"
GIFT = "bought gift cards"
CRYPTO = "sent crypto"
REMOTE = "gave remote access to my device"
ID_DOCS = "shared ID documents or personal details"
REPLIED = "replied to the message"

ACTIONS: tuple[str, ...] = (
    LINK, LOGIN, CODE, CARD_DETAILS, BANK, CARD_PAID, GIFT, CRYPTO, REMOTE, ID_DOCS, REPLIED,
)
URGENCY_ORDER: tuple[str, ...] = ("Do this now", "Today", "This week")


class Step(NamedTuple):
    text: str
    urgency: str
    actions: frozenset[str]  # empty = always included


def _s(text: str, urgency: str, *actions: str) -> Step:
    return Step(text, urgency, frozenset(actions))


# VERIFY: left out on purpose (not sure of exact standard wording/numbers):
#  - credit report checks / fraud alerts for shared ID documents (differs by country)
#  - contacting a crypto exchange or wallet provider (not confident it is standard advice)
#  - any phone numbers, deadlines, or what a bank/issuer can do (no legal or refund claims)
STEPS: tuple[Step, ...] = (
    _s("Stop replying to the message.", "Do this now"),
    _s("Keep screenshots and evidence. Don't delete the message.", "Today"),
    _s("Contact your bank using the number on your card.", "Do this now",
       CARD_DETAILS, BANK, CARD_PAID, CODE),
    _s("Freeze or cancel the card.", "Do this now", CARD_DETAILS, CARD_PAID),
    _s("Contact the gift card company straight away.", "Do this now", GIFT),
    _s("Disconnect the device from the internet.", "Do this now", REMOTE),
    _s("Remove the remote-access software.", "Do this now", REMOTE),
    _s("Change the password for that account, and for any other account where you used the same one.",
       "Do this now",
       LOGIN, CODE, REMOTE),
    _s("Turn on two-factor authentication.", "Today", LOGIN, CODE, REMOTE),
    _s("Run a security scan on your device.", "Today", LINK, REMOTE),
    _s("Check your statements for anything you don't recognise.", "Today",
       LOGIN, CODE, CARD_DETAILS, BANK, CARD_PAID, ID_DOCS),
    _s("Watch for follow-up scams. They often come next.", "This week", *ACTIONS),
)


def build_plan(actions: Iterable[str], country: str) -> list[Step]:
    """Merged, de-duplicated steps sorted by urgency, plus the country's reporting steps."""
    if country not in REPORT_CHANNELS:
        raise ValueError(f"Unsupported country: {country!r}")
    chosen = frozenset(actions)
    if not chosen:
        return []
    seen: set[str] = set()
    plan: list[Step] = []
    for step in STEPS:
        if (not step.actions or step.actions & chosen) and step.text not in seen:
            seen.add(step.text)
            plan.append(step)
    plan.sort(key=lambda s: URGENCY_ORDER.index(s.urgency))
    # Reporting comes last on purpose: it matters, but it is the least time-critical part.
    plan += [Step(line, "This week", frozenset()) for line in REPORT_CHANNELS[country]]
    return plan
