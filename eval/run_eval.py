"""Evaluate rules-only, model-only and hybrid on eval/dataset.json. Run from the repo root:
python eval/run_eval.py
Results are cached in eval/cache.json; delete it to re-call the API.
"""
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
import analyzer  # noqa: E402
import rules  # noqa: E402

DATASET = ROOT / "dataset.json"
CACHE = ROOT / "cache.json"
RESULTS = ROOT / "results.md"
RULES_THRESHOLD = 40
DELAY_SECONDS = 1.0
FLAGGED = {"likely scam", "suspicious"}
CONFIGS = ("rules-only", "model-only", "hybrid")


def load_json(path: Path, default: object) -> object:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def rules_only(text: str, client: OpenAI | None) -> dict:
    score = rules.run_rules(text)["score"]
    return {"flagged": score >= RULES_THRESHOLD, "verdict": f"rules score {score}"}


def model_only(text: str, client: OpenAI | None) -> dict:
    prompt = analyzer.build_prompt(text)
    for _ in range(2):
        parsed = analyzer.parse_reply(analyzer.call_model(client, prompt))
        if parsed:
            return {"flagged": parsed["verdict"] in FLAGGED, "verdict": parsed["verdict"]}
    raise ValueError("model returned invalid output twice")


def hybrid(text: str, client: OpenAI | None) -> dict:
    result = analyzer.analyze(text, client)
    if result["notice"]:  # analyze() fell back to rules-only; not a hybrid result
        raise RuntimeError(result["notice"])
    return {"flagged": result["verdict"] in FLAGGED, "verdict": result["verdict"]}


RUNNERS = {"rules-only": rules_only, "model-only": model_only, "hybrid": hybrid}


def run_all(messages: list[dict], client: OpenAI | None) -> dict:
    cache = load_json(CACHE, {})
    for config in CONFIGS:
        store = cache.setdefault(config, {})
        for i, msg in enumerate(messages, 1):
            if msg["id"] in store and "error" not in store[msg["id"]]:
                continue
            try:
                store[msg["id"]] = RUNNERS[config](msg["text"], client)
            except Exception as exc:  # API/parse failure: record, don't cache as a result
                store[msg["id"]] = {"error": f"{type(exc).__name__}: {exc}"}
            status = "ERROR" if "error" in store[msg["id"]] else "ok"
            print(f"{i}/{len(messages)} {config} {status}", flush=True)
            CACHE.write_text(json.dumps(cache, indent=2), encoding="utf-8")
            if config != "rules-only":
                time.sleep(DELAY_SECONDS)
    return cache


def metrics(messages: list[dict], store: dict) -> dict:
    tp = fp = tn = fn = errors = 0
    wrong = []
    for msg in messages:
        res = store.get(msg["id"], {"error": "missing"})
        if "error" in res:
            errors += 1
            continue
        is_scam = msg["label"] == "scam"
        tp += is_scam and res["flagged"]
        fn += is_scam and not res["flagged"]
        fp += (not is_scam) and res["flagged"]
        tn += (not is_scam) and not res["flagged"]
        if res["flagged"] != is_scam:
            wrong.append((msg, res["verdict"]))
    scored = tp + fp + tn + fn
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "errors": errors, "wrong": wrong,
            "accuracy": (tp + tn) / scored if scored else 0.0,
            "precision": precision, "recall": recall, "f1": f1}


def render(messages: list[dict], cache: dict) -> str:
    test = [m for m in messages if m["split"] == "test"]
    results = {c: metrics(test, cache.get(c, {})) for c in CONFIGS}
    model = os.getenv("FEATHERLESS_MODEL") or analyzer.DEFAULT_MODEL
    lines = ["# Second Look: Evaluation Results", "",
             f"Test split: {len(test)} messages ({sum(m['label'] == 'scam' for m in test)} scam, "
             f"{sum(m['label'] == 'legit' for m in test)} legitimate). Model: `{model}`. "
             f"Rules threshold: score >= {RULES_THRESHOLD}. "
             "\"likely scam\" and \"suspicious\" count as flagged.", "",
             "| Configuration | Accuracy | Precision | Recall | F1 | API errors (excluded) |",
             "|---|---|---|---|---|---|"]
    for c, r in results.items():
        lines.append(f"| {c} | {r['accuracy']:.0%} | {r['precision']:.0%} | {r['recall']:.0%} "
                     f"| {r['f1']:.2f} | {r['errors']} |")
    lines += ["", "Errors per configuration: "
              + ", ".join(f"{c} {r['errors']}" for c, r in results.items()) + "."]
    for c, r in results.items():
        lines += ["", f"## {c}", "", "| | Predicted scam | Predicted legit |", "|---|---|---|",
                  f"| **Actually scam** | {r['tp']} | {r['fn']} |",
                  f"| **Actually legit** | {r['fp']} | {r['tn']} |", ""]
        if not r["wrong"]:
            lines.append("No wrong answers.")
        for msg, verdict in r["wrong"]:
            kind = "missed scam" if msg["label"] == "scam" else "false alarm"
            lines.append(f"- **{msg['id']}** ({kind}, verdict: *{verdict}*): {msg['text']}")
    return "\n".join(lines) + "\n"


def main() -> None:
    load_dotenv()
    if not DATASET.exists():
        sys.exit(f"Dataset not found: {DATASET}")
    messages = load_json(DATASET, [])
    try:
        if "--from-cache" not in sys.argv:
            key = os.getenv("FEATHERLESS_API_KEY")
            client = OpenAI(base_url=analyzer.BASE_URL, api_key=key) if key else None
            run_all(messages, client)
    finally:  # always write results.md, even after Ctrl-C or a crash
        report = render(messages, load_json(CACHE, {}))
        RESULTS.write_text(report, encoding="utf-8")
        print(report)


if __name__ == "__main__":
    main()
