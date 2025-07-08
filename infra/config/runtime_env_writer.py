from dotenv import set_key
from pathlib import Path

ENV_PATH = Path(".env")

def update_runtime_env(key: str, value: str):
    ENV_PATH.touch(exist_ok=True)
    set_key(str(ENV_PATH), key, value)