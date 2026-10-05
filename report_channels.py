# Hardcoded on purpose (never from the model). Verify against official sites before release.
REPORT_CHANNELS: dict[str, list[str]] = {
    "UK": [
        "Forward scam texts to 7726.",
        "Report phishing emails to report@phishing.gov.uk.",
        "Report fraud to Report Fraud (reportfraud.police.uk, 0300 123 2040) in England, Wales and Northern Ireland, or to Police Scotland on 101 in Scotland.",
    ],
    "US": [
        "Report at reportfraud.ftc.gov.",
        "Forward scam texts to 7726.",
        "Report phishing to reportphishing@apwg.org.",
    ],
}
