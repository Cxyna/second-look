"""Scam recognition training scenarios and learning data."""
from typing import NamedTuple


class QuizScenario(NamedTuple):
    title: str
    scenario_type: str
    sender: str
    message: str
    is_scam: bool
    difficulty: str
    correct_explanation: str
    tell_signs: list[str]


SCENARIOS: list[QuizScenario] = [
    # --- EASY / BEGINNER ---
    QuizScenario(
        title="Delivery Fee SMS",
        scenario_type="SMS / Text Message",
        sender="+44 7911 123456 (Unknown Mobile)",
        message="Royal Mail: Your package has an unpaid shipping fee of £1.45. To prevent return to sender within 24 hours, update payment: http://royalmai1-fee.com/pay",
        is_scam=True,
        difficulty="Beginner",
        correct_explanation=(
            "This is a classic parcel delivery scam. Real postal services never send SMS from random personal "
            "mobile numbers demanding urgent payment with a lookalike domain."
        ),
        tell_signs=[
            "Lookalike domain: 'royalmai1-fee.com' uses the number 1 instead of the letter 'l'.",
            "Urgency tactic: 'within 24 hours' tries to trigger panic so you act before thinking.",
            "Suspicious sender: Sent from an ordinary personal mobile number (+44 79...), not an official Royal Mail gateway.",
        ],
    ),
    QuizScenario(
        title="Order Confirmation Receipt",
        scenario_type="Email Receipt",
        sender="auto-confirm@amazon.co.uk",
        message="Thank you for your order #204-1928401-29401. Your item 'Wireless Bluetooth Headphones' will be delivered tomorrow. View your order details in your Amazon account.",
        is_scam=False,
        difficulty="Beginner",
        correct_explanation=(
            "Genuine transactional receipt. It tells you an order was placed, quotes an order number, and doesn't threaten suspension or demand bank transfers."
        ),
        tell_signs=[
            "Authentic domain: Sent directly from the real amazon.co.uk address.",
            "No coercive threats or pressure to click unfamiliar third-party links.",
            "Mentions logging in via your normal app/account.",
        ],
    ),
    QuizScenario(
        title="Lottery / Inheritance Notification",
        scenario_type="Email Notification",
        sender="barrister.richardson@gmail.com",
        message="CONFIDENTIAL: You have been selected as the beneficiary of £4,500,000 from a deceased client. Please reply with your passport copy and bank details to release the escrow funds.",
        is_scam=True,
        difficulty="Beginner",
        correct_explanation=(
            "Classic 419 / advance-fee inheritance scam. Legitimate solicitors never contact random strangers from free Gmail accounts offering millions."
        ),
        tell_signs=[
            "Free webmail address: Real legal firms never conduct probate via @gmail.com.",
            "Too good to be true: You cannot inherit millions from someone you have never met.",
            "Harvesting identity: Asks for passport copies and bank details.",
        ],
    ),

    # --- MEDIUM / INTERMEDIATE ---
    QuizScenario(
        title="Two-Factor Security Code",
        scenario_type="SMS Verification",
        sender="Google (Official shortcode)",
        message="G-492104 is your Google verification code. Do not share this code with anyone.",
        is_scam=False,
        difficulty="Intermediate",
        correct_explanation=(
            "This is a legitimate verification code. It does not ask for money, links, passwords, or replies."
        ),
        tell_signs=[
            "No link attached: Genuine verification codes provide a number to type in yourself.",
            "No demand for money or passwords.",
            "Safety reminder: 'Do not share this code' is standard best practice for authentic services.",
        ],
    ),
    QuizScenario(
        title="Urgent Bank Security Alert",
        scenario_type="Email Notification",
        sender="security@barclays-account-alert.net",
        message="URGENT: Suspicious login from Moscow detected on your account. Your online banking is temporarily suspended. Click here to confirm your identity immediately: http://bit.ly/barclays-restore",
        is_scam=True,
        difficulty="Intermediate",
        correct_explanation=(
            "Banks will never ask you to verify your identity or log in through a shortened URL link or an unofficial domain."
        ),
        tell_signs=[
            "Hidden destination: Uses a bit.ly shortened link to disguise where the page actually leads.",
            "Unofficial sender domain: Real Barclays emails come from barclays.co.uk, not barclays-account-alert.net.",
            "Panic trigger: Fabricates a terrifying location ('Moscow') to make you click without checking.",
        ],
    ),
    QuizScenario(
        title="IT Department Password Expiry",
        scenario_type="Work Email",
        sender="helpdesk@company-internal-sso.info",
        message="Your corporate network password expires in 2 hours. Keep your current password by verifying your credentials at: https://portal.company.com.sso-auth.info/login",
        is_scam=True,
        difficulty="Intermediate",
        correct_explanation=(
            "Corporate spear-phishing attack. It uses a deceptive subdomain ('portal.company.com') to trick you, while the true destination domain is 'sso-auth.info'."
        ),
        tell_signs=[
            "Deceptive subdomain: The real website is '.sso-auth.info', not your company.",
            "Artificial urgency: 2-hour deadline to induce compliance.",
            "Disposable TLD: Uses .info instead of company infrastructure.",
        ],
    ),

    # --- HARD / ADVANCED (PRO JUDGE LEVEL) ---
    QuizScenario(
        title="WhatsApp 'Mum, it's me' Message",
        scenario_type="WhatsApp Chat",
        sender="+44 7700 900123 (Unknown Number)",
        message="Hi Mum, I dropped my phone down the toilet and this is my new temporary number. I have an urgent bill due today and my banking app is locked on this new phone. Can you transfer £450 to my friend so it doesn't bounce? Sort code: 20-04-15 Acc: 81920391",
        is_scam=True,
        difficulty="Advanced",
        correct_explanation=(
            "The infamous 'Hi Mum / Hi Dad' impersonation scam. Criminals exploit parental affection to bypass skepticism."
        ),
        tell_signs=[
            "Convenient excuse: Broken phone or lost wallet to explain contacting from an unknown number.",
            "Urgent request for money: Demands a direct bank transfer under emotional pressure.",
            "Third-party account: Asking to send money to an unfamiliar bank account.",
        ],
    ),
    QuizScenario(
        title="Reassurance Reverse-Psychology Phish",
        scenario_type="SMS Alert",
        sender="HSBC-Alert",
        message="HSBC Security: A transaction of £890.00 to CryptoPay Ltd is pending. If this was NOT you, call our fraud desk immediately on 0800 048 7192. HSBC will NEVER ask for your PIN or online password.",
        is_scam=True,
        difficulty="Expert",
        correct_explanation=(
            "Extremely sophisticated vishing lure. Scammers deliberately echo real bank safety advice ('HSBC will NEVER ask for your PIN') to win your trust, but the phone number connects directly to their call center."
        ),
        tell_signs=[
            "Reassurance bait: Real-sounding warnings ('we never ask for PIN') are used to disarm suspicion.",
            "Rogue inbound number: The phone number is an inbound fraud trap, not the official number on the back of your card.",
            "Reverse psychology: Making the victim initiate the phone call makes them feel in control.",
        ],
    ),
    QuizScenario(
        title="Real Doctor Appointment Reminder",
        scenario_type="SMS Notification",
        sender="NHS-NoReply",
        message="Reminder: You have an appointment at St Mary's Health Centre on 14 Oct at 10:15am with Dr. Watson. If you cannot attend, reply CANCEL to 83120 or call the practice on their usual number.",
        is_scam=False,
        difficulty="Advanced",
        correct_explanation=(
            "Legitimate healthcare notification. It requests no personal data, no credit card, no external web link, and specifies the official GP practice."
        ),
        tell_signs=[
            "No links or demands: Contains zero web links or requests for payment.",
            "Standard cancellation shortcode: Uses standard NHS shortcode mechanism.",
            "Specific local detail: References a real appointment and practice.",
        ],
    ),
    QuizScenario(
        title="Zero-Link Callback Social Engineering",
        scenario_type="Billing Email",
        sender="billing@geek-tech-renewals.com",
        message="Invoice #INV-89104: Your annual Total Protection Plan has automatically renewed for $499.00 and debited from your card ending in 4102. If you did not authorize this renewal or wish to request an immediate refund, please call our 24/7 billing line: +1 (888) 512-8921 within 48 hours.",
        is_scam=True,
        difficulty="Expert",
        correct_explanation=(
            "Classic 'Refund Scam' callback lure. Because spam filters flag links, scammers include no links at all—only an urgent fake invoice and phone number to lure victims into calling where remote-access software (AnyDesk/TeamViewer) is installed."
        ),
        tell_signs=[
            "Evasion of spam filters: Uses zero hyperlinks to bypass security crawlers.",
            "Fake charge panic: Claims you were already charged hundreds of dollars so you panic-call.",
            "Coerced refund trap: Directs you to a phone number where scammers impersonate technical support.",
        ],
    ),
]
