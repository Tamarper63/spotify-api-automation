from utils.yaml_loader import load_yaml_data


def load_flat_yaml_kv(filename: str, root_key: str) -> list[tuple[str, any]]:
    """
    Load a nested YAML dict and flatten it into (field_path, value) tuples.
    Supports dot-notation for nested fields.
    Example:
    {
      "a": {
        "b": {
          "c": 1
        }
      }
    } becomes [("a.b.c", 1)]
    """

    def flatten_dict(d, parent_key=""):
        items = []
        for k, v in d.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, full_key))
            else:
                items.append((full_key, v))
        return items

    raw = load_yaml_data(filename)
    data = raw.get(root_key)
    if not isinstance(data, dict):
        raise ValueError(f"{root_key} must be a dictionary in {filename}")
    return flatten_dict(data)
