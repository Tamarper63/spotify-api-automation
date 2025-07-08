from dotenv import set_key
from pathlib import Path

RUNTIME_ENV_PATH = Path(".runtime.env")

def update_runtime_env(key: str, value: str):
    RUNTIME_ENV_PATH.touch(exist_ok=True)
    set_key(str(RUNTIME_ENV_PATH), key, value)
