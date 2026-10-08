import html
import random
import streamlit as st

import quiz_data
from ui.theme import VERDICT_ICONS

st.html(
    '<div class="sl-hero"><h1>Spot the Scam</h1>'
    "<p>Test your scam detection skills against tricky real-world scenarios.</p>"
    '<span class="sl-note">Interactive Training: Learn the subtle psychological tricks scammers use.</span></div>'
)

# Initialize randomized scenario order
if "quiz_order" not in st.session_state:
    indices = list(range(len(quiz_data.SCENARIOS)))
    random.shuffle(indices)
    st.session_state["quiz_order"] = indices
    st.session_state["quiz_index"] = 0
    st.session_state["quiz_score"] = 0
    st.session_state["quiz_answers"] = {}

total = len(quiz_data.SCENARIOS)
current_step = st.session_state["quiz_index"]

# Top Controls: Randomize / Restart
col_top1, col_top2 = st.columns([3, 1])
with col_top2:
    if st.button("🎲 Shuffle & Restart", use_container_width=True):
        indices = list(range(len(quiz_data.SCENARIOS)))
        random.shuffle(indices)
        st.session_state["quiz_order"] = indices
        st.session_state["quiz_index"] = 0
        st.session_state["quiz_score"] = 0
        st.session_state["quiz_answers"] = {}
        st.rerun()

# Progress bar
st.progress((current_step) / total, text=f"Scenario {min(current_step + 1, total)} of {total}")

if current_step >= total:
    score = st.session_state["quiz_score"]
    pct = int((score / total) * 100)
    badge_css = "safe" if pct >= 80 else ("warn" if pct >= 60 else "scam")

    st.html(
        f'<div class="sl-card sl-verdict {badge_css}">'
        f'<div class="sl-head"><span class="sl-title">Training Complete!</span></div>'
        f'<p class="sl-reason">You scored <b>{score} out of {total}</b> ({pct}%).</p>'
        '</div>'
    )

    if pct == 100:
        st.balloons()
        st.success("🌟 Outstanding! You outsmarted even the expert reverse-psychology attacks.")
    elif pct >= 60:
        st.info("👍 Solid work! A few tricky expert-level details caught you, but you understand the main danger signs.")
    else:
        st.warning("⚠️ Scammers are getting more sophisticated every day. Review the red flags below to stay safe!")

    if st.button("Play Again with New Shuffle", type="primary"):
        indices = list(range(len(quiz_data.SCENARIOS)))
        random.shuffle(indices)
        st.session_state["quiz_order"] = indices
        st.session_state["quiz_index"] = 0
        st.session_state["quiz_score"] = 0
        st.session_state["quiz_answers"] = {}
        st.rerun()

    st.stop()

scenario_idx = st.session_state["quiz_order"][current_step]
scenario = quiz_data.SCENARIOS[scenario_idx]
esc = html.escape

# Difficulty badge styling
diff_class = "danger" if scenario.difficulty in ("Advanced", "Expert") else ("warn" if scenario.difficulty == "Intermediate" else "safe")

# Scenario Card
st.html(
    f'<div class="sl-card">'
    f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">'
    f'<span class="sl-badge warn">{esc(scenario.scenario_type)}</span>'
    f'<span class="sl-badge {diff_class}">Difficulty: {esc(scenario.difficulty)}</span>'
    f'</div>'
    f'<h3 style="margin:0 0 0.5rem 0;">{esc(scenario.title)}</h3>'
    f'<p style="margin:0 0 1rem 0; font-size:0.95rem; opacity:0.85;"><b>From:</b> <code>{esc(scenario.sender)}</code></p>'
    f'<div class="sl-msg">{esc(scenario.message)}</div>'
    f'</div>'
)

user_answered = current_step in st.session_state["quiz_answers"]

if not user_answered:
    st.markdown("### Would you trust this or is it a scam?")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚨 This looks like a Scam", use_container_width=True, type="primary"):
            st.session_state["quiz_answers"][current_step] = True
            if scenario.is_scam:
                st.session_state["quiz_score"] += 1
            st.rerun()
            
    with col2:
        if st.button("✅ This looks Safe", use_container_width=True):
            st.session_state["quiz_answers"][current_step] = False
            if not scenario.is_scam:
                st.session_state["quiz_score"] += 1
            st.rerun()
else:
    user_choice = st.session_state["quiz_answers"][current_step]
    was_correct = (user_choice == scenario.is_scam)

    if was_correct:
        st.html(
            '<div class="sl-card sl-verdict safe">'
            f'<div class="sl-head"><span class="sl-icon" aria-hidden="true">{VERDICT_ICONS["safe"]}</span>'
            '<span class="sl-title">Correct!</span></div>'
            f'<p class="sl-reason">{esc(scenario.correct_explanation)}</p>'
            '</div>'
        )
    else:
        st.html(
            '<div class="sl-card sl-verdict scam">'
            f'<div class="sl-head"><span class="sl-icon" aria-hidden="true">{VERDICT_ICONS["scam"]}</span>'
            '<span class="sl-title">Not quite!</span></div>'
            f'<p class="sl-reason">{esc(scenario.correct_explanation)}</p>'
            '</div>'
        )

    st.subheader("Key Red Flags to Spot:")
    for sign in scenario.tell_signs:
        st.markdown(f"- 🔎 {sign}")

    st.write("")
    if st.button("Next Scenario →", type="primary"):
        st.session_state["quiz_index"] += 1
        st.rerun()
