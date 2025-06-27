import base64
from pathlib import Path


def read_image_as_base64(relative_path: str) -> str:
    root = Path(__file__).resolve().parent.parent  # points to project root (spotify-api-automation/)
    full_path = root / relative_path
    return base64.b64encode(full_path.read_bytes()).decode("utf-8")