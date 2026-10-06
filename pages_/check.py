import html
import re

import streamlit as st

import analyzer
import simplify
from redact import redact
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

# type -> (singular, plural)
HIDDEN_LABELS = {
    "email": ("email address", "email addresses"),
    "phone": ("phone number", "phone numbers"),
    "card": ("card number", "card numbers"),
    "account": ("bank account", "bank accounts"),
    "id": ("ID number", "ID numbers"),
    "code": ("one-time code", "one-time codes"),
}

# Input is already HTML-escaped; "[PHONE]" etc. contain nothing escapable.
HIDDEN_TAG = re.compile(r"\[(?:EMAIL|PHONE|CARD|ACCOUNT|ID|CODE)\]")
HIDDEN_MARK = r'<span style="outline:1px dotted currentColor;border-radius:3px;padding:0 2px">\g<0></span>'

st.html(
    '<div class="sl-hero"><h1>Check a message</h1>'
    "<p>Paste a suspicious message and get a second opinion before you click, pay or reply</p>"
    '<span class="sl-note">Nothing is stored. Your text is sent to Featherless for analysis, with personal numbers hidden first if you leave the switch below on.</span></div>'
)


def load_example(text: str) -> None:
    st.session_state["message"] = text


@st.fragment
def explain_card(result: dict) -> None:
    """Fragment: the click reruns only this card, so the verdict stays; the text is never stored."""
    if st.button("Explain it simply"):
        with st.spinner("Writing..."):
            text = simplify.explain_simply(result)
        st.html(
            '<div class="sl-card"><h3>In plain words</h3>'
            f'<p class="sl-reason">{html.escape(text)}</p>'
            '<p class="sl-legend">Written by AI. It may be wrong, so use the verdict above too.</p></div>'
        )


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

hide = st.toggle("Hide personal details before sending", value=True)
st.caption(
    "Replaces emails, phone numbers, card and bank numbers, ID numbers and one-time codes with "
    "placeholders before anything is checked. It can't reliably hide names or addresses, so "
    "remove those yourself if they matter."
)

analyze_clicked = st.button("Analyze", type="primary")
if analyze_clicked and not message.strip():
    st.warning("Paste a message first.")
elif analyze_clicked:
    shown, hidden = redact(message) if hide else (message, [])
    with st.spinner("Checking..."):
        result = analyzer.analyze(shown)

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
        + "</div>"
    )
    explain_card(result)
    if steps:
        st.html(f'<div class="sl-card"><h3>What to do now</h3><ol>{steps}</ol></div>')
    st.html(
        '<div class="sl-card"><div class="sl-msg">'
        f'{HIDDEN_TAG.sub(HIDDEN_MARK, highlight(shown, result["evidence_phrases"]))}</div>'
        '<p class="sl-legend">Highlighted words are the parts that made us suspicious. '
        "Dotted boxes like [PHONE] are details we hid.</p></div>"
    )

    if hide:
        parts = [f"{n} {HIDDEN_LABELS[k][n != 1]}" for k, n in hidden if k in HIDDEN_LABELS]
        st.html(
            '<div class="sl-card"><h3>What we hid before sending</h3><p>'
            + (esc(", ".join(parts)) if parts else "Nothing needed hiding.")
            + "</p></div>"
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
