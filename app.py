import streamlit as st

from pages_.registry import PAGES
from ui.theme import apply_theme

st.set_page_config(page_title="Second Look", page_icon="🔍", layout="centered")
apply_theme()

pages = [st.Page(p.path, title=p.title, icon=p.icon, default=p.title == "Home") for p in PAGES if p.enabled]
nav = st.navigation(pages, position="hidden")  # hidden so the theme selector stays first in the sidebar
with st.sidebar:
    for page in pages:
        st.page_link(page)
nav.run()
