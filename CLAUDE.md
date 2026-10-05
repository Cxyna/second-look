# Second Look

Streamlit app (ForgeHacks, AI + Cybersecurity track) that checks suspicious messages
with rule-based checks plus a Featherless model call.

## Layout
- `app.py` — Streamlit UI
- `rules.py` — rule-based checks
- `analyzer.py` — Featherless model call; combines with rule results
- `text.py` — scratch Featherless/OpenAI-client script
- `tests/test_rules.py` — pytest tests for `rules.py`
- `.env.example` — key template; `requirements.txt` — deps

## Env keys (`.env`)
- `FEATHERLESS_API_KEY`
- `FEATHERLESS_MODEL` (default `Qwen/Qwen3-32B`)

**Never read or print `.env`.** Use `.env.example` for key names.

## Commands
- Run app: `streamlit run app.py`
- Tests: `pytest`
- Venv: `.venv` (Windows: `.venv\Scripts\activate`)