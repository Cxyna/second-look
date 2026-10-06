import html

import streamlit as st

esc = html.escape

SECTIONS: list[tuple[str, list[str]]] = [
    ("What happens to your text", [
        "If the privacy switch is on, emails, phone numbers, card numbers, bank details, ID numbers and "
        "one-time codes are replaced on your own computer first.",
        "The masked text is sent to Featherless, which runs the AI model that reads it.",
        "This app doesn't save, log or share your messages.",
        "Names and addresses are not hidden.",
        "Check Featherless's own privacy policy for how they handle requests.",
        "If this app is hosted online, the hosting service may keep standard server logs.",
    ]),
    ("What the AI does and what it doesn't", [
        "The AI reads the message, explains it and drafts text.",
        "The checked steps in the recovery plan and the impersonation guide are fixed content written ahead "
        "of time. They are not generated.",
        "Every AI answer is labelled and can be wrong.",
    ]),
    ("Limits", [
        "This is not legal or financial advice.",
        "It doesn't replace your bank or the police.",
        "It can miss scams and can flag genuine messages.",
    ]),
    ("Built for ForgeHacks 2026", [
        "Everything was built during the event. Nothing existed before October 3.",
        "Made with Python and Streamlit, using Qwen3-32B via Featherless.",
        "Claude Code was used as a coding assistant.",
        "The test messages are fictional.",
    ]),
]
# VERIFY: no claims about hosting provider, retention or compliance; the code can't back them.

st.html('<div class="sl-hero"><h1>About and privacy</h1>'
        "<p>What this app does with your text, and what it can't do.</p></div>")

for title, lines in SECTIONS:
    items = "".join(f"<li>{esc(s)}</li>" for s in lines)
    st.html(f'<div class="sl-card"><h3>{esc(title)}</h3><ul>{items}</ul></div>')
