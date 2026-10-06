from typing import NamedTuple


class PageInfo(NamedTuple):
    title: str
    path: str
    icon: str
    blurb: str
    enabled: bool


PAGES: list[PageInfo] = [
    PageInfo("Home", "pages_/home.py", ":material/home:", "", True),
    PageInfo("Check a message", "pages_/check.py", ":material/verified_user:",
             "Paste a message and get a plain-English verdict.", True),
    PageInfo("Already clicked or paid?", "pages_/clicked.py", ":material/emergency:",
             "Step-by-step help if you already acted.", True),
    PageInfo("Is it really them?", "pages_/verify.py", ":material/person_search:",
             "Check whether a sender is who they say they are.", True),
    PageInfo("How accurate is it?", "pages_/accuracy.py", ":material/fact_check:",
             "See how well the checker performs.", True),
    PageInfo("About and privacy", "pages_/about.py", ":material/lock:",
             "What we do with your text.", True),
]
