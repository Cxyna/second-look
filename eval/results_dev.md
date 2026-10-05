# Second Look: Evaluation Results

Dev split: 20 messages (10 scam, 10 legitimate). Model: `Qwen/Qwen3-32B`. Rules threshold: score >= 40. "likely scam" and "suspicious" count as flagged.

| Configuration | Accuracy | Precision | Recall | F1 | API errors (excluded) |
|---|---|---|---|---|---|
| rules-only | 70% | 100% | 40% | 0.57 | 0 |
| model-only | 100% | 100% | 100% | 1.00 | 0 |
| hybrid | 100% | 100% | 100% | 1.00 | 0 |

Errors per configuration: rules-only 0, model-only 0, hybrid 0.

## rules-only

| | Predicted scam | Predicted legit |
|---|---|---|
| **Actually scam** | 4 | 6 |
| **Actually legit** | 0 | 10 |

- **s07** (missed scam, verdict: *rules score 0*): This is Mark from Lloyds fraud department. Your account is compromised. For your safety, move your savings into a new safe account, sort code 04-00-99, account 12345678. Do not tell branch staff.
- **s10** (missed scam, verdict: *rules score 0*): Morning Alex, can you pick up £500 of iTunes vouchers on the company card? It's a surprise for a client. Scratch off and send me photos of the codes, I'm in back-to-back calls.
- **s13** (missed scam, verdict: *rules score 20*): Hi dad, my phone screen is smashed so I'm texting from a mate's. I'm stuck abroad and lost my wallet. Can you send £300 by gift card? So embarrassed, please hurry.
- **s16** (missed scam, verdict: *rules score 20*): Sweetheart, I'm in hospital in Lagos after an accident and my cards are blocked. Please send $900 via Western Union to my nurse, Grace Okafor. I'll pay you back when we meet.
- **s19** (missed scam, verdict: *rules score 20*): URGENT: New token LUNARX is about to 100x. Insiders are buying before listing. Connect your wallet at lunarx-presale.xyz to claim your free airdrop before it ends tonight.
- **s25** (missed scam, verdict: *rules score 0*): Hello, this is Kevin from Windows Support. We have detected hackers accessing your router. Please install AnyDesk so I can remove them. It will cost $199 for the one-year protection.

## model-only

| | Predicted scam | Predicted legit |
|---|---|---|
| **Actually scam** | 10 | 0 |
| **Actually legit** | 0 | 10 |

No wrong answers.

## hybrid

| | Predicted scam | Predicted legit |
|---|---|---|
| **Actually scam** | 10 | 0 |
| **Actually legit** | 0 | 10 |

No wrong answers.
