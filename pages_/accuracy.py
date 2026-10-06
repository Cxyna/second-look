import html

import streamlit as st

from accuracy_data import BEFORE_TUNING, N_LEGIT, N_MESSAGES, N_SCAM, RESULTS, wilson_interval

esc = html.escape


def pct(x: float) -> str:
    return f"{round(x * 100)}%"


def rate(successes: int, total: int) -> str:
    lo, hi = wilson_interval(successes, total)
    return f"{pct(successes / total)} (likely {pct(lo)} to {pct(hi)})"


def card(title: str, value: str, note: str) -> str:
    return (f'<div class="sl-tile"><span>{esc(title)}</span><b>{esc(value)}</b>'
            f"<small>{esc(note)}</small></div>")


def table(head: list[str], rows: list[list[str]]) -> str:
    th = "".join(f"<th>{esc(h)}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="sl-table"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


hy = RESULTS["hybrid"]
st.html(
    '<div class="sl-hero"><h1>How accurate is it?</h1>'
    f"<p>Tested on {N_MESSAGES} fictional messages. A small test, so treat the numbers as a rough guide.</p></div>"
)

st.html(
    '<div class="sl-tiles">'
    + card("Overall correct", f"{hy['accuracy']}%", "full app")
    + card("Scams caught", rate(hy["tp"], hy["tp"] + hy["fn"]), f"{hy['tp']} of {hy['tp'] + hy['fn']} scams")
    + card("False alarms", rate(hy["fp"], hy["fp"] + hy["tn"]), f"{hy['fp']} of {hy['fp'] + hy['tn']} genuine messages")
    + "</div>"
)

st.subheader("Comparison")
rows = []
for r in RESULTS.values():
    rows.append([r["label"], f"{r['accuracy']}%", f"{r['precision']}%", f"{r['recall']}%", f"{r['f1']:.2f}",
                 rate(r["tp"], r["tp"] + r["fn"]), rate(r["fp"], r["fp"] + r["tn"]),
                 f"{r['tp']} / {r['fn']} / {r['fp']} / {r['tn']}", str(r["errors"])])
st.html(table(["Setup", "Accuracy", "Precision", "Recall", "F1", "Scams caught", "False alarms",
               "Caught / missed / false alarm / correct pass", "Errors (excluded)"], rows))
st.caption("Flagged means 'likely scam' or 'suspicious'. Errors are failed AI calls, left out of that row's scores.")

st.subheader("Full app: what it said")
st.html(table(["", "Said scam or suspicious", "Said safe"],
              [["Actually a scam", str(hy["tp"]), str(hy["fn"])],
               ["Actually genuine", str(hy["fp"]), str(hy["tn"])]]))

st.subheader("Before tuning (development run)")
st.html(table(["Setup", "Genuine messages wrongly flagged", "Scams caught", "Overall correct"],
              [[b["label"], f"{b['fp']} of {b['fp'] + b['tn']}", f"{b['tp']} of {b['tp'] + b['fn']}", f"{b['accuracy']}%"]
               for b in BEFORE_TUNING.values()]))
st.write("This was a development run. We used it to improve the AI's prompt, so it is not an unseen test. "
         "The tables above come from a separate set the prompt was never tuned on.")

st.subheader("How we measured it")
st.write(f"{N_MESSAGES} fictional messages ({N_SCAM} scams, {N_LEGIT} genuine) were written for this project by an AI. "
         "They were never used to tune the prompt. It is a small sample, so the ranges are wide.")

st.subheader("What it gets wrong")
st.write("The three missed scams were early-stage messages with no request yet, such as a wrong-number opener "
         "or a romance opener. One borderline false alarm: a friend asking for money back, with a sort code mentioned.")

st.subheader("What this does not show")
for t in ("It was not tested on real messages or on other languages.",
          "The rules-only score is low partly because the test messages use invented brand names.",
          "It was measured without the privacy shield.",
          "Results can vary between runs."):
    st.write("- " + t)
