# Hardcoded on purpose (never from the model). Verify against official sites before release.
TYPED_CHANNELS: dict[str, list[tuple[str, str]]] = {  # type: text | email | fraud | general
    "UK": [
        ("text", "Forward scam texts to 7726."),
        ("email", "Report phishing emails to report@phishing.gov.uk."),
        ("fraud", "Report fraud to Report Fraud (reportfraud.police.uk, 0300 123 2040) in England, Wales and Northern Ireland, or to Police Scotland on 101 in Scotland."),
    ],
    "US": [
        ("fraud", "Report at reportfraud.ftc.gov."),
        ("text", "Forward scam texts to 7726."),
        ("email", "Report phishing to reportphishing@apwg.org."),
    ],
}

# recovery.py, the Report it section and their tests read plain lines
REPORT_CHANNELS: dict[str, list[str]] = {c: [t for _, t in v] for c, v in TYPED_CHANNELS.items()}
