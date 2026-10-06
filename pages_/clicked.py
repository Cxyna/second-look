import re

import streamlit as st

from recovery import ACTIONS, build_plan


def slug(text: str) -> str:
    return re.sub(r"\W+", "-", text.lower()).strip("-")


st.html(
    '<div class="sl-hero"><h1>Already clicked or paid?</h1>'
    "<p>This is common and it's not your fault. Acting quickly helps.</p>"
    '<span class="sl-note">Nothing is stored. Ticks last only for this visit.</span></div>'
)


def show_plan() -> None:
    """Snapshot the choices and clear old ticks (session state only)."""
    for key in [k for k in st.session_state if k.startswith("done-")]:
        del st.session_state[key]
    st.session_state["plan_actions"] = [a for a in ACTIONS if st.session_state.get(f"act-{a}")]
    st.session_state["plan_country"] = st.session_state["country"]


st.markdown("**What happened? Tick everything that applies.**")
for action in ACTIONS:
    # Not str.capitalize(): it lowercases the rest, turning "ID" into "id".
    st.checkbox(action[0].upper() + action[1:], key=f"act-{action}")
st.radio("Country", ["UK", "US"], key="country", horizontal=True)
st.button("Show my plan", type="primary", on_click=show_plan)

plan_actions = st.session_state.get("plan_actions")
if plan_actions is None:
    st.stop()
if not plan_actions:
    st.info("Tick at least one thing that happened, then press “Show my plan”.")
    st.stop()

plan = build_plan(plan_actions, st.session_state["plan_country"])
done = sum(bool(st.session_state.get(f"done-{slug(s.text)}")) for s in plan)
st.progress(done / len(plan), text=f"{done} of {len(plan)} steps done")

current = None
for i, step in enumerate(plan):
    if step.urgency != current:
        current = step.urgency
        st.subheader(current)
    # Hardcoded text in a markdown widget label (not raw HTML), so no escaping needed.
    st.checkbox(step.text, key=f"done-{slug(step.text)}")
