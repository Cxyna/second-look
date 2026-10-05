import re
from difflib import SequenceMatcher
from urllib.parse import urlparse

URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>\"']+", re.IGNORECASE)
TRAILING_PUNCT = ".,;:!?)]}"
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "ow.ly"}
BRANDS = ("amazon", "paypal", "google", "apple", "microsoft", "netflix")
DIGIT_FIX = str.maketrans("013", "ole")
SECOND_LEVEL_SUFFIXES = {"co.uk", "com.au", "co.jp", "com.br"}
TYPO_RATIO = 0.8
LOOKALIKE_POINTS = 40
SHORTENER_POINTS = 25
PATTERN_POINTS = 20
MAX_SCORE = 100


def extract_urls(text: str) -> list[str]:
    return [m.rstrip(TRAILING_PUNCT) for m in URL_RE.findall(text)]


def _host(url: str) -> str:
    if "://" not in url:
        url = "//" + url
    try:
        host = urlparse(url).hostname or ""
    except ValueError:
        return ""
    return host.lower().rstrip(".")


def is_shortener(url: str) -> bool:
    return _host(url) in SHORTENERS


def _is_typo_of(label: str, brand: str) -> bool:
    fixed = label.translate(DIGIT_FIX)
    return fixed == brand or SequenceMatcher(None, fixed, brand).ratio() > TYPO_RATIO


def lookalike_domain(url: str) -> str | None:
    labels = _host(url).split(".")
    if len(labels) < 2:
        return None
    suffix_len = 2 if ".".join(labels[-2:]) in SECOND_LEVEL_SUFFIXES else 1
    if len(labels) <= suffix_len:
        return None
    name = labels[-suffix_len - 1]
    subdomains = labels[: -suffix_len - 1]
    if name in BRANDS:
        return None
    for brand in BRANDS:
        if brand in subdomains or any(_is_typo_of(p, brand) for p in name.split("-")):
            return brand
    return None


PATTERNS = {
    "urgency": re.compile(r"\b(act now|urgent|immediately|within 24 hours|final notice|suspended)\b", re.I),
    "credentials": re.compile(r"\b(verify your (account|identity)|password|login|confirm your)\b", re.I),
    "payment": re.compile(r"\b(gift cards?|wire transfer|bitcoin|crypto|western union)\b", re.I),
}


def find_patterns(text: str) -> list[str]:
    return [name for name, rx in PATTERNS.items() if rx.search(text)]


def run_rules(text: str) -> dict:
    urls = list(dict.fromkeys(extract_urls(text)))
    shorteners = [u for u in urls if is_shortener(u)]
    lookalikes = {u: b for u in urls if (b := lookalike_domain(u))}
    patterns = find_patterns(text)
    score = (
        LOOKALIKE_POINTS * len(lookalikes)
        + SHORTENER_POINTS * len(shorteners)
        + PATTERN_POINTS * len(patterns)
    )
    return {
        "urls": urls,
        "shorteners": shorteners,
        "lookalikes": lookalikes,
        "patterns": patterns,
        "score": min(score, MAX_SCORE),
    }
