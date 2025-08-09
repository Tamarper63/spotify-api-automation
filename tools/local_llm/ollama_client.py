from __future__ import annotations

import os, json, requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
EMB_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

def chat(messages, model: str = CHAT_MODEL, stream: bool = False, options: dict | None = None) -> str:
    payload = {"model": model, "messages": messages, "stream": bool(stream)}
    if options: payload["options"] = options
    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=300)
    r.raise_for_status()
    return r.json()["message"]["content"]

def embed(texts: list[str], model: str = EMB_MODEL) -> list[list[float]]:
    # /api/embeddings מקבל prompt אחד; נחבר טקסטים עם מפריד ברור
    sep = "\n\n###\n\n"
    prompt = sep.join(texts)
    r = requests.post(f"{OLLAMA_URL}/api/embeddings", json={"model": model, "prompt": prompt}, timeout=300)
    r.raise_for_status()
    v = r.json()["embedding"]
    # מחזיר וקטור אחד; נפרק לפי ספירת הטקסטים ע"י hashing separator
    # פתרון פרקטי יותר: נקרא פעם לכל טקסט (פחות יעיל אך פשוט/אמין)
    out = []
    for t in texts:
        r2 = requests.post(f"{OLLAMA_URL}/api/embeddings", json={"model": model, "prompt": t}, timeout=300)
        r2.raise_for_status()
        out.append(r2.json()["embedding"])
    return out
