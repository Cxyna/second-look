import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.getenv("FEATHERLESS_API_KEY")
if not key:
    raise SystemExit("No key found. Check .env is in this folder and has FEATHERLESS_API_KEY=...")

client = OpenAI(base_url="https://api.featherless.ai/v1", api_key=key)
reply = client.chat.completions.create(
    model="Qwen/Qwen3-32B",
    messages=[{"role": "user", "content": "Say hi in five words."}],
)
print(reply.choices[0].message.content)