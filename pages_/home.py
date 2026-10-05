import streamlit as st

from pages_.registry import PAGES

st.html(
    '<div class="sl-hero"><h1>Second Look</h1>'
    "<p>Paste a suspicious message and get a second opinion before you click, pay or reply</p></div>"
)

with st.container(key="card-hero"):
    st.subheader("Check a message")
    st.write("Paste it in, and we'll tell you whether it looks safe, suspicious or like a scam.")
    st.page_link("pages_/check.py", label="Check a message", icon=":material/verified_user:")

with st.container(key="grid-features"):
    for page in PAGES[2:]:
        with st.container(key=f"card-{page.path}"):
            st.subheader(page.title)
            st.write(page.blurb)
            if page.enabled:
                st.page_link(page.path, label=page.title, icon=page.icon)
            else:
                st.html('<span class="sl-soon">Coming soon</span>')

# TODO: accuracy tile. Add it only once the eval gives a real, reproducible number.
st.html(
    '<div class="sl-tiles">'
    '<div class="sl-tile"><b>0 messages stored</b></div>'
    '<div class="sl-tile"><b>Runs rule checks and an AI model</b></div></div>'
)
