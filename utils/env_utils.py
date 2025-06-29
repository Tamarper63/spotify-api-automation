import os


def update_env_var(key: str, value: str, env_path: str = ".env") -> None:
    """
    Update a key-value pair in the .env file. Create it if not exists.
    """
    lines = []
    updated = False

    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[idx] = f"{key}={value}\n"
                updated = True
                break

    if not updated:
        lines.append(f"{key}={value}\n")

    with open(env_path, "w") as f:
        f.writelines(lines)

    os.environ[key] = value  # update current runtime
