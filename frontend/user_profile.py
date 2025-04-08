import json
import os
from datetime import datetime
from collections import Counter

USER_DATA_FILE = "frontend/data/user_data.json"

# Default structure for a new user profile
default_user_data = {
    "username": "Historian",
    "created_on": str(datetime.now()),
    "search_history": [],
    "visited_videos": [],
    "stats": {
        "total_searches": 0,
        "unique_topics": 0,
        "videos_visited": 0
    }
}

def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        return default_user_data

    with open(USER_DATA_FILE, "r") as f:
        data = json.load(f)

    # Fill in missing top-level and nested keys
    for key, value in default_user_data.items():
        if key not in data:
            data[key] = value
        elif isinstance(value, dict):
            for subkey, subval in value.items():
                if subkey not in data[key]:
                    data[key][subkey] = subval

    return data


def save_user_data(data):
    """Saves user profile to JSON."""
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def update_search_history(query):
    data = load_user_data()
    if query not in data["search_history"]:
        data["search_history"].append(query)
        data["stats"]["unique_topics"] = len(data["search_history"])
    data["stats"]["total_searches"] += 1

    # NEW
    data["last_active"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    counter = Counter(data["search_history"])
    most_common = counter.most_common(1)
    data["most_searched"] = most_common[0][0] if most_common else "N/A"

    save_user_data(data)


def add_visited_video(video_url):
    """Tracks visited videos."""
    data = load_user_data()
    if video_url not in data["visited_videos"]:
        data["visited_videos"].append(video_url)
        data["stats"]["videos_visited"] = len(data["visited_videos"])
    save_user_data(data)

def get_stats():
    """Returns current stats for the dashboard."""
    data = load_user_data()
    return data["stats"]

def get_username():
    data = load_user_data()
    return data.get("username", "Historian")

def update_last_active():
    data = load_user_data()
    data["last_active"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    save_user_data(data)

def update_most_searched():
    data = load_user_data()
    counter = Counter(data["search_history"])
    most_common = counter.most_common(1)
    data["most_searched"] = most_common[0][0] if most_common else "N/A"
    save_user_data(data)

