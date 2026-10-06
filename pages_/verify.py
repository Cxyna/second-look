import html

import streamlit as st

from impersonation import IDENTITY_NOTE, SAFE_WORD_ADVICE, SCENARIOS

esc = html.escape

st.html(
    '<div class="sl-hero"><h1>Is it really them?</h1>'
    "<p>Pick who is contacting you and get a plain guide to checking if they are genuine.</p>"
    '<span class="sl-note">Nothing is stored. No AI model is called.</span></div>'
)

options = {v["label"]: k for k, v in SCENARIOS.items()}
preset = st.session_state.pop("handoff_scenario", None)  # read once, so a refresh can't replay it
if preset in SCENARIOS:
    st.session_state["who"] = SCENARIOS[preset]["label"]
chosen_label = st.selectbox("Who is contacting you?", list(options), key="who")
scenario = SCENARIOS[options[chosen_label]]

st.info(
    "📌 " + IDENTITY_NOTE,
    icon=None,
)

with st.expander("How this scam usually works", expanded=True):
    st.write(scenario["how_it_works"])

with st.expander("Warning signs"):
    items = "".join(f"<li>{esc(s)}</li>" for s in scenario["warning_signs"])
    st.html(f"<ul>{items}</ul>")

with st.expander("Check it like this"):
    for i, step in enumerate(scenario["check_steps"], 1):
        st.html(
            f'<div class="sl-step"><b>{esc(str(i))}.</b> {esc(step)}</div>'
        )

with st.expander("Questions only the real person could answer"):
    items = "".join(f"<li>{esc(q)}</li>" for q in scenario["questions"])
    st.html(f"<ul>{items}</ul>")

with st.expander("Never"):
    items = "".join(f"<li>{esc(n)}</li>" for n in scenario["never"])
    st.html(f"<ul>{items}</ul>")

with st.expander("Set up a family safe word"):
    st.write(SAFE_WORD_ADVICE)
