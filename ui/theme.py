"""Themes as CSS-variable dicts, injected as one static <style> block."""
import html
import re

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
    "Ocean Breeze": {
        "base": "#0b192c", "surface": "#12253e", "overlay": "#1e3a5f",
        "muted": "#7089a8", "subtle": "#9bb3d1", "text": "#f0f5fc",
        "love": "#ff6b81", "gold": "#fbc02d", "rose": "#f8a5c2",
        "pine": "#26de81", "foam": "#45aaf2", "iris": "#4bcffa",
    },
    "Nord Light": {
        "base": "#f5f7fa", "surface": "#ffffff", "overlay": "#e5e9f0",
        "muted": "#7b889b", "subtle": "#4c566a", "text": "#2e3440",
        "love": "#bf616a", "gold": "#d08770", "rose": "#ebcb8b",
        "pine": "#2e7d32", "foam": "#88c0d0", "iris": "#5e81ac",
    },
    "Warm Paper": {
        "base": "#fbf8f3", "surface": "#ffffff", "overlay": "#f0ebe1",
        "muted": "#8c827a", "subtle": "#635b54", "text": "#38332e",
        "love": "#c0392b", "gold": "#d35400", "rose": "#e67e22",
        "pine": "#27ae60", "foam": "#2980b9", "iris": "#8e44ad",
    },
    "Midnight Emerald": {
        "base": "#081c15", "surface": "#102a22", "overlay": "#1b3d32",
        "muted": "#6b9080", "subtle": "#92b4a7", "text": "#d8f3dc",
        "love": "#ff5a5f", "gold": "#ffd166", "rose": "#f4a261",
        "pine": "#2ec4b6", "foam": "#52b788", "iris": "#70e000",
    },
    "Cyber Slate": {
        "base": "#0f172a", "surface": "#1e293b", "overlay": "#334155",
        "muted": "#64748b", "subtle": "#94a3b8", "text": "#f8fafc",
        "love": "#f43f5e", "gold": "#f59e0b", "rose": "#fb7185",
        "pine": "#10b981", "foam": "#38bdf8", "iris": "#6366f1",
    },
    "Clean Studio": {
        "base": "#f8fafc", "surface": "#ffffff", "overlay": "#f1f5f9",
        "muted": "#94a3b8", "subtle": "#64748b", "text": "#0f172a",
        "love": "#e11d48", "gold": "#d97706", "rose": "#be123c",
        "pine": "#059669", "foam": "#0284c7", "iris": "#4f46e5",
    },
    "Amethyst Luxury": {
        "base": "#130e1e", "surface": "#1f1730", "overlay": "#2e2247",
        "muted": "#7c6f96", "subtle": "#aa9cc7", "text": "#f7f4fc",
        "love": "#ff4d6d", "gold": "#ffb703", "rose": "#ff758f",
        "pine": "#06d6a0", "foam": "#4cc9f0", "iris": "#a370f7",
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
  --edge: color-mix(in srgb, var(--accent) 26%, transparent);
  --glow: 0 8px 30px -4px color-mix(in srgb, var(--accent) 18%, transparent); }
.stApp, [data-testid="stHeader"] { background: var(--base); color: var(--text); }
[data-testid="stHeader"] { backdrop-filter: blur(12px); background: color-mix(in srgb, var(--base) 80%, transparent); }
[data-testid="stSidebar"] {
  background: var(--surface); border-right: 1px solid var(--edge);
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.12);
}
html, body, .stApp, button, input, textarea {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", "Helvetica Neue", Arial, sans-serif;
  letter-spacing: -0.012em;
}
.stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp span,
.stApp [data-testid="stMarkdownContainer"] { color: var(--text); }
.block-container { max-width: 900px; padding: 2.2rem 1.75rem 4rem; }
[data-testid="stVerticalBlock"] { gap: 1.35rem; }

/* Luxury Cards */
.sl-card, [class*="st-key-card"], [data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--surface); border: 1px solid var(--edge); border-radius: 18px;
  box-shadow: 0 10px 30px -8px rgba(0, 0, 0, 0.16), var(--glow); padding: 1.6rem 1.85rem;
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s ease;
  position: relative; overflow: hidden;
}
[class*="st-key-card"]:hover {
  border-color: color-mix(in srgb, var(--accent) 60%, transparent);
  transform: translateY(-3px);
  box-shadow: 0 16px 36px -8px rgba(0, 0, 0, 0.22), var(--glow);
}
[data-testid="stVerticalBlockBorderWrapper"] > div { border: 0; }

/* Hero Section */
.sl-hero {
  margin-bottom: 1.8rem; text-align: left;
  padding: 1.5rem 0 0.5rem;
  position: relative;
}
.sl-hero h1 {
  margin: 0; font-size: 2.85rem; font-weight: 850; letter-spacing: -0.035em; line-height: 1.12;
  background: linear-gradient(135deg, var(--text) 30%, color-mix(in srgb, var(--accent) 85%, var(--text)));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.sl-hero p {
  margin: .65rem 0 1.1rem; font-size: 1.22rem; max-width: 36em; opacity: 0.92; line-height: 1.55;
  font-weight: 400;
}
.sl-note {
  display: inline-flex; align-items: center; gap: 0.5rem; font-size: .88rem; padding: .38rem 1.1rem; border-radius: 999px;
  background: var(--overlay); color: var(--text); border: 1px solid var(--edge); font-weight: 550;
  backdrop-filter: blur(8px);
}
.sl-tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.15rem; margin-top: 1rem; }
.sl-tile {
  background: var(--surface); border-radius: 18px; padding: 1.35rem 1.5rem; color: var(--text);
  border: 1px solid var(--edge); box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  display: flex; flex-direction: column; justify-content: center;
}
.sl-tile b { display: block; font-size: 1.15rem; font-weight: 650; letter-spacing: -0.01em; }
.sl-soon { display: inline-block; font-size: .82rem; padding: .2rem .8rem; border-radius: 999px;
  background: var(--overlay); color: var(--subtle); border: 1px solid var(--edge); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }

/* Verdict Banners */
.sl-card { color: var(--text); }
.sl-verdict {
  border-left: 10px solid var(--accent); border-radius: 20px;
  backdrop-filter: blur(10px);
}
.sl-verdict.scam {
  border-left-color: var(--love);
  background: linear-gradient(135deg, color-mix(in srgb, var(--love) 10%, var(--surface)), var(--surface));
  border-color: color-mix(in srgb, var(--love) 35%, var(--edge));
}
.sl-verdict.warn {
  border-left-color: var(--gold);
  background: linear-gradient(135deg, color-mix(in srgb, var(--gold) 10%, var(--surface)), var(--surface));
  border-color: color-mix(in srgb, var(--gold) 35%, var(--edge));
}
.sl-verdict.safe {
  border-left-color: var(--pine);
  background: linear-gradient(135deg, color-mix(in srgb, var(--pine) 10%, var(--surface)), var(--surface));
  border-color: color-mix(in srgb, var(--pine) 35%, var(--edge));
}
.sl-head { display: flex; align-items: center; gap: 1.25rem; }
.sl-icon { font-size: 3.6rem; line-height: 1; display: inline-flex; flex: none; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.15)); }
.sl-icon svg { display: block; }
.sl-verdict.scam .sl-icon { color: var(--love); }
.sl-verdict.warn .sl-icon { color: var(--gold); }
.sl-verdict.safe .sl-icon { color: var(--pine); }
.sl-badges { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1rem; }
.sl-badge {
  display: inline-flex; align-items: center; gap: .4rem; padding: .3rem .85rem; border-radius: 999px;
  font-size: .84rem; font-weight: 650; letter-spacing: -0.01em; border: 1px solid var(--edge);
  backdrop-filter: blur(6px);
}
.sl-badge.danger {
  background: color-mix(in srgb, var(--love) 16%, var(--surface));
  color: var(--love); border-color: color-mix(in srgb, var(--love) 40%, transparent);
}
.sl-badge.warn {
  background: color-mix(in srgb, var(--gold) 16%, var(--surface));
  color: var(--gold); border-color: color-mix(in srgb, var(--gold) 40%, transparent);
}
.sl-badge.safe {
  background: color-mix(in srgb, var(--pine) 16%, var(--surface));
  color: var(--pine); border-color: color-mix(in srgb, var(--pine) 40%, transparent);
}
.sl-card h3 { margin: 1.25rem 0 .6rem; font-size: 1.25rem; font-weight: 700; letter-spacing: -0.015em; }
.sl-card ol { margin: 0; padding-left: 1.45rem; }
.sl-card li { margin: .5rem 0; line-height: 1.55; }
.sl-msg {
  white-space: pre-wrap; overflow-wrap: anywhere; font-size: 1.08rem; line-height: 1.65;
  background: color-mix(in srgb, var(--overlay) 50%, transparent); padding: 1.1rem 1.3rem; border-radius: 14px;
  border: 1px solid var(--edge);
}
.sl-msg mark { background: var(--gold); color: #12101e; padding: 0.12em .4em; border-radius: 6px; font-weight: 650; }
.sl-tile span, .sl-tile small { display: block; }
.sl-table { width: 100%; border-collapse: separate; border-spacing: 0; background: var(--surface); color: var(--text); border-radius: 14px; overflow: hidden; border: 1px solid var(--edge); }
.sl-table th, .sl-table td { border-bottom: 1px solid var(--edge); padding: .75rem 1rem; text-align: left; }
.sl-table tr:last-child td { border-bottom: 0; }
.sl-table th { background: var(--overlay); font-weight: 650; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.03em; }
.sl-legend { font-size: .9rem; margin: .85rem 0 0; opacity: 0.85; line-height: 1.5; }

/* Interactive Controls & Buttons */
.stButton > button, [data-testid="stPageLink-NavLink"] {
  border-radius: 14px; min-height: 3rem; padding: .55rem 1.5rem; font-weight: 650; font-size: 0.98rem;
  background: var(--surface); color: var(--text) !important; border: 1px solid var(--edge);
  transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
.stButton > button p, [data-testid="stPageLink-NavLink"] p { color: var(--text) !important; }
.stButton > button:hover, [data-testid="stPageLink-NavLink"]:hover {
  border-color: var(--accent); background: var(--overlay); transform: translateY(-1.5px);
  color: var(--text) !important;
  box-shadow: 0 4px 14px rgba(0,0,0,0.1);
}
.stButton > button:hover p, [data-testid="stPageLink-NavLink"]:hover p { color: var(--text) !important; }

.stButton > button[kind="primary"] {
  min-height: 3.5rem; font-size: 1.18rem; padding: .65rem 2.6rem;
  border-radius: 14px; font-weight: 750; letter-spacing: -0.01em;
  background: linear-gradient(135deg, var(--accent), color-mix(in srgb, var(--accent) 85%, #000));
  color: var(--on-accent) !important; border-color: var(--accent);
  box-shadow: 0 6px 20px color-mix(in srgb, var(--accent) 40%, transparent); }
.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px);
  background: linear-gradient(135deg, color-mix(in srgb, var(--accent) 90%, #fff), var(--accent));
  color: var(--on-accent) !important;
  box-shadow: 0 8px 24px color-mix(in srgb, var(--accent) 50%, transparent);
}
.stButton > button[kind="primary"] * { color: var(--on-accent) !important; }
[data-testid="stMarkdownContainer"] a { color: var(--accent); text-decoration: underline; text-underline-offset: 3px; font-weight: 550; }
.st-key-grid-features { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.35rem; align-items: stretch; }
.st-key-grid-features > div { display: flex; }
.st-key-grid-features > div > [data-testid="stVerticalBlock"] { flex: 1; }
textarea, [data-baseweb="select"] > div, [data-baseweb="textarea"], [data-baseweb="input"] > div {
  background: var(--overlay) !important; color: var(--text) !important; border-radius: 14px !important;
  border: 1px solid var(--edge) !important; transition: border-color 0.18s ease, box-shadow 0.18s ease;
}
textarea:focus, [data-baseweb="textarea"]:focus-within, [data-baseweb="input"]:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 30%, transparent) !important;
}
[data-testid="stFileUploader"] {
  background: color-mix(in srgb, var(--surface) 70%, var(--base));
  border: 2px dashed var(--edge); border-radius: 16px;
  padding: 1.2rem; transition: all 0.18s ease;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--accent);
  background: var(--surface);
}
[data-testid="stExpander"] { border: 1px solid var(--edge); border-radius: 16px; background: var(--surface); }
label[data-baseweb="checkbox"]:has(input:checked) > span:first-child {
  background: var(--accent) !important; border-color: var(--accent) !important; }
label[data-baseweb="radio"]:has(input:checked) > div:first-child {
  background: var(--accent) !important; border-color: var(--accent) !important; }
[data-testid="stProgress"] [role="progressbar"] > div > div { background: var(--accent) !important; }
a:focus-visible, button:focus-visible, textarea:focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; }
@media (max-width: 640px) {
  .st-key-grid-features { grid-template-columns: 1fr; }
  .sl-hero h1 { font-size: 2.1rem; } .sl-title { font-size: 1.6rem; } .sl-icon { font-size: 2.9rem; }
  .sl-card, [class*="st-key-card"] { padding: 1.2rem; border-radius: 16px; }
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


def _svg(body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="1em" height="1em" '
            f'fill="currentColor" aria-hidden="true" focusable="false">{body}</svg>')


# Static markup, three different shapes so the icon never relies on colour alone.
VERDICT_ICONS = {
    "scam": _svg('<path d="M12 2a10 10 0 100 20 10 10 0 000-20zm4.7 12.3l-1.4 1.4L12 13.4l-3.3 3.3-1.4-1.4'
                 'L10.6 12 7.3 8.7l1.4-1.4L12 10.6l3.3-3.3 1.4 1.4L13.4 12z"/>'),
    "warn": _svg('<path d="M12 2L1 21h22zm1 15h-2v-2h2zm0-4h-2V9h2z"/>'),
    "safe": _svg('<path d="M12 2a10 10 0 100 20 10 10 0 000-20zm-2 15l-5-5 1.4-1.4L10 14.2l7.6-7.6L19 8z"/>'),
}


def accuracy_tile_html() -> str:
    """Home stat tile, numbers read from accuracy_data. The link is an st.page_link (no full reload)."""
    import accuracy_data as ad
    text = f"{ad.RESULTS['hybrid']['accuracy']}% accuracy on {ad.N_MESSAGES} unseen test messages"
    return f'<div class="sl-tile"><b>{html.escape(text)}</b></div>'


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


def highlight(text: str, phrases: list[str]) -> str:
    """Escape every segment of the message; only wrap already-escaped phrases in <mark>."""
    phrases = sorted({p for p in phrases if p}, key=len, reverse=True)
    if not phrases:
        return html.escape(text)
    parts = re.split(f"({'|'.join(map(re.escape, phrases))})", text)
    return "".join(
        f"<mark>{html.escape(p)}</mark>" if i % 2 else html.escape(p) for i, p in enumerate(parts)
    )
