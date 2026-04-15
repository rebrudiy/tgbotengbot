import json
import os
from modes import DEFAULT_MODE, DEFAULT_LENGTH

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "data", "users.json")


def _load() -> dict:
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(data: dict) -> None:
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_settings(user_id: int) -> dict:
    data = _load()
    user = data.get(str(user_id), {})
    return {
        "mode": user.get("mode", DEFAULT_MODE),
        "length": user.get("length", DEFAULT_LENGTH),
    }


def set_mode(user_id: int, mode: str) -> None:
    data = _load()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {}
    data[uid]["mode"] = mode
    _save(data)


def set_length(user_id: int, length: str) -> None:
    data = _load()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {}
    data[uid]["length"] = length
    _save(data)
