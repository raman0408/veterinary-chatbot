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

def save_history(phone_number: str, history):
    file_path = get_user_file_path(phone_number)

    os.makedirs(BASE_PATH, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(history, f, indent = 2)

def append_message(phone_number: str, role: str, content: str):
    history = load_history(phone_number)

    history.append({
        "role": role,
        "content": content
    })

    save_history(phone_number, history)
