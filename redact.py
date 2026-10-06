"""Privacy shield: mask personal numbers and emails before text leaves the app."""
import re

_MONTHS = "jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec"
_FLAGS = re.IGNORECASE

# Spans that must survive untouched. Swapped for sentinels, restored at the end.
_PROTECT = [
    re.compile(r"(?:https?://|www\.)\S+", _FLAGS),
    re.compile(r"[£$€]\s?\d[\d,]*(?:\.\d+)?"),
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    re.compile(r"\b\d{1,2}[/.]\d{1,2}[/.]\d{2,4}\b"),
    re.compile(rf"\b\d{{1,2}}(?:st|nd|rd|th)?\s+(?:{_MONTHS})[a-z]*\.?,?\s+\d{{4}}\b", _FLAGS),
    re.compile(r"#\s?\d+|\border(?:\s+(?:number|no\.?|id))?\s*:?\s*#?\d+", _FLAGS),
]
_EMAIL = re.compile(r"[\w.+-]{1,64}@[\w-]{1,63}(?:\.[\w-]{1,63}){1,8}")
# Bare domains (with optional path) are protected after emails are masked.
_DOMAIN = re.compile(r"\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,}(?:/\S*)?", _FLAGS)
_IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,3})?\b")
_SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_NI = re.compile(r"\b[A-Z]{2} ?\d{2} ?\d{2} ?\d{2} ?[A-D]\b")
_ACCOUNT = re.compile(
    r"\b\d{2}[- ]\d{2}[- ]\d{2}\b[\s,;:]*(?:(?:account|acc|a/c|number|no\.?)[\s:.,#]*){0,3}\d{8}\b",
    _FLAGS,
)
_CARD = re.compile(r"\b\d(?:[ -]?\d){12,18}\b")
_PHONE = re.compile(
    r"(?:\+44[ -]?|\b0)\d(?:[ -]?\d){8,9}\b"
    r"|(?:\+1[ -.]?)?(?:\(\d{3}\)|\b\d{3})[ -.]?\d{3}[ -.]\d{4}\b"
)
_KEY = r"(?:code|otp|passcode|pin)"
_OTP_AFTER = re.compile(rf"(\b{_KEY}\b[^\d\n]{{0,15}}?)\b\d{{4,8}}\b", _FLAGS)
_OTP_BEFORE = re.compile(rf"\b\d{{4,8}}\b(?=[^\d\n]{{0,15}}\b{_KEY}\b)", _FLAGS)

_SENTINEL = re.compile("([-]+)")
_PUA = re.compile("[-]")
_FAILED = "[message hidden: could not be checked]"


def _luhn(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
    return total % 10 == 0


def _token(i: int) -> str:
    return "" + "".join(chr(0xE100 + int(d)) for d in str(i)) + ""


def redact(text: str) -> tuple[str, list[tuple[str, int]]]:
    """Return (masked text, [(type, count), ...]). The report never holds original values."""
    if not isinstance(text, str):
        return "", []
    try:
        counts: dict[str, int] = {}
        kept: list[str] = []

        def mask(kind: str, placeholder: str):
            def repl(m: re.Match) -> str:
                counts[kind] = counts.get(kind, 0) + 1
                return placeholder
            return repl

        def keep(m: re.Match) -> str:
            kept.append(m.group(0))
            return _token(len(kept) - 1)

        def card(m: re.Match) -> str:
            return mask_cards(m.group(0))

        def mask_cards(s: str) -> str:
            # Windows aligned to digit groups, so a neighbouring number can't hide a card
            # but an invalid number can't match through a Luhn-valid slice of itself.
            groups = list(re.finditer(r"\d+", s))
            for a in range(len(groups)):
                digits, best = "", None
                for j in range(a, len(groups)):
                    digits += groups[j].group(0)
                    if len(digits) > 19:
                        break
                    if len(digits) >= 13 and _luhn(digits):
                        best = j
                if best is not None:
                    counts["card"] = counts.get("card", 0) + 1
                    return s[: groups[a].start()] + "[CARD]" + mask_cards(s[groups[best].end() :])
            return s

        def otp(m: re.Match) -> str:
            counts["code"] = counts.get("code", 0) + 1
            return m.group(1) + "[CODE]"

        out = _PUA.sub("", text)
        for p in _PROTECT:
            out = p.sub(keep, out)
        out = _EMAIL.sub(mask("email", "[EMAIL]"), out)
        out = _DOMAIN.sub(keep, out)
        out = _IBAN.sub(mask("id", "[ID]"), out)
        out = _SSN.sub(mask("id", "[ID]"), out)
        out = _NI.sub(mask("id", "[ID]"), out)
        out = _ACCOUNT.sub(mask("account", "[ACCOUNT]"), out)
        out = _PHONE.sub(mask("phone", "[PHONE]"), out)
        out = _CARD.sub(card, out)
        out = _OTP_AFTER.sub(otp, out)
        out = _OTP_BEFORE.sub(mask("code", "[CODE]"), out)
        out = _SENTINEL.sub(lambda m: kept[int("".join(str(ord(c) - 0xE100) for c in m.group(1)))], out)
        order = ["email", "phone", "card", "account", "id", "code"]
        return out, [(k, counts[k]) for k in order if k in counts]
    except Exception:
        # Fail closed: never let unmasked text through if masking itself breaks.
        return _FAILED, []
