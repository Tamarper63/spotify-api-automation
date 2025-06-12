import yaml
from pathlib import Path


def load_yaml_data(filename: str) -> dict:
    """
    Load YAML test data file from the tests/data directory (relative to project root).
    """
    root_dir = Path(__file__).resolve().parents[1]  # utils/ is in root
    path = root_dir / "tests" / "data" / filename

    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
