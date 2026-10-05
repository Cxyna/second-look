# Second Look: Evaluation Results

Test split: 40 messages (20 scam, 20 legitimate). Model: `Qwen/Qwen3-32B`. Rules threshold: score >= 40. "likely scam" and "suspicious" count as flagged.

| Configuration | Accuracy | Precision | Recall | F1 | API errors (excluded) |
|---|---|---|---|---|---|
| rules-only | 50% | 0% | 0% | 0.00 | 0 |
| model-only | 75% | 67% | 100% | 0.80 | 0 |
| hybrid | 68% | 61% | 100% | 0.75 | 0 |

Errors per configuration: rules-only 0, model-only 0, hybrid 0.

## rules-only

| | Predicted scam | Predicted legit |
|---|---|---|
| **Actually scam** | 0 | 20 |
| **Actually legit** | 0 | 20 |

- **s02** (missed scam, verdict: *rules score 0*): USPS: Your package 9400 1000 0000 0000 0000 00 is on hold due to an incomplete address. Update within 12 hours: usps-package-hold.top/update
- **s03** (missed scam, verdict: *rules score 0*): Evri: Your parcel is waiting. A customs fee of £2.99 is due before we can deliver. Pay now: bit.ly/3xEvriPay
- **s05** (missed scam, verdict: *rules score 0*): Barclays Fraud Team: Unusual activity on your account. A payment of £850 to J. Marlow is pending. If this wasn't you, log in at barclays-secure-verify.co to cancel.
- **s06** (missed scam, verdict: *rules score 20*): Chase Alert: Your debit card has been locked after a suspicious $640 charge. Verify your identity now at chase-cardsecurity.net/unlock to restore access.
- **s08** (missed scam, verdict: *rules score 20*): Hi Priya, it's Graham. I'm stuck in a meeting and can't talk. I need 5 x $100 Amazon gift cards for a client today. Buy them and send me the codes by text. I'll reimburse you. Keep it quiet for now.
- **s09** (missed scam, verdict: *rules score 20*): Hello Tom, this is your MD, Susan Hale. Are you at your desk? I need you to do something urgent and discreet. Reply asap, I'm on my personal number as my work phone is dead.
- **s11** (missed scam, verdict: *rules score 0*): Mum it's me, I dropped my phone in the loo and this is my new number. I'm in trouble, I need £400 sent to a friend right now for a bill. Please don't call, just transfer. I'll explain later.
- **s12** (missed scam, verdict: *rules score 0*): Grandma, it's Tyler. I was in a car accident and I'm at the police station. I need $2,500 for bail. Please don't tell Mom and Dad. A lawyer will call you with where to wire it.
- **s14** (missed scam, verdict: *rules score 0*): Hello my dear, I am Colonel James Burke, US Army, stationed overseas. I feel a deep connection with you. I need $1,800 to pay for leave papers so I can finally fly to meet you my love.
- **s15** (missed scam, verdict: *rules score 0*): Hey beautiful, I know we've only talked for 3 weeks but I love you. My business shipment is stuck at customs and I need £1,200 for fees. You are the only one I trust. Will you help me?
- **s17** (missed scam, verdict: *rules score 20*): Join our private group! Our AI trading bot turned $500 into $7,300 in 7 days. Guaranteed 20% daily returns. Deposit USDT at crypto-alpha-gains.io now, only 12 spots left!
- **s18** (missed scam, verdict: *rules score 0*): Hi, I saw your profile. I'm a trader with Meridian Capital. My clients earn 300% monthly on forex signals. Send £250 to start and I'll double it by Friday. No risk.
- **s20** (missed scam, verdict: *rules score 20*): HMRC: You are eligible for a tax refund of £412.60. To receive it, submit your bank details within 24 hours at hmrc-refund-claim.org.uk. Failure to do so may result in forfeiture.
- **s21** (missed scam, verdict: *rules score 20*): HM Revenue & Customs final notice: unpaid tax of £1,870. A warrant will be issued for your arrest unless you pay today by bank transfer. Call 0113 496 0000 immediately.
- **s23** (missed scam, verdict: *rules score 20*): IRS Final Warning: Your 2023 tax return has errors. A federal case has been opened in your name. Pay $3,200 in Apple gift cards today to avoid arrest. Call 555-0142.
- **s24** (missed scam, verdict: *rules score 0*): MICROSOFT WARNING: Your computer is infected with 3 viruses! Call our certified technicians now on 0800 555 0188. Do not shut down your PC or you will lose all your data.
- **s26** (missed scam, verdict: *rules score 20*): Your Apple ID was used to purchase a MacBook Pro for $1,499. If you did not authorise this, call Apple Support at 1-800-555-0176 immediately to cancel the order.
- **s27** (missed scam, verdict: *rules score 20*): Your Netflix account has been suspended due to a billing problem. Update your payment details within 24 hours at netflix-billing-update.co to avoid permanent closure.
- **s29** (missed scam, verdict: *rules score 20*): Amazon: Your Prime membership could not be renewed. Your account will be suspended in 6 hours. Verify your card at amazon-account-verify.top/signin.
- **s30** (missed scam, verdict: *rules score 0*): Google: Your Gmail storage is full and your account will be deleted in 48 hours. Click here to keep your data: goo.gl/Xk29Ls then sign in to confirm.

## model-only

| | Predicted scam | Predicted legit |
|---|---|---|
| **Actually scam** | 20 | 0 |
| **Actually legit** | 10 | 10 |

- **l02** (false alarm, verdict: *suspicious*): Chase: A $62.18 purchase at TRADER JOE'S #512 was made with your card ending in 7730. Reply STOP to opt out of alerts. We'll never ask for your password by text.
- **l03** (false alarm, verdict: *suspicious*): Monzo: You've been paid £150.00 by Sam Okoye. Your balance is now £842.17. Open the app to see the details.
- **l06** (false alarm, verdict: *suspicious*): Amazon: Your order of 'Silicone Baking Mat Set' has shipped and arrives Thursday. Track your package anytime in Your Orders on amazon.com.
- **l08** (false alarm, verdict: *likely scam*): Your GitHub password reset code is 482910. It expires in 15 minutes. If you didn't ask for this, ignore this message. Nobody from GitHub will ask for this code.
- **l11** (false alarm, verdict: *likely scam*): Your Lloyds Bank one-time passcode is 307845. It expires in 10 minutes. We will never call to ask for this code.
- **l12** (false alarm, verdict: *likely scam*): Your Venmo security code is 619204. Never share this code, Venmo will never ask for it.
- **l17** (false alarm, verdict: *suspicious*): Thanks for covering the Airbnb! My half is $212.50. Sending via Venmo now, let me know when you get it.
- **l18** (false alarm, verdict: *suspicious*): Hey it's Maya, can you Zelle me $18 for your share of the pizza last Friday? No rush.
- **l20** (false alarm, verdict: *suspicious*): Your cart misses you! Use code SAVE15 for 15% off your order at nike.com. Offer ends Sunday. View in browser | Unsubscribe | Privacy Policy
- **l23** (false alarm, verdict: *suspicious*): Hi Chris, your Jiffy Lube oil change is scheduled for Saturday at 10:00 AM. Reply YES to confirm or call us at (555) 010-2299 to reschedule.

## hybrid

| | Predicted scam | Predicted legit |
|---|---|---|
| **Actually scam** | 20 | 0 |
| **Actually legit** | 13 | 7 |

- **l02** (false alarm, verdict: *likely scam*): Chase: A $62.18 purchase at TRADER JOE'S #512 was made with your card ending in 7730. Reply STOP to opt out of alerts. We'll never ask for your password by text.
- **l05** (false alarm, verdict: *suspicious*): UPS: Your package from Wayfair has been delivered to the front porch at 2:14 PM. Photo available in your UPS My Choice account.
- **l06** (false alarm, verdict: *suspicious*): Amazon: Your order of 'Silicone Baking Mat Set' has shipped and arrives Thursday. Track your package anytime in Your Orders on amazon.com.
- **l08** (false alarm, verdict: *likely scam*): Your GitHub password reset code is 482910. It expires in 15 minutes. If you didn't ask for this, ignore this message. Nobody from GitHub will ask for this code.
- **l09** (false alarm, verdict: *likely scam*): Microsoft account: A request was made to change the password for ja***@outlook.com. If this was you, tap the link in the Microsoft Authenticator app. If not, no action needed.
- **l11** (false alarm, verdict: *likely scam*): Your Lloyds Bank one-time passcode is 307845. It expires in 10 minutes. We will never call to ask for this code.
- **l12** (false alarm, verdict: *likely scam*): Your Venmo security code is 619204. Never share this code, Venmo will never ask for it.
- **l17** (false alarm, verdict: *suspicious*): Thanks for covering the Airbnb! My half is $212.50. Sending via Venmo now, let me know when you get it.
- **l18** (false alarm, verdict: *suspicious*): Hey it's Maya, can you Zelle me $18 for your share of the pizza last Friday? No rush.
- **l21** (false alarm, verdict: *suspicious*): Black Friday early access: take up to 40% off at Best Buy. Free shipping over $35. Shop deals at bestbuy.com/blackfriday. Manage preferences or unsubscribe.
- **l23** (false alarm, verdict: *likely scam*): Hi Chris, your Jiffy Lube oil change is scheduled for Saturday at 10:00 AM. Reply YES to confirm or call us at (555) 010-2299 to reschedule.
- **l24** (false alarm, verdict: *suspicious*): Octopus Energy: Your bill for April is ready. £64.20 will be taken by Direct Debit on 5 May. View your statement in the app.
- **l29** (false alarm, verdict: *suspicious*): IRS: Your tax return was accepted. Check your refund status at irs.gov/refunds with Where's My Refund. The IRS never initiates contact by text or email to ask for personal info.
