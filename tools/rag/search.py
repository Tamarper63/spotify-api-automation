from __future__ import annotations
import pickle
from pathlib import Path
import numpy as np
from tools.local_llm.ollama_client import embed

def load_index(path: str = "data/rag_index.pkl"):
    root = Path(__file__).resolve().parents[2]
    with open(root / path, "rb") as f:
        obj = pickle.load(f)
    return obj["records"], obj["matrix"]

def retrieve(query: str, k: int = 6, index_path: str = "data/rag_index.pkl") -> list[dict]:
    records, M = load_index(index_path)
    qv = np.asarray(embed([query])[0], dtype=np.float32)
    qv = qv / (np.linalg.norm(qv) + 1e-9)
    scores = M @ qv
    top = np.argsort(-scores)[:k]
    return [{"score": float(scores[i]), **records[i]} for i in top]
