"""Throwaway: send one fictional message through analyzer's real prompt N times, classify replies."""
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import analyzer  # noqa: E402

RUNS = int(os.getenv("PROBE_RUNS", "10"))
MESSAGE = "Royal Mail: your parcel is held due to unpaid postage of £1.45. Pay within 24 hours or it will be returned: http://bit.ly/rm-redeliver"
IDS = [i for i in os.getenv("PROBE_IDS", "").split(",") if i]  # eval ids (fictional), instead of the Royal Mail text
OUT = Path(__file__).with_name("probe_out.txt")


def classify(raw: str, finish: str | None) -> str:
    if analyzer.parse_reply(raw):
        return "parsed"
    if not raw.strip():
        return "empty reply"
    if "<think>" in raw and "</think>" not in raw:
        return "cut off inside <think>"
    if finish == "length":
        return "cut off (finish_reason=length)"
    if "```" in raw:
        return "markdown fence, still unparsed"
    try:
        json.loads(raw)
        return "valid JSON, wrong shape/verdict"
    except ValueError:
        return "invalid JSON"


def main() -> None:
    load_dotenv()
    client = OpenAI(base_url=analyzer.BASE_URL, api_key=os.environ["FEATHERLESS_API_KEY"])
    msgs = [MESSAGE]
    if IDS:
        data = json.loads((Path(__file__).parent.parent / "eval" / "fresh.json").read_text(encoding="utf-8"))
        msgs = [m["text"] for m in data if m["id"] in IDS]
    model = os.getenv("FEATHERLESS_MODEL") or analyzer.DEFAULT_MODEL
    counts: Counter[str] = Counter()
    with OUT.open("w", encoding="utf-8") as f:
        for i, text in ((i, t) for t in msgs for i in range(RUNS)):
            prompt = analyzer.build_prompt(text)
            try:
                r = client.with_options(timeout=analyzer.TIMEOUT_SECONDS, max_retries=0).chat.completions.create(
                    model=model, messages=[{"role": "user", "content": prompt}],
                    **({"extra_body": {"chat_template_kwargs": {"enable_thinking": False}}} if os.getenv("PROBE_NOTHINK") else {}))
                raw, finish = r.choices[0].message.content or "", r.choices[0].finish_reason
                toks = r.usage.completion_tokens if r.usage else None
            except Exception as exc:
                raw, finish, toks = "", f"error {type(exc).__name__}", None
            think = re.match(r"\s*<think>(.*?)(</think>|$)", raw, re.DOTALL)
            think_len = len(think.group(1)) if think else 0
            why = classify(raw, finish) if not finish.startswith("error") else finish
            tags = [t for t, hit in (("has <think>", "<think>" in raw), ("fence", "```" in raw)) if hit]
            counts[why] += 1
            f.write(f"=== run {i} | {why} | finish={finish} | {tags} | len={len(raw)}\n{raw!r}\n\n")
            print(f"run {i}: finish={finish} completion_tokens={toks} starts_with_think={bool(think)} think_chars={think_len} parsed={bool(analyzer.parse_reply(raw))}")
    for why, n in counts.most_common():
        print(f"{n:3d}/{sum(counts.values())}  {why}")


if __name__ == "__main__":
    main()
