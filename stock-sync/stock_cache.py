
import json
import os

CACHE_FILE = "cache.json"

def _load():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def _save(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

cache = _load()  # load whatever was saved last time, right when this file is imported

def update_cache(data):
    global cache
    cache = data
    _save(cache)

def read_cache():
    return cache