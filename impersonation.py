"""Hardcoded scenario data for the 'Is it really them?' page.

No model calls. No user data stored. All content is fixed at import time.
"""

IDENTITY_NOTE = (
    "Caller ID, a familiar voice, and a photo are not proof of identity. "
    "Phone numbers can be spoofed to show any name or number. "
    "Voices can be copied using widely available software. "
    "This tool makes no claim about spotting AI-generated audio or video."
)

SAFE_WORD_ADVICE = (
    "Agree on a word or short phrase that only your close family knows — something "
    "unlikely to come up in ordinary conversation. If anyone calls claiming to be a "
    "family member in an emergency, ask for the safe word before doing anything else. "
    "Choose it together in person, keep it private, and change it if you ever think "
    "it has been overheard. "
    "Don't use anything that can be found online, like a pet's name or a birthday, "
    "and never send it by text or email."
)

SCENARIOS: dict[str, dict] = {
    "relative": {
        "label": "A relative — new number or says they're in trouble",
        "how_it_works": (
            "Someone calls or messages claiming to be a family member or close friend "
            "with a new number, or says they are in an emergency and need money urgently. "
            "The urgency is designed to make you act before you have time to think."
        ),
        "warning_signs": [
            "They have a number you don't recognise and ask you not to call the old one.",
            "There is an urgent request for money, gift cards, or a bank transfer.",
            "They ask you to keep it secret from other family members.",
            "The story involves an accident, arrest, hospital, or being stranded abroad.",
            "They pressure you to act immediately.",
        ],
        "check_steps": [
            "Stop. Do not send money, gift cards, or personal details yet.",
            "Call or message them on the number or account you already had for them — "
            "not the new one given in this message.",
            "Ask another family member or close friend if they have heard from this person.",
            "Ask the family safe word if you have one.",
            "If you cannot reach them, wait a short time before acting — genuine "
            "emergencies rarely require payment within minutes.",
        ],
        "questions": [
            "What is our safe word? (Only ask this if you have set one up.)",
            "What did we talk about the last time we saw each other in person?",
            "What is the name of our childhood pet or a detail only we would know?",
            "What was the address of the first home we shared?",
        ],
        "never": [
            "Never send cash, gift cards, or wire transfers on the basis of one message or call.",
            "Never share bank details because someone claims to need them urgently.",
            "Never let yourself be rushed — legitimate family emergencies allow time to verify.",
            "Never pay before you have spoken to another family member.",
        ],
    },

    "boss-colleague": {
        "label": "A boss or colleague with an urgent request",
        "how_it_works": (
            "A message or call appears to come from a manager or colleague asking you "
            "to do something quickly — buy gift cards, make a payment, or share login "
            "details — often claiming they are unavailable to speak directly. "
            "These requests usually arrive by email or text and create a false sense of authority."
        ),
        "warning_signs": [
            "The request comes from an email address or number slightly different from the real one.",
            "They ask you to buy gift cards and send the codes.",
            "They say they are in a meeting or abroad and cannot talk.",
            "You are asked to keep the request confidential.",
            "There is pressure to act before checking with anyone else.",
        ],
        "check_steps": [
            "Stop. Do not buy gift cards, make transfers, or share credentials yet.",
            "Call or message your manager or colleague on the number or account you already had — "
            "not any contact given in the message.",
            "Check with another colleague who works with this person.",
            "Follow your workplace's normal authorisation process for payments — no genuine "
            "request should bypass it.",
            "If in doubt, speak to someone senior in person or by a separate channel.",
        ],
        "questions": [
            "What project did we work on together last week?",
            "What was discussed in our last team meeting?",
            "Ask about something you did together recently that was never written down in an email or chat.",
        ],
        "never": [
            "Never buy gift cards for a work request — gift cards are not a normal way for an employer to ask for payment.",
            "Never share passwords or login codes by text or email.",
            "Never make a payment outside normal approval channels because of an urgent message.",
            "Never assume a familiar name in an email address means it is genuine.",
        ],
    },

    "bank-tax-company": {
        "label": "Someone from a bank, tax office, or company",
        "how_it_works": (
            "A caller or message claims to be from your bank, a tax authority, or a "
            "well-known company, often saying your account is at risk or that you owe "
            "money and must act immediately. "
            "The goal is to make you transfer money to a 'safe account' or hand over "
            "security codes."
        ),
        "warning_signs": [
            "They ask you to move money to a 'safe' or 'holding' account.",
            "They ask for your full PIN, password, or one-time passcode.",
            "They say your account has been compromised and you must act now.",
            "The caller ID matches your bank's number — this can be faked.",
            "They ask you to stay on the line while you visit a branch or cashpoint.",
        ],
        "check_steps": [
            "Stop. Do not transfer money or share security codes yet.",
            "Hang up and call the organisation back on a number you already had — "
            "printed on your card, your statement, or the organisation's official website — "
            "not any number given in the call or message.",
            # VERIFY: confirm whether it's safe to say "wait a few minutes before calling back"
            # on all networks, as some landlines keep the line open briefly after hanging up.
            "Use a different phone if possible when calling back.",
            "Ask another family member or trusted person before moving any money.",
            "Remember: your bank will never ask for your full PIN or one-time passcode.",
        ],
        "questions": [
            "What is the exact amount and date of my last transaction you can see?",
            "What is the full name on my account?",
            "What branch or service did I last contact you through?",
        ],
        "never": [
            "Never give your full PIN, password, or one-time passcode to a caller.",
            "Never move money to a 'safe account' at a caller's request — banks do not do this.",
            "Never stay on the line with a suspicious caller and then immediately call your bank "
            "from the same phone without hanging up first.",
            "Never let a caller talk you out of checking with someone you trust.",
        ],
    },

    "wrong-number": {
        "label": "A 'wrong number' message from a stranger",
        "how_it_works": (
            "You receive a friendly message that appears to be intended for someone else. "
            "When you reply to correct them, the stranger strikes up a conversation and "
            "eventually introduces an investment opportunity, a romantic interest, or a "
            "request for help."
        ),
        "warning_signs": [
            "The first message is friendly and seems harmless — a recipe, a greeting, a photo.",
            "The person is very quick to build a warm relationship.",
            "They introduce a topic like cryptocurrency, forex, or a 'can't lose' investment.",
            "They avoid video calls or always have a reason they cannot meet.",
            "They eventually ask for money, a gift, or access to your accounts.",
        ],
        "check_steps": [
            "Stop. Do not send money or personal details to someone you met this way.",
            "Do not continue the conversation on a different app they suggest.",
            "Use a number or account you already had for a trusted friend or family "
            "member to talk through the situation before acting.",
            "Search the name and phrases they use online to see if others report the same.",
            "Remember that genuine wrong numbers rarely lead to lasting friendships or "
            "investment tips.",
        ],
        "questions": [
            "What specific thing did I tell you about myself that I have not posted publicly?",
            "What was the exact reason you first messaged me, in your own words?",
        ],
        "never": [
            "Never send money to someone you only met through an unexpected message.",
            "Never move to a different messaging app at their request.",
            "Never share financial account details or identification documents.",
            "Never let a sense of friendship or romance override caution with someone you have "
            "never met in person.",
        ],
    },

    "online-contact": {
        "label": "Someone I met online asks for money or to move chats",
        "how_it_works": (
            "Someone you met on a dating site, social platform, or game builds a relationship "
            "over weeks or months, then has an emergency or opportunity requiring money — "
            "often claiming they will repay you soon. "
            "They may also ask you to continue talking on a less monitored platform."
        ),
        "warning_signs": [
            "They have never met you in person despite many conversations.",
            "Video calls are always blurry, brief, or cancelled at the last moment.",
            "They have a dramatic story: military abroad, working on an oil rig, a sick relative.",
            "They ask for money via wire transfer, gift cards, or cryptocurrency.",
            "They suggest moving from the platform where you met to a private channel.",
        ],
        "check_steps": [
            "Stop. Do not send money or move to another platform yet.",
            "Contact a trusted friend or family member using a number or account you already "
            "had, and describe the situation to them before acting.",
            "Do a reverse image search on their profile photos.",
            "Ask for a live video call where they hold up a handwritten note with today's date.",
            "If they refuse video or make repeated excuses, treat this as a serious warning sign.",
        ],
        "questions": [
            "What is the name of the street where we first said we would meet?",
            "What specific detail did I share about myself that I have not posted publicly?",
            "Can you appear on video right now, holding a note with today's date written on it?",
        ],
        "never": [
            "Never send money, gift cards, or cryptocurrency to someone you have not met in person.",
            "Never share intimate photos that could later be used as leverage.",
            "Never move to a platform they choose just because they ask.",
            "Never let the length of an online relationship be proof that the person is genuine.",
        ],
    },

    "marketplace": {
        "label": "A buyer or seller on a marketplace",
        "how_it_works": (
            "A buyer sends more than the asking price and asks you to send back the difference, "
            "or sends a fake payment confirmation and asks you to ship first. "
            "A seller takes payment and disappears, or sends a counterfeit item."
        ),
        "warning_signs": [
            "A buyer sends more than the asking price and wants the difference wired back.",
            "Payment 'confirmation' arrives by email but the money is not yet in your account.",
            "A seller insists on payment by bank transfer, gift card, or cryptocurrency.",
            "They pressure you to complete the transaction before you can verify payment.",
            "Their account was created very recently or has no reviews.",
        ],
        "check_steps": [
            "Stop. Do not ship goods or send money until payment is confirmed in your account.",
            "Log into your bank or payment account directly — not via a link in any message — "
            "and confirm funds have cleared.",
            "Contact the marketplace's support team on the number or account you already "
            "had from their official site, not from a number or link in a message.",
            "For large purchases, meet in person in a safe public place if possible.",
            "If something feels wrong, walk away — there will be other buyers and sellers.",
        ],
        "questions": [
            "Can you provide the item's serial number or proof of purchase?",
            "Can we meet in person, or use the marketplace's official payment protection?",
            "Has the payment actually cleared in my account yet — not just a confirmation message?",
        ],
        "never": [
            "Never ship an item before payment is confirmed in your account.",
            "Never send money back for an overpayment — the original payment is likely to bounce and you will lose both.",
            "Never pay by gift card, wire transfer, or cryptocurrency for marketplace goods.",
            "Never click a payment link sent in a message — go to the site directly.",
        ],
    },
}
