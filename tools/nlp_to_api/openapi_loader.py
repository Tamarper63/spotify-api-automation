from pathlib import Path


def load_api_doc(path: str) -> str:
    base_dir = Path(__file__).resolve().parents[2]  # root of project
    full_path = base_dir / path
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()
