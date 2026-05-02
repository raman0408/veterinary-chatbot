import os
import json

BASE_PATH = "data/users"

def get_user_file_path(phone_number:str) -> str:
    return os.path.join(BASE_PATH, f"{phone_number}.json")

def load_history(phone_number: str):
    file_path = get_user_file_path(phone_number)

    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except:
        return []


def append_message(phone_number: str, role: str, content: str, summary=None):
    path = get_user_file_path(phone_number)

    if os.path.exists(path):
        with open(path, "r") as f:
            history = json.load(f)
    else:
        history = []
    
    message = {
        "role": role,
        "content": content
    }

    if summary:
        message["summary"] = summary
    
    history.append(message)

    with open(path, "w") as f:
        json.dump(history, f, indent = 2)

