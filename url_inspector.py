"""Deep inspection of URLs and domain names for deceptive tricks."""
from __future__ import annotations

from urllib.parse import urlparse
import rules

# Suspicious / high-abuse TLDs often used for throwaway phishing
SUSPICIOUS_TLDS = {
    "xyz", "top", "buzz", "icu", "cfd", "click", "live", "vip", "club",
    "work", "online", "site", "rest", "surf", "fit", "sbs"
}


def inspect_url(raw_url: str) -> dict:
    url = raw_url.strip()
    if not url:
        return {"error": "Please enter a URL or domain."}

    # Add scheme if missing
    parsed_input = url if "://" in url else "//" + url
    try:
        parsed = urlparse(parsed_input)
        host = (parsed.hostname or "").lower().rstrip(".")
    except Exception:
        return {"error": "Invalid URL format."}

    if not host:
        return {"error": "Could not identify a valid domain host."}

    labels = host.split(".")
    if len(labels) < 2:
        return {"error": "Domain must contain at least a name and a top-level domain (e.g. example.com)."}

    # Determine registered domain (e.g., example.co.uk vs example.com)
    suffix_len = 2 if ".".join(labels[-2:]) in rules.SECOND_LEVEL_SUFFIXES else 1
    tld = ".".join(labels[-suffix_len:])
    registered_domain = ".".join(labels[-suffix_len - 1:])
    subdomains = labels[:-suffix_len - 1]
    subdomain_str = ".".join(subdomains) if subdomains else ""

    # Checks
    is_short = rules.is_shortener(url)
    lookalike_brand = rules.lookalike_domain(url)
    is_suspicious_tld = labels[-1] in SUSPICIOUS_TLDS

    # Deceptive subdomain trick: e.g. paypal.com.login-verify.xyz
    deceptive_subdomains = []
    for brand in rules.BRANDS:
        if brand in subdomains:
            deceptive_subdomains.append(brand)

    # Check whether the registered domain is an authentic brand
    is_official_brand = False
    official_for = None
    for brand, domains in rules.BRANDS.items():
        if registered_domain in domains:
            is_official_brand = True
            official_for = brand
            break

    # Calculate risk assessment
    risk_level = "Safe"
    risk_reasons = []

    if lookalike_brand:
        risk_level = "High Risk"
        risk_reasons.append(f"Domain is a typo or lookalike mimicking official brand '{lookalike_brand}'.")

    if deceptive_subdomains:
        risk_level = "High Risk"
        risk_reasons.append(
            f"Uses deceptive subdomain '{subdomain_str}' to pretend to be {', '.join(deceptive_subdomains).title()}, "
            f"while the actual destination is '{registered_domain}'."
        )

    if is_short:
        if risk_level != "High Risk":
            risk_level = "Suspicious"
        risk_reasons.append("URL shortener obscures the true destination link.")

    if is_suspicious_tld and not is_official_brand:
        if risk_level == "Safe":
            risk_level = "Suspicious"
        risk_reasons.append(f"Uses '.{labels[-1]}' which is a high-risk TLD frequently used in disposable phishing campaigns.")

    if is_official_brand:
        risk_level = "Safe"
        risk_reasons = [f"This is an official registered domain of {official_for.title()}."]

    return {
        "raw_url": raw_url,
        "host": host,
        "registered_domain": registered_domain,
        "subdomain": subdomain_str or "None (Root)",
        "tld": tld,
        "is_shortener": is_short,
        "lookalike_brand": lookalike_brand,
        "deceptive_subdomains": deceptive_subdomains,
        "is_official_brand": is_official_brand,
        "official_for": official_for,
        "risk_level": risk_level,
        "risk_reasons": risk_reasons,
    }
