from __future__ import annotations
import os, pickle
from pathlib import Path
from typing import Iterable
import numpy as np

from tools.local_llm.ollama_client import embed

def _iter_files(root: Path, exts: tuple[str, ...] = (".md", ".txt")) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.suffix.lower() in exts and p.is_file():
            yield p

def _chunk(text: str, size: int = 1200, overlap: int = 150) -> list[str]:
    chunks, i, n = [], 0, len(text)
    while i < n:
        j = min(i + size, n)
        chunks.append(text[i:j])
        i = j - overlap if j < n else j
        if i < 0: i = 0
    return [c.strip() for c in chunks if c.strip()]

def build_index(docs_dir: str = "docs", out_path: str = "data/rag_index.pkl"):
    root = Path(__file__).resolve().parents[2]
    docs = (root / docs_dir).resolve()
    out = (root / out_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    for fp in _iter_files(docs):
        text = fp.read_text(encoding="utf-8")
        for chunk in _chunk(text):
            records.append({"path": str(fp.relative_to(root)), "text": chunk})

    if not records:
        raise RuntimeError(f"No documents found under {docs}")

    vecs = embed([r["text"] for r in records])  # list[list[float]]
    M = np.asarray(vecs, dtype=np.float32)
    norms = np.linalg.norm(M, axis=1, keepdims=True) + 1e-9
    M = M / norms

    with open(out, "wb") as f:
        pickle.dump({"records": records, "matrix": M}, f)

    print(f"[RAG] indexed {len(records)} chunks → {out}")

if __name__ == "__main__":
    build_index()
