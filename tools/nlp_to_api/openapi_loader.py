from pathlib import Path

def load_api_doc(path: str) -> str:
    root = Path(__file__).resolve().parents[2]
    full = root / path
    if not full.exists():
        raise FileNotFoundError(f"API documentation not found at: {full}")
    return full.read_text(encoding="utf-8")
