from __future__ import annotations
import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
import requests

from tools.nlp_to_api.openapi_loader import load_api_doc
from tools.nlp_to_api.prompt_template import TEMPLATE

ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"
_ = load_dotenv(dotenv_path=ENV_PATH) or load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL_DEFAULT = "llama3.1"

def _default_model() -> str:
    return os.getenv("LLM_MODEL", OLLAMA_MODEL_DEFAULT)

def _ollama_chat(messages, model: str) -> str:
    payload = {"model": model, "messages": messages, "stream": False}
    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=300)
    r.raise_for_status()
    data = r.json()
    return data["message"]["content"]

def query_api_with_nlp(
    user_input: str,
    doc_path: str = "docs/spotify_api_snippet.md",
    model: str | None = None,
    mode: str = "free"  # free = תשובה חופשית, api = החזרת פרטי API
) -> dict | str:
    api_docs = load_api_doc(doc_path)
    model = model or _default_model()

    if mode == "api":
        system_prompt = TEMPLATE.format(api_docs=api_docs)
    else:
        system_prompt = (
            "אתה עוזר טכני שיודע לענות בעברית ובאנגלית. "
            "יש לך את תיעוד ה־API הבא:\n"
            f"{api_docs}\n"
            "ענה לשאלת המשתמש בצורה ברורה, ואם רלוונטי – פרט גם על הקריאות ל־API."
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    reply_text = _ollama_chat(messages, model=model)

    if mode == "api":
        return _extract_json(reply_text)
    return reply_text.strip()

def _extract_json(text: str) -> dict:
    m = re.search(r"\{[\s\S]+\}", text)
    if not m:
        raise ValueError("No valid JSON found in model output.")
    return json.loads(m.group(0))
