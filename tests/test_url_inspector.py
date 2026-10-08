import pytest
import url_inspector


def test_inspect_empty():
    res = url_inspector.inspect_url("")
    assert "error" in res


def test_inspect_official_brand():
    res = url_inspector.inspect_url("https://www.paypal.com/signin")
    assert res["is_official_brand"] is True
    assert res["official_for"] == "paypal"
    assert res["risk_level"] == "Safe"


def test_inspect_deceptive_subdomain():
    res = url_inspector.inspect_url("https://paypal.com.verify-login.xyz/auth")
    assert res["registered_domain"] == "verify-login.xyz"
    assert "paypal" in res["deceptive_subdomains"]
    assert res["risk_level"] == "High Risk"


def test_inspect_lookalike_domain():
    res = url_inspector.inspect_url("http://paypa1-security.com")
    assert res["lookalike_brand"] == "paypal"
    assert res["risk_level"] == "High Risk"


def test_inspect_shortener():
    res = url_inspector.inspect_url("https://bit.ly/claim-prize")
    assert res["is_shortener"] is True
    assert res["risk_level"] == "Suspicious"
