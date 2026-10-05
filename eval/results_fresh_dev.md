# Second Look: Evaluation Results

Dev split: 50 messages (22 scam, 28 legitimate). Model: `Qwen/Qwen3-32B`. Rules threshold: score >= 40. "likely scam" and "suspicious" count as flagged.

| Configuration | Accuracy | Precision | Recall | F1 | API errors (excluded) |
|---|---|---|---|---|---|
| rules-only | 58% | 100% | 5% | 0.09 | 0 |
| model-only | 94% | 95% | 90% | 0.92 | 3 |
| hybrid | 92% | 95% | 86% | 0.90 | 0 |

Errors per configuration: rules-only 0, model-only 3, hybrid 0.

## rules-only

| | Predicted scam | Predicted legit |
|---|---|---|
| **Actually scam** | 1 | 21 |
| **Actually legit** | 0 | 28 |

- **f29** (missed scam, verdict: *rules score 0*): Halberd Bank Fraud Team: we've blocked a £950 payment. Never share your PIN with anyone. To confirm it was not you, read us the 6-digit code we are about to send you.
- **f30** (missed scam, verdict: *rules score 0*): Hi, this is Halberd Bank security. We just sent you a verification code by mistake while checking your account. Please read it back to me so I can cancel it and keep your money safe.
- **f31** (missed scam, verdict: *rules score 0*): Brightwater Card: unusual spend of £1,240.00 detected at Vexel Electronics. If this wasn't you, secure your account now: brightwatercard-secure.com/verify
- **f32** (missed scam, verdict: *rules score 20*): Hi Dana, it's Marcus. In a meeting and can't talk. Can you quickly pick up some Tanglewood gift cards for a client thank-you? About £200 total. Scratch off and send me the codes here. I'll reimburse you today.
- **f33** (missed scam, verdict: *rules score 20*): Morning, can you pull the headcount report together for the board and send it over? Thanks. Also, I need a favour while I'm travelling: please buy 4 x $100 gift cards and message me the codes. Keep this between us until I'm back.
- **f35** (missed scam, verdict: *rules score 20*): IRS Notice: an unresolved balance of $1,873.00 is on your account. A payment arrangement is required today. Call 800-555-0142 immediately to avoid enforcement action. Case ref 7731-AX.
- **f36** (missed scam, verdict: *rules score 0*): Hi, sorry to message out of the blue. I saw your profile and honestly you seem like the kindest person. I'm on a rig off Norway for another month with bad signal but I think about you every day. Can I call you tonight?
- **f37** (missed scam, verdict: *rules score 0*): Good morning my love. I wish you were here. My daughter's school fees are due and the bank here has frozen my card. I hate asking, but could you help me with $400 until I'm home? I'll pay you back, I promise.
- **f38** (missed scam, verdict: *rules score 0*): Redkite Couriers: your parcel is held at the depot. A £1.45 redelivery fee is due. Pay securely at redkitecouriers.co.uk.parcel-pay.com to rebook delivery.
- **f39** (missed scam, verdict: *rules score 0*): We reviewed your application for Customer Support Associate (remote, £2,800/month) and you're hired! Before we send your contract and laptop, please pay a £95 background check and training fee to our HR agent.
- **f40** (missed scam, verdict: *rules score 0*): Hi Priya, following up on invoice 4410 for $12,450. Please note our bank details have changed as of this month. New account: 000111222, routing 000000000. Please update your records and pay by Friday.
- **f41** (missed scam, verdict: *rules score 0*): Hi, is this Kevin? We met at Danielle's party last week. Sorry if I have the wrong number!
- **f42** (missed scam, verdict: *rules score 0*): Hello, I think I have the wrong number but you sound like a lovely person. I'm Anna, I'm new in town. Do you mind if we chat? I'd love a friend.
- **f43** (missed scam, verdict: *rules score 20*): Quillpad: someone signed in to your account from Lagos. We've paused it to protect you. Restore access here: quillpad-support.net/restore. Never share your password with anyone.
- **f44** (missed scam, verdict: *rules score 0*): Halberd Bank: you've been set up as a new payee for £2,400. If this wasn't you, call us straight away on 0330 555 0199 and move your savings to a safe account that we will set up for you.
- **f45** (missed scam, verdict: *rules score 0*): Mum, I dropped my phone in the sea and this is my new number. Can you send some money for a repair? I can't use the banking app right now. I'll explain later, please don't call it.
- **f46** (missed scam, verdict: *rules score 20*): Longbarrow Energy: you are due a £140 winter bill credit. To receive it, verify your account at longbarrow-energy-rebate.co.uk. This offer closes at midnight.
- **f47** (missed scam, verdict: *rules score 0*): Parcel notice: we attempted delivery of your Marlow & Finch order but your address is incomplete. Pay a £2.99 handling fee at marlowfinch-delivery.com/pay to release the parcel.
- **f48** (missed scam, verdict: *rules score 0*): Final reminder: your Tanglewood Music subscription has been auto-renewed for $389.99. If you didn't authorise this, call our billing line on 888-555-0176 to arrange an immediate refund.
- **f49** (missed scam, verdict: *rules score 0*): Hi, I'm interested in the sofa you listed. I'll pay in full today and arrange my courier. I just need you to confirm with the code I'm about to text you, it's a verification the marketplace uses.
- **f50** (missed scam, verdict: *rules score 20*): Dear customer, your Brightwater Card has been suspended due to a security review. We will never ask for your PIN. To reactivate, reply with your full card number and the 3-digit code on the back.

## model-only

| | Predicted scam | Predicted legit |
|---|---|---|
| **Actually scam** | 18 | 2 |
| **Actually legit** | 1 | 26 |

- **f06** (false alarm, verdict: *likely scam*): hey sorry to chase, can you send me your half of the Airbnb? it was £86.50. my sort code is in our old chat. cheers!
- **f36** (missed scam, verdict: *likely safe*): Hi, sorry to message out of the blue. I saw your profile and honestly you seem like the kindest person. I'm on a rig off Norway for another month with bad signal but I think about you every day. Can I call you tonight?
- **f42** (missed scam, verdict: *likely safe*): Hello, I think I have the wrong number but you sound like a lovely person. I'm Anna, I'm new in town. Do you mind if we chat? I'd love a friend.

## hybrid

| | Predicted scam | Predicted legit |
|---|---|---|
| **Actually scam** | 19 | 3 |
| **Actually legit** | 1 | 27 |

- **f06** (false alarm, verdict: *likely scam*): hey sorry to chase, can you send me your half of the Airbnb? it was £86.50. my sort code is in our old chat. cheers!
- **f36** (missed scam, verdict: *likely safe*): Hi, sorry to message out of the blue. I saw your profile and honestly you seem like the kindest person. I'm on a rig off Norway for another month with bad signal but I think about you every day. Can I call you tonight?
- **f41** (missed scam, verdict: *likely safe*): Hi, is this Kevin? We met at Danielle's party last week. Sorry if I have the wrong number!
- **f42** (missed scam, verdict: *likely safe*): Hello, I think I have the wrong number but you sound like a lovely person. I'm Anna, I'm new in town. Do you mind if we chat? I'd love a friend.
