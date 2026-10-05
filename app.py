import html
import re

import streamlit as st

import analyzer
from report_channels import REPORT_CHANNELS

EXAMPLES = {
    "Parcel scam": "Royal Mail: your parcel is held due to unpaid postage of £1.45. Pay within 24 hours or it will be returned: http://bit.ly/rm-redeliver",
    "Bank alert scam": "URGENT: Unusual activity on your account. Your login has been suspended. Verify your account immediately at http://paypa1-secure.com/login",
    "Boss gift card": "Hi, it's your manager. I'm stuck in a meeting and need 5 gift cards for a client, $100 each. Buy them now and send me the codes. Keep it between us.",
    "Legitimate": "Hi Sam, are we still on for lunch Thursday at 12:30? I booked the table at the usual place. Let me know if that changes.",
}
BANNERS = {
    "likely scam": (st.error, "Likely scam"),
    "suspicious": (st.warning, "Suspicious"),
    "likely safe": (st.success, "Likely safe"),
}

st.title("Second Look")
st.write("Paste a suspicious message and get a second opinion before you click, pay, or reply.")


def load_example(text: str) -> None:
    st.session_state["message"] = text


def highlight(text: str, phrases: list[str]) -> str:
    """Escape every segment of the message; only wrap already-escaped phrases in <mark>."""
    phrases = sorted({p for p in phrases if p}, key=len, reverse=True)
    if not phrases:
        return html.escape(text)
    parts = re.split(f"({'|'.join(map(re.escape, phrases))})", text)
    return "".join(
        f"<mark>{html.escape(p)}</mark>" if i % 2 else html.escape(p) for i, p in enumerate(parts)
    )


cols = st.columns(len(EXAMPLES))
for col, (label, example) in zip(cols, EXAMPLES.items()):
    col.button(label, on_click=load_example, args=(example,), use_container_width=True)

message = st.text_area("Message", key="message", height=160)
country = st.selectbox("Country", list(REPORT_CHANNELS))
st.caption("Your text is sent to Featherless's API for analysis and isn't stored by this app.")

analyze_clicked = st.button("Analyze", type="primary")
if analyze_clicked and not message.strip():
    st.warning("Paste a message first.")
elif analyze_clicked:
    with st.spinner("Checking..."):
        result = analyzer.analyze(message)

    if result["notice"]:
        st.warning(result["notice"])
    show, label = BANNERS.get(result["verdict"], BANNERS["suspicious"])
    show(f"**{label}**")
    st.text(f"Scam type: {result['scam_type']}")
    st.html(f'<div style="white-space:pre-wrap">{highlight(message, result["evidence_phrases"])}</div>')
    st.subheader("Why")
    st.text(result["reasoning"])
    if result["actions"]:
        st.subheader("What to do")
        for i, action in enumerate(result["actions"], 1):
            st.text(f"{i}. {action}")

    rules = result["rules"]
    st.write(f"**Rule score:** {rules['score']}/100")
    flagged = [f"{u} (URL shortener)" for u in rules["shorteners"]] + [
        f"{u} (lookalike of {b})" for u, b in rules["lookalikes"].items()
    ]
    if flagged:
        st.subheader("Flagged links (not clickable)")
        for item in flagged:
            st.code(item, language=None)

st.subheader("Report it")
for line in REPORT_CHANNELS[country]:
    st.write(f"- {line}")
