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
# verdict -> (icon, plain-English headline, CSS class)
VERDICTS = {
    "likely scam": ("🚫", "This looks like a scam", "scam"),
    "suspicious": ("⚠️", "This looks suspicious", "warn"),
    "likely safe": ("✅", "This looks safe", "safe"),
}

st.html(
    '<div class="sl-hero"><h1>Check a message</h1>'
    "<p>Paste a suspicious message and get a second opinion before you click, pay or reply</p>"
    '<span class="sl-note">Nothing is stored. Your text is sent to Featherless for analysis.</span></div>'
)


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


st.markdown("**Try an example**")
cols = st.columns(len(EXAMPLES))
for col, (label, example) in zip(cols, EXAMPLES.items()):
    col.button(label, on_click=load_example, args=(example,), use_container_width=True)

message = st.text_area("Message", key="message", height=160)

analyze_clicked = st.button("Analyze", type="primary")
if analyze_clicked and not message.strip():
    st.warning("Paste a message first.")
elif analyze_clicked:
    with st.spinner("Checking..."):
        result = analyzer.analyze(message)

    if result["notice"]:
        st.warning(result["notice"])
    icon, headline, css = VERDICTS.get(result["verdict"], VERDICTS["suspicious"])
    esc = html.escape
    steps = "".join(f"<li>{esc(a)}</li>" for a in result["actions"])
    st.html(
        f'<div class="sl-card sl-verdict {css}">'
        f'<div class="sl-head"><span class="sl-icon" aria-hidden="true">{icon}</span>'
        f'<span class="sl-title">{headline}</span></div>'
        f'<p class="sl-reason">{esc(result["reasoning"])}</p>'
        + (f"<h3>What to do now</h3><ol>{steps}</ol>" if steps else "")
        + "</div>"
    )
    st.html(
        '<div class="sl-card"><div class="sl-msg">'
        f'{highlight(message, result["evidence_phrases"])}</div>'
        '<p class="sl-legend">Highlighted words are the parts that made us suspicious.</p></div>'
    )

    rules = result["rules"]
    flagged = [f"{u} (URL shortener)" for u in rules["shorteners"]] + [
        f"{u} (lookalike of {b})" for u, b in rules["lookalikes"].items()
    ]
    with st.expander("How we checked this"):
        st.text(f"Scam type: {result['scam_type']}")
        st.write(f"**Rule score:** {rules['score']}/100")
        if flagged:
            st.write("**Flagged links (not clickable)**")
            for item in flagged:
                st.code(item, language=None)

@st.fragment
def report_card() -> None:
    """Fragment: changing the country reruns only this card, so the result stays visible."""
    with st.container(border=True):
        country = st.selectbox("Country", list(REPORT_CHANNELS))
        st.subheader("Report it")
        for line in REPORT_CHANNELS[country]:
            st.write(f"- {line}")


report_card()
