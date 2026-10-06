"""Themes as CSS-variable dicts, injected as one static <style> block."""
import streamlit as st

DEFAULT_THEME = "Rose Pine"

_ROSE_PINE = {
    "base": "#191724", "surface": "#1f1d2e", "overlay": "#26233a",
    "muted": "#6e6a86", "subtle": "#908caa", "text": "#e0def4",
    "love": "#eb6f92", "gold": "#f6c177", "rose": "#ebbcba",
    "pine": "#31748f", "foam": "#9ccfd8", "iris": "#c4a7e7",
}

THEMES: dict[str, dict[str, str]] = {
    "Rose Pine": _ROSE_PINE,
    "Rose Pine Moon": {**_ROSE_PINE, "base": "#232136", "surface": "#2a273f", "overlay": "#393552"},
    "Rose Pine Dawn": {
        "base": "#faf4ed", "surface": "#fffaf3", "overlay": "#f2e9e1",
        "muted": "#9893a5", "subtle": "#797593", "text": "#575279",
        "love": "#b4637a", "gold": "#ea9d34", "rose": "#d7827e",
        "pine": "#286983", "foam": "#56949f", "iris": "#907aa9",
    },
    "Catppuccin Mocha": {
        "base": "#1e1e2e", "surface": "#181825", "overlay": "#313244",
        "muted": "#6c7086", "subtle": "#a6adc8", "text": "#cdd6f4",
        "love": "#f38ba8", "gold": "#f9e2af", "rose": "#f5e0dc",
        "pine": "#94e2d5", "foam": "#89dceb", "iris": "#cba6f7",
    },
    "Tokyo Night": {
        "base": "#1a1b26", "surface": "#24283b", "overlay": "#2f334d",
        "muted": "#565f89", "subtle": "#a9b1d6", "text": "#c0caf5",
        "love": "#f7768e", "gold": "#e0af68", "rose": "#ff9e64",
        "pine": "#73daca", "foam": "#7dcfff", "iris": "#bb9af7",
    },
    "High Contrast": {
        "base": "#000000", "surface": "#0a0a0a", "overlay": "#1a1a1a",
        "muted": "#bdbdbd", "subtle": "#e0e0e0", "text": "#ffffff",
        "love": "#ff6b8a", "gold": "#ffd33d", "rose": "#ffb4a8",
        "pine": "#4fd1c5", "foam": "#7ee7ff", "iris": "#d0b0ff",
    },
}

def _lum(hex_color: str) -> float:
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    r, g, b = (c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    """WCAG contrast ratio between two #rrggbb colours."""
    hi, lo = sorted((_lum(a), _lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def on_color(bg: str) -> str:
    """Black or white, whichever reads better on bg."""
    return max(("#000000", "#ffffff"), key=lambda c: contrast(c, bg))


# Static. Only the :root variable block in front of it varies, and that comes from THEMES.
_CSS = """
:root { --accent: var(--iris);
  --edge: color-mix(in srgb, var(--accent) 45%, transparent);
  --glow: 0 0 24px color-mix(in srgb, var(--accent) 22%, transparent); }
.stApp, [data-testid="stHeader"] { background: var(--base); color: var(--text); }
[data-testid="stSidebar"] { background: var(--surface); }
html, body, .stApp, button, input, textarea { font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
.stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp span,
.stApp [data-testid="stMarkdownContainer"] { color: var(--text); }
.block-container { max-width: 880px; padding: 3rem 1.5rem 4rem; }
[data-testid="stVerticalBlock"] { gap: 1.25rem; }

.sl-card, [class*="st-key-card"], [data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--surface); border: 1px solid var(--edge); border-radius: 20px;
  box-shadow: var(--glow); padding: 1.5rem 1.75rem; }
[data-testid="stVerticalBlockBorderWrapper"] > div { border: 0; }
.sl-hero h1 { margin: 0; font-size: 2.8rem; letter-spacing: -0.02em; }
.sl-hero p { margin: .6rem 0 1rem; font-size: 1.25rem; max-width: 32em; }
.sl-note { display: inline-block; font-size: .9rem; padding: .25rem .9rem; border-radius: 999px;
  background: var(--overlay); color: var(--text); border: 1px solid var(--edge); }
.sl-tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }
.sl-tile { background: var(--overlay); border-radius: 20px; padding: 1rem 1.25rem; color: var(--text); }
.sl-tile b { display: block; font-size: 1.15rem; }
.sl-soon { display: inline-block; font-size: .85rem; padding: .1rem .7rem; border-radius: 999px;
  background: var(--overlay); color: var(--text); }

.sl-card { color: var(--text); }
.sl-verdict { border-left: 10px solid var(--accent); }
.sl-verdict.scam { border-left-color: var(--love); }
.sl-verdict.warn { border-left-color: var(--gold); }
.sl-verdict.safe { border-left-color: var(--pine); }
.sl-head { display: flex; align-items: center; gap: 1.1rem; }
.sl-icon { font-size: 3.6rem; line-height: 1; }
.sl-title { font-size: 1.9rem; font-weight: 700; line-height: 1.2; }
.sl-reason { margin: 1rem 0 0; font-size: 1.1rem; }
.sl-card h3 { margin: 1.2rem 0 .5rem; font-size: 1.1rem; }
.sl-card ol { margin: 0; padding-left: 1.4rem; }
.sl-card li { margin: .35rem 0; }
.sl-msg { white-space: pre-wrap; overflow-wrap: anywhere; }
.sl-msg mark { background: var(--gold); color: #191724; padding: 0 .2em; border-radius: 4px; }
.sl-legend { font-size: .9rem; margin: .8rem 0 0; }

.stButton > button, [data-testid="stPageLink-NavLink"] {
  border-radius: 999px; min-height: 3rem; padding: .5rem 1.5rem; font-weight: 600;
  background: var(--overlay); color: var(--text); border: 1px solid var(--edge); }
.stButton > button[kind="primary"] { min-height: 3.5rem; font-size: 1.15rem; padding: .6rem 2.5rem;
  background: var(--accent); color: var(--on-accent); border-color: var(--accent); box-shadow: var(--glow); }
.stButton > button[kind="primary"] * { color: var(--on-accent) !important; }
[data-testid="stMarkdownContainer"] a { color: var(--accent); text-decoration: underline; }
.st-key-grid-features { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.25rem; }
.stButton > button p { color: inherit; }
.stButton > button:hover, [data-testid="stPageLink-NavLink"]:hover { border-color: var(--accent); }
textarea, [data-baseweb="select"] > div, [data-baseweb="textarea"] {
  background: var(--overlay) !important; color: var(--text) !important; border-radius: 16px !important; }
[data-testid="stExpander"] { border: 1px solid var(--edge); border-radius: 20px; background: var(--surface); }
label[data-baseweb="checkbox"]:has(input:checked) > span:first-child {
  background: var(--accent) !important; border-color: var(--accent) !important; }
label[data-baseweb="radio"]:has(input:checked) > div:first-child {
  background: var(--accent) !important; border-color: var(--accent) !important; }
[data-testid="stProgress"] [role="progressbar"] > div > div { background: var(--accent) !important; }
a:focus-visible, button:focus-visible, textarea:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
@media (max-width: 640px) {
  .st-key-grid-features { grid-template-columns: 1fr; }
  .sl-hero h1 { font-size: 2rem; } .sl-title { font-size: 1.5rem; } .sl-icon { font-size: 2.8rem; }
  .sl-card, [class*="st-key-card"] { padding: 1.1rem; }
}
"""


# Static, appended after _CSS so it wins. Bigger text, spacing, buttons and tick-boxes.
_LARGE_CSS = """
html { font-size: 125%; }
.stApp p, .stApp li, .stApp label, .stApp span, .stApp textarea { line-height: 1.7; }
.stButton > button, [data-testid="stPageLink-NavLink"] { min-height: 4rem; font-size: 1.2rem; padding: .75rem 1.75rem; }
.stButton > button[kind="primary"] { min-height: 4.5rem; font-size: 1.35rem; }
label[data-baseweb="checkbox"] > span:first-child, label[data-baseweb="radio"] > div:first-child {
  transform: scale(1.4); margin-right: .6rem; }
[data-testid="stCheckbox"] label, [data-testid="stToggle"] label { min-height: 2.5rem; }
"""


def build_css(name: str, large: bool = False) -> str:
    colors = {**THEMES[name], "on-accent": on_color(THEMES[name]["iris"])}
    variables = "".join(f"--{k}: {v};" for k, v in colors.items())
    return f"<style>:root{{{variables}}}{_CSS}{_LARGE_CSS if large else ''}</style>"


def apply_theme() -> None:
    """Render the sidebar theme selector and large-text switch, and inject the CSS."""
    with st.sidebar:
        name = st.selectbox("Theme", list(THEMES), key="theme")
        large = st.toggle("Larger text and buttons", key="large_text")
    st.html(build_css(name, large))
