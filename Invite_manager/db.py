import json
import os

DB_FILE = "invites.json"

def load_data():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_invite(guild_id, inviter_id, new_user_id):
    data = load_data()
    guild_id = str(guild_id)
    inviter_id = str(inviter_id)

    if guild_id not in data:
        data[guild_id] = {"counts": {}}

    if inviter_id not in data[guild_id]["counts"]:
        data[guild_id]["counts"][inviter_id] = 0

    data[guild_id]["counts"][inviter_id] += 1
    save_data(data)

def get_user_invite_count(guild_id, user_id):
    data = load_data()
    guild_id = str(guild_id)
    user_id = str(user_id)

    if guild_id not in data:
        return 0

    return data[guild_id]["counts"].get(user_id, 0)

def get_leaderboard(guild_id):
    data = load_data()
    guild_id = str(guild_id)
    if guild_id not in data:
        return []

    leaderboard = sorted(data[guild_id]["counts"].items(), key=lambda x: x[1], reverse=True)
    return leaderboard

def clear_invites(guild_id, user_id=None):
    data = load_data()
    guild_id = str(guild_id)

    if guild_id not in data:
        return

    if user_id:
        user_id = str(user_id)
        data[guild_id]["counts"].pop(user_id, None)
    else:
        data[guild_id]["counts"] = {}

    save_data(data)
