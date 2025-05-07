import os
import configparser
import json
import time

def load_config(config_file='.config'):
    config = configparser.ConfigParser()
    config.read(config_file)
    
    username = config.get('settings', 'username')
    password = config.get('settings', 'password')
    workspace = config.get('settings', 'workspace')
    cache_file = config.get('settings', 'cache_file')
    min_approval = config.get('settings', 'min_approval')
    min_default_reviewer_approval = config.get('settings', 'min_default_reviewer_approval')
    workspace_list = config.get('settings', 'workspace_list')
    return username, password, workspace, cache_file, min_approval, min_default_reviewer_approval, workspace_list

def clear_cache(cache_file='.cache.json'):
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print("Cache cleared.")
    else:
        print("No cache file found to clear.")


def save_cache(data_key, data_value, cache_file='.cache.json'):
    cache = {}
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cache = json.load(f)
        except json.JSONDecodeError:
            pass

    cache[data_key] = {
        "timestamp": time.time(),
        "data": data_value
    }

    with open(cache_file, 'w') as f:
        json.dump(cache, f)

def load_cache(data_key, cache_file='.cache.json', max_age_hours=24):
    if not os.path.exists(cache_file):
        return None

    try:
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    except json.JSONDecodeError:
        return None

    section = cache.get(data_key)
    if not section:
        return None

    timestamp = section.get('timestamp')
    if not timestamp or time.time() - timestamp > max_age_hours * 3600:
        return None

    return section.get('data')