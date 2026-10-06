import pytest

from redact import redact


def masked(text: str) -> str:
    return redact(text)[0]


def report(text: str) -> dict[str, int]:
    return dict(redact(text)[1])


def test_valid_luhn_card_masked() -> None:
    for card in ("4111111111111111", "4111 1111 1111 1111", "4111-1111-1111-1111"):
        assert masked(f"card {card} ok") == "card [CARD] ok"
    assert report("4111 1111 1111 1111") == {"card": 1}


def test_invalid_luhn_not_masked_as_card() -> None:
    assert "[CARD]" not in masked("number 4111111111111112 here")


def test_sort_code_and_account() -> None:
    assert masked("Pay 12-34-56 acc 12345678 now") == "Pay [ACCOUNT] now"
    out = masked("sort code 12-34-56 account number 12345678")
    assert "12-34-56" not in out and "12345678" not in out and "[ACCOUNT]" in out
    assert report("12-34-56 12345678") == {"account": 1}


@pytest.mark.parametrize(
    "phone",
    ["07911 123456", "+44 7911 123456", "020 7946 0958", "(555) 123-4567", "555-123-4567", "+1 555 123 4567"],
)
def test_phone_formats(phone: str) -> None:
    assert masked(f"call {phone} today") == "call [PHONE] today"


def test_email() -> None:
    assert masked("mail jo.bloggs+x@example.co.uk now") == "mail [EMAIL] now"


def test_ssn_and_ni() -> None:
    assert masked("ssn 123-45-6789 end") == "ssn [ID] end"
    assert masked("NI QQ 12 34 56 C end") == "NI [ID] end"
    assert masked("NI QQ123456C end") == "NI [ID] end"


def test_iban() -> None:
    assert masked("iban GB82 WEST 1234 5698 7654 32 end") == "iban [ID] end"


def test_otp_needs_keyword() -> None:
    assert masked("your code is 482913") == "your code is [CODE]"
    assert masked("OTP: 4829") == "OTP: [CODE]"
    assert masked("PIN 1234 please") == "PIN [CODE] please"
    assert masked("passcode 48291367") == "passcode [CODE]"
    assert masked("we are 4829 strong") == "we are 4829 strong"


@pytest.mark.parametrize(
    "text",
    [
        "go to https://example.com/a?b=1234567890 now",
        "visit www.example.co.uk today",
        "pay £1,240.00 or $389.99 now",
        "on 2024-03-15 and 15/03/2024 and 3 March 2024",
        "order #12345678 and order number 987654321",
    ],
)
def test_protected_untouched(text: str) -> None:
    assert redact(text) == (text, [])


def test_idempotent() -> None:
    text = "a@b.com 07911 123456 4111 1111 1111 1111 code 4829 123-45-6789 12-34-56 12345678 GB82WEST12345698765432"
    once = masked(text)
    assert masked(once) == once


@pytest.mark.parametrize("text", ["", " ", "x" * 200_000, "9" * 100_000, "é😀‮\x00\ud800"[:-1], "1 " * 50_000, "a@" * 50_000], ids=range(7))
def test_never_raises(text: str) -> None:
    out, rep = redact(text)
    assert isinstance(out, str) and isinstance(rep, list)


def test_non_string_does_not_raise() -> None:
    assert redact(None)[0] == ""  # type: ignore[arg-type]


def test_report_has_no_originals() -> None:
    text = "a@b.com 07911 123456 4111111111111111 123-45-6789"
    rep = redact(text)[1]
    assert all(isinstance(t, str) and isinstance(n, int) for t, n in rep)
    flat = repr(rep)
    for secret in ("a@b.com", "07911", "4111", "123-45"):
        assert secret not in flat
    assert dict(rep) == {"email": 1, "phone": 1, "card": 1, "id": 1}
