from utils.yaml_loader import load_yaml_data


def get_valid_playlist_ids():
    """
    Returns a list of valid playlist IDs from playlist_ids.yaml
    """
    return load_yaml_data("playlist_ids.yaml")["playlist_ids"]


def get_valid_playlists_with_names():
    """
    Returns a list of tuples: (playlist_id, expected_name) from playlist_metadata.yaml
    """
    playlists = load_yaml_data("playlist_metadata.yaml")["valid_playlists"]
    return [(p["id"], p["expected_name"]) for p in playlists]


def get_invalid_playlist_ids():
    """
    Returns a list of invalid playlist IDs for negative testing
    """
    return load_yaml_data("invalid_playlist_ids.yaml")["invalid_ids"]


def get_playlists_expected_responses():
    playlists = load_yaml_data("playlist_metadata.yaml")["valid_playlists"]
    return [(p["id"], p["expected"]) for p in playlists]


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
