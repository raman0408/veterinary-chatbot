from fastapi import APIRouter

from backend.services.memory import load_history, append_message
from backend.graph.builder import build_graph

router = APIRouter()

graph = build_graph()

@router.post("/chat")
def chat(data: dict):
    phone = data.get("phone")
    message = data.get("message")

    # --- Load History ---
    history = load_history(phone)

    # --- Invoke Graph ---
    result = graph.invoke({
        "phone": phone,
        "message": message,
        "history": history
    })

    response = result["response"]
    summary = result["summary"]

    # --- Save Messages ---
    append_message(phone, "user", message)
    append_message(phone, "assistant", response, summary)

    return {
        "response": response
    }

@router.get("/history/{phone}")
def get_history(phone: str):
    history = load_history(phone)
    return {
        "history": history
    }

