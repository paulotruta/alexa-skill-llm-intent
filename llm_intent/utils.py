import json
from os.path import exists

CONFIG_FILE = "config.json"


def load_config() -> dict:
    if not exists(CONFIG_FILE):
        raise ValueError("Config file does not exist")

    with open(CONFIG_FILE) as f:
        return json.load(f)
