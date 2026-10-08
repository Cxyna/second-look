import html
import streamlit as st

import url_inspector
from ui.theme import VERDICT_ICONS

st.html(
    '<div class="sl-hero"><h1>Inspect a link</h1>'
    "<p>Check where a website or link actually goes before you tap or enter credentials.</p>"
    '<span class="sl-note">Safe Sandbox: We analyze domain structure locally without visiting or triggering the link.</span></div>'
)

EXAMPLES = [
    ("Real PayPal", "https://www.paypal.com/signin"),
    ("Subdomain Trick", "https://paypal.com.account-verify.xyz/login"),
    ("Typo Lookalike", "https://paypa1-secure-billing.com"),
    ("Shortened Link", "https://bit.ly/royalmail-fee"),
]

st.markdown("**Try an example link:**")
cols = st.columns(len(EXAMPLES))
for col, (label, ex_url) in zip(cols, EXAMPLES):
    if col.button(label, use_container_width=True):
        st.session_state["inspect_input"] = ex_url

url_input = st.text_input(
    "Enter a URL, website address, or link from a message",
    key="inspect_input",
    placeholder="e.g. royalmail-tracking.xyz/parcel",
)

if st.button("Inspect Link", type="primary"):
    if not url_input.strip():
        st.warning("Please enter a link or domain to inspect.")
    else:
        with st.spinner("Deconstructing domain anatomy..."):
            res = url_inspector.inspect_url(url_input)

        if "error" in res:
            st.error(res["error"])
        else:
            esc = html.escape
            risk = res["risk_level"]
            css_class = "scam" if risk == "High Risk" else ("warn" if risk == "Suspicious" else "safe")
            icon_key = "scam" if risk == "High Risk" else ("warn" if risk == "Suspicious" else "safe")

            st.html(
                f'<div class="sl-card sl-verdict {css_class}">'
                f'<div class="sl-head"><span class="sl-icon" aria-hidden="true">{VERDICT_ICONS[icon_key]}</span>'
                f'<span class="sl-title">{risk}</span></div>'
                + "".join(f'<p class="sl-reason">⚠️ {esc(r)}</p>' for r in res["risk_reasons"])
                + '</div>'
            )

            # Visual Anatomy Breakdown Table
            st.subheader("Domain Anatomy")
            st.caption("Scammers trick people by hiding the real destination behind confusing subdomains or lookalike spellings.")

            st.html(
                '<table class="sl-table">'
                '<tr><th>Element</th><th>Extracted Value</th><th>Explanation</th></tr>'
                f'<tr><td><b>True Destination Domain</b></td><td><code>{esc(res["registered_domain"])}</code></td><td>This is the actual website owner you are connecting to.</td></tr>'
                f'<tr><td><b>Subdomain / Prefix</b></td><td><code>{esc(res["subdomain"])}</code></td><td>Often used by scammers to display a trusted brand name before the real domain.</td></tr>'
                f'<tr><td><b>Top-Level Domain (TLD)</b></td><td><code>.{esc(res["tld"])}</code></td><td>The registry domain suffix.</td></tr>'
                f'<tr><td><b>Full Hostname</b></td><td><code>{esc(res["host"])}</code></td><td>The full server address.</td></tr>'
                '</table>'
            )

            if res["is_official_brand"]:
                st.success(f"Verified: `{res['registered_domain']}` is the authentic registered domain of {res['official_for'].title()}.")
