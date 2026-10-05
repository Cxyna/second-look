from rules import (
    extract_urls,
    find_patterns,
    is_shortener,
    lookalike_domain,
    run_rules,
)


def test_extract_urls_finds_multiple():
    text = "see http://a.com/x and https://b.org then www.c.net"
    assert extract_urls(text) == ["http://a.com/x", "https://b.org", "www.c.net"]


def test_extract_urls_strips_trailing_punctuation():
    assert extract_urls("go to (https://a.com/x).") == ["https://a.com/x"]


def test_extract_urls_none_found():
    assert extract_urls("no links here") == []


def test_extract_urls_empty():
    assert extract_urls("") == []


def test_is_shortener_known():
    assert is_shortener("https://bit.ly/abc")
    assert is_shortener("http://TinyURL.com/x")


def test_is_shortener_legit_site_not_flagged():
    assert not is_shortener("https://amazon.com/dp/123")


def test_is_shortener_lookalike_host_not_flagged():
    assert not is_shortener("https://notbit.ly.com/x")


def test_is_shortener_bare_host_without_scheme():
    assert is_shortener("bit.ly/abc")


def test_is_shortener_empty():
    assert not is_shortener("")


def test_lookalike_digit_substitution():
    assert lookalike_domain("https://paypa1.com/login") == "paypal"
    assert lookalike_domain("http://amaz0n.com") == "amazon"


def test_lookalike_one_letter_typo():
    assert lookalike_domain("https://amazom.com") == "amazon"


def test_lookalike_brand_in_subdomain_of_other_site():
    assert lookalike_domain("https://amazon.com.evil.io/x") == "amazon"


def test_lookalike_legit_amazon_not_flagged():
    assert lookalike_domain("https://amazon.com/dp/123") is None
    assert lookalike_domain("https://www.amazon.com") is None
    assert lookalike_domain("https://smile.amazon.com") is None


def test_lookalike_unrelated_domain_not_flagged():
    assert lookalike_domain("https://maple.com") is None
    assert lookalike_domain("https://example.org") is None


def test_lookalike_empty():
    assert lookalike_domain("") is None


def test_find_patterns_scam_message_flags_several():
    found = find_patterns("Act now! Verify your account password or buy a gift card")
    assert {"urgency", "credentials", "payment"} <= set(found)


def test_find_patterns_case_insensitive():
    assert "urgency" in find_patterns("ACT NOW")


def test_find_patterns_benign_message_not_flagged():
    assert find_patterns("Lunch at noon? Your Amazon order has shipped.") == []


def test_find_patterns_empty():
    assert find_patterns("") == []


def test_run_rules_clean_message_with_legit_link_scores_zero():
    result = run_rules("Your order shipped: https://www.amazon.com/dp/123")
    assert result["urls"] == ["https://www.amazon.com/dp/123"]
    assert result["shorteners"] == []
    assert result["lookalikes"] == {}
    assert result["patterns"] == []
    assert result["score"] == 0


def test_run_rules_phishing_message_scores_high():
    result = run_rules("Act now! Verify your account at http://paypa1.com/login")
    assert result["lookalikes"] == {"http://paypa1.com/login": "paypal"}
    assert result["score"] >= 70


def test_run_rules_shortener_flagged():
    result = run_rules("click https://bit.ly/abc")
    assert result["shorteners"] == ["https://bit.ly/abc"]
    assert 0 < result["score"] < 70


def test_run_rules_score_capped_at_100():
    text = "Act now verify your account gift card http://paypa1.com http://bit.ly/x"
    assert run_rules(text)["score"] == 100


def test_run_rules_empty():
    assert run_rules("") == {
        "urls": [],
        "shorteners": [],
        "lookalikes": {},
        "patterns": [],
        "score": 0,
    }


def test_lookalike_hyphenated_brand_flagged():
    assert lookalike_domain("https://paypal-secure.com") == "paypal"
    assert lookalike_domain("https://secure-paypal.com") == "paypal"


def test_lookalike_brand_cctld_not_flagged():
    assert lookalike_domain("https://www.google.co.uk") is None
    assert lookalike_domain("https://login.paypal.co.uk") is None


def test_lookalike_cctld_with_fake_subdomain_still_flagged():
    assert lookalike_domain("https://paypal.co.uk.evil.io") == "paypal"


def test_trailing_dot_host_legit_not_flagged():
    assert lookalike_domain("https://paypal.com.") is None


def test_trailing_dot_host_shortener_detected():
    assert is_shortener("https://bit.ly./x")


def test_malformed_ipv6_does_not_raise():
    assert not is_shortener("http://[::1")
    assert lookalike_domain("http://[::1") is None


def test_run_rules_duplicate_urls_counted_once():
    result = run_rules("https://bit.ly/a https://bit.ly/a https://bit.ly/a")
    assert result["urls"] == ["https://bit.ly/a"]
    assert result["score"] == 25


def test_extract_urls_bare_domains():
    text = "visit usps-package-hold.top/update or bit.ly/3xEvriPay or goo.gl/Xk29Ls now"
    assert extract_urls(text) == [
        "usps-package-hold.top/update",
        "bit.ly/3xEvriPay",
        "goo.gl/Xk29Ls",
    ]


def test_extract_urls_bare_common_tld_and_co_uk():
    assert extract_urls("go to example.co.uk, or foo.com.") == ["example.co.uk", "foo.com"]


def test_extract_urls_ignores_ordinary_text():
    assert extract_urls("Use e.g. a card, i.e. 3.50 or file.txt. Hi.There") == []


def test_extract_urls_ignores_email_domain():
    assert extract_urls("mail john.smith@gmail.com") == []


def test_shortener_bare_domain_scores():
    assert run_rules("pay at goo.gl/Xk29Ls")["shorteners"] == ["goo.gl/Xk29Ls"]


def test_lookalike_brand_in_unrelated_domain():
    assert lookalike_domain("amazon-account-verify.top") == "amazon"
    assert lookalike_domain("https://usps-package-hold.top/update") == "usps"
    assert lookalike_domain("https://chase-secure.net") == "chase"
    assert lookalike_domain("https://royalmail-redelivery.com") == "royalmail"
    assert lookalike_domain("https://hmrc.gov.uk.evil.io") == "hmrc"
    assert lookalike_domain("https://paypal.xyz") == "paypal"


def test_lookalike_real_brand_domains_not_flagged():
    for url in (
        "https://www.chase.com/login", "https://barclays.co.uk", "https://www.hmrc.gov.uk/x",
        "https://irs.gov", "https://amazon.com", "https://nike.com", "https://bestbuy.com",
        "https://tracking.dhl.com", "https://www.lloydsbank.com", "https://dvla.gov.uk",
    ):
        assert lookalike_domain(url) is None, url


def test_short_brand_names_not_substring_matched():
    assert lookalike_domain("https://groups.com") is None
    assert lookalike_domain("https://cups.org") is None


def test_run_rules_legit_messages_with_real_links_score_zero():
    for msg in (
        "Your Chase statement is ready: chase.com/statements",
        "Refund details at www.hmrc.gov.uk/refunds",
        "Track at amazon.com/orders or barclays.co.uk/help. Total 3.50, e.g. cash",
        "Shoes at nike.com and deals at bestbuy.com/deals",
    ):
        assert run_rules(msg)["score"] == 0, msg


def test_run_rules_bare_domain_scam_scores():
    assert run_rules("Parcel held: usps-package-hold.top/update")["score"] >= 40


def test_extract_urls_scam_tlds_without_path():
    assert extract_urls("see paypal-secure.app and usps-hold.shop") == [
        "paypal-secure.app",
        "usps-hold.shop",
    ]


def test_extract_urls_ignores_missing_space_prose():
    assert extract_urls("done.Help ok.Link Thanks.Me see.Top") == []


def test_lookalike_regional_real_domains_not_flagged():
    for url in ("https://amazon.de", "https://www.amazon.in", "https://google.ca",
                "https://paypal.de", "https://login.microsoftonline.com"):
        assert lookalike_domain(url) is None, url


def test_lookalike_plural_not_treated_as_typo():
    assert lookalike_domain("https://apples.com") is None
    assert lookalike_domain("https://googles.com") is None
